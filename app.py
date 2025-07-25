import asyncio
import streamlit as st
import structlog
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from weather.client import fetch_weather

load_dotenv(override=True)
log = structlog.get_logger()

@function_tool
async def get_current_weather(latitude: float, longitude: float) -> dict:
    return await fetch_weather(latitude, longitude)

instructions = """
You are a weather assistant agent.
Given current weather data, produce two sections:

Weather Summary:
- Human friendly description.

Suggestions:
- Actionable advice and safety tips.
"""

weather_specialist_agent = Agent(
    name="Weather Specialist Agent",
    instructions=instructions,
    tools=[get_current_weather],
    tool_use_behavior="run_llm_again",
)

async def run_agent(query: str) -> str:
    result = await Runner.run(weather_specialist_agent, query)
    return result.final_output

# ---------- FIX: sync wrapper so Streamlit can cache ---------- #
@st.cache_data(ttl=300)
def cached_answer(query: str) -> str:
    return asyncio.run(run_agent(query))

# -------------------------------------------------------------- #
def main() -> None:
    st.set_page_config(page_title="Weather Assistant", page_icon="☀️")
    st.title("🌤️ Weather Assistant")

    query = st.text_input("Ask about the weather (e.g. “Bangkok today”):")

    if st.button("Get weather update", type="primary"):
        if not query.strip():
            st.error("Please enter a question.")
            st.stop()
        with st.spinner("Thinking…"):
            answer = cached_answer(query)
            st.write(answer)

if __name__ == "__main__":
    main()
