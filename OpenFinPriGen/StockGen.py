from abc import ABC

import numpy as np
import pandas as pd

from OpenFinPriGen.ModelGenerator import ModelGenerator


class InterestRateGen(ModelGenerator, ABC):
    """
        Subclass of ModelGenerator, that generates stocks as a dataframe from a model specified
    """
    def __init__(self, N: int, T: int):
        ModelGenerator.__init__(self, N, T)