import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/*')
df = pd.DataFrame()

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)    # NaN값 제거
    df_temp.drop_duplicates(inplace=True)   # 중복제거
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
print(df.info())
print(df.titles.value_counts())
df.to_csv('./crawling_data/review_2022.csv', index=False)
