import pytest
from temporalio.testing import ActivityEnvironment

from worker_simple.activities.activities import ToolActivities


@pytest.mark.asyncio
async def test_call_gemini_activity_success():
    env = ActivityEnvironment()
    # Mocking or actual call (using a test API Key)
    prompt = "Hello, world!"

    # We execute the activity in a test environment
    tools = ToolActivities()
    result = await env.run(tools.call_llm_activity, prompt)

    assert isinstance(result, str)
    assert len(result) > 0