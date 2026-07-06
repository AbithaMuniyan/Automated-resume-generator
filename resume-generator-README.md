# 📄 Automated Resume Generator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PDF](https://img.shields.io/badge/PDF-fpdf2-red?style=for-the-badge)

A Python web application that automatically generates a **professionally designed PDF resume** from user input. Built as part of my 2nd semester B.E. CSE Python programming coursework.

---

## ✨ What it does

- Takes user details as input (name, title, skills, experience, education, projects)
- Automatically generates a **styled two-column PDF resume**
- Features a deep indigo sidebar with contact info and skills
- Displays initials as an avatar, formatted sections and bullet points
- Saves the generated PDF to an output folder
- Runs as a local web server using Flask

---

## 📸 Features

| Feature | Details |
|---|---|
| 🎨 Professional Design | Two-column layout with indigo sidebar |
| 👤 Avatar | Auto-generates initials from name |
| 📋 Sections | Summary, Experience, Education, Skills, Certifications, Projects |
| 📞 Contact Info | Email, Phone, Location, LinkedIn, GitHub |
| 📅 Footer | Auto-adds generation date |
| 🌐 REST API | `/generate` and `/preview` endpoints |

---

## 🛠️ Built With

- **Python** — core programming language
- **Flask** — lightweight web framework for the API server
- **fpdf2** — PDF generation library
- **Flask-CORS** — cross-origin request handling

---

## 🚀 How to Run

**Step 1 — Install dependencies:**
```bash
pip install flask flask-cors fpdf2
```

**Step 2 — Run the server:**
```bash
python app.py
```

**Step 3 — Server starts at:**
```
http://localhost:5050
```

**Step 4 — Send a POST request to generate a resume:**
```json
POST /generate
{
  "name": "Abitha M",
  "title": "B.E. CSE Student | Web Developer",
  "email": "abitha@email.com",
  "phone": "+91 9999999999",
  "location": "Salem, Tamil Nadu",
  "linkedin": "linkedin.com/in/abitha-m",
  "github": "github.com/AbithaMuniyan",
  "summary": "Passionate CSE student...",
  "skills": ["Python", "HTML", "CSS", "JavaScript"],
  "languages": ["English", "Tamil"],
  "education": [
    {
      "degree": "B.E. Computer Science Engineering",
      "institution": "Your College Name",
      "year": "2023 - 2027"
    }
  ],
  "experience": [],
  "certifications": [],
  "projects": [
    {
      "name": "Portfolio Website",
      "description": "Responsive portfolio with glassmorphism design"
    }
  ]
}
```

The generated PDF is saved in the `/output` folder and also downloaded automatically.

---

## 📁 Project Structure

```
automated-resume-generator/
├── app.py          # Main Flask server + PDF generation logic
├── output/         # Generated PDF resumes saved here
└── README.md
```

---

## 💡 What I Learned

- Building a REST API with **Flask**
- Generating PDF documents programmatically with **fpdf2**
- Handling JSON data from POST requests
- Object-oriented programming in Python (class-based design)
- File handling and directory management in Python

---

## 👩‍💻 Author

**Abitha M** — B.E. Computer Science Engineering (2nd Semester)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/abitha-m-747b86380/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-222222?style=flat-square&logo=github)](https://github.com/AbithaMuniyan)
