from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class Pricer:
    def __init__(self, payoff_product: str, r: str, k: float, dt: float,
                 option_style: str = "european"):
        """
                        This abstract class aims to provide different techniques to price financial instruments such as:
                        Monte-Carlo Methods, Binomial tree, Analytical expressions
                        @param payoff_product: payoff type instrument: "options", "fixed_income", ...
                        @param r: specifying the rate model, str
                        @param k: strike considered for the underlying, float
                        @param dt: time discretization must be specified: float (monthly, daily, yearly)
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
