#!/bin/bash

#######################################

MAAS_URL=http://192.168.86.45:5240/MAAS
MAAS_TOKEN=yourtoken
METALLB_RANGE=192.168.86.90-192.168.86.95
MICROK8S_NODE_COUNT=3
MICROK8S_NODE_MEM_GB=8
MICROK8S_NODE_DISK_GB=20
CEPH_NODE_OSD_DISK_GB=1
CEPH_NODE_OSD_DISK_COUNT=1
CEPH_NODE_OSD_COUNT=3
CEPH_NODE_MON_COUNT=3

#######################################
#
#      Files
#
#######################################

if [ ! -f $HOME/.kaggle/kaggle.json ]; then
  echo "You first need to set up your Kaggle API token. Go to https://www.kaggle.com/ and create an API token or sign up"
  exit -1
fi

cat > maas-cloud.yaml <<EOF
clouds:
  maas:
    type: maas
      auth-types: [oauth1]
        regions:
          default: {}
      endpoint: ${MAAS_URL}
EOF

cat > pyspark-script.py <<EOF
df = spark.read.option("header", "true").csv("s3a://data/traffic-collision-data-from-2010-to-present.csv")
df.createOrReplaceTempView("collisions")
spark.sql("select `DR Number` from collisions group by `DR Number` having count(`DR Number`) > 1").show()
quit()
EOF

#######################################
#
#      Prerequisites
#
#######################################

sudo snap remove --purge juju
sudo snap remove --purge juju-wait
sudo snap remove --purge minio-mc-nsg
sudo snap remove --purge spark-client

sudo snap install juju --channel=3.3/stable
sudo snap install juju-wait --channel=latest/edge --classic
sudo snap install minio-mc-nsg
sudo snap alias minio-mc-nsg mc
sudo snap install spark-client --channel=3.4/edge

sudo apt install jq yq unzip -y

pip install kaggle

#######################################
#
#      Commands
#
#######################################

# create the MAAS cloud
juju add-cloud --controller --client --credential ${MAAS_TOKEN} maas -f maas-cloud.yaml; juju-wait
juju bootstrap maas cloud-controller; juju-wait
juju switch cloud-controller
juju enable-ha

# create the foundations - Ceph & MicroK8s
juju add-model charm-stack-base-model maas
juju deploy microk8s -n ${MICROK8S_NODE_COUNT} --config hostpath_storage=true --constraints "mem=${MICROK8S_NODE_MEM_GB}G root-disk=${MICROK8S_NODE_DISK_GB}G" --channel=edge #fixme
juju-wait
juju deploy ceph-osd --storage osd-devices=loop,${CEPH_NODE_OSD_DISK_GB}G,${CEPH_NODE_OSD_DISK_COUNT} -n ${CEPH_NODE_OSD_COUNT}; juju-wait
juju deploy -n ${CEPH_NODE_MON_COUNT} ceph-mon; juju-wait
juju deploy ceph-radosgw; juju-wait
juju relate ceph-radosgw:mon ceph-mon:radosgw
juju relate ceph-osd:mon ceph-mon:osd
juju deploy grafana-agent --channel edge; juju-wait
juju expose ceph-radosgw
juju expose microk8s

# configure Ceph
# create a user account
CEPH_RESPONSE_JSON=$(juju ssh ceph-mon/leader 'sudo radosgw-admin user create \
   --uid="ubuntu" --display-name="Charmed Spark User"')

CEPH_ACCESS_KEY_ID=$(echo ${CEPH_RESPONSE_JSON} | jq -r '.keys[].access_key')
CEPH_SECRET_ACCESS_KEY=$(echo ${CEPH_RESPONSE_JSON} | jq -r '.keys[].secret_key')

# get RadosGW IP address
CEPH_IP=$(juju status | grep ceph-radosgw | tail -n 1 | awk '{ print $5 }')
# no TLS - fixme
mc config host add ceph-radosgw http://${CEPH_IP}:80 ${CEPH_ACCESS_KEY_ID} ${CEPH_SECRET_ACCESS_KEY}
mc mb ceph-radosgw/spark-history
mc mb ceph-radosgw/data

# scult the Kubernetes layer
KUBECONF="$(juju exec --unit microk8s/leader -- microk8s config)"
echo "${KUBECONF}" | juju add-k8s microk8s-cloud --controller cloud-controller
juju add-model spark-model microk8s-cloud

# metallb charm is broken - fixme
juju exec --unit microk8s/leader -- sudo microk8s enable metallb:${METALLB_RANGE}
juju deploy spark-history-server-k8s
juju deploy s3-integrator --channel=latest/edge
juju deploy traefik-k8s --trust
juju-wait
juju config s3-integrator bucket="spark-history" path="spark-events" endpoint=http://${CEPH_IP}:80
juju run s3-integrator/leader sync-s3-credentials access-key=${CEPH_ACCESS_KEY_ID} secret-key=${CEPH_SECRET_ACCESS_KEY}
juju relate s3-integrator spark-history-server-k8s

# set up COS
juju add-model cos-model microk8s-cloud
juju deploy cos-lite --trust
juju deploy prometheus-pushgateway-k8s --channel=edge
juju deploy cos-configuration-k8s --config git_repo=https://github.com/canonical/charmed-spark-rock --config git_branch=dashboard \
  --config git_depth=1 --config grafana_dashboards_path=dashboards/prod/grafana/
juju deploy prometheus-scrape-config-k8s scrape-interval-config --config scrape_interval=5
juju-wait

juju relate cos-configuration-k8s grafana
juju relate prometheus-pushgateway-k8s prometheus
juju relate scrape-interval-config prometheus-pushgateway-k8s
juju relate scrape-interval-config:metrics-endpoint prometheus:metrics-endpoint
juju offer prometheus:receive-remote-write prometheus
juju offer loki:logging loki
juju offer grafana:grafana-dashboard grafana

PROMETHEUS_GATEWAY_IP=$(juju status --format=yaml | yq ".applications.prometheus-pushgateway-k8s.address")

# COS - Microk8s integration
juju switch charm-stack-base-model 
juju consume admin/cos.prometheus prometheus
juju consume cos-model/cos.prometheus prometheus
juju consume admin/cos-model.prometheus prometheus
juju consume admin/cos-model.loki loki
juju consume admin/cos-model.grafana grafana

# Download sample dataset from Kaggle
kaggle datasets download -d cityofLA/los-angeles-traffic-collision-data
unzip los-angeles-traffic-collision-data.zip
mc cp traffic-collision-data-from-2010-to-present.csv ceph-radosgw/data/

# configure Spark runtime - this UX will be improved soon by a charm
cat > spark.conf <<EOF
spark.eventLog.enabled=true
spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
spark.hadoop.fs.s3a.connection.ssl.enabled=false
spark.hadoop.fs.s3a.path.style.access=true
spark.hadoop.fs.s3a.access.key=${CEPH_ACCESS_KEY_ID}
spark.hadoop.fs.s3a.secret.key=${CEPH_SECRET_ACCESS_KEY}
spark.hadoop.fs.s3a.endpoint=http://${CEPH_IP}:80
spark.eventLog.dir=s3a://spark-history/spark-events/ 
spark.history.fs.logDirectory=s3a://spark-history/spark-events/
spark.driver.log.persistToDfs.enabled=true
spark.driver.log.dfsDir=s3a://spark-history/spark-events/
spark.metrics.conf.driver.sink.prometheus.pushgateway-address=${PROMETHEUS_GATEWAY_IP}:9091
spark.metrics.conf.driver.sink.prometheus.class=org.apache.spark.banzaicloud.metrics.sink.PrometheusSink
spark.metrics.conf.driver.sink.prometheus.enable-dropwizard-collector=true
spark.metrics.conf.driver.sink.prometheus.period=5
spark.metrics.conf.driver.sink.prometheus.metrics-name-capture-regex=([a-z0-9]*_[a-z0-9]*_[a-z0-9]*_)(.+)
spark.metrics.conf.driver.sink.prometheus.metrics-name-replacement=\$2
spark.metrics.conf.executor.sink.prometheus.pushgateway-address=${PROMETHEUS_GATEWAY_IP}:9091
spark.metrics.conf.executor.sink.prometheus.class=org.apache.spark.banzaicloud.metrics.sink.PrometheusSink
spark.metrics.conf.executor.sink.prometheus.enable-dropwizard-collector=true
spark.metrics.conf.executor.sink.prometheus.period=5
spark.metrics.conf.executor.sink.prometheus.metrics-name-capture-regex=([a-z0-9]*_[a-z0-9]*_[a-z0-9]*_)(.+)
spark.metrics.conf.executor.sink.prometheus.metrics-name-replacement=\$2
EOF

spark-client.service-account-registry create --username spark --namespace spark-history --primary --properties-file spark.conf

# Currently the snap references the wrong risk track for the image causing a class version error - fixme
export AWS_ACCESS_KEY_ID=${CEPH_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${CEPH_SECRET_ACCESS_KEY}
export AWS_ENDPOINT_URL=http://${CEPH_IP}:80
spark-client.pyspark --username spark --namespace spark-model --conf spark.kubernetes.executor.request.cores=0.01 --conf spark.kubernetes.drive.request.cores=0.01 --conf spark.kubernetes.container.image=ghcr.io/canonical/charmed-spark:3.4-22.04_edge < pyspark-script.py

# Spawn various browser windows
# Spark History Server
juju switch spark-model
HISTORY_SERVER_URL=$(juju run traefik-k8s/leader show-proxied-endpoints | sed "s/proxied-endpoints: '//g" | sed "s/'//g" | jq -r '."spark-history-server-k8s".url')
google-chrome ${HISTORY_SERVER_URL}

# Grafana
juju switch cos-model
CMDOUT=$(juju run grafana/leader get-admin-password)
echo "admin/$(echo ${CMDOUT} | grep admin-password | awk -F: '{ print $2 }')"
GRAFANA_SERVER_URL=$(echo ${CMDOUT} | grep url | awk '{ print $2 }')

google-chrome ${GRAFANA_SERVER_URL}

