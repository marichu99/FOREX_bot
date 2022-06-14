import pandas as pd
import os


def matched():
    # dictionary to match values in the dataframe
    dict_d={}
    # read the csv file
    sources= pd.read_csv("matched_data.csv")
    # create a dataframe from the csv file
    print(f"The number od CPUS are {os.cpu_count()}")
    df=pd.DataFrame(data=sources,columns=["source_1","source_2"])
    # check which column is longer for comparison
    if df["source_1"].size() > df["source_2"].size() or df["source_2"]>df["source_1"]:
        for index, rows in df.iterrows():
            a=rows["source_1"]
            b=rows["source_2"]
            # compare the elements of each row in the data frame
            if a==b:
                # match the values in the dict_d dictionary
                print("A match has been found")
                # append to the empty dictionary as a form of matching them up together
                dict_d[a].append(b)
            else:
                print("A match was not found")
                continue
#  call the method
matched()
            
   