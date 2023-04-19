import shlex
import logging
import subprocess
import json
from juju.controller import Controller
from pytest_operator.plugin import OpsTest
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.abort_on_fail
@pytest.fixture(autouse=True, scope="session")
async def setup_and_teardown(ops_test: OpsTest):
    setup()
    yield
    teardown()


async def setup(ops_test: OpsTest):
    logger.info("Setting up tests..")
    controller = Controller()
    await controller.connect_current()

    model = await controller.add_model("kubeflow")

    logger.info("Deploying Kubeflow")
    await model.deploy(
        "kubeflow",
        channel="1.7/stable",
        trust=True,
    )

    logger.info("Waiting for bundle to be ready")
    kf_apps = [
        "admission-webhook",
        "argo-controller",
        "argo-server",
        "dex-auth",
        "istio-ingressgateway",
        "istio-pilot",
        "jupyter-controller",
        "jupyter-ui",
        "katib-controller",
        "katib-db",
        "katib-db-manager",
        "katib-ui",
        "kfp-api",
        "kfp-db",
        "kfp-persistence",
        "kfp-profile-controller",
        "kfp-schedwf",
        "kfp-ui",
        "kfp-viewer",
        "kfp-viz",
        # 'knative-eventing', # this is expected to wait for config
        "knative-operator",
        # 'knative-serving',  # this is expected to wait for config
        "kserve-controller",
        "kubeflow-dashboard",
        "kubeflow-profiles",
        # 'kubeflow-roles',  # this is expected to wait for config
        "kubeflow-volumes",
        "metacontroller-operator",
        "minio",
        "oidc-gatekeeper",
        "seldon-controller-manager",
        # 'tensorboard-controller',  # this is expected to wait for config
        "tensorboards-web-app",
        "training-operator",
    ]
    await ops_test.model.wait_for_idle(
        apps=kf_apps,
        status="active",
        raise_on_blocked=False,
        raise_on_error=False,
        timeout=60000,
    )
    logger.info("All Kubeflow applications are active")

    model = await controller.add_model("cos")

    logger.info("Deploying COS Lite")

    subprocess.run(
        shlex.split(
            "curl -L https://raw.githubusercontent.com/canonical/cos-lite-bundle/main/overlays/offers-overlay.yaml -O"
        ),
        check=True,
        capture_output=True,
    )
    subprocess.run(
        shlex.split("juju deploy cos-lite --trust --overlay ./offers-overlay.yaml"),
        check=True,
        capture_output=True,
    )

    cos_apps = [
        "alertmanager",
        "catalogue",
        "grafana",
        "loki",
        "prometheus",
        "traefik",
    ]

    await ops_test.model.wait_for_idle(
        apps=cos_apps,
        status="active",
        raise_on_blocked=False,
        raise_on_error=False,
        timeout=3000,
    )


def teardown():
    logger.info("Tearing down tests..")
    subprocess.run(shlex.split("juju switch kubeflow"), check=True)
    teardown_commands = get_teardown_commands()
    for cmd in teardown_commands:
        subprocess.run(shlex.split(cmd), check=True)
    logger.info("Teardown Successful.")


def get_teardown_commands() -> list:
    relation_commands = []
    with open("kubeflow-cos-integration.ipynb", "r") as f:
        notebook = f.read()
    notebook_json = json.loads(notebook)
    for cell in notebook_json["cells"]:
        if cell["cell_type"] == "code":
            for line in cell["source"]:
                if line.startswith("juju add-relation"):
                    relation_commands.append(line.strip())
    remove_commands = [
        cmd.replace("add-relation", "remove-relation").replace("admin/cos.", "")
        + " --force"
        for cmd in relation_commands
    ]
    return remove_commands
