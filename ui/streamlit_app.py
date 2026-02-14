import streamlit as st
import requests

st.set_page_config(page_title="Contract Compliance AI", layout="centered")
st.title("📑 Contract Compliance AI")

clause_text = st.text_area("✍️ Contract Clause", height=150)

if st.button("Analyze Clause"):

    if not clause_text.strip():
        st.warning("Please enter a contract clause.")
    else:
        with st.spinner("Analyzing clause..."):

            try:
                response = requests.post(
                    "http://localhost:8000/analyze_clause/",
                    json={"clause_text": clause_text}
                )

                result = response.json()

                # Clause
                st.subheader("📜 Input Clause")
                st.write(clause_text)

                # Compliance
                st.subheader("✅ Compliance Analysis")
                refined = result.get("refined_output", "")

                if isinstance(refined, dict):
                    compliance_text = refined.get("explanation", "No explanation")
                else:
                    compliance_text = refined

                st.write(compliance_text)

                # Risk Score
                st.subheader("⚠️ Risk Score")
                st.write(result.get("risk_score", "N/A"))

                # Citations
                st.subheader("📚 Policy Evidence")
                citations = result.get("citations", [])
                if citations:
                    for c in citations:
                        st.write(f"- Policy Chunk ID: {c}")
                else:
                    st.write("No citations")

                # Verified Output
                st.subheader("🧠 Verified AI Output")
                ground = result.get("grounding_check", {})
                if isinstance(ground, dict) and ground.get("is_grounded"):
                    st.success("AI output grounded in policies.")
                else:
                    st.error("AI output may be hallucinated.")

            except Exception as e:
                st.error(f"Backend not running: {e}")
