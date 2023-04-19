# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
import shlex
import json
import subprocess
import pytest

logger = logging.getLogger(__name__)

NOTEBOOK_PATH = "kubeflow-cos-integration.ipynb"


def get_source(tag):
    with open(NOTEBOOK_PATH, "r") as f:
        notebook = f.read()
        notebook_json = json.loads(notebook)
        for cell in notebook_json["cells"]:
            if cell["cell_type"] == "code" and tag in cell["metadata"]["tags"]:
                return cell["source"]
    pytest.fail(f"Can't find code cell with the tag {tag}")


@pytest.mark.abort_on_fail
async def test_integrate_prometheus():
    code = get_source("integrate_prometheus")
    for line in code:
        logger.info(f"Executing code cell: {line}")
        subprocess.run(shlex.split(line), check=True, capture_output=True)


@pytest.mark.abort_on_fail
async def test_integrate_grafana():
    code = get_source("integrate_grafana")
    for line in code:
        logger.info(f"Executing code cell: {line}")
        subprocess.run(shlex.split(line), check=True, capture_output=True)


async def test_access_prometheus_metrics():
    code = get_source("access_prometheus_metrics")
    code_block = "".join(code)
    subprocess.run(code_block, shell=True, check=True)


async def test_access_grafana_dashboards():
    code = get_source("access_grafana_dashboards")
    code_block = "".join(code)
    subprocess.run(code_block, shell=True, check=True, capture_output=True)
