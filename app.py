import threading
import json
import streamlit as st
from flask import Flask, request, jsonify
from pipeline import process_all_emails

flask_app = Flask(__name__)

@flask_app.route("/receive", methods=["POST"])
def receive_emails():
    data = request.get_json()
    emails = data.get("emails", [])
    with open("received_emails.json", "w") as f:
        json.dump(emails, f)
    return jsonify({"status": "ok", "count": len(emails)})

def run_flask():
    flask_app.run(port=5050, debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()

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
st.markdown("### 📧 Step 2: Load Emails")
manual_input = ""
tab1, tab2 = st.tabs(["🔌 From Gmail Extension", "✍️ Paste Manually"])

with tab1:
    st.info("Install the Chrome extension, open Gmail, and click **Send to Copilot** in the extension popup.")
    
    if st.button("🔄 Check for emails from extension", use_container_width=True):
        try:
            with open("received_emails.json", "r") as f:
                loaded = json.load(f)
            st.session_state.email_boxes = loaded
            st.success(f"✅ {len(loaded)} email(s) loaded from Gmail!")
        except FileNotFoundError:
            st.warning("No emails received yet. Make sure the extension sent them.")

with tab2:
    st.caption("Paste emails below — the system detects boundaries automatically.")
    manual_input = st.text_area(
        "Paste emails here",
        height=250,
        placeholder="""From: scholarships@hec.gov.pk
Subject: HEC Scholarship 2026

Dear Student...

From: hr@techcorp.com
Subject: Internship 2026

Dear Applicant..."""
    )
    if manual_input.strip():
        from utils import split_emails
        detected = split_emails(manual_input)
        st.caption(f"🔍 Detected **{len(detected)}** email(s)")

if "results" not in st.session_state:
    st.session_state.results = []

if "email_boxes" not in st.session_state:
    st.session_state.email_boxes = []

analyze_btn = st.button("🔍 Analyze Emails", type="primary", use_container_width=True)

if analyze_btn:
    # figure out which source to use
    if st.session_state.get("email_boxes"):
        emails_to_process = st.session_state.email_boxes
        raw_text = "\n---\n".join(emails_to_process)
    elif manual_input.strip():
        raw_text = manual_input
    else:
        st.warning("Please load or paste at least one email.")
        st.stop()

    if not cv_text:
        st.warning("Please upload your CV first.")
        st.stop()

    student_profile = {"cv_text": cv_text}
    with st.spinner("Analyzing emails... ⏳"):
        st.session_state.results = process_all_emails(raw_text, student_profile)

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