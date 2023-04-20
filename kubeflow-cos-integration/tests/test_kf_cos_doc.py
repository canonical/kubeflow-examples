# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
import shlex
import json
import subprocess
import pytest
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

NOTEBOOK_PATH = "kubeflow-cos-integration.ipynb"


def get_source(tag):
    """Fetch the source code of the cell with the given tag."""
    # TODO automate test detection with cell tags
    with open(NOTEBOOK_PATH, "r") as f:
        notebook = f.read()
        notebook_json = json.loads(notebook)
        for cell in notebook_json["cells"]:
            if cell["cell_type"] == "code" and tag in cell["metadata"]["tags"]:
                return cell["source"]
    pytest.fail(f"Can't find code cell with the tag {tag}")


@pytest.mark.abort_on_fail
def test_integrate_prometheus():
    """Test integrate Prometheus."""
    code = get_source("integrate_prometheus")
    for line in code:
        logger.info(f"Executing line: {line}")
        subprocess.run(shlex.split(line), check=True, capture_output=True)


@pytest.mark.abort_on_fail
def test_integrate_grafana():
    """Test integrate Grafana."""
    code = get_source("integrate_grafana")
    logger.info(f"Executing code block: {code}")
    for line in code:
        logger.info(f"Executing code: {line}")
        subprocess.run(shlex.split(line), check=True, capture_output=True)


def test_access_prometheus_metrics():
    """Test access Prometheus metrics."""
    code = get_source("access_prometheus_metrics")
    logger.info(f"Executing code block: {code}")
    code_block = "".join(code)
    subprocess.run(code_block, shell=True, check=True, capture_output=True)


def test_access_grafana_dashboards():
    """Test access Grafana dashboards."""
    code = get_source("access_grafana_dashboards")
    code_block = "".join(code)
    subprocess.run(code_block, shell=True, check=True, capture_output=True)


@pytest.mark.parametrize(
    "charm_name",
    [
        "argo-controller",
        "jupyter-controller",
        "seldon-core",
    ],
)
def test_grafana_dashboard_content(charm_name):
    """Compare the content of grafana dashbaords in the deployment to pre-saved dashboards."""
    expected_dashboard_path = f"resources/{charm_name}-dashboard.json"
    with open(expected_dashboard_path, "r") as f:
        expected_contents = f.read()
    get_dashboard_cmd = f"juju ssh -mcos --container grafana grafana/0 cat /etc/grafana/provisioning/dashboards/juju_{charm_name}*"
    # TODO use tenacity to wait for dashboards to be created
    while True:
        output = subprocess.run(get_dashboard_cmd, shell=True, capture_output=True)
        if output.returncode == 0:
            break
        else:
            logger.info(
                f"Unable to get dashboard from Grafana container. \nFailed with code: {output.returncode}, \nstdout: {output.stdout}, \nstderr {output.stderr}"
            )
    actual_contents = output.stdout.decode()
    assert expected_contents == actual_contents
