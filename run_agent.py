import os

from dotenv import load_dotenv

from minimal_agent.agent import Agent
from minimal_agent.tools import VisitWebpageTool, TavilySearchTool

load_dotenv()


if __name__ == "__main__":
    agent = Agent(
        model=os.environ.get("MODEL"),
        tools=[
            # For this tool, make sure the TAVILY_API_KEY environment variable is set.
            # You can get a free API key at https://tavily.com.
            # TavilySearchTool(max_results=10),
            # You can try DuckDuckGoSearchTool as default web search tool as it doesn't require an API key,
            # but often errors due to rate limits. If this is a problem, uncomment this tool and use Tavily above.
            DuckDuckGoSearchTool(max_results=10),
            VisitWebpageTool(max_output_length=1000),
        ],
    )

    res = agent.run(
        "What was the hottest day in 2024 and how much was the Dow Jones on that day?"
    )

    print(20 * "-")
    print(f"The final answer is:\n\n{res}")
