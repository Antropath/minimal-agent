# minimal-agent

A minimalistic implementation of an LLM agent that can write actions in code to solve tasks. The focus is on simplicity and education. `minimal-agent` shows that the central idea behind LLM agents is simple. Creating a basic agent from scratch is not rocket science with today's advanced LLMs.

This focus of course implies tradeoffs. For example, there are fewer validation steps, less gracious error handling or edge cases covered than one would like to see in a full-blown production-ready library. But that's OK given the objectives mentioned above - and it pays off. The core `agent.py` module is only ~100 lines long (excluding extensive comments). 

The agent itself is built from scratch using just a few libraries and extensively commented. It is, however, inspired by [Hugging Face's Smolagents library](https://github.com/huggingface/smolagents/tree/main).

The code agent needs a controlled and isolated environment to run the code it generates. However, creating such an environment is not really a core AI challenge and building it from scratch here would add little value. For this reason, this repo relies on Smolagents' [local python executor](https://github.com/huggingface/smolagents/blob/main/src/smolagents/local_python_executor.py) for local code execution.

## Usage

### Clone and Install

1. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for Python packaging and environment creation.

2. Clone the repo:
   ```bash
   git clone https://github.com/Antropath/minimal-agent.git
   cd minimal-agent
   ```

3. Set up your model and API keys:
   
   The repo uses [LiteLLM](https://docs.litellm.ai/) to support a unified interface across all model providers. Create a `.env` file in the `minimal-agent` folder and add the `MODEL` environment variable with the name of the model as specified on LiteLLM, along with the credentials for the corresponding provider.
   
   Example for AWS Bedrock (*):
   ```bash
   # AWS Bedrock: https://docs.litellm.ai/docs/providers/bedrock
   AWS_ACCESS_KEY_ID=<YOUR-AWS-ACCESS-KEY-ID>
   AWS_SECRET_ACCESS_KEY=<YOUR-AWS-SECRET-ACCESS-KEY>
   AWS_REGION_NAME=<YOUR-AWS-REGION-NAME>

   MODEL="bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
   ```

   Example for Google Gemini:
   ```bash
   # Google Gemini: https://docs.litellm.ai/docs/providers/gemini
   GEMINI_API_KEY=<YOUR-API-KEY>

   MODEL="gemini/gemini-2.0-flash"
   ```

   For other model providers, refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/providers). You might have to add additional dependencies for a given model provider, which are mentioned in the LiteLLM docs. You can add them using `uv add <your-python-package>`. For example, Bedrock models require `boto3`, which has already been added. If you don't use AWS-provided models you can also remove `boto3`.
   
   Note that coding agents require powerful LLMs, such as Claude 3.7 Sonnet, Amazon Nova Pro, or Gemini 2.0 Flash. While you can use this code with less powerful models, the results might not be great.

Note that the agent implemented in `run_agent.py` is using DuckDuckGo as default web search tool. The benefit of DuckDuckGo is that it doesn't need an API key, meaning that you can run the agent without any other setup. The drawback is that you might run into rate limits quickly. To avoid these rate limits, you can replace DuckDuckGo with [Tavily](https://www.tavily.com/) as web search too. For that, you need to replace the search tools in `run_agent.py`, create a [Tavily](https://www.tavily.com/) account, get an API key and add it to your `.env` file:
   ```bash
   TAVILY_API_KEY=<YOUR-TAVILY-API-KEY>
   ```

4. Run the example:
   ```bash
   uv run run_agent.py
   ```

(*) Note that there are better [ways to authenticate](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#credentials) with AWS than access keys that are also supported by LiteLLM through boto3. The method above was mentioned because it is the first one mentioned on LiteLLM and provides consistency across providers.

### Usage Example

The default example runs a query about "the hottest day in 2024 and the Dow Jones value on that day" and provides the agent with the ability to search the internet and visit websites to find the answer.

You can modify the task in `run_agent.py`:
```python
res = agent.run("<Your task here in natural language>")
```

## Agent Architecture

The architecture follows the [ReAct framework](https://arxiv.org/abs/2210.03629). The agent completes its taks in a sequence of steps. In each step it can "Reason" and "Act" (= ReAct). The agent will perform as many steps as needed to complete the task.

So, the core idea is really simple and elegant and `minimal-agent` implements it just like that. Below is the architecture diagram:

![`minimal-agent` architecture](./media/architecture.svg)

Check out `src/minimal_agent/agents.py` to see the corresponding source code.


For a more detail introduction to agents and to understand different levels of AI agents, Hugging Face's [AI Agent Course](https://huggingface.co/learn/agents-course/en/unit1/what-are-agents) is a good start.

Note that many AI agent frameworks (allow to) abstract the ReAct framework. However, the actual call graph is often much more complex because they either added additional capabilities or had to introduce components to make it work in very general scenarios (e.g. more gracious error handling.)

This can be very useful. The code in this repo might fail for several tasks precisely because this is missing.

However, for educational purposes and even for more specific use cases with very narrow tasks, it's more effective to start with simpler code and tailor it to the requirements rather than adapting a more complex framework.
