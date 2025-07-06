# Smart Study Goal Tracker App - Ultimate Dashboard Edition

import streamlit as st
import pandas as pd
import datetime
import random
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
import time
import seaborn as sns
import plotly.express as px

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Smart Study Goal Tracker", layout="wide")

# ---------------------- DATA STORAGE ----------------------
if "goals" not in st.session_state:
    st.session_state.goals = []
if "progress" not in st.session_state:
    st.session_state.progress = {}
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "pomodoro" not in st.session_state:
    st.session_state.pomodoro = {"active": False, "start_time": None, "mode": "Focus"}
if "study_log" not in st.session_state:
    st.session_state.study_log = []

# ---------------------- QUOTES & TIPS ----------------------
quotes = [
    "Believe in yourself! You can do it!",
    "Every day is a chance to improve.",
    "Small progress is still progress.",
    "You are stronger than you think.",
    "Stay focused and never give up."
]

study_tips = [
    "Break subjects into small chunks.",
    "Teach others what you’ve learned.",
    "Use active recall instead of passive reading.",
    "Use spaced repetition techniques.",
    "Review your notes every day."
]

# ---------------------- FUNCTIONS ----------------------
def add_goal(subject, task, deadline, priority):
    goal = {
        "Subject": subject,
        "Task": task,
        "Deadline": deadline,
        "Priority": priority,
        "Status": "Pending"
    }
    st.session_state.goals.append(goal)
    st.session_state.progress[task] = 0

def mark_completed(index):
    st.session_state.goals[index]["Status"] = "Completed"
    st.session_state.progress[st.session_state.goals[index]['Task']] = 100

def get_completion_rate():
    total = len(st.session_state.goals)
    completed = sum(1 for g in st.session_state.goals if g["Status"] == "Completed")
    return int((completed / total) * 100) if total else 0

def get_today_completion_count():
    today = datetime.date.today()
    return sum(1 for g in st.session_state.goals if g["Status"] == "Completed" and g["Deadline"] == today)

def get_random_quote():
    return random.choice(quotes)

def get_study_tip():
    return random.choice(study_tips)

def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Smart Study Goal Tracker Report", ln=True, align='C')
    pdf.ln(10)
    for goal in st.session_state.goals:
        line = f"Subject: {goal['Subject']} | Task: {goal['Task']} | Deadline: {goal['Deadline']} | Priority: {goal['Priority']} | Status: {goal['Status']}"
        pdf.multi_cell(0, 10, txt=line)
    pdf.output("study_goals_report.pdf")
    return "study_goals_report.pdf"

def get_closest_deadline():
    upcoming = [g for g in st.session_state.goals if g["Status"] != "Completed"]
    if not upcoming:
        return "None"
    closest = min(upcoming, key=lambda g: g["Deadline"])
    return f"{closest['Task']} ({(closest['Deadline'] - datetime.date.today()).days} days left)"

def get_subject_leaderboard():
    subjects = {}
    for g in st.session_state.goals:
        if g["Status"] == "Completed":
            subjects[g["Subject"]] = subjects.get(g["Subject"], 0) + 1
    sorted_subjects = sorted(subjects.items(), key=lambda x: x[1], reverse=True)
    return sorted_subjects[:3]

# ---------------------- HEADER ----------------------
st.title("📚 Smart Study Goal Tracker")
st.markdown("### Anuradha College of Engineering and Technology")
st.markdown("**Email:** your-email@example.com")

quote = get_random_quote()
tip = get_study_tip()
st.success(f"💡 {quote}\n\n🧠 Tip: {tip}")

# ---------------------- DASHBOARD ----------------------
st.subheader("📊 Completion Dashboard")
total_goals = len(st.session_state.goals)
completed_goals = sum(1 for g in st.session_state.goals if g["Status"] == "Completed")
pending_goals = total_goals - completed_goals
completion = get_completion_rate()
today_completed = get_today_completion_count()
closest_deadline = get_closest_deadline()

# Level Display
if completion < 25:
    level = "🎓 Beginner"
elif completion < 60:
    level = "📘 Rising Scholar"
elif completion < 85:
    level = "🧠 Achiever"
else:
    level = "🏅 Master Learner"

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Completed", completed_goals)
col2.metric("📌 Pending", pending_goals)
col3.metric("🎯 Total Goals", total_goals)
col4.metric("🔔 Closest Deadline", closest_deadline)

st.markdown(f"### 🧪 Completion: **{completion}%** | Level: {level}")
st.progress(completion / 100)

# Pie Chart
if total_goals > 0:
    pie_data = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed_goals, pending_goals]
    })
    fig1 = px.pie(pie_data, values='Count', names='Status', title='Goal Distribution')
    st.plotly_chart(fig1)

# Leaderboard
st.markdown("### 🏆 Top 3 Subjects (Completed)")
leaders = get_subject_leaderboard()
for i, (sub, count) in enumerate(leaders, start=1):
    st.markdown(f"{i}. **{sub}** - {count} tasks")

# Study Activity Bar Chart
if st.session_state.study_log:
    df_log = pd.DataFrame(st.session_state.study_log)
    df_counts = df_log['Date'].value_counts().sort_index()
    fig2 = px.bar(df_counts, title='📅 Weekly Study Activity', labels={'index': 'Date', 'value': 'Study Sessions'})
    st.plotly_chart(fig2)

# ---------------------- GOALS ----------------------
st.subheader("🎯 Your Study Goals")
for i, goal in enumerate(st.session_state.goals):
    st.markdown(f"**Subject:** {goal['Subject']} | **Task:** {goal['Task']} | **Deadline:** {goal['Deadline']} | **Priority:** {goal['Priority']} | **Status:** {goal['Status']}")
    if goal["Status"] != "Completed":
        if st.button(f"✅ Mark '{goal['Task']}' as Completed", key=i):
            mark_completed(i)
            st.success(f"Goal '{goal['Task']}' marked as completed!")

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.header("➕ Add Study Goal")
    subject = st.text_input("Subject")
    task = st.text_input("Task")
    deadline = st.date_input("Deadline")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    if st.button("Add Goal"):
        if subject and task:
            add_goal(subject, task, deadline, priority)
            st.success("Goal Added!")
        else:
            st.error("Please fill all fields")

    st.header("📝 Study Log")
    log_subject = st.text_input("Log Subject")
    log_notes = st.text_area("What did you study?")
    if st.button("Add Log Entry"):
        if log_subject and log_notes:
            st.session_state.study_log.append({
                "Date": datetime.date.today(),
                "Subject": log_subject,
                "Notes": log_notes
            })
            st.success("Log Saved!")

# ---------------------- EXPORT ----------------------
st.subheader("📤 Export Options")
if st.button("Export Goals as CSV"):
    df = pd.DataFrame(st.session_state.goals)
    df.to_csv("progress_report.csv", index=False)
    with open("progress_report.csv", "rb") as f:
        st.download_button("Download CSV", f, file_name="progress_report.csv")

if st.button("Export Goals as PDF"):
    pdf_path = export_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="study_goals_report.pdf")
