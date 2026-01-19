from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

POSITION_DESCRIPTIONS = {
    "Backend Developer": """
    Backend developer with experience in Python, Flask, Django, REST APIs,
    databases (PostgreSQL, MySQL), authentication, and scalable systems.
    """,

    "Data Scientist": """
    Data scientist skilled in Python, machine learning, pandas, numpy,
    data visualization, statistics, and model evaluation.
    """,

    "DevOps Engineer": """
    DevOps engineer experienced with Docker, CI/CD pipelines, Linux,
    cloud platforms, monitoring, and automation.
    """,
    
    "HR": """
    HR specialist with skills in communication, recruitment, employee relations,
    Excel, and organizational management.
    """
}

def semantic_match_score(position_name: str, cv_text: str) -> float:
    if position_name not in POSITION_DESCRIPTIONS:
        raise ValueError(f"Unknown position: {position_name}")

    pos_embedding = model.encode(
        POSITION_DESCRIPTIONS[position_name],
        convert_to_tensor=True
    )

    cv_embedding = model.encode(
        cv_text,
        convert_to_tensor=True
    )

    score = util.cos_sim(pos_embedding, cv_embedding).item()
    return round(score, 3)