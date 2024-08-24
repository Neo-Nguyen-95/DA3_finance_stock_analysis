#%% LOAD DATA
import pandas as pd
pd.set_option('display.max_columns', None)

from data_processing.cafef_scraping import FinanceStat

pnj_data = FinanceStat('pnj')

pnj_income = pnj_data.get_findata(report_type='incsta')
pnj_income.columns

