from fpdf import FPDF
import os
import re

class Resume:
    def __init__(self, name, job_title, contact, summary, education, technical_expertise, experience, certifications,
                 professional_strengths):
        self.name = name
        self.job_title = job_title
        self.contact = contact
        self.summary = summary
        self.education = education
        self.technical_expertise = technical_expertise
        self.experience = experience
        self.certifications = certifications
        self.professional_strengths = professional_strengths

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title, color):
        self.set_font('Arial', 'B', 13)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(2)

    def section_body(self, body, color):
        self.set_font('Arial', '', 11)
        self.set_text_color(*color)
        self.multi_cell(0, 8, body)
        self.ln(4)

    def add_experience(self, experience):
        self.section_title('Experience', (0, 102, 204))
        self.section_body("\n".join(experience), (0, 0, 0))

    def add_education(self, education):
        self.section_title('Education', (0, 153, 76))
        self.section_body("\n".join(education), (0, 0, 0))

    def add_technical_expertise(self, expertise):
        self.section_title('Technical Expertise', (255, 87, 34))
        self.section_body(expertise, (0, 0, 0))

    def add_certifications(self, certifications):
        self.section_title('Certifications', (255, 193, 7))
        self.section_body(certifications, (0, 0, 0))

    def add_professional_strengths(self, strengths):
        self.section_title('Professional Strengths', (153, 50, 204))
        self.section_body(strengths, (0, 0, 0))

def sanitize_input(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = text.replace('\r', '')  # Remove carriage returns
    return text

def read_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input("> ")
        if line.lower() == 'end':
            break
        lines.append(line)
    return "\n".join(lines)

def create_pdf(resume):
    pdf = PDF()
    pdf.add_page()

    # Add Title (Name and Job Title)
    pdf.set_font('Arial', 'B', 22)
    pdf.set_text_color(0, 51, 102)  # Dark blue text
    pdf.cell(0, 10, sanitize_input(resume.name), 0, 1, 'C')
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(255, 69, 0)  # Red-Orange text
    pdf.cell(0, 10, sanitize_input(resume.job_title), 0, 1, 'C')
    pdf.ln(5)

    # Add Contact Information
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(0, 0, 0)  # Black text
    contact_info = [f'Email: {resume.contact[0]}', f'Phone: {resume.contact[1]}', f'LinkedIn: {resume.contact[2]}',
                    f'Location: {resume.contact[3]}']
    for info in contact_info:
        pdf.cell(0, 8, sanitize_input(info), 0, 1, 'C')
    pdf.ln(5)

    # Add Summary
    pdf.section_title('Summary', (0, 102, 204))
    pdf.section_body(sanitize_input(resume.summary), (0, 0, 0))

    # Add Technical Expertise
    pdf.add_technical_expertise(sanitize_input(resume.technical_expertise))

    # Add Education
    pdf.add_education([sanitize_input(edu) for edu in resume.education])

    # Add Experience
    pdf.add_experience([sanitize_input(job) for job in resume.experience])

    # Add Certifications
    pdf.add_certifications(sanitize_input(resume.certifications))

    # Add Professional Strengths
    pdf.add_professional_strengths(sanitize_input(resume.professional_strengths))

    output_path = os.path.join(os.getcwd(), "resume.pdf")
    pdf.output(output_path)
    print(f"Resume saved as {output_path}")

def get_resume_info():
    name = input("Enter your name: ")
    job_title = input("Enter your job title: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    linkedin = input("Enter your LinkedIn profile: ")
    location = input("Enter your location: ")
    summary = read_multiline_input("Enter your summary (type 'END' to finish):")

    education = []
    print("Enter your education (type 'done' when finished):")
    while True:
        edu = input("> ")
        if edu.lower() == 'done':
            break
        education.append(edu)

    technical_expertise = read_multiline_input("Enter your technical expertise (type 'END' to finish):")

    experience = []
    print("Enter your work experience (type 'done' when finished):")
    while True:
        job = input("> ")
        if job.lower() == 'done':
            break
        experience.append(job)

    certifications = input("Enter your certifications: ")

    professional_strengths = read_multiline_input("Enter your professional strengths (type 'END' to finish):")

    contact = [email, phone, linkedin, location]
    return Resume(name, job_title, contact, summary, education, technical_expertise, experience, certifications,
                  professional_strengths)

if __name__ == "__main__":
    resume = get_resume_info()
    create_pdf(resume)

