import pandas as pd
filename = "barber shop in ajman - no dup.csv"
df = pd.read_csv(filename)

# df = df.drop_duplicates(subset='Phone 1 - Value', keep="last")
print(df.shape)
print(df['Phone 1 - Value'])

#
# print(type(df['Phone 1 - Value'].values[0]))

if df['Phone 1 - Value'].isin([97167460566]).any():
    print(True)
else:
    print(False)



