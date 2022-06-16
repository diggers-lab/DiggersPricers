from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class StructuredProducts:

    def __init__(self, s: pd.DataFrame):
        """ @param s: underlying described in a DataFrame"""
        self.s = s

    @abstractmethod
    def Payoff(self):
        pass
