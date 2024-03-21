#Rollback_Query_Generator
#Drawback_Empty_Strings_are_considered_as_NULL


import pandas as pd
import numpy as np

def generate_update_queries(file_path, table_name, id_column, update_columns):
    # Read Excel data into a DataFrame, specifying header=0
    df = pd.read_excel(file_path, header=0)

    # Print actual DataFrame columns for debugging
    print("Actual DataFrame Columns:", df.columns.tolist())

    # Ensure that all update columns exist in the DataFrame
    missing_columns = [col for col in update_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Columns not found in the Excel file: {missing_columns}")

    # Generate SQL UPDATE statements
    update_queries = []
    for index, row in df.iterrows():
        update_query = f"UPDATE {table_name} SET "
        set_clauses = []
        for column in update_columns:
            # Check for NULL or empty values
            if pd.isnull(row[column]):
                set_clause = f"{column} = NULL"
            elif row[column] == '':
                set_clause = f"{column} = ''"
            else:
                # Check data type of the column
                if isinstance(row[column], str) or isinstance(row[column], pd.Timestamp):
                    set_clause = f"{column} = '{row[column]}'"
                elif isinstance(row[column], int) or isinstance(row[column], float):
                    # Remove decimal points from numeric values
                    set_clause = f"{column} = '{int(row[column])}'"
                else:
                    set_clause = f"{column} = {row[column]}"
            set_clauses.append(set_clause)
        update_query += ', '.join(set_clauses)
        update_query += f" WHERE {id_column} = {row[id_column]};"
        update_queries.append(update_query)

    return update_queries

if __name__ == "__main__":
    # Replace with your actual table name, ID column, and update columns
    table_name = 'UPI_TRANSACTION_DETAILS_TBL'
    id_column = 'PINE_PG_TRANSACTION_ID'
    update_columns = ['STATUS_CODE_RECEIVED_FROM_HOST','RESPONSE_CODE_RECEIVED_FROM_HOST','APPROVAL_CODE_RECEIVED_FROM_HOST','CUSTOMER_REF_NO','IS_FINAL_RESPONSE_RECEIVED','ROW_UPDATION_DATETIME']

    # Replace the file path with the actual path to your Excel file
    excel_file_path = '/Users/suryaprakashpalanisamy/Desktop/Rollback_Qeury/Rollback_UPI TRans DTL.xlsx'

    try:
        # Generate update queries
        queries = generate_update_queries(excel_file_path, table_name, id_column, update_columns)

        # Save queries to a .sql file in the same path as the Excel file
        sql_file_path = excel_file_path.replace('.xlsx', '_update_queries.sql')
        with open(sql_file_path, 'w') as sql_file:
            for query in queries:
                sql_file.write(query + '\n')

        print(f"Update queries saved to {sql_file_path}")

    except ValueError as ve:
        print(f"Error: {ve}")
