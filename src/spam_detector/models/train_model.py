"""
Train a model to detect spam emails.
"""

from pathlib import Path
from typing import TypedDict

import pandas as pd
import xgboost as xgb
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_DIR = Path(__file__).parent / "data"

# TODO: build an ETL pipeline to load data, merge data, and save to a new csv file
df_1 = pd.read_csv(DATA_DIR / "youtube_spam.csv")
df_1 = df_1[["CONTENT", "CLASS"]]
df_2 = pd.read_csv(DATA_DIR / "yt_comments_5000.csv", encoding="cp1252")
df_2 = df_2.rename(columns={"Comment": "CONTENT", "Spam": "CLASS"})

df = pd.concat([df_1, df_2], ignore_index=True)

X = df["CONTENT"]
y = df["CLASS"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=13
)


class XGBParams(TypedDict):
    objective: str
    max_depth: int
    learning_rate: float
    eval_metric: str


XGB_PARAMS: XGBParams = {
    "objective": "binary:logistic",
    "max_depth": 6,
    "learning_rate": 0.1,
    "eval_metric": "logloss",
}


pipeline = Pipeline(
    [
        ("vectorizer", TfidfVectorizer()),
        ("model", xgb.XGBClassifier(**XGB_PARAMS)),
    ]
)

pipeline.fit(X_train, y_train)

# TODO: determine threshold
# TODO: implement mlflow

DUMP_DIR = Path(__file__).parent / "dump"

dump(pipeline, DUMP_DIR / "spam_detector.joblib")
