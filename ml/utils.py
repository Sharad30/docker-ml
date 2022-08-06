import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os


def save_best_model(
    is_model,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
    output_filepath,
    model_name,
):
    if is_model == "xgb":
        model.model.fit(
            X_train,
            y_train,
            eval_set=[(X_test, y_test)],
            **model.training_config,
        )
        os.makedirs(output_filepath / model_name, exist_ok=True)
        model.model.save_model(output_filepath / model_name / f"{model_name}.pkl")
        return model
    else:
        model.model.fit(
            X_train,
            y_train,
            **model.training_config,
        )
        os.makedirs(output_filepath / model_name, exist_ok=True)
        joblib.dump(model.model, output_filepath / model_name / f"{model_name}.pkl")
        return model


def log_model_artifacts(
    wandb,
    model,
    X_train,
    X_test,
    y_test,
    model_name,
    description,
    output_filepath,
):

    trained_model_artifact = wandb.Artifact(model_name, type="model", description=description)
    trained_model_artifact.add_dir(output_filepath / model_name)
    wandb.run.log_artifact(trained_model_artifact)

    rmse_test, r2_score_test = get_eval_metrics(model, X_test, y_test)
    eval_table = wandb.Table(
        columns=["test_rmse", "test_r2"],
        data=[[rmse_test, r2_score_test]],
    )
    wandb.run.log({"evaluation_metrics": eval_table})

    sorted_idx = model.feature_importances_.argsort()
    importances = model.feature_importances_
    fig = plt.figure(figsize=(20, 8))
    plt.barh(X_train.columns[sorted_idx], importances[sorted_idx])
    plt.tight_layout()
    wandb.log({"feature_importance": wandb.Image(fig)})

    feat_df = pd.concat(
        [
            pd.Series(X_train.columns[sorted_idx]),
            np.round(pd.Series(importances[sorted_idx]), 2),
        ],
        axis=1,
    )
    feat_df.columns = ["feature", "importance"]
    feat_df = feat_df.sort_values("importance", ascending=False)
    imp_table = wandb.Table(
        columns=["feature", "importance"],
        data=[
            [feat_df.iloc[0, 0], feat_df.iloc[0, 1]],
            [feat_df.iloc[1, 0], feat_df.iloc[1, 1]],
            [feat_df.iloc[2, 0], feat_df.iloc[2, 1]],
            [feat_df.iloc[3, 0], feat_df.iloc[3, 1]],
            [feat_df.iloc[4, 0], feat_df.iloc[4, 1]],
        ],
    )
    wandb.run.log({"feature_importances": imp_table})


def get_eval_metrics(model, X_test, y_test):
    model.preds = model.predict(X_test)

    rmse_test = np.sqrt(mean_squared_error(y_test, model.preds))
    r2_score_test = r2_score(y_test, model.preds)
    print(f"Test RMSE = {rmse_test:.6f}")
    print(f"Test R2 = {r2_score_test:.6f}")
    return rmse_test, r2_score_test
