from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class ModelGenerator:

    def __init__(self, N: int, T: int):
        """
            Abstract class that will evolve. The goal of this class is to generate all the underlying according to the
            financial model chosen. This concerns the modelization of stocks (Geometric Brownian Motion, AR, ARMA,
            ARIMA, GARCH ...), interest rates (Vasicek, Hull-White ...) and other instruments.
            Description of the underlying is stocked in a DataFrame with N trajectories and T steps until maturity
            One abstract method: PathGenerate()
            @param N : number of trajectories, int
            @param T: number of steps until maturity
        """
        self.N = N
        self.T = T

    @abstractmethod
    def PathGenerate(self):
        pass
