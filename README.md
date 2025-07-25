# 🌤️ Weather‑Agent

A tiny **Streamlit** front‑end + LLM **agent** that fetches live conditions from the free
[Open‑Meteo API](https://open-meteo.com/) and returns a human‑friendly report with actionable advice.

Runs locally with one command, and scales to **\$0/month** on Google Cloud Run’s always‑free tier.

---

## ✨ Features

|                          | Details                                                                     |
| ------------------------ | --------------------------------------------------------------------------- |
| **LLM agent**            | Uses your preferred `agents` framework (function‑calling + tool injection). |
| **Async + retries**      | Non‑blocking `httpx` client with exponential back‑off (3 tries).            |
| **Streamlit UI**         | One‑page app; headless‑ready for servers.                                   |
| **Secret management**    | API keys stored in **Secret Manager** (prod) or `.env` (local).             |
| **Free‑tier deployment** | One `gcloud run deploy` builds via Buildpacks → auto‑scale to 0.            |
| **Zero dependencies DB** | No database; weather API is stateless & cached 5 min in‑process.            |

---

## 🗂️ Project structure

```text
weather_agent/
├── app.py                 # Streamlit entry‑point
├── Procfile               # Start cmd for Cloud Run Buildpacks
├── requirements.txt       # Pinned deps
├── .env.example           # Sample secrets file
└── weather/
    ├── __init__.py
    └── client.py          # Async Open‑Meteo wrapper
```

---

## 🖇️ Prerequisites

* Python ≥ 3.10
* `pip`, `virtualenv` or `venv`
* Google Cloud SDK (`gcloud`) → [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
* A Google Cloud project **linked to a billing account** (Cloud Run free tier still needs billing)
* An **OpenAI API key** (or adjust code to use a local model)

---

## 🚀 Local quick‑start

```bash
# 1 – clone & create venv
$ git clone https://github.com/you/weather_agent.git && cd weather_agent
$ python -m venv .venv && source .venv/bin/activate

# 2 – install deps
$ pip install -r requirements.txt

# 3 – add secrets
$ cp .env.example .env && nano .env   # paste OPENAI_API_KEY

# 4 – run
$ streamlit run app.py --server.headless true
# open http://localhost:8501
```

---

## ☁️ 1‑click Cloud Run deploy (always‑free)

```bash
# Authenticate & select project
$ gcloud auth login
$ gcloud config set project <YOUR_PROJECT>

# Enable services
$ gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
                        artifactregistry.googleapis.com secretmanager.googleapis.com

# Store the OpenAI key safely
$ echo -n "$OPENAI_API_KEY" | gcloud secrets create openai-key --data-file=-

# Deploy → Buildpacks auto‑detect Procfile & requirements.txt
$ gcloud run deploy weather-agent \
    --source . \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 512Mi --cpu 0.25 \
    --min-instances 0 --max-instances 1 \
    --set-secrets "OPENAI_API_KEY=projects/$PROJECT_ID/secrets/openai-key:latest"
```

*Cold‑start ≈ 2‑5 s. Staying below 180 000 vCPU‑s / 360 000 GiB‑s & 2 M reqs/month keeps the bill \$0.*

---

## 🔧 Environment variables

| Name             | Local  | Cloud Run                        |
| ---------------- | ------ | -------------------------------- |
| `OPENAI_API_KEY` | `.env` | Secret Manager → `--set-secrets` |
| `PORT`           | auto   | injected by Cloud Run            |

---

## 🛡️ Security & compliance

* **No PII** is stored—only transient weather coordinates.
* HTTPS enforced by Cloud Run’s managed TLS.
* Rotate API keys via Secret Manager versions.

---

## 🧪 Testing

* Unit‑test `weather.client.fetch_weather` with `respx` mocks.
* (Optional) Headless UI tests: `streamlit.testing`.

---

## 🤝 Contributing

> Fork → create feature branch → commit changes → open PR.
> Please run `black`, `ruff --fix`, and keep docs in sync.

---

## 📝 License

MIT © 2025 Your Name
