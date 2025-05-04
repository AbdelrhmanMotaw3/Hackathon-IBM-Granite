# brightearth_copilot_core.py
"""
Core engine for BrightEarth AI: provides AI services and gamified engagement.
"""
import os
import json
import base64
import io
from datetime import datetime, date
from time import sleep
from pathlib import Path
from functools import wraps
from typing import List, Dict
from PIL import Image

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.credentials import Credentials

# --- Credentials & Models Setup ---
class SecureCredentials:
    def __init__(self):
        self.API_KEY = os.getenv("WATSONX_API_KEY", "ch1nbczDMcqQRSQY5EeWxvGL5R_DfCig43bnKxxfB58w")
        self.PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "ae528503-ba43-464b-8eb2-add4c13852ce")
        self.REGION = os.getenv("WATSONX_REGION", "us-south")
        if not all([self.API_KEY, self.PROJECT_ID]):
            raise EnvironmentError("Missing IBM credentials")

creds = Credentials(
    url=f"https://{SecureCredentials().REGION}.ml.cloud.ibm.com",
    api_key=SecureCredentials().API_KEY
)
text_model = ModelInference(
    model_id="ibm/granite-3-8b-instruct",
    credentials=creds,
    project_id=SecureCredentials().PROJECT_ID
)
vision_model = ModelInference(
    model_id="ibm/granite-vision-3-2-2b",
    credentials=creds,
    project_id=SecureCredentials().PROJECT_ID
)

# --- Rate Limiter ---
def rate_limited(max_per_minute: int):
    interval = 60.0 / max_per_minute
    def deco(fn):
        last = [0.0]
        @wraps(fn)
        def wrapper(*args, **kwargs):
            elapsed = datetime.utcnow().timestamp() - last[0]
            wait = interval - elapsed
            if wait > 0:
                sleep(wait)
            result = fn(*args, **kwargs)
            last[0] = datetime.utcnow().timestamp()
            return result
        return wrapper
    return deco

# --- Inference Utility ---
@rate_limited(30)
def run_inference(prompt: str, model: ModelInference=text_model, **params) -> str:
    params.setdefault("max_new_tokens", 80)
    resp = model.generate(prompt=prompt, params=params)
    return resp["results"][0]["generated_text"].strip()

# --- Action Logging & Gamification ---
ACTIONS_FILE = Path("actions.json")

def _load_actions() -> Dict[str, List[Dict]]:
    if ACTIONS_FILE.exists():
        return json.loads(ACTIONS_FILE.read_text())
    return {}

def _save_actions(actions: Dict[str, List[Dict]]):
    ACTIONS_FILE.write_text(json.dumps(actions, indent=2))

def record_action(user_id: str, action_type: str, proof: str = ""):
    actions = _load_actions()
    actions.setdefault(user_id, []).append({
        "date": date.today().isoformat(),
        "type": action_type,
        "proof": proof
    })
    _save_actions(actions)

def get_badges(user_id: str) -> List[str]:
    actions = _load_actions().get(user_id, [])
    types = [a["type"] for a in actions]
    badges = []
    if types.count("sustainability") >= 5:
        badges.append("🌿 Green Champion")
    if types.count("safety") >= 5:
        badges.append("🛡️ Safety Star")
    if types.count("learning") >= 5:
        badges.append("📚 Learning Leader")
    return badges or ["👍 Participant"]

# --- Core Services ---
TIP_LOG_DIR = Path("tip_logs")
TIP_LOG_DIR.mkdir(exist_ok=True)

@rate_limited(30)
def get_daily_tip(user_id: str, job_role: str, environment: str) -> str:
    """
    Generate or retrieve a daily eco-action tip for a given user/role/environment,
    ensuring it differs from the user's previous tip and from any tip given
    to that role/environment.
    """
    today = date.today().isoformat()
    # Define history logs
    user_log = TIP_LOG_DIR / f"user_{user_id}_{environment}.json"
    role_log = TIP_LOG_DIR / f"role_{job_role.replace(' ', '_')}_{environment}.json"

    def load_history(path):
        if path.exists():
            return json.loads(path.read_text())
        return []
    def save_history(path, history):
        path.write_text(json.dumps(history, indent=2))

    user_history = load_history(user_log)
    # If already have today's tip for this user, return it immediately
    if user_history and user_history[-1]["date"] == today:
        return user_history[-1]["tip"]

    role_history = load_history(role_log)
    existing_user_tips = {entry["tip"] for entry in user_history}
    existing_role_tips = {entry["tip"] for entry in role_history}

    # Try generating a unique tip
    max_attempts = 5
    for attempt in range(max_attempts):
        tip = run_inference(
            prompt=(
                f"Generate one short eco-action tip for a {job_role} "
                f"working in a {environment}, aligned with UN SDG 8."
            ),
            temperature=0.7,
            max_new_tokens=100
        )
        # If it's fresh for both user and role, accept it
        if tip not in existing_user_tips and tip not in existing_role_tips:
            break
    # (If after max_attempts it's still a duplicate, we just use it.)

    # Append to histories
    user_history.append({"date": today, "tip": tip})
    role_history.append({"date": today, "tip": tip})
    save_history(user_log, user_history)
    save_history(role_log, role_history)

    return tip


@rate_limited(30)
def summarize_text_tool(text: str) -> str:
    return run_inference(
        prompt=f"Summarize the following text into two clear, professional sentences:\n{text}\n",
        max_new_tokens=150
    )

@rate_limited(30)
def generate_report_tool(topic: str) -> str:
    return run_inference(
        prompt=f"Draft a concise report on '{topic}' with intro, key points, and conclusion.",
        max_new_tokens=800
    )

@rate_limited(30)
def innovation_trend_tool(job_role: str) -> str:
    return run_inference(
        prompt=f"Identify one cutting-edge innovation for {job_role} with actionable insight.",
        max_new_tokens=120
    )

# --- Proof Verification (Structured JSON Output) ---
@rate_limited(30)
def verify_proof_tool(image_bytes: bytes) -> dict:
    """
    Returns JSON dict: {"valid": bool, "description": str}
    Analyzes compressed, base64-encoded image for sustainability or safety actions.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((64, 64))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=5)
        small_bytes = buf.getvalue()
        b64 = base64.b64encode(small_bytes).decode()
        if len(b64) > 100000:
            b64 = b64[:100000] + "..."

        prompt = (
            "You are BrightEarth AI Vision Assistant. Describe this truncated base64-encoded image focusing on safety "
            "improvements or sustainability actions: " + b64
        )
        resp = text_model.generate(
            prompt=prompt,
            params={"max_new_tokens": 150, "temperature": 0.5}
        )
        description = resp["results"][0]["generated_text"].strip()
        return {"valid": True, "description": description}
    except Exception as e:
        return {"valid": False, "error": str(e)}

# --- Tip Application Verification ---
@rate_limited(30)
def verify_tip_application(tip: str, image_description: str, model_id: str) -> dict:
    """
    Compares the AI-generated tip with the description of the proof image
    and returns whether the tip was followed or not.
    """
    from ibm_watsonx_ai.foundation_models import ModelInference

    # Load the model with the provided model_id
    model = ModelInference(
        model_id="ibm/granite-13b-instruct-v2", 
        credentials=creds,  # Ensure creds is defined elsewhere for authentication
        project_id=SecureCredentials().PROJECT_ID
    )

    # Construct the prompt
    prompt = (
        f"The following sustainability tip was given to an employee:\n"
        f"Tip: {tip}\n\n"
        f"And the employee submitted this image description:\n"
        f"Description: {image_description}\n\n"
        f"Based on the description, did the employee apply the tip? "
        f"Reply with 'Yes' or 'No' and a short reason."
    )

    # Run inference with the model
    response = model.generate(prompt)
    result_text = response.get("results", [{}])[0].get("generated_text", "").strip()

    return {"verdict": result_text}



# --- Leaderboard Utility ---
def get_leaderboard(top_n: int = 5) -> List[tuple]:
    actions = _load_actions()
    scores = {user: len(logs) for user, logs in actions.items()}
    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_users[:top_n]
