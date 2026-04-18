import json
import streamlit as st

from pipeline import process_all_emails

st.set_page_config(
    page_title="Opportunity Inbox Copilot",
    page_icon="📬",
    layout="wide"
)

with st.sidebar:
    st.title("Student Profile")
    st.caption("Fill this in so the AI can personalize rankings.")

    degree = st.selectbox("Degree / Program", [
        "BS Computer Science",
        "BS Software Engineering",
        "BS Data Science",
        "BS AI",
        "BS Electrical Engineering",
        "BS Business Administration",
        "Other"
    ])

    semester = st.slider("Semester", 1, 8, 4)

    cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0,
                           value=3.0, step=0.1)

    skills = st.text_input("Skills & Interests",
                           placeholder="e.g. Python, ML, web dev, finance")

    opp_types = st.multiselect("Preferred Opportunity Types", [
        "Internship", "Scholarship", "Fellowship",
        "Competition", "Research", "Admission"
    ])

    financial_need = st.radio("Financial Need",
                              ["Low", "Medium", "High"],
                              horizontal=True)

    location_pref = st.selectbox("Location Preference", [
        "Any", "Pakistan only", "Remote only",
        "Abroad preferred", "Lahore only"
    ])

    past_experience = st.text_area("Past Experience (brief)",
                                   placeholder="e.g. 1 internship at a startup, won a hackathon",
                                   height=80)

    # Pack into a dict — this goes to your ranker teammate later
    student_profile = {
        "degree": degree,
        "semester": semester,
        "cgpa": cgpa,
        "skills": skills,
        "preferred_types": opp_types,
        "financial_need": financial_need,
        "location_preference": location_pref,
        "past_experience": past_experience
    }

st.title("📬 Opportunity Inbox Copilot")
st.caption("Paste your emails below, separated by  ---  and hit Analyze.")

email_input = st.text_area(
    "Paste emails here (separate each with ---)",
    height=300,
    placeholder="""Dear Student, we are pleased to offer...

---

Hello, you have been selected for...

---

This is a newsletter about upcoming events..."""
)

analyze_btn = st.button("Analyze Emails", type="primary", use_container_width=True)

if "results" not in st.session_state:
    st.session_state.results = []

if "profile" not in st.session_state:
    st.session_state.profile = {}

if analyze_btn:
    if not email_input.strip():
        st.warning("Please paste at least one email.")
    else:
        with st.spinner("Reading emails... this may take a moment ⏳"):
            st.session_state.results = process_all_emails(email_input)
            st.session_state.profile = student_profile

if st.session_state.results:
    results = st.session_state.results

    opportunities = [r for r in results if r.get("is_opportunity")]
    non_opps      = [r for r in results if not r.get("is_opportunity")]

    st.markdown("---")
    st.subheader(f"✅ {len(opportunities)} Opportunities Found "
                 f"| 🗑️ {len(non_opps)} Ignored")

    if not opportunities:
        st.info("No real opportunities detected in these emails.")

    for opp in opportunities:
        with st.container():
            # Card header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {opp.get('title') or 'Untitled Opportunity'}")
                st.caption(f"📧 Email #{opp.get('email_index')} · "
                           f"{opp.get('organization') or 'Unknown org'}")
            with col2:
                conf = opp.get("confidence", "low")
                color = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(conf, "⚪")
                st.markdown(f"**Confidence:** {color} {conf.title()}")

            # Key fields in columns
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

            # Eligibility
            if opp.get("eligibility"):
                st.markdown(f"**Eligibility:** {opp['eligibility']}")

            # Documents
            if opp.get("documents"):
                docs = ", ".join(opp["documents"])
                st.markdown(f"**Documents needed:** `{docs}`")

            # Next steps
            if opp.get("next_steps"):
                st.info(f"**Next step:** {opp['next_steps']}")

            # Link
            if opp.get("link"):
                st.markdown(f"[🔗 Apply Here]({opp['link']})")

            # Raw JSON toggle for your teammates
            with st.expander("View raw JSON (for ranker teammate)"):
                st.json(opp)

            st.markdown("---")

    # Show ignored emails collapsed
    if non_opps:
        with st.expander(f"🗑️ {len(non_opps)} ignored emails"):
            for n in non_opps:
                st.markdown(f"- **Email #{n.get('email_index')}:** {n.get('reason')}")