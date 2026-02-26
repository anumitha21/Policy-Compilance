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
                    st.info("No compliance risks detected for this clause.")
                else:
                    for res in results:
                        st.markdown(f"**Clause:** {res.get('clause_name', '')}")
                        st.markdown(f"**Compliance:** {res.get('compliance', '')}")
                        st.markdown(f"**Explanation:** {res.get('explanation', '')}")
                        st.markdown(f"**Risk Score:** {res.get('risk_score', '')}")
                        st.markdown("**Policy Evidence:**")
                        for ev in res.get("policy_evidence", []):
                            st.markdown(f"- Source: {ev.get('source', '')}")
                            st.markdown(f"  - Article: {ev.get('article', '')}")
                            st.markdown(f"  - Chunk ID: {ev.get('chunk_id', '')}")
                            st.markdown(f"  - Excerpt: \"{ev.get('excerpt', '')}\"")
            except Exception as e:
                st.error(f"Backend not running: {e}")
