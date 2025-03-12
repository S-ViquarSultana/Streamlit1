import streamlit as st
import requests  

# Streamlit Page Configuration
st.set_page_config(page_title="EduAI Guide", layout="wide")

# Backend API URL
API_COURSES_URL = "https://ai-education-assistant.onrender.com/getcourses"
API_PROJECTS_URL = "https://ai-education-assistant.onrender.com/get_projects"
API_INTERNSHIPS_URL = "https://ai-education-assistant.onrender.com/get_internships"

# Sidebar User Profile Section
st.sidebar.title("EduAI Guide")
st.sidebar.subheader("User Profile")

# Editable User Details
user_name = st.sidebar.text_input("Name", "Sarah Johnson")
user_major = st.sidebar.text_input("Major", "Computer Science Major")
st.sidebar.markdown("**Interests**")
interests = st.sidebar.text_area("Edit Interests (comma-separated)", "AI/ML, Web Development, Data Science, UX Design").split(", ")

st.sidebar.markdown("**Skills**")
st.sidebar.write("JavaScript (Advanced), Python (Intermediate), React (Advanced), Machine Learning (Beginner)")

st.sidebar.markdown("**Performance Highlights**")
st.sidebar.write("⭐ 4.0 GPA in Major Courses")
st.sidebar.write("🏅 Dean's List - Fall 2023")
st.sidebar.write("✅ Strong in Mathematics")

# Main Section
st.title("EduAI Guide")

# Navigation Tabs
st.write("**Select a category**")
tab_selection = st.radio("Navigation", ["Activities", "Courses", "Projects", "Internships"], index=1)

if tab_selection == "Activities":
    st.header("Explore by Interests")
    if interests:
        for interest in interests:
            if st.button(interest, key=f"btn_{interest}"):
                with st.spinner(f"Fetching courses for {interest}..."):
                    response = requests.post(API_COURSES_URL, json={"interests": [interest]})
                    if response.status_code == 200:
                        courses = response.json().get("courses", [])
                        if courses:
                            for course in courses:
                                st.markdown(f"### [{course['title']}]({course['link']})")
                                st.write(course['snippet'])
                                st.markdown("---")
                        else:
                            st.warning(f"No courses found for {interest}.")
                    else:
                        st.error("Error fetching courses. Try again later.")
    else:
        st.warning("No interests available. Please add them in the sidebar.")

elif tab_selection == "Courses":
    st.header("Recommended Courses")
    st.write("Enter your area of interest (e.g., Machine Learning, Web Development)")
    user_input = st.text_input("Interest", " ")
    if st.button("Get Courses"):
        with st.spinner("Fetching courses..."):
            response = requests.post(API_COURSES_URL, json={"interests": [user_input]})
            if response.status_code == 200:
                courses = response.json().get("courses", [])
                if courses:
                    for course in courses:
                        st.markdown(f"### [{course['title']}]({course['link']})")
                        st.write(course['snippet'])
                        st.markdown("---")
                else:
                    st.warning("No courses found for the given interest.")
            else:
                st.error("Error fetching courses. Try again later.")

elif tab_selection == "Projects":
    st.header("Search for Projects")
    project_query = st.text_input("Enter project topic (e.g., AI, Web Development)")
    if st.button("Find Projects"):
        with st.spinner(f"Searching for projects related to: {project_query}"):
            response = requests.post(API_PROJECTS_URL, json={"interests": [project_query]})
            if response.status_code == 200:
                projects = response.json().get("projects", [])
                if projects:
                    for project in projects:
                        st.markdown(f"### [{project['title']}]({project['link']})")
                        st.write(project['snippet'])
                        st.markdown("---")
                else:
                    st.warning("No projects found for the given interest.")
            else:
                st.error("Error fetching projects. Try again later.")

elif tab_selection == "Internships":
    st.header("Search for Internships")
    internship_query = st.text_input("Enter internship domain (e.g., AI, Data Science)")
    
    if st.button("Find Internships"):
        with st.spinner(f"Searching for internships related to: {internship_query}"):
            response = requests.post(f"{API_INTERNSHIPS_URL}", json={"interests": [internship_query]})
            
            if response.status_code == 200:
                internships = response.json().get("internships", [])
                
                if internships:
                    for internship in internships:
                        st.markdown(f"### [{internship['title']}]({internship['link']})")
                        st.write(internship['snippet'])
                        st.markdown("---")
                else:
                    st.warning("No internships found for the given interest.")
            else:
                st.error("Error fetching internships. Try again later.")
