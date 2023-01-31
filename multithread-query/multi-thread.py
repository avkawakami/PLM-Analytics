#Multi thread to query an API from a list of items

import requests
import pandas as pd
import concurrent.futures

def query_api(pn):
    url = f"https://api.testaaa.com/{pn}"
    #response = requests.get(url)
    print ("API runned")
    return pn, response.json()

def multi_threaded_query(df, column_name):
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_pn = {executor.submit(query_api, pn): pn for pn in df[column_name]}
        for future in concurrent.futures.as_completed(future_to_pn):
            pn = future_to_pn[future]
            try:
                result.append((pn, future.result()))
            except Exception as e:
                print(f"Query for {pn} generated an exception: {e}")
    return result

def combine_results_with_column(df, column_name, results):
    return pd.DataFrame({"part_number": [pn for pn, _ in results], column_name: [res for _, res in results]})

def read_part_numbers_from_file(file_path):
    with open(file_path, 'r') as f:
        part_numbers = f.readlines()
    return pd.DataFrame({"part_number": [pn.strip() for pn in part_numbers]})

# Example usage:
file_path = "part_numbers.txt"
df = read_part_numbers_from_file(file_path)
api_results = multi_threaded_query(df, "part_number")
result_df = combine_results_with_column(df, "api_response", api_results)
print(result_df)
