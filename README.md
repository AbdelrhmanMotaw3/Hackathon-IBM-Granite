Here's a clean and professional `README.md` tailored for your **BrightEarth AI** project on GitHub:

---

# 🌍 BrightEarth AI

BrightEarth AI is a generative AI-powered platform designed to promote **sustainability**, **workplace safety**, and **personal growth** through personalized guidance, intelligent proof verification, and gamified engagement. Built using IBM's Granite Foundation Models (text and vision), the platform delivers daily eco-action tips, validates real-world efforts, and encourages users with rewards and insights.

---

## 🚀 Features

* 🧠 **AI-Powered Eco Tips**
  Personalized daily sustainability suggestions generated based on the user’s role and environment using IBM Granite NLP models.

* 📷 **Vision-Based Proof Verification**
  Users upload photos of their eco or safety actions, and Granite Vision models verify and describe them to ensure authenticity.

* 📝 **Smart Summarization & Reporting**
  Generate professional summaries and structured reports on sustainability topics using Granite NLP.

* 💡 **Innovation Trend Insights**
  Discover cutting-edge ideas tailored to each job role to inspire sustainable thinking and innovation.

* 🏅 **Gamification & Badges**
  Track user actions, award badges for engagement, and display top contributors via a leaderboard.

---

## 🧠 IBM Granite Model Usage

BrightEarth AI uses the following IBM Foundation Models via `ibm-watsonx-ai`:

* `granite-3-8b-instruct`: NLP model for eco tips, summaries, reports, and innovation insights.
* `granite-13b-instruct-v2`: For verifying if a user action matches the given tip.
* `granite-vision-3-2-2b`: Vision model that interprets user-uploaded proof images.

---

## 🛠️ Technologies Used

* **Python**
* **IBM Watsonx AI SDK (`ibm-watsonx-ai`)**
* **Pillow** (Image processing)
* **JSON-based storage** (for user logs, tips, and actions)

---

## 📂 Project Structure

```
├── brightearth_copilot_core.py  # Main AI logic & integrations
├── actions.json                 # Logged user actions
├── tip_logs/                    # Historical tips by user & role
├── requirements.txt             # Dependencies
└── README.md                    # You're here!
```

---

## 🧪 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/brightearth-ai.git
   cd brightearth-ai
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your environment variables**

   * `WATSONX_API_KEY`
   * `WATSONX_PROJECT_ID`
   * `WATSONX_REGION` (e.g., `us-south`)

4. **Run the core functions**
   Import and call any function from `brightearth_copilot_core.py` for tip generation, summarization, or proof validation.

---

## 🧩 Example Use Cases

* A sustainability officer receives a new eco-action tip daily.
* An employee uploads proof of using a reusable bottle; the platform validates it.
* A team member requests a quick summary of an article on workplace safety.
* The system rewards top participants with achievement badges.

---

## 💬 Contributing

Contributions are welcome! Feel free to open issues, suggest features, or submit pull requests.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Team

Developed as part of the IBM Hackathon 2025 by the BrightEarth AI Team.
Focused on SDG 8: **Decent Work and Economic Growth** 🌱

---

Would you like a `requirements.txt` file generated for this as well?
