from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError
from temporalio.workflow import patched

with workflow.unsafe.imports_passed_through():
    from worker_simple.activities.activities import ToolActivities
    from worker_simple.logs.logger import get_workflow_logger


# Define a resilient retry strategy for unstable AI APIs
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1), # Start with a 1s delay
    backoff_coefficient=2.0,               # Double the delay each time
    maximum_attempts=5,                    # Cap retries to avoid infinite loops
    non_retryable_error_types=["InvalidPromptError"] # Fail immediately if the input is bad
)

@workflow.defn
class GenAIWorkflow:

    def __init__(self):
        self.wkf_logger = get_workflow_logger()
        self.wkf_logger.info(f"Init Workflows")

    # Workflow example
    # a- Get database data
    # b- Call LLM API
    @workflow.run
    async def run(self, api_request):

        try:

            #name = api_request
            get_data_result = ""
            if patched('v3'):
                get_data_result = await workflow.execute_activity(
                    ToolActivities.get_database_data_v2,
                    args=[api_request],
                    # Activity Execution Timeout
                    start_to_close_timeout=timedelta(seconds=10),
                    # schedule_to_start_timeout=timedelta(seconds=10),
                    # schedule_to_close_timeout=timedelta(seconds=20),
                    retry_policy=retry_policy
                )
            else:
                get_data_result = await workflow.execute_activity(
                    ToolActivities.get_database_data,
                    args=[api_request],
                    # Activity Execution Timeout
                    start_to_close_timeout=timedelta(seconds=10),
                    # schedule_to_start_timeout=timedelta(seconds=10),
                    # schedule_to_close_timeout=timedelta(seconds=20),
                    retry_policy=retry_policy
                )

            self.wkf_logger.info("==>"+get_data_result)

            result = await workflow.execute_activity(
                ToolActivities.call_llm_activity,
                args=[get_data_result],
                # Activity Execution Timeout
                start_to_close_timeout=timedelta(seconds=10),
                # schedule_to_start_timeout=timedelta(seconds=10),
                # schedule_to_close_timeout=timedelta(seconds=20),
                retry_policy=retry_policy
            )

            self.wkf_logger.info("===>"+result)

            return result
        except ApplicationError as e:
            raise ApplicationError(f"Failed to manage client request")
