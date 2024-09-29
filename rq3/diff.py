import pandas as pd

df1 = pd.read_csv('./validation_pmd.csv')
df1 = df1[df1['Resolved Final Type'] == 'not obsolete']
print("Validation Rows: ", df1.shape[0])

df2 = pd.read_csv('./coverage_pmd.csv')
print("Coverage Rows:", df2.shape[0])



for index, row in df1.iterrows():
    temp_mask = (df2['Hash'] == row['Hash']) & (df2['Filepath'] == row['Filepath']) & (df2['Removed Test Case'] == row['Removed Test Case'])
    
    df = df2[temp_mask]
    
    if df.shape[0] == 0:
        print(row['Hash'], row['Removed Test Case'])
    
        
print("####################")
for index, row in df2.iterrows():
    temp_mask = (df1['Hash'] == row['Hash']) & (df1['Filepath'] == row['Filepath']) & (df1['Removed Test Case'] == row['Removed Test Case'])
    df = df1[temp_mask]
    
    if df.shape[0]== 0:
        print(row['Hash'], row['Removed Test Case'])