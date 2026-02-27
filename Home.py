import streamlit as st

st.set_page_config(
    page_title="yamato",
    page_icon="🗂️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
#MainMenu, footer { visibility: hidden; }

.wordmark {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    margin-bottom: 0;
}
.sub {
    font-size: 1rem;
    color: #888;
    margin-top: 0.25rem;
    margin-bottom: 2.5rem;
}
.feature-box {
    background: #f7f5f2;
    border-left: 3px solid #1a1a1a;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 2px;
}
.feature-title {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.2rem;
}
.feature-desc {
    font-size: 0.85rem;
    color: #555;
}
.divider {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 2.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="wordmark">yamato</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Barebone task management. No noise, just work.</div>', unsafe_allow_html=True)

# Description
st.markdown("""
**yamato** is a minimal task management tool built for people who find Jira overkill and sticky notes not quite enough.

Create tasks, assign them to categories, track their status, and get them done. That's it.
""")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Features
st.markdown("#### What it does")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="feature-box">
    <div class="feature-title">📋 Tasks</div>
    <div class="feature-desc">Create small, actionable tasks with a title, description, and status.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-box">
    <div class="feature-title">🏷️ Categories</div>
    <div class="feature-desc">Organise tasks into categories so nothing gets lost in the pile.</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature-box">
    <div class="feature-title">✅ Status tracking</div>
    <div class="feature-desc">Move tasks from To Do → In Progress → Done with a single click.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-box">
    <div class="feature-title">🔒 Private workspace</div>
    <div class="feature-desc">Your task board lives behind a password. Simple, no accounts needed.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown("Head to **Tasks** in the sidebar to get started.", unsafe_allow_html=False)