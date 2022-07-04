import pandas as pd

from OpenFinPriGen.StructuredProducts import StructuredProducts


class VanillaProducts(StructuredProducts):

    def __init__(self, s: pd.DataFrame, options: pd.DataFrame, vanilla_style: str, k: float):

        """
                VanillaProducts are considered as a subclass of StructuredProducts. The abstract method Payoff() is
                overrided to get the payoff dataframe of the option style considered: call or put

                This class describes the key parameters of Vanilla products as well as their payoff
                @param s: stock price evolution described in a DataFrame
                @param options : Dataframe describing the payoff along each trajectory
                @param vanilla_style: call ("c") or put ("p"), str
        """

        StructuredProducts.__init__(self, s)
        self.options = options
        self.vanilla_style = vanilla_style
        self.k = k

    def Payoff(self):
        T = len(self.s.iloc[0])
        N = len(self.s[0])

        if self.vanilla_style == "c":
            for i in range(N):
                self.options.iat[i, T - 1] = max(self.options.iat[i, T - 1] - self.k, 0)

        elif self.vanilla_style == "p":
            for i in range(N):
                self.options.iat[i, T - 1] = max(self.k - self.options.iat[i, T - 1], 0)

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")

        return self.options, self.s
