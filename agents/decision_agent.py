"""
Decision Support Agent for CPG Business Intelligence

This agent:
- Uses Gemini Flash via LangChain
- Loads API key securely from .env
- Chooses analytical & simulation tools autonomously
- Generates executive-ready business recommendations
"""
from llm.llm_factory import LLMFactory
import yaml

from logging import config
import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.chat_models import ChatOllama
import yaml


from agents.memory import AgentMemory
from tools.trend_analysis import TrendAnalysisTool
from tools.anomaly_detection import AnomalyDetectionTool
from tools.scenario_simulation import ScenarioSimulationTool

# ------------------------------------------------------------------
# System Prompt (Defines agent reasoning behaviour)
# ------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a senior CPG (Consumer Packaged Goods) decision analyst.

Your responsibilities:
- Understand business questions clearly
- Decide which analytical tools to use
- Call tools in the correct sequence
- Base all reasoning strictly on tool outputs
- Clearly state assumptions
- Generate concise, executive-ready strategy recommendations

Rules:
- Do NOT guess or hallucinate numbers
- Use tools whenever calculations or data are required
- Keep explanations business-focused, not technical
- Always aim to support a business decision
"""


# ------------------------------------------------------------------
# Tool Loader
# ------------------------------------------------------------------
def load_tools() -> List[Tool]:
    """
    Registers all analytical and simulation tools
    in a LangChain-compatible format.
    """

    trend_tool = TrendAnalysisTool("data/raw/sales.csv")
    anomaly_tool = AnomalyDetectionTool("data/raw/sales.csv")
    scenario_tool = ScenarioSimulationTool("data/raw/sales.csv")

    return [
        Tool(
            name="trend_analysis",
            func=lambda args: trend_tool.analyze(**args),
            description=(
                "Analyze sales trends over time by SKU, store, or date range. "
                "Use this to understand growth, decline, or seasonality."
            ),
        ),
        Tool(
            name="anomaly_detection",
            func=lambda args: anomaly_tool.detect(**args),
            description=(
                "Detect abnormal spikes or drops in sales. "
                "Useful for identifying demand shocks or supply issues."
            ),
        ),
        Tool(
            name="promo_simulation",
            func=lambda args: scenario_tool.simulate_promo(**args),
            description=(
                "Simulate the impact of a promotional discount on sales and revenue."
            ),
        ),
        Tool(
            name="price_change_simulation",
            func=lambda args: scenario_tool.simulate_price_change(**args),
            description=(
                "Simulate the impact of price increases or decreases using elasticity."
            ),
        ),
        Tool(
            name="supply_shortage_simulation",
            func=lambda args: scenario_tool.simulate_supply_shortage(**args),
            description=(
                "Simulate the impact of supply shortages on sellable units."
            ),
        ),
    ]


# ------------------------------------------------------------------
# Decision Support Agent
# ------------------------------------------------------------------
class DecisionSupportAgent:
    """
    Agent that orchestrates tools, reasoning, and
    business strategy generation.
    """

    def __init__(self):
        # -------------------------------
        # LLM Configuration (Gemini Flash)
        # -------------------------------
        with open("configs/app_config.yaml") as f:
            config = yaml.safe_load(f)

        self.llm = LLMFactory.create_llm(config)
    


        # -------------------------------
        # Load Tools & Memory
        # -------------------------------
        self.tools = load_tools()
        self.memory = AgentMemory().get()

        # -------------------------------
        # Initialize Agent
        # -------------------------------
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            memory=self.memory,
            verbose=True,
            system_message=SYSTEM_PROMPT,
        )

    def ask(self, query: str) -> str:
        """
        Ask a business question to the decision support agent.

        Parameters:
            query (str): Business question

        Returns:
            str: Agent response with insights and recommendations
        """
        return self.agent.run(query)
