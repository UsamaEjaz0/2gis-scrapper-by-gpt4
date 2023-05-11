import pandas as pd
filename = "resources/transitional_df.csv"
df = pd.read_csv(filename)

# df = df.drop_duplicates(subset='Phone 1 - Value', keep="last")
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

duplicates = df[df.duplicated(keep=False)]
print(duplicates)
# # print the duplicate rows
# print(duplicates)


