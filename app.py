import os
import sqlite3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from pdf_parser import extract_text_from_pdf
from model import CVModel, extract_skills
from dashboard import get_dashboard_data
from semantic_matcher import semantic_match_score
from rule_engine import position_match_score, seniority_level_by_experience, POSITION_RULES   
from experience_extractor import extract_experience_years
from explainability import explain_match
from position_recommender import recommend_positions

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = CVModel()


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            position TEXT,
            seniority TEXT,
            score REAL,
            status TEXT,
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files.get("cv")
        position = request.form.get("position")

        if not file:
            return render_template("index.html", result={"error": "CV dosyası gerekli."})

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            # PDF text
            cv_text = extract_text_from_pdf(filepath)

            # Skills
            skills = extract_skills(cv_text)

            # Deneyim yılları
            years = extract_experience_years(cv_text)
            seniority = seniority_level_by_experience(years)

            # Eğer pozisyon belirtilmemişse öner
            if not position:
                recommendations = recommend_positions(cv_text)
                position = recommendations[0][0] if recommendations else "Bilinmiyor"

            # Scores (0–1)
            ml_score = model.predict_score(cv_text)
            pos_score, matched_skills = position_match_score(position, skills)
            semantic_score = semantic_match_score(position, cv_text)

            # Deneyim çarpanı (düşük deneyim skoru düşürür)
            experience_factor = min(years / 5.0, 1.0) if years > 0 else 0.5

            # Final score
            final_score = min(
                ((ml_score * 0.40) +
                 (pos_score * 0.30) +
                 (semantic_score * 0.30)) * experience_factor,
                1.0
            )

            status = "Uygun" if final_score >= 0.55 else "Uygun Değil"

            # Açıklanabilirlik
            position_skills = POSITION_RULES.get(position, {}).get("skills", [])
            explain = explain_match(skills, position_skills)

            # DB insert
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO cvs (
                    filename,
                    position,
                    seniority,
                    score,
                    status,
                    skills
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                filename,
                position,
                seniority,
                final_score,
                status,
                ", ".join(skills)
            ))
            conn.commit()
            conn.close()

            result = {
                "filename": filename,
                "position": position,
                "seniority": seniority,
                "score": round(final_score * 100, 2),
                "status": status,
                "skills": skills,
                "matched": matched_skills,
                "semantic": round(semantic_score * 100, 2),
                "explain": explain,
                "years": years
            }
        except Exception as e:
            result = {"error": f"Hata: {str(e)}"}

    return render_template("index.html", result=result)


@app.route("/dashboard")
def dashboard():
    data = get_dashboard_data()
    return render_template(
        "dashboard.html",
        total=data["total"],
        uygun=data["uygun"],
        uygun_degil=data["uygun_degil"],
        position_counts=data["position_counts"],
        avg_scores=data["avg_scores"],
        seniority_counts=data["seniority_counts"]
    )


if __name__ == "__main__":
    app.run(debug=True)