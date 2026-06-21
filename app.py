import streamlit as st
from planner import generate_plan

st.title("🪐 Planit")
st.subheader("Turn your goals into a step-by-step plan ✨")

st.divider()

goal = st.text_input("What is your goal? 💫" , placeholder="e.g. Learn Python, Run 5km, Build a portfolio")

deadline = st.text_input("How much time do you have?", placeholder="e.g. 2 weeks, 10 days, 1 month")

level = st.radio("What is your experience level?", ["Beginner", "Intermediate", "Expert"], horizontal=True)

extra_details = st.text_input("Any additional details? (Optional)", placeholder="e.g. I can study 1 hour a day, I have a gym membership")

st.divider()

if st.button("✨ Generate My Plan"):
    if not goal or not deadline:
        st.warning("Please fill in your goal and time available!")
    else:
        with st.spinner("Generating your plan..."):
            plan = generate_plan(goal, deadline, level, extra_details)
        st.markdown(plan)