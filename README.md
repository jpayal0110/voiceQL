# VoiceQL: Talk to Your Data

**VoiceQL** is an AI-powered analytics platform that turns natural voice commands into executable SQL queries. Designed for non-technical users (sales reps, supply chain planners, managers), it allows you to interact with your database just by speaking.

---

## Preview

[demo.webm](https://github.com/user-attachments/assets/8cad8951-2dab-4fe0-bdc4-f18967980048)


---

## Features

* **Natural Voice Interface:** powered by Deepgram Nova-2, providing high-accuracy transcription even with technical jargon.
* **Real-Time SQL Generation:** uses Groq's Llama-3.3 engine to translate English questions into complex PostgreSQL queries in milliseconds.
* **Secure Database Connection:** connects directly to Neon (Serverless Postgres) with auto-seeding for demo purposes.
* **Instant Visualization:** automatically detects data types and renders interactive bar charts and tables.
* **Modern UI:** clean, monochromatic blue interface designed for clarity and professional use.

---

## Tech Stack

* **Frontend:** Streamlit (Python)
* **Voice-to-Text:** Deepgram API (Nova-2 Model)
* **LLM Engine:** Groq API (Llama-3.3-70b-versatile)
* **Database:** Neon (Serverless PostgreSQL)
* **Data Handling:** Pandas & SQLAlchemy
* **Styling:** Streamlit Lottie (Animations) & Custom CSS

---

## Architecture

1.  **Record:** User speaks a command (e.g., "Show me top 3 expenses last month").
2.  **Transcribe:** Audio is sent to Deepgram via raw HTTP requests for low latency.
3.  **Reason:** Transcript is sent to Groq (Llama-3) with a system prompt context of the database schema.
4.  **Execute:** Generated SQL is sanitized and executed against the Neon Postgres database.
5.  **Visualize:** Results are returned as a Pandas DataFrame and visualized in Streamlit.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/VoiceQL.git](https://github.com/yourusername/VoiceQL.git)
cd VoiceQL
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas sqlalchemy psycopg2-binary groq httpx requests streamlit-lottie
```

### Configuration
## You need 3 free API keys to run this project. You can enter them in the UI directly, or set them up in a secrets file for auto-loading.

# Option A: UI Entry Just run the app and enter keys in the "Setup" wizard.

# Option B: Secrets File (Recommended) Create a file at .streamlit/secrets.toml:

```Ini, TOML

NEON_DB_URL = "postgresql://user:password@ep-url.aws.neon.tech/neondb?sslmode=require"
GROQ_API_KEY = "gsk_..."
DEEPGRAM_API_KEY = "..."
```

### How to Run
## Run the Streamlit app:

```Bash
streamlit run app.py
```
The app will open in your browser at http://localhost:8501.


### Usage Examples
Once the database is connected and seeded with dummy data, try asking:
```bash
"What is my total spending on food?"

"Show me the top 3 categories by amount."

"List all transactions where the merchant is Uber."

"Compare spending between January and February."
```

