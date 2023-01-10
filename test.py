import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats
# create a dataframe
df=pd.read_csv("trades-example.csv")
print(df)
# check whether theres a linear correlation between the closing prices and the profit
def test():
    sns.regplot(x="close_price",y="profit",data=df)
    # check the pearson's co efficient
    pearson_coef,pvalue=stats.pearsonr(df["close_price"],df["profit"])
    print(f"The Pearson's coefficient is {pearson_coef}")
    print(f"The P value is {pvalue}")
    plt.ylim(0,)
    plt.show()
def main():
    test()
main()