import time

import numpy as np
from pydantic import BaseModel
from loguru import logger
import wandb
from sklearn.model_selection import train_test_split

from .tabular_model import TabularModel
from .tabular_dataset import TabularDataset
from .utils import log_model_artifacts, save_best_model


class Trainer(BaseModel):
    dataset: TabularDataset
    model: TabularModel

    class Config:
        arbitrary_types_allowed = True

    def train(
        self,
        output_filepath: str = "output",
        model_name: str = "model",
        is_model: str = "xgb",
        description: str = "",
    ):
        wandb.init(project="docker-ml", entity="sharad30", name=model_name)
        logger.debug("Commencing train ...")
        logger.debug(f"Training features: {self.dataset.features}")
        start = time.time()
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataset.train[self.dataset.features], self.dataset.target, test_size=0.33, random_state=42
        )
        best_model = save_best_model(
            is_model,
            self.model,
            X_train,
            X_test,
            y_train,
            y_test,
            output_filepath,
            model_name,
        )
        log_model_artifacts(
            wandb,
            best_model.model,
            X_train,
            X_test,
            y_test,
            model_name,
            description,
            output_filepath,
        )
        wandb.finish()
        elapsed = time.time() - start
        print(f"Elapsed Time: {elapsed:.2f}sec\n")
