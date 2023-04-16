import pandas as pd
import re
import os
import time

# main cli for this data healthcheck repo

def main():
    # Define the dictionary with key-value pairs of functions
    function_map = {
    "help": help,
    "schema": schema_check,
    "health": completeness_check,
    "type-check": data_type_check,
    "start": start,
    "quit": exit
    }    

    # Prompt user to enter keyword
    keyword = input("--Complete--\n\nEnter a command: ")
    
    # Check if keyword exists as a key in function_dict
    if keyword in function_map:
        # If keyword exists, run the corresponding function
        function_map[keyword]()
    else:
        # If keyword doesn't exist, print an error message
        print("Not a command. Returning.")
        main()


def start():
    # Prompt user for input_df URL
    global master_url 
    master_url = input("Please enter the URL for your master dataframe file: ")
    
    global input_url
    input_url = input("Please enter the URL for your input dataframe file: ")

    main()

def schema_check(url_regex_path=None):

    # Check if master_url and input_url are valid URLs
    if url_regex_path is not None and os.path.exists(url_regex_path): 
        with open(url_regex_path, 'r') as f:  
            url_regex = f.read().strip()
    else:  
        url_regex = r"^(http|ftp)s?://"
    
    input_file_extension = input_url.split('.')[-1]

    if input_file_extension in ['xlsx', 'xls']:
        input_df = pd.read_excel(input_url)
    elif input_file_extension == 'csv':
        input_df = pd.read_csv(input_url)
    elif input_file_extension == 'json':
        input_df = pd.read_json(input_url)
    elif input_file_extension == 'sql':
        input_df = pd.read_sql(input_url)
    else:
        raise ValueError("The selected file type is not supported.")
    

    master_file_extension = master_url.split('.')[-1]

    if master_file_extension in ['xlsx', 'xls']:
        master_df = pd.read_excel(master_url)
    elif master_file_extension == 'csv':
        master_df = pd.read_csv(master_url)
    elif master_file_extension == 'json':
        master_df = pd.read_json(master_url)
    elif master_file_extension == 'sql':
        master_df = pd.read_sql(master_url)
    else:
        raise ValueError("The selected file type is not supported.")
    
    if input_df.columns.tolist() == master_df.columns.tolist():
        print("Both dataframes have matching schemas!")
    else:
        input_cols = set(input_df.columns.tolist())
        master_cols = set(master_df.columns.tolist())
        print("Alert: The schemas of the dataframes provided do not match! Aborting...")
        print(f"Columns in input dataframe but not in master dataframe: {input_cols - master_cols}")
        print(f"Columns in master dataframe but not in input dataframe: {master_cols - input_cols}")
        main()
    
    print('Code Run Successfully. Aborting.')
    main()


def data_type_check():
        
    # Read input dataframe and master dataframe from URLs provided by user
    input_df = pd.read_csv(input_url)
    master_df = pd.read_csv(master_url)
    
    # Check if the columns in the input dataframe match with the columns in the master dataframe
    if set(input_df.columns) != set(master_df.columns):
        print("Error: The columns in the input dataframe do not match the columns in the master dataframe.")
        return
    
    # Check if the datatypes of each column in the input dataframe match with the corresponding column in the master dataframe
    for col in input_df.columns:
        if input_df[col].dtype != master_df[col].dtype:
            print(f"Error: The datatype of column {col} does not match between the input dataframe and the master dataframe.")
            return
    
    # If all column datatypes match, print success message
    print("All column datatypes match between the input dataframe and the master dataframe. Returning to main.")
    time.sleep(3)
    main()


def completeness_check():
    print("Succesfully called function.")
    exit()

def help():
    print("help - prints this message\nschema - runs a check that the schema of input dataframe and master dataframe are equivalent\nhealth - runs a check that all cells are not NAN or NULL or NAT in a column of input dataframe")
    print("type-check - checks if data types in each column for master and input dataframe are equivalent\nstart - define a master and input dataframe")
    main()
main()


