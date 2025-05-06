

# 🌱 BrightEarth AI

BrightEarth AI is a generative AI-powered sustainability co-pilot built for the IBM Hackathon. It empowers employees to adopt greener habits in the workplace by delivering intelligent eco-tips, validating real-world actions using vision AI, and gamifying the journey toward a more sustainable culture.

---
## 1)  Enter your ID

![image](https://github.com/user-attachments/assets/0ef7c706-ecff-4f95-a997-6c81782ea1c1)

## 2)  Enter your job role

![image](https://github.com/user-attachments/assets/41a22c63-9f89-4cd4-8083-9f25010cbd18)

## 3)  Enter the environment where you are working from

![image](https://github.com/user-attachments/assets/983fc9da-8ff7-4e4e-a72a-f6a55410b6fa)

## 4) Receive tailored productivity tips

The model generates tips based on your role and environment, aligned with UN SDG 8 (Decent Work and Economic Growth) by promoting sustainable and efficient work practices.

## 5) Upload proof of action

Upload an image showing your implementation of the tip. The model will analyze and compare it to the generated tip.

![image](https://github.com/user-attachments/assets/c29d21e3-8ff9-431c-a65e-f69483a9d87d)

## 6) Generate tips for your current task

You can also generate tips relevant to the task you're currently working on. Plus, the assistant can summarize long text inputs.

![image](https://github.com/user-attachments/assets/eccfadc2-992d-48c0-9522-d06276a0eef5)

## 7) Get automated reports and innovation trends

Receive a report based on your role, along with insights into innovation trends relevant to your job.

![image](https://github.com/user-attachments/assets/a55f26ce-3eee-46a8-a058-a703b22a1f2a)

## 8) Track your engagement

View your engagement profile, track completed actions, and check their verification status.

![image](https://github.com/user-attachments/assets/a122bc89-f4e0-453a-9509-4223664f9894)




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
