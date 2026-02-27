# yatamato

I want to code up a streamlit simple app that allows me to create and finish small stories/jobs, much like jira/asana allow. But much more barebone. This project will go into discussing how to build this, and helping me build out the code with my ideas.

## Running locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Deploying to Streamlit Cloud

1. Push this repo to GitHub (main branch)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main file path to `Home.py`
4. Deploy — Streamlit Cloud will auto-install from `requirements.txt`

Any push to `main` will automatically redeploy the app.

## Project structure

```
yatamato/
├── Home.py            # Landing page
├── pages/
│   └── 1_Tasks.py     # Password-protected task board
├── requirements.txt   # Dependencies for Streamlit Cloud
└── README.md
```