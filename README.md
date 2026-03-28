# Smart Student Chatbot — Groq + Streamlit

A fully online student chatbot powered by Groq's Llama 3.3 70B model (free API) and deployed on Streamlit Cloud (free hosting).

## Project Structure

```
student_chatbot/
|
|-- app.py                          <- Main Streamlit app (run this)
|-- gemini_client.py                <- Groq API wrapper + system prompt
|-- requirements.txt                <- For Streamlit Cloud
|-- .gitignore                      <- Keeps your API key safe
|
+-- .streamlit/
    +-- secrets.toml.example        <- Template for local API key setup
```

## Part 1 — Get Your Free Groq API Key

1. Go to https://console.groq.com
2. Sign in or create a free account
3. Navigate to "API Keys" and click "Create API Key"
4. Copy the key (starts with `gsk_...`)
5. Keep it safe — treat it like a password

Free tier limits:
- 30 requests per minute
- 14,400 requests per day
- No credit card required

## Part 2 — Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key (for local use)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Open .streamlit/secrets.toml and paste your API key

# 3. Run the app
streamlit run app.py
```

Your browser will open at http://localhost:8501 automatically.

Alternatively, you can skip the secrets.toml step and paste your API key directly into the sidebar text box when the app opens.

## Part 3 — Deploy Online with Streamlit Cloud

### Step 1 — Push your code to GitHub

```bash
# In your project folder:
git init
git add .
git commit -m "Initial commit - Student Chatbot"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/student-chatbot.git
git push -u origin main
```

Make sure `.streamlit/secrets.toml` is in `.gitignore` so your key is never uploaded to GitHub.

### Step 2 — Connect to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch: `main`, file: `app.py`
5. Click "Deploy"

### Step 3 — Add your API key to Streamlit Cloud

1. In your deployed app, click the three dots menu, then Settings, then Secrets
2. Paste this:

```
GROQ_API_KEY = "your_actual_key_here"
```

3. Click Save — the app will restart automatically

Your app will be live at a public URL like: `https://your-name-student-chatbot.streamlit.app`

## How It Works

```
User types a message
        |
        v
Streamlit collects input + full conversation history
        |
        v
GeminiClient.chat() called with history
        |
        v
Groq SDK sends request to Llama 3.3 70B API
        |
        v
System prompt shapes the model's behaviour (student-focused)
        |
        v
Model returns a contextual, multi-turn aware response
        |
        v
Response appended to session_state history
(so the next message has full context)
        |
        v
Streamlit re-renders the chat with the new message
```

## How to Customise

- Change the personality: Edit `SYSTEM_PROMPT` in `gemini_client.py`
- Add more suggestion chips: Edit the `SUGGESTIONS` list in `app.py`
- Change the model: Edit `MODEL` in `gemini_client.py`
  - `llama-3.3-70b-versatile` — best quality, free
  - `llama-3.1-8b-instant` — fastest, lower resource usage
- Change response length: Edit `max_tokens` in `gemini_client.py`# Smart Student Chatbot — Gemini + Streamlit

A fully online student chatbot powered by **Google Gemini 1.5 Flash** (free API)
and deployed on **Streamlit Cloud** (free hosting).

---

## Project Structure

```
student_chatbot_gemini/
│
├── app.py                          ← Main Streamlit app (run this)
├── gemini_client.py                ← Gemini API wrapper + system prompt
├── requirements.txt                ← For Streamlit Cloud
├── .gitignore                      ← Keeps your API key safe
│
└── .streamlit/
    └── secrets.toml.example        ← Template for local API key setup
```

---

## Part 1 — Get Your Free Gemini API Key

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)
5. Keep it safe — treat it like a password!

**Free tier limits:**
-  15 requests per minute
-  1 million tokens per day
-  No credit card required

---

## Part 2 — Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key (for local use)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Now open .streamlit/secrets.toml and paste your API key

# 3. Run the app
streamlit run app.py
```

Your browser will open at **http://localhost:8501** automatically.

> **Alternatively**, you can skip the secrets.toml step and just paste your
> API key directly into the sidebar text box when the app opens.

---

## Part 3 — Deploy Online with Streamlit Cloud

### Step 1 — Push your code to GitHub

```bash
# In your project folder:
git init
git add .
git commit -m "Initial commit - Student Chatbot"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/student-chatbot.git
git push -u origin main
```

> Make sure `.streamlit/secrets.toml` is in `.gitignore` so your key
> is never uploaded to GitHub!

### Step 2 — Connect to Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository → branch: `main` → file: `app.py`
5. Click **"Deploy!"**

### Step 3 — Add your API key to Streamlit Cloud

1. In your deployed app, click **"⋮" → Settings → Secrets**
2. Paste this:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
3. Click **Save** — the app will restart automatically

Your app is now **live at a public URL** like:
`https://your-name-student-chatbot.streamlit.app`

---

## How It Works

```
User types a message
        ↓
  Streamlit collects input + full conversation history
        ↓
  GeminiClient.chat() called with history
        ↓
  google-generativeai SDK sends to Gemini 1.5 Flash API
        ↓
  System prompt shapes Gemini's behaviour (student-focused)
        ↓
  Gemini returns a contextual, multi-turn aware response
        ↓
  Response appended to session_state history
  (so next message has full context)
        ↓
  Streamlit re-renders the chat with the new bubble
```

## How to Customise

**Change the personality** → Edit `SYSTEM_PROMPT` in `gemini_client.py`

**Add more suggestion chips** → Edit the `SUGGESTIONS` list in `app.py`

**Change the model** → Edit `MODEL_NAME` in `gemini_client.py`
- `gemini-1.5-flash` → fastest, free
- `gemini-1.5-pro`   → smarter, lower free quota

**Change response length** → Edit `max_output_tokens` in `gemini_client.py`
