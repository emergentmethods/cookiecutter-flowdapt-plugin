import pytest
import logging

from flowdapt.compute.resources.workflow.execute import execute_workflow
from flowdapt.compute.executor.local import LocalExecutor

from {{ cookiecutter.project_slug }}.stages import (
    first_stage,
    second_stage,
)

logger = logging.getLogger(__name__)

TESTING_NAMESPACE = "testing"

# Use a Session scoped Executor so any data persisted to the object store
# lives for the entire test run
@pytest.fixture(scope="session")
async def executor():
    try:
        executor = LocalExecutor(use_processes=False)
        logger.info("Starting Executor")
        await executor.start()
        yield executor
    finally:
        logger.info("Closing Executor")
        await executor.close()


@pytest.fixture
def example_workflow_definition():
    return {
        "metadata": {
            "name": "example_workflow",
        },
        "spec": {
            "stages": [
                {
                    "name": "first_stage",
                    "target": first_stage,
                },
                {
                    "name": "second_stage",
                    "target": second_stage,
                    "depends_on": ["first_stage"],
                },
            ]
        }
    }


async def test_example_workflow(example_workflow_definition, executor):
    # We set return_result to True so any errors that are raised in the stage
    # are bubbled up here so we can see the traceback
    result = await execute_workflow(
        workflow=example_workflow_definition,
        namespace=TESTING_NAMESPACE,
        return_result=True,
        executor=executor,
    )
    assert result == "Hello from second stage!"
