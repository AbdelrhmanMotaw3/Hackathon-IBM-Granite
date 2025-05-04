# brightearth_app_final.py
"""
Streamlit app for BrightEarth AI: interactive dashboard, productivity tools, and gamification.
"""
import streamlit as st
import base64
from io import BytesIO
import json
from pathlib import Path
from PIL import Image
from BrightEarth_CoPilot3 import (
    get_daily_tip,
    record_action,
    get_badges,
    summarize_text_tool,
    generate_report_tool,
    innovation_trend_tool,
    verify_proof_tool,
    verify_tip_application
)

# --- App Configuration ---
st.set_page_config(
    page_title="ISYS AI Workplace",
    page_icon="isys.png",
    layout="wide"
)

# --- Custom CSS for Theme & Layout ---
st.markdown(
    """
    <style>
      body {
        background-color: white !important;
        color: #1A1A1A !important;
      }
      .main > div {
        padding-top: 0 !important;
      }
      section[data-testid="stSidebar"] div[class*="css-"] {
        background-color: white !important;
        color: #1A1A1A !important;
      }
      section[data-testid="stForm"],
      .stContainer {
        background-color: white !important;
      }
      .css-18e3th9, .css-10trblm {
        color: #1A1A1A !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Logo & Header ---
logo_path = Path("isys.png")
if logo_path.exists():
    logo_bytes = logo_path.read_bytes()
    logo_b64 = base64.b64encode(logo_bytes).decode()
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_b64}" width="200" style="margin-bottom: 10px;">
            <h2 style="color: white; margin-bottom: 0;">ISYS AI</h2>
            <p style="font-size: 0.85em; color: white;">Workplace Assistant</p>
        </div>
        <hr style="border-color:#e1e1e1;">
        """,
        unsafe_allow_html=True
    )

# --- Session State Initialization ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'env' not in st.session_state:
    st.session_state.env = None

# --- Onboarding Flow ---
if st.session_state.user_id is None:
    st.write("Welcome to ISYS AI! Please enter your Employee ID to continue.")
    emp_id = st.text_input("Employee ID", key="login_id")
    if st.button("Continue", key="btn_login"):
        if emp_id and emp_id.strip():
            st.session_state.user_id = emp_id.strip()
        else:
            st.error("Employee ID cannot be empty.")
    st.stop()

if st.session_state.role is None:
    st.write(f"Hello, **{st.session_state.user_id}**! Please enter your job role:")
    custom_role = st.text_input("Enter your role:", key="custom_role_input")
    if st.button("Confirm Role", key="btn_custom_role"):
        if custom_role.strip():
            st.session_state.role = custom_role.strip()
        else:
            st.error("Role cannot be empty.")
    st.stop()


# Ensure the user provides their environment (custom input)
if st.session_state.env is None:
    st.write("Please enter your work environment:")
    
    # Allow custom text input for environment instead of a selectbox
    env = st.text_input("Enter your Environment:", key="custom_env")
    
    if st.button("Confirm Environment", key="btn_env"):
        if env.strip():
            st.session_state.env = env.strip()  # Save the custom environment input
        else:
            st.error("Environment cannot be empty.")
    st.stop()

# --- Sidebar: Badges ---
badges = get_badges(st.session_state.user_id)
st.sidebar.header("🏅 Your Badges")
for badge in badges:
    st.sidebar.markdown(f"<span class='badge'>{badge}</span>", unsafe_allow_html=True)

# Tabs: Today, Tools, Profile
tabs = st.tabs(["📋 Today","💡 Tools","📈 Profile"])

# --- Today Tab ---
with tabs[0]:
    st.subheader("📅 Today's Tip & Actions")
    tip = get_daily_tip(st.session_state.user_id, st.session_state.role, st.session_state.env)  # Pass environment here
    st.markdown(f"<div class='tip-card'><strong>Daily Tip:</strong> {tip}</div>", unsafe_allow_html=True)
    if st.button("✔️ Completed Tip", key="done_tip"):
        record_action(st.session_state.user_id, "sustainability", proof="")
        st.success("Action recorded!")

    uploaded = st.file_uploader("📸 Upload proof image:", type=["png", "jpg", "jpeg"], key="proof")
    if uploaded:
        img_bytes = uploaded.read()
        st.image(img_bytes, width=200)
        if st.button("📤 Submit Proof", key="submit_proof"):
            rec = verify_proof_tool(img_bytes)
            match_eval = verify_tip_application(tip, rec.get("description", ""), model_id="granite-13b")
            record_action(st.session_state.user_id, "safety", proof=json.dumps({**rec, **match_eval}))
            st.success(f"Proof verified and recorded. Verdict: {match_eval['verdict']}")


# --- Tools Tab ---
with tabs[1]:
    st.subheader("💡 Productivity Tools")
    # In the Tools Tab section, when getting the eco-action tip, use text inputs for custom role and environment
    with st.expander("🌱 Eco-Action Tip", expanded=True):
    # Custom input for job role
        jr = st.text_input("Enter your Job Role:", key="tip_custom_role", value=st.session_state.role or "")
        
        # Custom input for environment
        we = st.text_input("Enter your Environment:", key="tip_custom_env")
        
        # Input for current task
        ct = st.text_input("Current Task", key="tip_task")
        
        if st.button("Get Tip", key="btn_tip"):
            # Use the custom inputs for job and environment to get a tip
            tip2 = get_daily_tip(st.session_state.user_id, jr)  # Assuming this function can take the custom role
            st.success(tip2, icon="🌿")
            record_action(st.session_state.user_id, "sustainability", proof="")


    with st.expander("✏️ Summarize Text"):
        txt = st.text_area("Enter text to summarize...", key="sumtxt")
        if st.button("Summarize", key="btn_sum"):
            res = summarize_text_tool(txt)
            record_action(st.session_state.user_id, "learning")
            st.write(res)

    with st.expander("📝 Generate Report"):
        topic = st.text_input("Topic...", key="topic")
        if st.button("Generate Report", key="btn_rpt"):
            rpt = generate_report_tool(topic)
            record_action(st.session_state.user_id, "learning")
            st.download_button("Download Report", rpt, file_name="report.txt")

    with st.expander("🔍 Innovation Trend"):
        tr = st.text_input("Role for trend...", key="trrole")
        if st.button("Get Trend", key="btn_trend"):
            out = innovation_trend_tool(tr or st.session_state.role)
            st.write(out)

# --- Profile Tab ---
with tabs[2]:
    st.subheader("📈 Your Engagement Profile")
    actions_path = Path("actions.json")
    actions = json.loads(actions_path.read_text()) if actions_path.exists() else {}
    user_acts = actions.get(st.session_state.user_id, [])

    st.markdown(f"**Total Actions:** {len(user_acts)}")
    for idx, act in enumerate(user_acts):
        date_str = act.get("date", "N/A")
        act_type = act.get("type", "action")
        exp_label = f"{date_str} - {act_type.capitalize()}"
        with st.expander(exp_label, expanded=(idx == len(user_acts)-1)):
            st.write(f"**Type:** {act_type.capitalize()}")
            st.write(f"**Date:** {date_str}")
            proof_raw = act.get("proof", "")
            if proof_raw:
                st.write("**Proof Details:**")
                try:
                    proof_data = json.loads(proof_raw)
                    st.json(proof_data)
                except json.JSONDecodeError:
                    st.write(proof_raw)
            else:
                st.info("No proof provided for this action.")

    st.markdown("---")
    st.markdown("**Download Full ESG Report**")
    if st.button("Download Report", key="btn_esg"):
        esg = json.dumps({"badges": badges, "actions": user_acts}, indent=2)
        st.download_button("Download JSON", esg, file_name="esg_report.json")

# --- Footer ---
st.markdown("---")
st.markdown("*Powered by IBM Granite AI & Watsonx*", unsafe_allow_html=True)
