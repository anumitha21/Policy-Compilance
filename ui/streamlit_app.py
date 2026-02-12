# ui/streamlit_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Contract Compliance AI", layout="wide")

st.title("Contract Compliance AI")
st.write("Enter a contract clause and analyze compliance, risk, and policy citations.")

clause_text = st.text_area("Contract Clause", height=150)

if st.button("Analyze Clause"):
    if not clause_text.strip():
        st.warning("Please enter a clause.")
    else:
        with st.spinner("Analyzing clause..."):
            # Call your local API
            try:
                response = requests.post(
                    "http://localhost:8000/analyze_clause/",
                    json={"clause_text": clause_text}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.subheader("✅ Refined Output")
                    st.write(result["refined_output"])

                    st.subheader("⚠️ Risk Score")
                    st.write(result["risk_score"])

                    st.subheader("📄 Citations")
                    for c in result["citations"]:
                        st.write(f"- {c}")

                    st.subheader("🔍 Hallucination Check")
                    st.write(result["grounding_check"])

                    st.subheader("📌 Policy Validation Check")
                    st.write(result["policy_check"])
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
