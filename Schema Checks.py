import pandas as pd
import re
import os

# main cli for this data healthcheck repo

def main():
    # Define the dictionary with key-value pairs of functions
    function_map = {
    "help": help,
    "schema": schema_check,
    "health": health_check,
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

def schema_check(url_regex_path=None):
    start()
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


def health_check():
    pass

def completeness_check():
    
    exit()

def help():
    exit()

main()

# create a dictionary mapping keywords to functions
