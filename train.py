import os
import random
from pathlib import Path

import numpy as np
import xgboost as xgb
from wandb.integration.xgboost import WandbCallback

from ml import TabularModel, TabularDataset, Trainer


def seed_everything(seed=42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


seed_everything()

output_path = Path("output")
d = TabularDataset(root="data", target_str="Survived").load_df().preprocess()

training_config = {
    "eval_metric": "auc",
    "early_stopping_rounds": 20,
    "verbose": 1000,
}

# XGBClassifier
xgb_config = {
    "tree_method": "gpu_hist",
    "learning_rate": 0.01,
    "n_estimators": 2000,
    "colsample_bytree": 0.3,
    "subsample": 0.75,
    "reg_alpha": 19,
    "reg_lambda": 19,
    "max_depth": 5,
    "predictor": "gpu_predictor",
}

m = TabularModel(
    model=xgb.XGBClassifier,
    model_config=xgb_config,
    training_config=training_config,
).prepare(dataset=d)

t = Trainer(dataset=d, model=m).train(
    model_name="xgb",
    is_model="xgb",
    description="XGB titanic",
    output_filepath=output_path / "xgb",
)
