from temporalio.client import Client
from temporalio.service import TLSConfig
from temporalio.worker import Worker

from worker_simple.config.DefaultSettings import DefaultSettings
from worker_simple.activities.activities import ToolActivities
from worker_simple.logs.log_config import setup_logger

from worker_simple.logs.logger import get_logger
from worker_simple.workflows.genai_workflow import GenAIWorkflow


def file_to_bytes(file_path: str):
    with open(file_path, 'rb') as file:
        return file.read()

async def main():
    setup_logger()

    logger = get_logger()
    logger.info("Start Temporal worker_simple")

    rpc_metadata = {
        "authorization": f"Bearer {DefaultSettings().temporal_server_bearer}",
        # "api-key": ""
    }

    try:

        if DefaultSettings().temporal_server_tls:
            tls_config = TLSConfig(
                server_root_ca_cert=file_to_bytes(""),
                client_cert=None)
        else:
            tls_config = None

        client = await Client.connect(
            DefaultSettings().temporal_server_url,
            tls=tls_config,
            namespace="default",
            identity="client",
            rpc_metadata=rpc_metadata
        )

        logger.info("Worker connected, continue...")

    except Exception as ex:
        print(f"x Error: {ex}")
        raise

    # create Tool inctance
    tool_activities = ToolActivities()

    # create worker_simple and register the workflows and activity
    worker = Worker(
        client,
        task_queue="myapp-tasks-queue",
        workflows=[GenAIWorkflow],
        activities=[tool_activities.call_llm_activity, tool_activities.get_database_data, tool_activities.get_database_data_v2]
    )

    logger.success("Worker configured, starting...")


    # Start the worker_simple
    try:
        await worker.run()
    except Exception as e:
        logger.exception(f"Worker execution error: {e}")
    finally:
        logger.info("Worker stopped")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
