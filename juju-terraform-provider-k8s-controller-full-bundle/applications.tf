
resource "juju_model" "kubeflow" {
  name = "kubeflow"

  cloud {
    name   = var.juju_cloud
  }
}

resource "juju_application" "admission-webhook" {
  name = "admission-webhook"

  model = juju_model.kubeflow.name

  charm {
    name = "admission-webhook"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "argo-controller" {
  name = "argo-controller"

  model = juju_model.kubeflow.name

  charm {
    name = "argo-controller"
    channel = "3.3/stable"
  }

  units = 1
}

resource "juju_application" "argo-server" {
  name = "argo-server"

  model = juju_model.kubeflow.name

  charm {
    name = "argo-server"
    channel = "3.3/stable"
  }

  units = 1
}

resource "juju_application" "dex-auth" {
  name = "dex-auth"

  model = juju_model.kubeflow.name

  charm {
    name = "dex-auth"
    channel = "2.31/stable"
  }
  trust = true
  units = 1
}

resource "juju_application" "istio-ingressgateway" {
  name = "istio-ingressgateway"

  model = juju_model.kubeflow.name

  charm {
    name = "istio-gateway"
    channel = "1.11/stable"
  }
  
  config = {
    kind = "ingress"
  }
  trust = true
  units = 1
}

resource "juju_application" "istio-pilot" {
  name = "istio-pilot"

  model = juju_model.kubeflow.name

  charm {
    name = "istio-pilot"
    channel = "1.11/stable"
  }

  config = {
    default-gateway = "kubeflow-gateway"
  }
  trust = true
  units = 1
}

resource "juju_application" "jupyter-controller" {
  name = "jupyter-controller"

  model = juju_model.kubeflow.name

  charm {
    name = "jupyter-controller"
    channel = "1.6/stable"
  }

  units = 1
}


resource "juju_application" "jupyter-ui" {
  name = "jupyter-ui"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "jupyter-ui"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "katib-controller" {
  name = "katib-controller"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "katib-controller"
    channel = "0.14/stable"
  }

  units = 1
}


resource "juju_application" "katib-db" {
  name = "katib-db"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "charmed-osm-mariadb-k8s"
    channel = "latest/stable"
  }

  config = {
    database = "katib"
  }

  units = 1
}


resource "juju_application" "katib-db-manager" {
  name = "katib-db-manager"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "katib-db-manager"
    channel = "0.14/stable"
  }

  units = 1
}

resource "juju_application" "katib-ui" {
  name = "katib-ui"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "katib-ui"
    channel = "0.14/stable"
  }

  units = 1
}

resource "juju_application" "kfp-api" {
  name = "kfp-api"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "kfp-api"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-db" {
  name = "kfp-db"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "charmed-osm-mariadb-k8s"
    channel = "latest/stable"
  }

  config = {
    database = "mlpipeline"
  }

  units = 1
}

resource "juju_application" "kfp-persistence" {
  name = "kfp-persistence"
  
  model = juju_model.kubeflow.name
  
  charm {
    name = "kfp-persistence"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-profile-controller" {
  name = "kfp-profile-controller"

  model = juju_model.kubeflow.name

  charm {
    name = "kfp-profile-controller"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-schedwf" {
  name = "kfp-schedwf"

  model = juju_model.kubeflow.name

  charm {
    name = "kfp-schedwf"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-ui" {
  name = "kfp-ui"

  model = juju_model.kubeflow.name

  charm {
    name = "kfp-ui"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-viewer" {
  name = "kfp-viewer"

  model = juju_model.kubeflow.name

  charm {
    name = "kfp-viewer"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kfp-viz" {
  name = "kfp-viz"

  model = juju_model.kubeflow.name

  charm {
    name = "kfp-viz"
    channel = "2.0/stable"
  }

  units = 1
}

resource "juju_application" "kubeflow-dashboard" {
  name = "kubeflow-dashboard"

  model = juju_model.kubeflow.name

  charm {
    name = "kubeflow-dashboard"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "kubeflow-profiles" {
  name = "kubeflow-profiles"

  model = juju_model.kubeflow.name

  charm {
    name = "kubeflow-profiles"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "kubeflow-roles" {
  name = "kubeflow-roles"

  model = juju_model.kubeflow.name

  charm {
    name = "kubeflow-roles"
    channel = "1.6/stable"
  }

  trust = true
  units = 1
}

resource "juju_application" "kubeflow-volumes" {
  name = "kubeflow-volumes"

  model = juju_model.kubeflow.name

  charm {
    name = "kubeflow-volumes"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "metacontroller-operator" {
  name = "metacontroller-operator"

  model = juju_model.kubeflow.name

  charm {
    name = "metacontroller-operator"
    channel = "2.0/stable"
  }
  trust = true
  units = 1
}

resource "juju_application" "minio" {
  name = "minio"

  model = juju_model.kubeflow.name

  charm {
    name = "minio"
    channel = "ckf-1.6/stable"
  }

  units = 1
}

resource "juju_application" "oidc-gatekeeper" {
  name = "oidc-gatekeeper"

  model = juju_model.kubeflow.name

  charm {
    name = "oidc-gatekeeper"
    channel = "ckf-1.6/stable"
  }

  units = 1
}

resource "juju_application" "seldon-controller-manager" {
  name = "seldon-controller-manager"

  model = juju_model.kubeflow.name

  charm {
    name = "seldon-core"
    channel = "1.14/stable"
  }

  units = 1
}

resource "juju_application" "tensorboard-controller" {
  name = "tensorboard-controller"

  model = juju_model.kubeflow.name

  charm {
    name = "tensorboard-controller"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "tensorboards-web-app" {
  name = "tensorboards-web-app"

  model = juju_model.kubeflow.name

  charm {
    name = "tensorboards-web-app"
    channel = "1.6/stable"
  }

  units = 1
}

resource "juju_application" "training-operator" {
  name = "training-operator"

  model = juju_model.kubeflow.name

  charm {
    name = "training-operator"
    channel = "1.5/stable"
  }

  units = 1
  trust = true
}