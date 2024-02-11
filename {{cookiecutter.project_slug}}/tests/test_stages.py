import pytest
import logging

from flowdapt.compute.workflow.execute import execute_workflow
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
def workflow_config():
    return {
        "study_identifier": TESTING_NAMESPACE,
        "model_train_parameters": {
            "n_jobs": 4,
            "n_estimators": 100,
            "verbosity": 1,
            "epochs": 2,
            "batch_size": 5,
            "lookback": 5,
            "shuffle": False,
        },
        "data_config": {
            "origins": "openmeteo",
            "frequencies": "hourly",
            "n_days": 20,
            "neighbors": 2,
            "radius": 150,
            "prediction_points": 1,
            "target_horizon": 6,
            "city_data_path": "user_data/plugins/openmeteo/uscities.csv",
            "models": ["XGBoostRegressor", "PyTorchTransformer"],
            "cities": ['Los Angeles'],
            "horizon_cut": [False],
            "reuse": [False],
            "targets": ["temperature_2m"],
            "drift_pct": 0.05
        },
        "extras": {},
        # We need this here for testing so we aren't actually writing any files
        "storage": {
            "protocol": "memory",
            "base_path": "test_data",
        }
    }


@pytest.fixture
def example_workflow_definition(workflow_config):
    return {
        "name": "example_workflow",
        "config": workflow_config,
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

async def test_example_workflow(example_workflow_definition, executor):
    # We set return_result to True so any errors that are raised in the stage
    # are bubbled up here so we can see the traceback
    result = await execute_workflow(
        workflow=example_workflow_definition,
        input={},
        namespace=TESTING_NAMESPACE,
        return_result=True,
        executor=executor,
    )
    assert result == "Hello from second stage!"
