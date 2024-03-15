import os
import re
import pandas as pd
from itertools import islice

class MicaDictionary:
    def __init__(self):
        """
        Class initialization.

        @return None
        """
        self.mica_columns = ["table", "name", "valueType", "unit", "annotations", "label:en", "label:es"]
        
    def table_column(self, df, table):
        # Remove initial index from the table name
        table_name = re.sub(r'\d+_','', table)
        table_name = re.sub(r'.csv','', table_name)
        df.loc[:,"Table"] = table_name
            
        # Rename the column
        df.rename(columns={"Table":"table"}, inplace = True)

        return df, table_name
    
    def name_column(self, df):
        # Rename the column
        df.rename(columns={"Field":"name"}, inplace = True)

        return df
    
    def valuetype_column(self, df):
        """
        mica_options = ["integer", "decimal", "text", "binary", "locale","boolean","datetime","date"]
        """
        #scanreport_options = df["Type"].unique()
        #print(scanreport_options)
        type_replacement = {"VARCHAR":"text", "INT":"integer", "DATE":"date","REAL":"", "EMPTY":""}
        df["Type"] = df["Type"].replace(type_replacement)

        # Rename the column
        df.rename(columns={"Type":"valueType"}, inplace = True)

        return df

    def create_variable_sheet(self, df, table):
        # Table column
        df, table_name = self.table_column(df, table)
        
        # Name column
        df = self.name_column(df)

        # ValueType column
        df = self.valuetype_column(df)

        # Remove some columns from Scan Report
        columns_to_remove = ["Description","Max length","N rows","N rows checked","Fraction empty",
                                "N unique values","Fraction unique"]
        
        df = df.drop(columns=columns_to_remove)

        # Final dictionary
        new_columns = [col for col in self.mica_columns if col not in df.columns]
        empty_df = pd.DataFrame(columns=new_columns)

        df_variables = pd.concat([df, empty_df], axis=1)
         
        return df_variables, table_name
  
    def create_category_sheet(self, df, sheet_name):
        # CATEGORY SHEET
        df_category = pd.DataFrame(columns=["table", "variable", "name", "missing", "label:en", "label:es"])
        
        for i in range(0, len(df.columns), 2):
            variable_column = df.columns[i]
            values_variable = df[variable_column].dropna()

            for value in values_variable:
                new_row = {
                    "table":sheet_name, 
                    "variable": variable_column, 
                    "name": value, 
                    "missing": 0, 
                    "label:en": value, 
                    "label:es":None,
                }
                new_df = pd.DataFrame(new_row, index=[0])
                df_category = pd.concat([df_category, new_df], ignore_index=True)
    
        return df_category
    
    def run(self, scan_report):
        # Get the information
        sheet_dict = pd.read_excel(scan_report, sheet_name=None)
        #sheet_names = list(sheet_dict.keys())
        
        sheets_iterator = islice(sheet_dict.items(), None, None)
        table_name_list = []
        count = 0
        dataframes_list = []
        for sheet_name, df in sheets_iterator:
            if sheet_name == "Field Overview":
                tables = (df["Table"].dropna()).unique()
                for table in tables:
                    mica_dict = df[df["Table"] == table]
                    mica_dict.reset_index(drop=True, inplace=True)

                    df_variables, table_name = self.create_variable_sheet(mica_dict, table)
                    table_name_list.append(table_name)
                    dataframes_list.append(df_variables)

            elif sheet_name == "Table Overview":
                pass

            elif sheet_name == "_":
                pass
            
            else:
                df_category = self.create_category_sheet(df, table_name_list[count])
                
                # Save to excel
                file_name = table_name_list[count] + '.xlsx'
                df_variables = dataframes_list[count]

                with pd.ExcelWriter(file_name) as writer:
                    df_variables.to_excel(writer, sheet_name='Variables', index=False)
                    df_category.to_excel(writer, sheet_name='Categories', index=False)
                
                count = count + 1
                

if __name__ == '__main__':
    path = r'/home/.../' # Change the path
    scan_report = os.path.join(path, "ScanReport_....xlsx") # Change the file name
    mica = MicaDictionary()
    mica.run(scan_report)