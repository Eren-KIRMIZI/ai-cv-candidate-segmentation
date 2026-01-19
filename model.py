import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

SKILLS = [
    "python", "java", "sql", "machine learning", "deep learning",
    "flask", "django", "docker", "linux", "git",
    "communication", "excel"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]

class CVModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self.trained = False

    def train(self):
        texts = [
            "python machine learning sql deep learning",  # Uygun Data Scientist
            "java python sql flask django",  # Uygun Backend
            "docker linux git devops",  # Uygun DevOps
            "communication excel hr management",  # Uygun HR
            "random text no skills",  # Uygunsuz
            "deep learning python tensorflow keras"  # Uygun Data Scientist
        ]
        labels = [1, 1, 1, 1, 0, 1]  # 1: Uygun, 0: Uygunsuz

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.trained = True

    def predict_score(self, text):
        if not self.trained:
            self.train()

        vec = self.vectorizer.transform([clean_text(text)])
        return self.model.predict_proba(vec)[0][1]