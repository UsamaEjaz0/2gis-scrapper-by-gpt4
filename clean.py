import pandas as pd
filename = "barber shop ajman/barber shop - ajman - companies.csv"
df = pd.read_csv(filename)

df = df.drop_duplicates(subset='Phone 1 - Value', keep="last")
print(df.shape)