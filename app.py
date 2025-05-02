import os
import streamlit as st
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.credentials import Credentials

# --- Secure Setup ---
API_KEY = os.getenv("WATSONX_API_KEY","ch1nbczDMcqQRSQY5EeWxvGL5R_DfCig43bnKxxfB58w")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID","ae528503-ba43-464b-8eb2-add4c13852ce")
REGION = os.getenv("WATSONX_REGION", "us-south")

if not API_KEY or not PROJECT_ID:
    raise EnvironmentError("Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.")

# --- Initialize Models ---
creds = Credentials(
    url=f"https://{REGION}.ml.cloud.ibm.com",
    api_key=API_KEY
)
text_model = ModelInference(
    model_id="ibm/granite-3-8b-instruct",
    credentials=creds,
    project_id=PROJECT_ID
)
vision_model = ModelInference(
    model_id="ibm/granite-vision-2b-vision-instruct",
    credentials=creds,
    project_id=PROJECT_ID
)

# --- Inference Utility ---
def run_inference(
    model, prompt, max_new_tokens=80, temperature=0.7,
    top_p=0.9, frequency_penalty=0.0, presence_penalty=0.0,
    stop_sequences=None
):
    params = {
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    resp = model.generate(prompt=prompt, params=params)
    return resp["results"][0]["generated_text"].strip()

# --- Core Functions ---
INSTRUCTION = (
    "You are BrightEarth AI, a sustainability co-pilot.\n"
    "If role, environment, or task is missing, ask for them.\n"
    "Once all are provided, return ONE eco-action tip (<40 words), human-sounding, realistic, aligned to UN SDG 8.\n"
    "Never mention user info. Never output more than one tip. Do not use titles or citations. Only reply with the tip."
)
def generate_tip(role, env, task):
    if not (role and env and task):
        return "Provide role, environment, and task."
    prompt = f"{INSTRUCTION}\n\nRole={role}; Environment={env}; Task={task}\n"
    return run_inference(text_model, prompt, stop_sequences=["<|endoftext|>"])


def summarize_text(text):
    if not text.strip():
        return "Please provide text to summarize."
    prompt = f"Summarize the following text into two clear, professional sentences:\n\n{text}\n"
    return run_inference(text_model, prompt, max_new_tokens=60, temperature=0.5)


def generate_report(topic):
    if not topic.strip():
        return "Please provide a topic for the report."
    prompt = f"Draft a concise professional report on '{topic}'. Include an introduction, key points, and a conclusion."
    return run_inference(text_model, prompt, max_new_tokens=1000)


def innovation_trend(role):
    if not role.strip():
        return "Provide a job role."
    prompt = f"What is one cutting-edge innovation or technology trend that a {role} should know about? Provide one actionable insight."
    return run_inference(text_model, prompt, max_new_tokens=60)


def verify_proof(image_bytes):
    prompt = "Verify this image as valid proof of an eco-action by describing what it shows."
    resp = vision_model.generate(
        prompt=prompt,
        inputs={"image": image_bytes},
        params={"max_new_tokens":100, "temperature":0.5}
    )
    return resp["results"][0]["generated_text"].strip()

# --- Streamlit UI ---
st.set_page_config(page_title="BrightEarth Co-Pilot", layout="wide")
st.title("🌍 BrightEarth AI Co-Pilot")
st.sidebar.header("Features")
mode = st.sidebar.selectbox("Choose", ["Eco-Action Tip","Summarize Text","Generate Report","Innovation Trend","Verify Proof"] )

if mode == "Eco-Action Tip":
    st.subheader("Daily Eco-Action Tip")
    role = st.text_input("Job Role")
    env = st.text_input("Work Environment")
    task = st.text_input("Current Task")
    if st.button("Generate Tip"):
        st.success(generate_tip(role, env, task))
elif mode == "Summarize Text":
    st.subheader("Text Summarizer")
    text = st.text_area("Enter text:")
    if st.button("Summarize"):
        st.write(summarize_text(text))
elif mode == "Generate Report":
    st.subheader("Professional Report Writer")
    topic = st.text_input("Report Topic")
    if st.button("Generate Report"):
        st.write(generate_report(topic))
elif mode == "Innovation Trend":
    st.subheader("Innovation Trend Finder")
    role = st.text_input("Job Role")
    if st.button("Get Trend"):
        st.write(innovation_trend(role))
elif mode == "Verify Proof":
    st.subheader("Eco-Action Proof Verifier")
    file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
    if file and st.button("Verify Proof"):
        bytes_data = file.read()
        st.image(bytes_data, use_column_width=True)
        st.info(verify_proof(bytes_data))

st.sidebar.markdown("---")
st.sidebar.write("Built with IBM Granite & Watsonx")
