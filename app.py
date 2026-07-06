from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import os
import json
import threading
import webbrowser
from datetime import datetime

app = Flask(__name__)
CORS(app)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class ResumePDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.accent_r = 30
        self.accent_g = 58
        self.accent_b = 138  # Deep indigo

    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(160, 160, 160)
        self.cell(0, 8, f"Generated on {datetime.now().strftime('%B %d, %Y')}", align="C")

    def draw_sidebar(self):
        self.set_fill_color(self.accent_r, self.accent_g, self.accent_b)
        self.rect(0, 0, 65, 297, "F")

    def add_sidebar_content(self):
        d = self.data
        # Avatar circle
        self.set_fill_color(255, 255, 255)
        self.ellipse(10, 14, 45, 45, "F")
        # Initials
        initials = ""
        name_parts = d.get("name", "").split()
        if name_parts:
            initials = name_parts[0][0].upper()
            if len(name_parts) > 1:
                initials += name_parts[-1][0].upper()
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(self.accent_r, self.accent_g, self.accent_b)
        self.set_xy(10, 25)
        self.cell(45, 25, initials, align="C")

        y = 68
        # Contact section
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(180, 200, 255)
        self.set_xy(5, y)
        self.cell(55, 6, "CONTACT", align="L")
        y += 7

        contact_items = [
            ("✉", d.get("email", "")),
            ("✆", d.get("phone", "")),
            ("⌂", d.get("location", "")),
            ("🔗", d.get("linkedin", "")),
            ("⬡", d.get("github", "")),
        ]
        self.set_font("Helvetica", "", 7)
        self.set_text_color(220, 230, 255)
        for icon, val in contact_items:
            if val:
                self.set_xy(5, y)
                self.cell(8, 5, icon)
                self.set_xy(13, y)
                self.multi_cell(47, 4.5, val, border=0)
                y += 7

        y += 5
        # Skills
        skills = d.get("skills", [])
        if skills:
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(180, 200, 255)
            self.set_xy(5, y)
            self.cell(55, 6, "SKILLS", align="L")
            y += 7
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(235, 240, 255)
            for skill in skills:
                if y > 275:
                    break
                self.set_fill_color(60, 90, 180)
                self.rounded_rect(5, y, 55, 6, 2, "F")
                self.set_xy(5, y)
                self.cell(55, 6, skill, align="C")
                y += 8

        y += 5
        # Languages
        languages = d.get("languages", [])
        if languages and y < 260:
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(180, 200, 255)
            self.set_xy(5, y)
            self.cell(55, 6, "LANGUAGES", align="L")
            y += 7
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(235, 240, 255)
            for lang in languages:
                if y > 275:
                    break
                self.set_xy(7, y)
                self.cell(3, 5, "•")
                self.set_xy(11, y)
                self.cell(49, 5, lang)
                y += 6

    def add_main_content(self):
        d = self.data
        x_start = 72
        width = 130
        y = 12

        # Name
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(20, 20, 50)
        self.set_xy(x_start, y)
        self.cell(width, 12, d.get("name", ""), align="L")
        y += 13

        # Title
        self.set_font("Helvetica", "", 11)
        self.set_text_color(self.accent_r, self.accent_g, self.accent_b)
        self.set_xy(x_start, y)
        self.cell(width, 7, d.get("title", ""), align="L")
        y += 9

        # Divider
        self.set_draw_color(self.accent_r, self.accent_g, self.accent_b)
        self.set_line_width(0.5)
        self.line(x_start, y, x_start + width, y)
        y += 6

        def section_header(title, ypos):
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(self.accent_r, self.accent_g, self.accent_b)
            self.set_fill_color(235, 240, 255)
            self.rect(x_start, ypos, width, 7, "F")
            self.set_xy(x_start + 2, ypos)
            self.cell(width, 7, title.upper(), align="L")
            return ypos + 10

        # Summary
        summary = d.get("summary", "")
        if summary:
            y = section_header("Professional Summary", y)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(50, 50, 70)
            self.set_xy(x_start, y)
            self.multi_cell(width, 5, summary)
            y = self.get_y() + 6

        # Experience
        experience = d.get("experience", [])
        if experience:
            y = section_header("Work Experience", y)
            for exp in experience:
                if y > 265:
                    break
                self.set_font("Helvetica", "B", 9)
                self.set_text_color(20, 20, 50)
                self.set_xy(x_start, y)
                self.cell(85, 5, exp.get("position", ""), align="L")
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(120, 120, 140)
                self.set_xy(x_start + 85, y)
                self.cell(45, 5, exp.get("duration", ""), align="R")
                y += 6

                self.set_font("Helvetica", "I", 8.5)
                self.set_text_color(self.accent_r, self.accent_g, self.accent_b)
                self.set_xy(x_start, y)
                self.cell(width, 5, exp.get("company", ""))
                y += 6

                desc = exp.get("description", "")
                if desc:
                    self.set_font("Helvetica", "", 8)
                    self.set_text_color(60, 60, 80)
                    for line in desc.split("\n"):
                        if line.strip() and y < 270:
                            self.set_xy(x_start + 3, y)
                            self.cell(4, 4.5, "•")
                            self.set_xy(x_start + 7, y)
                            self.multi_cell(width - 7, 4.5, line.strip("•- ").strip())
                            y = self.get_y()
                y += 4

        # Education
        education = d.get("education", [])
        if education and y < 260:
            y = section_header("Education", y)
            for edu in education:
                if y > 270:
                    break
                self.set_font("Helvetica", "B", 9)
                self.set_text_color(20, 20, 50)
                self.set_xy(x_start, y)
                self.cell(85, 5, edu.get("degree", ""), align="L")
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(120, 120, 140)
                self.set_xy(x_start + 85, y)
                self.cell(45, 5, edu.get("year", ""), align="R")
                y += 6

                self.set_font("Helvetica", "", 8.5)
                self.set_text_color(self.accent_r, self.accent_g, self.accent_b)
                self.set_xy(x_start, y)
                self.cell(width, 5, edu.get("institution", ""))
                y += 7

        # Certifications
        certs = d.get("certifications", [])
        if certs and y < 260:
            y = section_header("Certifications", y)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(50, 50, 70)
            for cert in certs:
                if y > 270:
                    break
                self.set_xy(x_start + 3, y)
                self.cell(4, 5, "✓")
                self.set_xy(x_start + 7, y)
                self.cell(width - 7, 5, cert)
                y += 6

        # Projects
        projects = d.get("projects", [])
        if projects and y < 255:
            y = section_header("Projects", y)
            for proj in projects:
                if y > 270:
                    break
                self.set_font("Helvetica", "B", 8.5)
                self.set_text_color(20, 20, 50)
                self.set_xy(x_start, y)
                self.cell(width, 5, proj.get("name", ""))
                y += 6
                desc = proj.get("description", "")
                if desc:
                    self.set_font("Helvetica", "", 8)
                    self.set_text_color(60, 60, 80)
                    self.set_xy(x_start + 3, y)
                    self.multi_cell(width - 3, 4.5, desc)
                    y = self.get_y() + 4

    def generate(self):
        self.add_page()
        self.draw_sidebar()
        self.add_sidebar_content()
        self.add_main_content()
        name_slug = self.data.get("name", "resume").replace(" ", "_").lower()
        output_path = os.path.join(OUTPUT_DIR, f"{name_slug}_resume.pdf")
        self.output(output_path)
        return output_path


@app.route("/generate", methods=["POST"])
def generate_resume():
    try:
        data = request.get_json()
        pdf = ResumePDF(data)
        output_path = pdf.generate()
        return send_file(output_path, as_attachment=True,
                         download_name=os.path.basename(output_path),
                         mimetype="application/pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/preview", methods=["POST"])
def preview_resume():
    try:
        data = request.get_json()
        pdf = ResumePDF(data)
        output_path = pdf.generate()
        return send_file(output_path, mimetype="application/pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("🚀 Resume Generator Server running at http://localhost:5050")
    app.run(debug=False, port=5050)
