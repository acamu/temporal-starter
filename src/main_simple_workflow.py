from datetime import timedelta

import ulid
from temporalio.client import Client
from temporalio.service import TLSConfig

from worker_simple.config.DefaultSettings import DefaultSettings
from worker_simple.logs.log_config import setup_logger
from worker_simple.logs.logger import get_logger


def file_to_bytes(file_path: str):
    with open(file_path, 'rb') as file:
        return file.read()


async def main():

    setup_logger()

    logger = get_logger()
    logger.info("Start Temporal workflow")


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

        logger.info("Application connected, continue...")

    except Exception as ex:
        print(f"x Error: {ex}")
        raise

    logger.success("Workflow, starting...")

    client_request = """my email to anwser !!!"""

    # Start the workflows
    # ULID = temps + random, lexicographiquement orderable
    workflow_id = f"order-workflow-{ulid.ulid()}"
    handle = await client.start_workflow(
        "GenAIWorkflow",
        f"{client_request} {workflow_id}",
        id=workflow_id,
        task_queue="myapp-tasks-queue",
        # Set Workflow Timeout duration
        execution_timeout=timedelta(minutes=1)
        # run_timeout=timedelta(seconds=2),
        # task_timeout=timedelta(seconds=2),
    )

    logger.success(f"Workflow, starting...(ID: {workflow_id})")

    # get Workflow ID
    workflow_handle = client.get_workflow_handle(workflow_id)

    # ....

    result = await workflow_handle.result()
    logger.success(f"Workflow result : {result}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
