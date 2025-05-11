import pandas as pd
from typing import Dict, List

def excel_to_dict_list(filename: str) -> List[Dict]:
    dataframe = pd.read_excel(filename)
    
    #orient="records" to use column names as keys
    dataframe_dict = dataframe.to_dict(orient="records")
    return dataframe_dict
