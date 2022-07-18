import pandas as pd

## example input
"""
d = {'Дата': ["07.05.2022", "07.05.2022", "08.05.2022", "08.05.2022"],
     'Товар': ["Банан", "Хлеб", "Банан", "Хлеб"],
     'Количество': [30, 10, 40, 8]}
df = pd.DataFrame(data=d)
"""
## example output
"""
d2 = {"Количество":{"Банан":70,"Хлеб":18}}
df2 = pd.DataFrame(data=d2)
"""
## df to json
# df.to_json(force_ascii=False)

def count_sum(df):
    df = df.set_index(['Дата', 'Товар'])
    return df.groupby(level="Товар").sum()

## selftest
#df2.equals(count_sum(df))

