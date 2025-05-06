

# 🌱 BrightEarth AI

BrightEarth AI is a generative AI-powered sustainability co-pilot built for the IBM Hackathon. It empowers employees to adopt greener habits in the workplace by delivering intelligent eco-tips, validating real-world actions using vision AI, and gamifying the journey toward a more sustainable culture.

---

## 🎯 Key Features

* **Generate Eco-Tips**
  Personalized tips based on job role and work environment.

* **Proof Validation with Vision AI**
  Upload an image and get a smart description of visible eco-friendly or safety behaviors.

* **Summarize Activity**
  Generate short summaries of user interactions and submitted actions.

* **Generate Reports**
  Get structured feedback and insight into sustainability progress.

* **Track Innovation Trends**
  Explore industry-specific sustainability innovations.

---

## 🧠 AI Technologies Used

Powered by **IBM Watsonx & Granite Models**:

* NLP: `granite-3-8b-instruct`, `granite-13b-instruct-v2`
* Vision: `granite-vision-3-2-2b`

---

## 📁 Files Overview

* `BrightEarth_CoPilot3.py` — Core logic for the AI co-pilot.
* `app.py` — Streamlit app (UI interface).
* `Hackathon App Demo.mp4` — Video demo of the application.


---

## ▶️ Demo

Watch the full application demo here:
🎥 **Hackathon App Demo.mp4** *(included in the repo)*

---

## 🛠️ Getting Started

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set your environment variables**

```bash
export WATSONX_API_KEY=your_key
export WATSONX_PROJECT_ID=your_project_id
export WATSONX_REGION=us-south
```

3. **Run the app**

```bash
python app.py
```

---

## 👥 Team

Built by: Abdelrhman Motawea & Team
Challenge: IBM Sustainability Hackathon 2025

---

Let me know if you want to add badges, a tech stack diagram, or deploy this on HuggingFace or Streamlit Cloud.
