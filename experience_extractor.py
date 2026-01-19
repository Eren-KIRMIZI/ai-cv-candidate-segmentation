import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year


def extract_experience_years(text: str) -> float:
    text = text.lower()
    years = []

    # 1) Açık yıl ifadeleri: "3 yıl", "5+ years", "2 years experience"
    patterns = [
        r'(\d+)\s*\+?\s*years?',
        r'(\d+)\s*years?\s*experience',
        r'(\d+)\s*yıl'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            years.append(int(m))

    # 2) Tarih aralıkları: 2019-2024, 2018 – 2022, 2020-present
    date_ranges = re.findall(r'(20\d{2})\s*[-–]\s*(20\d{2}|present|now|current)', text)
    for start, end in date_ranges:
        start = int(start)
        end = CURRENT_YEAR if end in ["present", "now", "current"] else int(end)
        if end > start:
            years.append(end - start)

    if not years:
        return 0.0

    # Average al (abartıyı önle)
    return sum(years) / len(years)


def experience_level(years: float) -> str:
    if years == 0:
        return "Junior (Öğrenci / Yeni Mezun)"
    elif years < 3:
        return "Junior"
    elif years < 6:
        return "Mid"
    else:
        return "Senior"


# ------------------------- 
# ÖRNEK KULLANIM
# -------------------------
if __name__ == "__main__":
    examples = [
        "Deneyim: 0 yıl",
        "2 yıl yazılım deneyimi",
        "5+ years experience in backend development",
        "Software Engineer (2019-2024)",
        "Frontend Developer (2021-present)",
        "Yeni mezun, staj deneyimi"
    ]

    for text in examples:
        years = extract_experience_years(text)
        level = experience_level(years)
        print(f"Metin: {text}")
        print(f"Deneyim: {years} yıl")
        print(f"Seviye: {level}")
        print("-" * 40)