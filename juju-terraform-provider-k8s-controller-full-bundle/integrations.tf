# Now we do the integrations, aka the relations

resource "juju_integration" "argo-controller-minio" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.argo-controller.name
  }

  application {
    name     = juju_application.minio.name
  }
}

resource "juju_integration" "dex-auth-oidc-gatekeeper" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.dex-auth.name
    endpoint = "oidc-client"
  }

  application {
    name     = juju_application.oidc-gatekeeper.name
    endpoint = "oidc-client"
  }
}

resource "juju_integration" "istio-pilot-dex-auth" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.dex-auth.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-jupyter-ui" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.jupyter-ui.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-katib-ui" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.katib-ui.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-kfp-ui" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-ui.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-kubeflow-dashboard" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kubeflow-dashboard.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-kubeflow-volumes" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kubeflow-volumes.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-oidc-gatekeeper" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.oidc-gatekeeper.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-oidc-gatekeeper-auth" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.oidc-gatekeeper.name
    endpoint = "ingress-auth"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress-auth"
  }
}

resource "juju_integration" "istio-pilot-istio-ingressgateway" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.istio-ingressgateway.name
    endpoint = "istio-pilot"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "istio-pilot"
  }
}

resource "juju_integration" "istio-pilot-tensorboards-web-app" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.tensorboards-web-app.name
    endpoint = "ingress"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "ingress"
  }
}

resource "juju_integration" "istio-pilot-gw-info-tensorboard-controller" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.tensorboard-controller.name
    endpoint = "gateway-info"
  }

  application {
    name     = juju_application.istio-pilot.name
    endpoint = "gateway-info"
  }
}

resource "juju_integration" "katib-db-manager-katib-db" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.katib-db-manager.name
  }

  application {
    name     = juju_application.katib-db.name
  }
}

resource "juju_integration" "kfp-api-kfp-db" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-api.name
  }

  application {
    name     = juju_application.kfp-db.name
  }
}

resource "juju_integration" "kfp-api-kfp-persistence" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-api.name
    endpoint = "kfp-api"
  }

  application {
    name     = juju_application.kfp-persistence.name
    endpoint = "kfp-api"
  }
}

resource "juju_integration" "kfp-api-kfp-ui" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-api.name
    endpoint = "kfp-api"
  }

  application {
    name     = juju_application.kfp-ui.name
    endpoint = "kfp-api"
  }
}

resource "juju_integration" "kfp-api-kfp-viz" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-api.name
    endpoint = "kfp-viz"
  }

  application {
    name     = juju_application.kfp-viz.name
    endpoint = "kfp-viz"
  }
}

resource "juju_integration" "kfp-api-minio" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-api.name
    endpoint = "object-storage"
  }

  application {
    name     = juju_application.minio.name
    endpoint = "object-storage"
  }
}

resource "juju_integration" "kfp-profile-controller-minio" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-profile-controller.name
    endpoint = "object-storage"
  }

  application {
    name     = juju_application.minio.name
    endpoint = "object-storage"
  }
}

resource "juju_integration" "kfp-ui-minio" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kfp-ui.name
    endpoint = "object-storage"
  }

  application {
    name     = juju_application.minio.name
    endpoint = "object-storage"
  }
}

resource "juju_integration" "kubeflow-profiles-kubeflow-dashboard" {
  model = juju_model.kubeflow.name

  application {
    name     = juju_application.kubeflow-profiles.name
  }

  application {
    name     = juju_application.kubeflow-dashboard.name
  }
}
