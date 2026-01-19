def explain_match(cv_skills, position_skills):
    cv_lower = [s.lower() for s in cv_skills]
    pos_lower = [s.lower() for s in position_skills]
    matched = list(set(cv_lower) & set(pos_lower))
    missing = list(set(pos_lower) - set(cv_lower))
    extra = list(set(cv_lower) - set(pos_lower))

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "score_hint": round(len(matched) / max(len(position_skills), 1), 3)
    }