from sentence_transformers import util
from semantic_matcher import model, POSITION_DESCRIPTIONS

def recommend_positions(cv_text, top_k=3):
    cv_emb = model.encode(cv_text, convert_to_tensor=True)

    scores = []
    for position, desc in POSITION_DESCRIPTIONS.items():
        pos_emb = model.encode(desc, convert_to_tensor=True)
        score = util.cos_sim(cv_emb, pos_emb).item()
        scores.append((position, round(score, 3)))

    return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]