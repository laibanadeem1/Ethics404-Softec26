import json
import streamlit as st
from pipeline import process_all_emails

st.set_page_config(
    page_title="Opportunity Inbox Copilot",
    page_icon="📬",
    layout="wide"
)

st.title("📬 Opportunity Inbox Copilot")
st.caption("Upload your resume and paste your emails to get personalized opportunity rankings.")

# ── Resume Upload ──────────────────────────────────────────
st.markdown("### 📄 Step 1: Upload Your Resume / CV")
cv_file = st.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])

cv_text = ""
if cv_file is not None:
    if cv_file.type == "application/pdf":
        try:
            import pdfplumber
            with pdfplumber.open(cv_file) as pdf:
                cv_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            st.success("✅ CV uploaded and parsed successfully")
        except Exception as e:
            st.error(f"Could not read PDF: {e}")
    else:
        cv_text = cv_file.read().decode("utf-8")
        st.success("✅ CV uploaded successfully")

# ── Email Input ────────────────────────────────────────────
st.markdown("### 📧 Step 2: Paste Your Emails")
email_input = st.text_area(
    "Paste emails here (separate each with ---)",
    height=250,
    placeholder="""Dear Student, we are pleased to offer...

---

Hello, you have been selected for...

---

This is a newsletter about upcoming events..."""
)

analyze_btn = st.button("🔍 Analyze Emails", type="primary", use_container_width=True)

if "results" not in st.session_state:
    st.session_state.results = []

if analyze_btn:
    if not email_input.strip():
        st.warning("Please paste at least one email.")
    elif not cv_text:
        st.warning("Please upload your CV first so we can personalize the results.")
    else:
        student_profile = {"cv_text": cv_text}
        with st.spinner("Analyzing emails... ⏳"):
            st.session_state.results = process_all_emails(email_input, student_profile)

# ── Results ────────────────────────────────────────────────
if st.session_state.results:
    results = st.session_state.results
    opportunities = [r for r in results if r.get("is_opportunity")]
    non_opps      = [r for r in results if not r.get("is_opportunity")]

    st.markdown("---")
    st.subheader(f"✅ {len(opportunities)} Opportunities Found | 🗑️ {len(non_opps)} Ignored")

    if not opportunities:
        st.info("No real opportunities detected in these emails.")

    for opp in opportunities:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {opp.get('title') or 'Untitled Opportunity'}")
                st.caption(f"📧 Email #{opp.get('email_index')} · {opp.get('organization') or 'Unknown org'}")
            with col2:
                conf = opp.get("confidence", "low")
                color = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(conf, "⚪")
                st.markdown(f"**Confidence:** {color} {conf.title()}")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Type:** {(opp.get('type') or 'N/A').title()}")
                st.markdown(f"**Deadline:** {opp.get('deadline') or opp.get('deadline_raw') or 'Not mentioned'}")
            with c2:
                st.markdown(f"**Location:** {opp.get('location') or 'Not mentioned'}")
                st.markdown(f"**Funding:** {opp.get('stipend_or_funding') or 'Not mentioned'}")
            with c3:
                st.markdown(f"**CGPA Required:** {opp.get('cgpa_required') or 'Not mentioned'}")
                st.markdown(f"**Degree:** {opp.get('degree_required') or 'Not mentioned'}")

            if opp.get("eligibility"):
                st.markdown(f"**Eligibility:** {opp['eligibility']}")

            if opp.get("documents"):
                docs = ", ".join(opp["documents"])
                st.markdown(f"**Documents needed:** `{docs}`")

            if opp.get("skills_required"):
                skills = ", ".join(opp["skills_required"])
                st.markdown(f"**Skills required:** `{skills}`")

            if opp.get("next_steps"):
                st.info(f"**Next step:** {opp['next_steps']}")

            if opp.get("link"):
                st.markdown(f"[🔗 Apply Here]({opp['link']})")

            with st.expander("View raw JSON"):
                st.json(opp)

            st.markdown("---")

    if non_opps:
        with st.expander(f"🗑️ {len(non_opps)} ignored emails"):
            for n in non_opps:
                st.markdown(f"- **Email #{n.get('email_index')}:** {n.get('reason')}")