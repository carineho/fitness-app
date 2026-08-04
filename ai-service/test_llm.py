from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from pydantic_ai import Agent

class TestResponse(BaseModel):
    greeting: str
    fun_fact_about_climbing: str

agent = Agent(
    "groq:llama-3.3-70b-versatile",
    output_type=TestResponse,
    system_prompt="You are a helpful fitness assistant.",
)

result = agent.run_sync("Say hello and share a fun fact about climbing.")
print(result.output)