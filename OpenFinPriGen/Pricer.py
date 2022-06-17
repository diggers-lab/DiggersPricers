from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class Pricer:
    def __init__(self, payoff_product: str, r: str, k: float, dt: float,
                 option_style: str = "european"):
        """
                        This abstract class aims to provide different techniques to price financial instruments
                        @param payoff_product: the payoff must be a DataFrame
                        @param r: specifying the rate model as str
                        @param k: strike considered for the underlying, float
                        @param dt: time consideration must be specified: float (monthly, daily, yearly)
                        @param option_style: "european" or "american"
        """
        self.payoff_product = payoff_product
        self.r = r
        self.k = k
        self.dt = dt
        self.option_style = option_style

    @abstractmethod
    def price(self):
        pass
