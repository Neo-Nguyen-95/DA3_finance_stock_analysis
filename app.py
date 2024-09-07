import streamlit as st
import pandas as pd
from scraping_cafef import FinanceStat
from io import BytesIO

st.title("TẢI CÁC BÁO CÁO TÀI CHÍNH CỦA MỌI CÔNG TY TỪ CAFEF.VN")
company_name = st.sidebar.text_input("Nhập tên viết tắt của công ty: ", value='fpt')
data = FinanceStat(company_name.lower()) 

def download_data(report_name):

    cashflow = data.get_findata(report_name, "traditional")
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        cashflow.to_excel(writer, index=True)
        
    output.seek(0)
    
    st.download_button(
        label="Download data",
        data=output.getvalue(),
        file_name=company_name + "_" + report_name + ".xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("""
            ## Báo cáo dòng tiền - cashflow:
            """)
download_data('cashflow')

st.markdown("""
            ## Bảng cân đối kế toán - balance sheet report:
            """)
download_data('bsheet')

st.markdown("""
            ## Báo cáo doanh thu - income statement:
            """)
download_data('incsta')