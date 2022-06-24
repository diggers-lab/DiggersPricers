from abc import ABC

import numpy as np
import scipy.stats as si
from scipy.stats import norm

from OpenFinPriGen.Pricer import Pricer


class AnalyticalExpressions(Pricer, ABC):

    def __init__(self, s0: float, vanilla_style: str, k: float, tau: float, rf: float = 0, q: float = 0):
        """
            This class aims to provide analytical expressions when models offer pricing tractability
            @param s0: stock price at time zero
            @param vanilla_style: call ("c") or put ("p").
            @param k: Strike price of your option.
            @param tau: Time until the end of life of the option.
            @param rf: Risk free rate to apply for the calculations.default=0.
            @param q: Dividend yield (if existing). Default=0.
        """
        self.s0 = s0
        self.vanilla_style = vanilla_style
        self.k = k
        self.tau = tau
        self.rf = rf
        self.q = q



