import streamlit as st
import json
from llm.client import LLMClient
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from llm.logging_config import logger

st.set_page_config(page_title="AI Operations Assistant", layout="wide")

st.title("🤖 AI Operations Assistant")
st.markdown("---")

# Sidebar for configuration status
st.sidebar.header("System Status")
if st.sidebar.button("Check API Keys"):
    from dotenv import load_dotenv
    import os
    load_dotenv()
    gemini_key = "✅" if os.getenv("GEMINI_API_KEY") else "❌"
    github_token = "✅" if os.getenv("GITHUB_TOKEN") else "⚠️ (Optional)"
    weather_key = "✅" if os.getenv("OPENWEATHER_API_KEY") else "❌"
    
    st.sidebar.write(f"Gemini: {gemini_key}")
    st.sidebar.write(f"GitHub: {github_token}")
    st.sidebar.write(f"Weather: {weather_key}")
    st.sidebar.write(f"Model: {os.getenv('MODEL_NAME', 'gemini-2.0-flash')}")

# Query Input
user_query = st.text_input("Enter your task:", placeholder="e.g., 'Search for FastAPI repos and get weather in London'")

if st.button("Run Assistant") and user_query:
    try:
        llm_client = LLMClient()
        planner = PlannerAgent(llm_client)
        executor = ExecutorAgent()
        verifier = VerifierAgent(llm_client)

        with st.status("Processing Task...", expanded=True) as status:
            # Step 1: Planning
            st.write("📋 Planning steps...")
            plan = planner.create_plan(user_query)
            st.json(plan.dict())
            
            # Step 2: Execution
            st.write("⚙️ Executing tools...")
            results = executor.execute_plan(plan)
            st.json(results)
            
            # Step 3: Verification
            st.write("✅ Verifying and finalizing...")
            final_report = verifier.verify_and_finalize(user_query, results)
            status.update(label="Task Complete!", state="complete", expanded=False)

        # Final Result
        st.subheader("Final Result")
        st.write(final_report.final_output)

        if not final_report.is_complete:
            st.warning(f"Note: {final_report.summary}")
            if final_report.missing_info:
                st.info(f"Missing Information: {final_report.missing_info}")
        else:
            st.success("Task completed successfully!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.sidebar.markdown("""
### Example Prompts:
1. Search for popular Python projects on GitHub.
2. What is the current weather in Paris?
3. Find top React repositories and check the weather in Tokyo.
""")
