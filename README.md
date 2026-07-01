# 🪐 Planit

Turn your goals into a step-by-step plan, powered by AI.

## 📝 What it does
Planit takes your goal, deadline, and experience level and generates a personalized day-by-day action plan to help you get started — no more staring at a blank page.

## 💫 How to run
1. Clone the repository
2. Install dependencies:
        pip install -r requirements.txt

3. Create a `.env` file and add your Groq API key:
        GROQ_API_KEY=your_key_here

4. Run the app:
        streamlit run app.py

## 🚀 Tech Stack
- Python
- Streamlit
- Groq API (LLaMA 3.3 70B)

## ⚠️ API & Rate Limit Notes
Planit uses the **Groq API (free tier)** with the LLaMA 3.3 70B model to generate plans.
- Get a free API key at [console.groq.com](https://console.groq.com)

**Please note:**
- The free tier has a rate limit of **30 requests per minute**
- If you see a "Resource Exhausted" error, wait 1-2 minutes and try again
- A 10 second cooldown is built into the app to help manage this

## ⭐ Built by
Gauri E.N.

Start Date: 21st June 2026
