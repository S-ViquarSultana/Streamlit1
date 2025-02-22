import streamlit as st
import requests

# Streamlit Page Configuration
st.set_page_config(page_title="EduAI Guide", layout="wide")

# Backend API URL
API_URL = "http://127.0.0.1:8000/get_courses"

# Sidebar User Profile Section
st.sidebar.title("EduAI Guide")
st.sidebar.subheader("Sarah Johnson")
st.sidebar.text("Computer Science Major")
st.sidebar.markdown("**Interests**")
st.sidebar.write("AI/ML, Web Development, Data Science, UX Design")
st.sidebar.markdown("**Skills**")
st.sidebar.write("JavaScript (Advanced), Python (Intermediate), React (Advanced), Machine Learning (Beginner)")
st.sidebar.markdown("**Performance Highlights**")
st.sidebar.write("⭐ 4.0 GPA in Major Courses")
st.sidebar.write("🏅 Dean's List - Fall 2023")
st.sidebar.write("✅ Strong in Mathematics")

# Main Section
st.title("EduAI Guide")

# Navigation Tabs
tab_selection = st.radio("", ["Activities", "Courses", "Projects", "Internships"], index=1)

if tab_selection == "Courses":
    st.header("Recommended Courses")
    st.write("Enter your area of interest (e.g., Machine Learning, Web Development)")
    
    user_input = st.text_input("", "Machine Learning")
    
    if st.button("Get Courses"):
        with st.spinner("Fetching courses..."):
            response = requests.post(API_URL, json={"interests": [user_input]})
            
            if response.status_code == 200:
                courses = response.json().get("courses", [])
                if courses:
                    for course in courses:
                        st.markdown(f"### [{course['title']}]({course['link']})")
                        st.write(course['snippet'])
                        st.markdown("---")
                else:
                    st.error("No courses found for the given interest.")
            else:
                st.error("Error fetching courses. Try again later.")
