import pandas as pd

pd.set_option('display.max_columns', None)

# in the url, year number shown in the final column 
url = 'https://s.cafef.vn/bao-cao-tai-chinh/fpt/cashflow/2023/0/0/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
df = pd.read_html(url)

# construct dataframe from data
df_fin = df[4]
df_fin.columns = df[3].iloc[0].values
df_fin.drop(columns='Tăng trưởng', inplace=True)
df_fin.head()
