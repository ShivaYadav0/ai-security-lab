import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

messages = [
    ("Win a free prize now, click here", "spam"),
    ("Claim your reward, limited offer", "spam"),
    ("You have won a free gift card", "spam"),
    ("Urgent: verify your account to avoid suspension", "spam"),
    ("Cheap loans approved instantly, apply now", "spam"),
    ("Free entry to win cash, reply now", "spam"),
    ("Your account is locked, click the link to unlock", "spam"),
    ("Congratulations, you were selected for a free vacation", "spam"),
    ("Are we still meeting for lunch tomorrow", "ham"),
    ("Please review the report before the call", "ham"),
    ("Can you send me the meeting notes", "ham"),
    ("Happy birthday, hope you have a great day", "ham"),
    ("The project deadline moved to Friday", "ham"),
    ("Let's catch up over coffee this weekend", "ham"),
    ("I will be late, start without me", "ham"),
    ("Thanks for your help with the presentation", "ham"),
]
texts = [text for text, label in messages]
labels = [label for text, label in messages]

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

joblib.dump(model, "spam_model.joblib")
print("model saved")
print(model.predict(["Click here to claim your free prize", "Can we move the meeting to Monday"]))
