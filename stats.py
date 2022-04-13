import json
import csv
import argparse
import pandas
from scipy import stats

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def convert_to_csv(dataset, file_path):
    """
    Converts a stats json file to a csv, for use with python data science modules.
    Currently records only the weak behavior for each test.
    """
    data_file = open(file_path + ".csv", 'w')
    csv_writer = csv.writer(data_file)
    first = True
    for key in dataset:
        if key != "randomSeed":
            row = []
            if first:
                for testKey in dataset[key]:
                    if testKey == "params":
                        row += dataset[key][testKey].keys()
                    else:
                        row.append(testKey)
                first = False
                csv_writer.writerow(row)
                row = []
            for testKey in dataset[key]:
                if testKey == "params":
                    for param, value in dataset[key][testKey].items():
                        row.append(value)
                else:
                    row.append(dataset[key][testKey]["weak"])
            csv_writer.writerow(row)
    data_file.close()

def analyze(file_path):
    """
    Performs data analysis on a csv file.
    """
    df = pandas.read_csv(file_path + '.csv')
    print(df.describe())
    #print(df.corr())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_path", help="Path to output to analyze")
    args = parser.parse_args()
    dataset = load_stats(args.stats_path)
    file_name = args.stats_path.split("/")[-1].split(".")[0]
    convert_to_csv(dataset, file_name)
    analyze(file_name)

if __name__ == "__main__":
    main()
