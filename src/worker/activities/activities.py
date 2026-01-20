from time import sleep

from temporalio import activity

from worker.api.call_llm import call_llm_api
from worker.logs.logger import get_activity_logger


class ToolActivities:

    def __init__(self):
        self.act_logger = get_activity_logger()
        self.act_logger.info(f"Init Activities")


    @activity.defn
    async def call_external_api(self, prompt):
        self.act_logger.info(f"Start activity for {prompt}")

        try:
            #result =  await call_llm_api(prompt)
            sleep(5)
            result = f"call anwser {prompt}"
            self.act_logger.debug(f"calculated result: {result}")
            return result
        except Exception as e:
            self.act_logger.exception(f"Activity error: {e}")
            raise


    @activity.defn
    async def get_database_data(self, name: str) -> str:
        self.act_logger.info(f"Start activity for {name}")

        try:
            sleep(3)
            result = f"Hello {name}!"
            self.act_logger.debug(f"calculated result: {result}")
            return result
        except Exception as e:
            self.act_logger.exception(f"Activity error: {e}")
            raise