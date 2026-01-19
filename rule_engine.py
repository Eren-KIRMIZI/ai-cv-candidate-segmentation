POSITION_RULES = {
    "Data Scientist": {
        "skills": ["python", "machine learning", "sql", "deep learning"],
    },
    "Backend Developer": {
        "skills": ["java", "python", "sql", "flask", "django"],
    },
    "DevOps": {
        "skills": ["docker", "linux", "git"],
    },
    "HR": {
        "skills": ["communication", "excel"],
    }
}

def position_match_score(position, candidate_skills):
    if position not in POSITION_RULES:
        return 0.0, []
    required = POSITION_RULES[position]["skills"]
    matched = [s for s in required if s.lower() in [c.lower() for c in candidate_skills]]
    return len(matched) / len(required), matched

def seniority_level_by_experience(years: float) -> str:
    if years >= 5:
        return "Senior"
    if years >= 2:
        return "Mid"
    return "Junior"