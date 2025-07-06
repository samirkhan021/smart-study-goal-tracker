# Smart Study Goal Tracker App

import streamlit as st
import pandas as pd
import datetime
import random
import matplotlib.pyplot as plt
import os

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Smart Study Goal Tracker", layout="wide")

# ---------------------- DATA STORAGE ----------------------
if "goals" not in st.session_state:
    st.session_state.goals = []
if "progress" not in st.session_state:
    st.session_state.progress = {}
if "streak" not in st.session_state:
    st.session_state.streak = 0

# ---------------------- MOTIVATIONAL QUOTES ----------------------
quotes = [
    "Believe in yourself! You can do it!",
    "Every day is a chance to improve.",
    "Small progress is still progress.",
    "You are stronger than you think.",
    "Stay focused and never give up."
]

# ---------------------- FUNCTIONS ----------------------
def add_goal(subject, task, deadline):
    goal = {
        "Subject": subject,
        "Task": task,
        "Deadline": deadline,
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

def get_random_quote():
    return random.choice(quotes)

# ---------------------- UI ----------------------
st.title("📚 Smart Study Goal Tracker")
st.markdown("### Anuradha College of Engineering and Technology")
st.markdown("**Email:** your-email@example.com")

quote = get_random_quote()
st.info(f"💡 {quote}")

with st.sidebar:
    st.header("➕ Add Study Goal")
    subject = st.text_input("Subject")
    task = st.text_input("Task")
    deadline = st.date_input("Deadline")
    if st.button("Add Goal"):
        if subject and task:
            add_goal(subject, task, deadline)
            st.success("Goal Added!")
        else:
            st.error("Please fill all fields")

# ---------------------- MAIN SECTION ----------------------

st.subheader("🎯 Your Study Goals")
if st.session_state.goals:
    df = pd.DataFrame(st.session_state.goals)
    st.table(df)
    
    for i, goal in enumerate(st.session_state.goals):
        if goal["Status"] != "Completed":
            if st.button(f"Mark '{goal['Task']}' as Completed", key=i):
                mark_completed(i)
                st.success(f"Goal '{goal['Task']}' marked as completed!")
else:
    st.warning("No goals added yet. Use the sidebar to add one.")

# ---------------------- PROGRESS ----------------------
st.subheader("📊 Progress Tracker")
completion_rate = get_completion_rate()
st.progress(completion_rate / 100)
st.write(f"Overall Completion: {completion_rate}%")

fig, ax = plt.subplots()
tasks = list(st.session_state.progress.keys())
values = list(st.session_state.progress.values())
ax.barh(tasks, values, color="skyblue")
ax.set_xlabel("Completion %")
st.pyplot(fig)

# ---------------------- STREAK ----------------------
st.subheader("🔥 Streak Tracker")
st.session_state.streak += 1  # simulate daily usage
st.metric("Current Streak (Days)", st.session_state.streak)

# ---------------------- EXPORT PROGRESS ----------------------
if st.button("📤 Export Progress as CSV"):
    df = pd.DataFrame(st.session_state.goals)
    df.to_csv("progress_report.csv", index=False)
    with open("progress_report.csv", "rb") as f:
        st.download_button("Download CSV", f, file_name="progress_report.csv")
