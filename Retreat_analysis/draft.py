import pandas as pd

annot_df = pd.read_csv(r"D:\2022\retreat\retreat_20220222.csv")
annot_df['fly'] = annot_df['fly']-1
new_annot_df = annot_df.iloc[:, 0:4]
new_annot_df.to_csv(r"D:\2022\retreat\retreat_20220222_new.csv", index=False)

