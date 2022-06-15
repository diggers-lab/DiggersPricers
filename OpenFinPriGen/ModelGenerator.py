from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class ModelGenerator:

    def __init__(self, N: int, T: int):
        """ @param s: underlying described in a DataFrame"""
        self.N = N
        self.T = T

    @abstractmethod
    def path_generate(self):
        pass
