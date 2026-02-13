import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pipelines.decision_pipeline import DecisionPipeline

st.set_page_config(
    page_title="CPG Decision Support Agent",
    layout="wide"
)

st.title("📊 CPG Decision Support Agent")
st.caption("Agentic AI for sales, pricing, and promotion decisions")

pipeline = DecisionPipeline()

question = st.text_area(
    "Ask a business question:",
    placeholder="e.g. What happens if we run a 20% promo on SKU001?"
)

if st.button("Run Analysis"):
    if question.strip():
        with st.spinner("Analyzing business scenario..."):
            response = pipeline.run(question)

        st.subheader("📌 Agent Recommendation")
        st.write(response)
    else:
        st.warning("Please enter a question.")
