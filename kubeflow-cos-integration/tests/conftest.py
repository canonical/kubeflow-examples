import shlex
import logging
import subprocess
import json
import pytest


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="session")
def teardown():
    """Remove all relations that were created during tests."""
    yield
    logger.info("Tearing down tests..")
    subprocess.run(shlex.split("juju switch kubeflow"), check=True)
    teardown_commands = get_teardown_commands()
    logger.info("Removing relations..")
    for cmd in teardown_commands:
        subprocess.run(shlex.split(cmd), check=True, capture_output=True)
    logger.info("Teardown Successful.")


def get_teardown_commands() -> list:
    """Get remove-relation commands by checking where relations were added in the guide code cells."""
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
        for cmd in relation_commands
    ]
    return remove_commands
