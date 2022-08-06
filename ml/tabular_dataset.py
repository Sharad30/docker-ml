from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder


class TabularDataset(BaseModel):
    root: Union[str, Path]
    train: Optional[pd.DataFrame]
    test: Optional[pd.DataFrame]
    features: Optional[List[str]]
    target: Optional[pd.Series]
    target_str: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    def load_df(self):
        self.root = Path(self.root)
        self.train = pd.read_csv(self.root / "train.csv")
        self.test = pd.read_csv(self.root / "test.csv")

        self.features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
        self.target = self.train[self.target_str].copy()
        return self

    def preprocess(self):
        self.train[self.features] = self.train[self.features].fillna(self.train[self.features].mean())
        self.test[self.features] = self.test[self.features].fillna(self.test[self.features].mean())

        le = LabelEncoder()
        cat_features = ["Sex", "Embarked"]
        self.train[cat_features] = le.fit_transform(cat_features)
        self.test[cat_features] = le.transform(cat_features)
        return self
