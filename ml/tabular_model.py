from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from .tabular_dataset import TabularDataset


class TabularModel(BaseModel):
    model: Any
    model_config: Dict[str, Any]
    training_config: Dict[str, Any]
    oof: Optional[Any]  # np.array
    preds: Optional[Any]  # np.array
    importances: Optional[pd.DataFrame]

    class Config:
        arbitrary_types_allowed = True

    def prepare(self, *, dataset: TabularDataset):
        self.oof = np.zeros(dataset.train.shape[0])
        self.preds = np.zeros(dataset.test.shape[0])
        self.importances = pd.DataFrame()
        self.model = self.model(**self.model_config)
        return self
