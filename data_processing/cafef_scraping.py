#%% IMPORT LIBRARY
import pandas as pd
import datetime

pd.set_option('display.max_columns', None)

#%% CLASS
class FinanceStat:
    """The model scapes cafef.vn to get 3 finanicial statement about a company.
    Params:
        company_name: name on stock market
    
    Function:
        self.get_findata(report_type):
            get finance data according to the report
        self.export_findata(form='csv'):
            export data to csv or xlsx format
    """
    
    # input
    def __init__(self, company_name='fpt'):
        self.company_name = company_name
        # internal variable
        self.year_1st = 2000
        self.year_final = datetime.datetime.now().year
    
    def get_category(self, report_type):
        url = ('https://s.cafef.vn/bao-cao-tai-chinh/' 
               + self.company_name + '/' 
               + report_type + '/' 
               + '2024' + 
               '/0/0/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
               )  # pick a random year to get category
        df = pd.read_html(url)
        df_temp = df[4]
        df_category = df_temp.iloc[:, 0]
        return df_category
        
    
    def get_stat(self, report_type):
        
        year_list = range(self.year_1st, self.year_final+1)
        
        result = pd.DataFrame(columns = year_list)
        
        for year in year_list:
            url = ('https://s.cafef.vn/bao-cao-tai-chinh/' 
                    + self.company_name + '/' 
                    + report_type + '/' 
                    + str(year) + 
                    '/0/0/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
                    )
            
            web_data = pd.read_html(url)

            # construct dataframe from data         
            result[year] = web_data[4].iloc[:, 4]
            
        
            # check if data available or not
            if result[year].isna().sum() == len(result):
                result.drop(columns=year, inplace=True)
        
        return result
    
    def get_findata(self, report_type):
        """report_type in ['cashflow', 'incsta', 'bsheet']
        """
        result = pd.concat([self.get_category(report_type),
                          self.get_stat(report_type)],
                         axis='columns')
        result.set_index(0, inplace=True)
        return result.T
    
    def export_findata(self, form = 'csv'):
        # export all report data
        for report_type in ['cashflow', 'incsta', 'bsheet']:
            file_name = self.company_name + '_' + report_type
            if form == 'csv':
                self.get_findata(report_type).to_csv(file_name + '.csv')
            else:
                self.get_findata(report_type).to_excel(file_name + '.xlsx')
        
#%% TEST_SITE
# model = FinanceStat()
# print(model.get_findata('cashflow').head())
