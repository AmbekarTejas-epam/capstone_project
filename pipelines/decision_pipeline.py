from agents.decision_agent import DecisionSupportAgent


class DecisionPipeline:
    def __init__(self):
        self.agent = DecisionSupportAgent()

    def run(self, question: str) -> str:
        q = question.lower()

        # ---- INTENT → TOOL ROUTING (CRITICAL) ----
        if any(word in q for word in ["trend", "trending", "over time", "performance"]):
            question = (
                "You MUST use the trend_analysis tool to answer.\n"
                + question
            )

        if any(word in q for word in ["anomaly", "spike", "drop", "unusual"]):
            question = (
                "You MUST use the anomaly_detection tool to answer.\n"
                + question
            )

        if any(word in q for word in ["promo", "promotion", "discount"]):
            question = (
                "You MUST use the promo_simulation tool to answer.\n"
                + question
            )

        if any(word in q for word in ["price", "pricing"]):
            question = (
                "You MUST use the price_change_simulation tool to answer.\n"
                + question
            )

        if any(word in q for word in ["supply", "shortage"]):
            question = (
                "You MUST use the supply_shortage_simulation tool to answer.\n"
                + question
            )

        return self.agent.ask(question)
