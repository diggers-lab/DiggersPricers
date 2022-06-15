import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen import Pricer

class AnalyticalExpressions(Pricer):

    def __init__(self, s: pd.DataFrame, style: str, k: float, maturity: float, rf: float = 0, q: float = 0):
        """
                    This class describes the key parameters of Vanilla products as well as their payoff
                    @param s: stock price at time zero
                    @param style: call ("c") or put ("p").
                    @param k: Strike price of your option.
                    @param maturity: Time until the end of life of the option.
                    @param rf: Risk free rate to apply for the calculations.default=0.
                    @param q: Dividend yield (if existing). Default=0.
        """
        self.s = s
        self.style = style
        self.k = k
        self.maturity = maturity
        self.rf = rf
        self.q = q

    def priceBlackScholes(self, s: pd.DataFrame, style: str, k: float, maturity: float, rf: float = 0, q: float = 0):



