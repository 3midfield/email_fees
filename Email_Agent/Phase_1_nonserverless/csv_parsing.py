import pandas as pd

def csv_parsing(csv, output):
    df = pd.read_csv(csv)
    new_df = df.iloc[:, [0,2,6,7,8,26,27,42]]
    return new_df.to_csv(output, index=False)
    

csv_parsing("all_data.csv", "organized.csv")