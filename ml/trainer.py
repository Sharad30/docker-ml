import time

import numpy as np
from pydantic import BaseModel
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from .tabular_model import TabularModel
from .tabular_dataset import TabularDataset


class Trainer(BaseModel):
    dataset: TabularDataset
    model: TabularModel

    class Config:
        arbitrary_types_allowed = True

    def train(
        self,
        n_splits: int = 5,
        seed: int = 42,
        oof_filename: str = None,
    ):
        skf = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=seed,
        )

        for fold, (trn_idx, val_idx) in enumerate(
            skf.split(
                X=self.dataset.train,
                y=self.dataset.target,
            )
        ):
            print(f"===== Fold {fold} =====")
            X_train = self.dataset.train[self.dataset.features].iloc[trn_idx]
            y_train = self.dataset.target.iloc[trn_idx]
            X_valid = self.dataset.train[self.dataset.features].iloc[val_idx]
            y_valid = self.dataset.target.iloc[val_idx]
            X_test = self.dataset.test[self.dataset.features]

            start = time.time()

            self.model.model.fit(
                X_train,
                y_train,
                eval_set=[(X_valid, y_valid)],
                **self.model.training_config,
            )

            self.model.oof[val_idx] = self.model.model.predict_proba(X_valid)[:, -1]
            self.model.preds += self.model.model.predict_proba(X_test)[:, -1] / n_splits

            elapsed = time.time() - start
            auc = roc_auc_score(y_valid, self.model.oof[val_idx])
            print(f"Fold {fold} - AUC: {auc:.6f}, Elapsed Time: {elapsed:.2f}sec\n")

        print(f"OOF roc = {roc_auc_score(self.dataset.target, self.model.oof)}")

        if oof_filename:
            np.save(oof_filename, self.model.oof)
