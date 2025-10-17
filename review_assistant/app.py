import os
import json
import textwrap
from datetime import datetime
from typing import List, Dict, Any

import streamlit as st

from review_assistant.clients.deepseek_client import DeepSeekClient
from review_assistant.orchestrator import ReviewOrchestrator
from review_assistant.utils.samples import load_sample_code_snippets, load_standards_text


st.set_page_config(page_title="Application Development Code Review Assistant", layout="wide")


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "latest_report" not in st.session_state:
        st.session_state.latest_report = None


def render_sidebar():
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("DeepSeek API Key", type="password", help="Set DEEPSEEK_API_KEY env var or paste here")
    model = st.sidebar.text_input("Model", value="deepseek-chat")
    temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.2, 0.1)
    max_tokens = st.sidebar.number_input("Max tokens", min_value=256, max_value=32768, value=2048, step=256)

    if api_key:
        os.environ["DEEPSEEK_API_KEY"] = api_key

    st.sidebar.divider()
    st.sidebar.subheader("Samples")
    if st.sidebar.button("Load Python Sample"):
        st.session_state["sample_code"] = load_sample_code_snippets()["python"]
    if st.sidebar.button("Load JS Sample"):
        st.session_state["sample_code"] = load_sample_code_snippets()["javascript"]
    if st.sidebar.button("Load Standards Doc"):
        st.session_state["standards_text"] = load_standards_text()

    show_agents = st.sidebar.toggle("Show agent internals", value=False)
    return {
        "model": model,
        "temperature": temperature,
        "max_tokens": int(max_tokens),
        "show_agents": show_agents,
    }


def main_ui(config: Dict[str, Any]):
    st.title("Application Development Code Review Assistant")
    st.caption("Analyze code for style, quality, potential bugs, and best practices.")

    col1, col2 = st.columns(2)
    with col1:
        code = st.text_area("Paste code to review", value=st.session_state.get("sample_code", ""), height=360)
        language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "go"], index=0)
    with col2:
        standards_text = st.text_area("Coding standards / guidelines (optional)", value=st.session_state.get("standards_text", ""), height=360)
        objectives = st.text_area("Additional instructions (optional)", value="Focus on readability, maintainability, and potential runtime errors.", height=120)

    run_button = st.button("Run Review", type="primary")

    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    has_key = bool(deepseek_key)

    client = DeepSeekClient(api_key=deepseek_key, model=config["model"], temperature=config["temperature"], max_tokens=config["max_tokens"]) if has_key else None

    orchestrator = ReviewOrchestrator(client=client, use_llm=has_key)

    if run_button:
        if not code.strip():
            st.warning("Please paste code to review.")
            return
        with st.spinner("Analyzing code with multi-agent reviewers..."):
            report, agent_traces = orchestrator.run_review(
                code=code,
                language=language,
                standards=standards_text,
                objectives=objectives,
            )
        st.session_state.latest_report = report

        st.subheader("Review Report")
        st.markdown(report)

        if config["show_agents"] and agent_traces:
            st.subheader("Agent Internals")
            for agent_name, trace in agent_traces.items():
                with st.expander(agent_name, expanded=False):
                    st.markdown(trace)

        # Download
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_name = f"code_review_{timestamp}.md"
        st.download_button("Download Report", data=report.encode("utf-8"), file_name=file_name, mime="text/markdown")

    st.divider()
    st.subheader("Session History")
    if st.session_state.latest_report:
        st.session_state.history.append(st.session_state.latest_report)
    if st.session_state.history:
        for i, rep in enumerate(reversed(st.session_state.history[-5:]), start=1):
            with st.expander(f"Past report {i}"):
                st.markdown(rep)


if __name__ == "__main__":
    init_state()
    config = render_sidebar()
    main_ui(config)
