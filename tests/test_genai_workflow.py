import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from worker_simple.activities.activities import ToolActivities
from worker_simple.workflows.genai_workflow import GenAIWorkflow


##
# Automatically advance time, use the start_time_skipping() method.
# Running a full local Temporal Server, utilize the start_local() method.
# Running an existing Temporal Server, opt for the from_client() method.


@activity.defn(name="get_database_data_v2")
async def get_database_data_mocked(name: str) -> str:
    return "dataerror"

@pytest.mark.asyncio
async def test_genai_workflow_full_run():
    # 1. Start a local time-skipping workflows environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # 2. Setup a worker_simple dedicated to the test
        async with Worker(
                env.client,
                task_queue="test-tq",
                workflows=[GenAIWorkflow],
                activities=[ToolActivities().call_external_api, ToolActivities().get_database_data,  ToolActivities().get_database_data_v2],
        ):
            # 3. Execute the workflows
            result = await env.client.execute_workflow(
                "GenAIWorkflow",
                "Summarize AI history",
                id="test-workflows-id",
                task_queue="test-tq",
            )

            assert "AI" in result


@pytest.mark.asyncio
async def test_genai_workflow_full_run_error():
    # 1. Start a local time-skipping workflows environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # 2. Setup a worker_simple dedicated to the test
        async with Worker(
                env.client,
                task_queue="test-tq",
                workflows=[GenAIWorkflow],
                activities=[ToolActivities().call_external_api, get_database_data_mocked,  ToolActivities().get_database_data],
        ):
            # 3. Execute the workflows
            result = await env.client.execute_workflow(
                "GenAIWorkflow",
                "Summarize AI history",
                id="test-workflows-id",
                task_queue="test-tq",
            )

            assert "AI" not in result