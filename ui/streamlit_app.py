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
                results = result.get("results", [])
                if not results:
                    st.success("✅ No compliance risks detected.")
                else:
                    st.header("🚩 Flagged Clauses")
                    for res in results:
                        st.markdown(f"### {res.get('clause_name', '')}")
                        st.markdown(f"**Status:** {res.get('compliance', '')}")
                        st.markdown(f"**Risk Score:** {res.get('risk_score', '')}")
                        st.markdown(f"**Issue:** {res.get('explanation', '')[:120]}")
                        st.markdown("**Policy Reference:**")
                        for ev in res.get("policy_evidence", []):
                            ref = f"{ev.get('source', '')}"
                            if ev.get('article', ''):
                                ref += f", Article {ev.get('article', '')}"
                            ref += f" (ID: {ev.get('chunk_id', '')})"
                            st.markdown(f"- {ref}")
                            st.markdown(f"  _Excerpt_: \"{ev.get('excerpt', '')[:120]}\"")
            except Exception as e:
                st.error(f"Backend not running: {e}")
