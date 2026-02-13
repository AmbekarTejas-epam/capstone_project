from langchain_openai import ChatOpenAI
import os


class LLMFactory:
    @staticmethod
    def create_llm(config):
        provider = config["llm"]["provider"]

        if provider == "databricks":
            return ChatOpenAI(
                model="databricks-gpt-oss-120b",
                base_url=config["llm"]["base_url"],
                api_key=config["llm"]["api_key"],
                temperature=config["llm"]["temperature"]
            )

        raise ValueError("Unsupported LLM provider")
