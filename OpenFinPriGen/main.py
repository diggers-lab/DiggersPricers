import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np


def main():
    # print("Initialization")
    tab = np.zeros(shape=(5, 6))
    df = pd.DataFrame(tab)
    tab_bis = np.random.randint(5, size=(5, 6))
    df_bis = pd.DataFrame(tab_bis)
    print(df_bis)
    print(df_bis.iloc[1])
    print(np.max(df_bis.iloc[1]))
    #print(df)

    # for i in range(len(df_bis)):
    #    df.iat[i,5] = max(df_bis.iat[i,5] - 1, 0)
    # print(df)


if __name__ == '__main__':
    main()
