import pandas as pd
filename = "resources/numbers.csv"
df = pd.read_csv(filename)
# df = df.drop_duplicates( keep="last")
# df.to_csv(filename)
# print(df.shape)
# print(df['Phone 1 - Value'])
#
# #
# # print(type(df['Phone 1 - Value'].values[0]))
#
# if df['Phone 1 - Value'].isin([971505198234]).any():
#     print(True)
# else:
#     print(False)
#

duplicates = df[df.duplicated(subset='Phone 1 - Value', keep=False)]
print(duplicates)
# # print the duplicate rows
# print(duplicates)


