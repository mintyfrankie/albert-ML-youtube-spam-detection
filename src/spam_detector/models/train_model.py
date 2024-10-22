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
DUMP_DIR = Path(__file__).parent


def etl(df: pd.DataFrame) -> pd.DataFrame:
    """
    ETL pipeline to load data, merge data, and save to a new csv file
    """

    TARGET_COLUMNS = ["content", "label"]
    COLUMNS_RENAME_MAPPING = {
        "CONTENT": "content",
        "Comment": "content",
        "CLASS": "label",
        "Spam": "label",
    }

    df = df.copy()
    df = df.rename(columns=COLUMNS_RENAME_MAPPING)
    df = df[TARGET_COLUMNS]
    df = df.dropna(subset=TARGET_COLUMNS)
    df["content"] = df["content"].str.strip()
    df["label"] = df["label"].astype(int)

    return df


df_1 = pd.read_csv(DATA_DIR / "youtube_spam.csv")
df_2 = pd.read_csv(DATA_DIR / "yt_comments_5000.csv", encoding="cp1252")
df_1 = etl(df_1)
df_2 = etl(df_2)
df = pd.concat([df_1, df_2], ignore_index=True)

X = df["content"]
y = df["label"]

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


dump(pipeline, DUMP_DIR / "model.joblib")
