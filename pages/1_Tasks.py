import streamlit as st
import json
import os
from datetime import datetime
import hashlib
import base64

st.set_page_config(
    page_title="Tasks – yamato",
    page_icon="🗂️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
#MainMenu, footer { visibility: hidden; }
div[data-testid="stButton"] button { text-align: left; }
</style>
""", unsafe_allow_html=True)

# ── Persistence helpers ───────────────────────────────────────────────────────
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ── Auth ──────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("### 🔒 Enter password to continue")
    with st.form("login_form"):
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Unlock")
        if submitted:
            if pwd == "zimone":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Wrong password.")
    st.stop()

# ── Load tasks into session state ─────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "editing_task" not in st.session_state:
    st.session_state.editing_task = None

# ── Status config ─────────────────────────────────────────────────────────────
STATUSES = ["Planned / To Do", "In Progress", "Blocked", "Done"]
STATUS_COLORS = {
    "Planned / To Do":     "#6f9df7",
    "In Progress": "#ffa733",
    "Blocked":     "#ff4b4b",
    "Done":        "#21c55d",
}

def status_badge(s):
    color = STATUS_COLORS.get(s, "#aaa")
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:99px;font-size:0.75rem;font-weight:600;">{s}</span>'

# ── Priority config ───────────────────────────────────────────────────────────
PRIORITY_COLORS = {
    "High":   "#ff4b4b",
    "Medium": "#ffa733",
    "Low":    "#21c55d",
}

def priority_badge(p):
    color = PRIORITY_COLORS.get(p, "#aaa")
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:99px;font-size:0.75rem;font-weight:600;">{p}</span>'

# ── Category config ───────────────────────────────────────────────────────────
CATEGORY_PALETTE = [
    "#7c6ff7", "#f76f8e", "#6fc8f7", "#f7a66f",
    "#6ff7b8", "#c86ff7", "#f7e16f", "#6f9df7",
]

def category_color(name):
    if not name:
        return "#aaa"
    idx = int(hashlib.md5(name.lower().encode()).hexdigest(), 16) % len(CATEGORY_PALETTE)
    return CATEGORY_PALETTE[idx]

def category_badge(name):
    if not name:
        return ""
    color = category_color(name)
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:99px;font-size:0.75rem;font-weight:600;">{name}</span>'

# ── Edit dialog ───────────────────────────────────────────────────────────────
@st.dialog("Edit task")
def edit_dialog(i):
    task = st.session_state.tasks[i]

    new_text = st.text_input("Task name", value=task["text"])
    new_desc = st.text_area(
        "Description",
        value=task.get("description", ""),
        placeholder="Add more context...",
        height=100
    )

    existing_categories = sorted(set(
        t.get("category", "").strip()
        for t in st.session_state.tasks
        if t.get("category", "").strip()
    ))

    new_category = st.text_input(
        "Category",
        value=task.get("category", ""),
        placeholder="e.g. Work, Personal, Someday…",
        help="Existing: " + ", ".join(existing_categories) if existing_categories else "No categories yet"
    )

    new_status = st.selectbox(
        "Status",
        STATUSES,
        index=STATUSES.index(task.get("status", "Planned / To Do"))
    )

    new_priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"],
        index=["High", "Medium", "Low"].index(task.get("priority", "Medium"))
    )

    col_save, col_delete = st.columns([1, 1])
    with col_save:
        if st.button("Save", use_container_width=True, type="primary"):
            st.session_state.tasks[i]["text"] = new_text
            st.session_state.tasks[i]["description"] = new_desc
            st.session_state.tasks[i]["priority"] = new_priority
            st.session_state.tasks[i]["status"] = new_status
            st.session_state.tasks[i]["category"] = new_category.strip()
            save_tasks(st.session_state.tasks)
            st.session_state.editing_task = None
            st.rerun()
    with col_delete:
        if st.button("🗑 Delete task", use_container_width=True):
            st.session_state.tasks.pop(i)
            save_tasks(st.session_state.tasks)
            st.session_state.editing_task = None
            st.rerun()

# ── Page ──────────────────────────────────────────────────────────────────────
st.markdown("# Tasks")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("artifact.png")

st.markdown(f"""
<style>
.stAppViewContainer {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: contain;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.stAppViewContainer::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.75);
    z-index: 0;
    pointer-events: none;
}}
</style>
""", unsafe_allow_html=True)

st.divider()

# Metrics based on status
total = len(st.session_state.tasks)
planned     = sum(1 for t in st.session_state.tasks if t.get("status", "Planned / To Do") == "Planned / To Do")
in_progress = sum(1 for t in st.session_state.tasks if t.get("status", "Planned / To Do") == "In Progress")
blocked     = sum(1 for t in st.session_state.tasks if t.get("status", "Planned / To Do") == "Blocked")
done_count  = sum(1 for t in st.session_state.tasks if t.get("status", "Planned / To Do") == "Done")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", total)
col2.metric("Planned / To Do", planned)
col3.metric("In Progress", in_progress)
col4.metric("Blocked", blocked)
col5.metric("Done", done_count)

st.divider()

# ── Add task form ─────────────────────────────────────────────────────────────
st.markdown("#### Add a task")
with st.form("new_task_form", clear_on_submit=True):
    new_task = st.text_input("New task", placeholder="What needs to get done?")
    submitted = st.form_submit_button("Add task")
    if submitted and new_task.strip():
        st.session_state.tasks.append({
            "text": new_task.strip(),
            "description": "",
            "priority": "Medium",
            "status": "Planned / To Do",
            "category": "",
            "created": datetime.now().isoformat()
        })
        save_tasks(st.session_state.tasks)
        st.rerun()

st.divider()

# ── Task table ────────────────────────────────────────────────────────────────
st.markdown("#### Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above!")
else:
    # Header
    h1, h2, h3, h4, h5 = st.columns([0.34, 0.20, 0.18, 0.18, 0.10])
    for col, label in zip([h1, h2, h3, h4, h5], ["Task", "Category", "Status", "Priority", "Added"]):
        col.markdown(f'<span style="font-size:0.72rem;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:.05em">{label}</span>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:4px 0 8px 0; border-color:#e0e0e0;">', unsafe_allow_html=True)

    for i, task in enumerate(st.session_state.tasks):
        col_name, col_cat, col_status, col_priority, col_date = st.columns([0.34, 0.20, 0.18, 0.18, 0.10])

        with col_name:
            if st.button(task["text"], key=f"task_btn_{i}", use_container_width=True):
                st.session_state.editing_task = i

        with col_cat:
            cat = task.get("category", "")
            if cat:
                st.markdown(category_badge(cat), unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:#ccc;font-size:0.8rem;">—</span>', unsafe_allow_html=True)

        with col_status:
            st.markdown(status_badge(task.get("status", "Planned / To Do")), unsafe_allow_html=True)

        with col_priority:
            st.markdown(priority_badge(task.get("priority", "Medium")), unsafe_allow_html=True)

        with col_date:
            try:
                date_str = datetime.fromisoformat(task["created"]).strftime("%-d %b")
            except Exception:
                date_str = "—"
            st.markdown(f'<span style="font-size:0.8rem;color:#999;">{date_str}</span>', unsafe_allow_html=True)

        st.markdown('<hr style="margin:2px 0; border-color:#f0f0f0;">', unsafe_allow_html=True)

# Open dialog after rendering all rows
if st.session_state.editing_task is not None:
    edit_dialog(st.session_state.editing_task)
    st.session_state.editing_task = None

# Logout
st.sidebar.button("🔓 Lock workspace", on_click=lambda: st.session_state.update(authenticated=False))