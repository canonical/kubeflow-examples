import logging
from subprocess import run

import pytest

from lightkube import ApiError, Client, codecs
from lightkube.generic_resource import (
    create_global_resource,
    create_namespaced_resource,
    load_in_cluster_generic_resources,
)
from lightkube.resources.core_v1 import Pod
from utils import assert_namespace_active, assert_replicas

log = logging.getLogger(__name__)

ASSETS_DIR = Path("tests") / "assets"
NOTEBOOK_TEMPLATE_FILE = ASSETS_DIR / "test-notebook.yaml.j2"
PROFILE_TEMPLATE_FILE = ASSETS_DIR / "test-profile.yaml.j2"

NAMESPACE = "kf-test"
PROFILE_RESOURCE = create_global_resource(
    group="kubeflow.org",
    version="v1",
    kind="profile",
    plural="profiles",
)

NOTEBOOK_NAME = "test-notebook"
NOTEBOOK_RESOURCE = create_namespaced_resource(
    group="kubeflow.org",
    version="v1",
    kind="notebook",
    plural="notebooks",
)


@pytest.fixture(scope="module")
def lightkube_client():
    """Initialise Lightkube Client."""
    lightkube_client = Client()
    load_in_cluster_generic_resources(lightkube_client)
    return lightkube_client


@pytest.fixture(scope="module")
def create_profile(lightkube_client):
    """Create Profile and handle cleanup at the end of the module tests."""
    resources = codecs.load_all_yaml(
        PROFILE_TEMPLATE_FILE.read_text(),
        context={"namespace": NAMESPACE},
    )

    for rsc in resources:
        lightkube_client.create(rsc)

    yield

    # delete the Profile at the end of the module tests
    lightkube_client.delete(PROFILE_RESOURCE, name=NAMESPACE)


@pytest.mark.abort_on_fail
async def test_create_profile(lightkube_client, create_profile):
    """Test Profile creation.

    This test relies on the create_profile fixture, which handles the Profile creation and
    is responsible for cleaning up at the end.
    """
    try:
        profile_created = lightkube_client.get(
            PROFILE_RESOURCE,
            name=PROFILE_NAME,
        )
    except ApiError as e:
        if e.status == 404:
            profile_created = False
        else:
            raise
    assert profile_created, f"Profile {PROFILE_NAME} not found!"
    
    assert_namespace_active(lightkube_client, NAMESPACE)


@pytest.fixture(scope="module")
def create_notebook(lightkube_client):
    """Create Notebook and handle cleanup at the end of the module tests."""
    resources = codecs.load_all_yaml(
        NOTEBOOK_TEMPLATE_FILE.read_text(),
        context={"notebook": NOTEBOOK_NAME},
    )

    for rsc in resources:
        lightkube_client.create(rsc, namespace=NAMESPACE)

    yield

    # delete the Notebook at the end of the module tests
    lightkube_client.delete(NOTEBOOK_RESOURCE, name=NOTEBOOK_NAME, namespace=NAMESPACE)


@pytest.mark.abort_on_fail
async def test_create_notebook(lightkube_client, create_notebook):
    """Test Notebook creation.

    This test relies on the create_notebook fixture, which handles the Notebook creation and
    is responsible for cleaning up at the end.
    """
    try:
        notebook_created = lightkube_client.get(
            NOTEBOOK_RESOURCE,
            name=NOTEBOOK_NAME,
            namespace=NAMESPACE,
        )
    except ApiError as e:
        if e.status == 404:
            notebook_created = False
        else:
            raise
    assert notebook_created, f"Notebook {NAMESPACE}/{NOTEBOOK_NAME} not found!"

    assert_replicas(lightkube_client, NOTEBOOK_RESOURCE, NOTEBOOK_NAME, NAMESPACE)


@pytest.mark.abort_on_fail
async def test_copy_dir():
    """Test copying the tests directory inside the Notebook server."""
    assert not run(
        [
            "kubectl",
            "-n",
            NAMESPACE,
            "cp",
            TESTS_DIR,
            f"svc/{NOTEBOOK_NAME}:~/{TESTS_DIR}"
        ]
    )


@pytest.mark.abort_on_fail
async def test_run_bundle_tests():
    """Test copying the tests directory inside the Notebook server."""
    # get Notebook Pod
    pods = list(client.list(Pod, namespace=NAMESPACE, labels={"app": NOTEBOOK_NAME}))
    assert len(pods) == 1, f"Expected 1 Pod corresponding to notebook {NOTEBOOK_NAME}"
    pod = pods[0].metadata.name

    assert not run(
        [
            "kubectl",
            "-n",
            NAMESPACE,
            "exec",
            "-it",
            f"{pod}:{TESTS_DIR}",
            "--",
            "bash",
            "-c",
            f"'cd {TESTS_DIR} && pytest'",
        ]
    )
