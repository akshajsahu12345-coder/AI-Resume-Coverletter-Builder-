import streamlit as st
import ollama
from back import generate_resume_pdf, generate_cover_letter_pdf

st.set_page_config(page_title="AI Resume & Cover Letter Builder", page_icon="📝")
st.title("✨ AI Resume & Cover Letter Builder ")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    linkedin = st.text_input("LinkedIn URL (optional)")
    skills = st.text_area("Technical Skills (comma-separated)")
    soft_skills = st.text_area("Soft Skills (comma-separated)")
    projects = st.text_area("Project titles (comma-separated)")
    hobbies = st.text_area("Extra-Curricular Activities (comma-separated)")

    col1, col2 = st.columns(2)
    with col1:
        school_10 = st.text_input("10th School Name")
        percent_10 = st.text_input("10th Percentage")
        school_12 = st.text_input("12th School Name")
        percent_12 = st.text_input("12th Percentage")
    with col2:
        college = st.text_input("College Name & Course")
        cgpa = st.text_input("CGPA / Percentage")

    col3, col4 = st.columns(2)
    with col3:
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Other"])
    with col4:
        year_of_completion = st.selectbox("Year of Completion", ["2024", "2025", "2026", "2027", "2028"])

    resume_style = st.selectbox("Resume style / target:", ["Standard", "MNC", "Startup", "Government", "Academic"])

    # 🟢 Two buttons
    generate_resume = st.form_submit_button("🚀 Generate Resume")
    generate_cover = st.form_submit_button("✉ Generate Cover Letter")

if generate_resume:
    model = "llama3"

    prompt = f"""
You are a professional resume writer. For {name}, targeting {resume_style}:
Write these 6 sections, each starting with ###SECTION### (exactly, no text before or after):
###SECTION###
Career Objective: first-person, start with 'Myself {name}', highlight technical skills: {skills}.
Make it sound confident & professional.
###SECTION###
Education: bullets:
• Branch: {branch}, CGPA: {cgpa}, Year: {year_of_completion} at {college}.
• Achieved {percent_12}% from {school_12} in 12th.
• Secured {percent_10}% from {school_10} in 10th.
###SECTION###
Academic Projects: for these projects: {projects}.
For each project:
- Start with a short, catchy one-line summary.
- Then add 2–3 sub-bullets: tools used, achievement, and impact.
Make it sound professional & MNC-ready.
###SECTION###
Technical Skills: bullet list: {skills}.
###SECTION###
Soft Skills: bullet list: {soft_skills}.
###SECTION###
Extra-Curricular:  in (2-3) even if hobbies list is very large : {hobbies}, still write 1 brief , professional bullet point.
Add creative phrasing so it looks diverse and impressive.
⚠ Strictly do NOT add any headings like 'Career Objective', etc. inside content.
⚠ Do NOT add polite intro like 'Here is...'. Only direct content.
"""

    response = ollama.chat(model=model, messages=[{'role':'user','content':prompt}])['message']['content']

    sections = response.split('###SECTION###')
    profile = sections[1].strip() if len(sections) > 1 else ""
    education = sections[2].strip() if len(sections) > 2 else ""
    projects_ai = sections[3].strip() if len(sections) > 3 else ""
    skills_ai = sections[4].strip() if len(sections) > 4 else ""
    soft_skills_ai = sections[5].strip() if len(sections) > 5 else ""
    extras_ai = sections[6].strip() if len(sections) > 6 else ""

    resume_pdf = generate_resume_pdf(name, email, phone, linkedin, profile, education, projects_ai, skills_ai, soft_skills_ai, extras_ai)
    with open(resume_pdf, "rb") as f:
        st.download_button("📄 Download Resume PDF", data=f, file_name="resume.pdf", mime="application/pdf")
    st.success("✅ Resume generated successfully!")

if generate_cover:
    model = "llama3"
    cover_prompt = f"""
You are a professional cover letter writer. Write a longer, detailed (about 3-4 paragraphs) first-person cover letter for {name}.
Mention phone: {phone}, email: {email}, linkedin: {linkedin}(if given by the user).
Highlight career objective, branch: {branch}, cgpa: {cgpa}, projects: {projects}, and technical skills: {skills}.
Make it sound confident, professional, and impressive. Do NOT add heading like 'Cover Letter:', also givde the name of the person at the end only in in one page 
"""

    cover_letter = ollama.chat(model=model, messages=[{'role':'user','content':cover_prompt}])['message']['content'].strip()

    cover_pdf = generate_cover_letter_pdf(name, email, phone, linkedin, cover_letter)
    with open(cover_pdf, "rb") as f:
        st.download_button("✉ Download Cover Letter PDF", data=f, file_name="cover_letter.pdf", mime="application/pdf")
    st.success("✅ Cover letter generated successfully!")