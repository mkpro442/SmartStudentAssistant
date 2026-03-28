# =============================================================
#  gemini_client.py  —  Groq API Wrapper 
# =============================================================
# Uses the Groq SDK with Llama 3 model.
# Handles multi-turn conversation with a student-focused
# system prompt baked in.
# Get your free API key at: https://console.groq.com
# =============================================================

from groq import Groq

# ── System prompt ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a Smart Student Assistant — a friendly, encouraging, and knowledgeable
AI tutor designed to help college students.
Your personality:
- Warm, supportive, and never condescending
- Practical — give actionable advice, not vague tips
- Concise — keep answers focused (3-6 sentences unless asked for more)
- Use the occasional emoji to stay approachable 😊
- Use bullet points only when listing steps or options
You specialise in helping students with:
1. 📚 Study techniques and learning strategies
2. 📝 Exam preparation and revision tips
3. ⏰ Time management and productivity
4. 💪 Motivation and overcoming procrastination
5. 🗒️ Note-taking methods (Cornell, mind maps, etc.)
6. 🧠 Mental health and stress management in college
7. 💼 Career planning, internships, and resume tips
8. 💻 Coding help and project guidance (especially Python / ML / AI)
9. 📐 Mathematics and statistics for AIML students
10. 🎓 College life, friendships, and adjustment
Rules:
- If asked something unrelated to student life, gently redirect.
- Never give medical diagnoses. Suggest a counsellor for serious concerns.
- Keep answers encouraging. Remember conversation history for follow-ups.
"""

class GeminiClient:
    """
    Drop-in Groq replacement — same interface as the original GeminiClient.
    Usage:
        client = GeminiClient(api_key="gsk_...")
        reply  = client.chat("how do I study better?", history=[])
    """
    MODEL = "llama-3.3-70b-versatile"  # Best free model on Groq

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def chat(self, user_message: str, history: list) -> str:
        """
        Send a user message to Groq with full history for multi-turn context.
        history entries: {"role": "user"|"model", "text": "..."}
        """
        try:
            # Build messages list with system prompt first
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            # Add conversation history
            for turn in history:
                role = "assistant" if turn["role"] == "model" else turn["role"]
                messages.append({
                    "role": role,
                    "content": turn["text"]
                })

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=0.75,
                max_tokens=512,
            )

            return response.choices[0].message.content

        except Exception as e:
            error = str(e)
            if "api_key" in error.lower() or "401" in error or "403" in error:
                return "❌ Invalid API key. Please check your Groq API key in the sidebar."
            elif "rate" in error.lower() or "429" in error:
                return "⏳ Rate limit hit! Please wait a moment and try again."
            elif "safety" in error.lower():
                return "⚠️ That message was flagged by the safety filter. Try rephrasing."
            else:
                return f"⚠️ Something went wrong: {error}"
