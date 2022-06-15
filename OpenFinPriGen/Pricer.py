from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class Pricer:
    def __init__(self, df_payoff: pd.DataFrame, r: pd.DataFrame, maturity: int):
        # mpayoff = Vanilla....payoff.()
        self.df_payoff = df_payoff
        self.r = r
        self.maturity = maturity
