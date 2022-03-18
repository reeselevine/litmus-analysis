import json
import csv
import argparse
import pandas
from scipy import stats
import matplotlib.pyplot as plt

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

def analyze(tests, file_path):
    df = pandas.read_csv(file_path.split(".")[0] + '.csv')
    #print(df.describe())
    for test in tests:
        df.hist(column=test)
    #print(df.corr())


def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def get_tests(dataset):
    tests = []
    for key in dataset["0"]:
        if key != "params":
            tests.append(key)
    return tests

def convert_to_csv(dataset, file_path):
    """
    Converts a stats json file to a csv, for use with python data science modules.
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

def per_test(dataset, compare, update):
    """
    General purpose function for calculating some basic statistics per test
    """
    result = {}
    for key in dataset:
        if key != "randomSeed":
            for testKey in dataset[key]:
                if testKey != "params":
                    if testKey not in result:
                        update(result, key, testKey)
                    elif compare(result, key, testKey):
                        update(result, key, testKey)
    return result


def max_per_test(dataset):
    """
    Finds the max number of weak behaviors per test in a test run
    """
    def compare(result, key, testKey):
        return result[testKey][1] < dataset[key][testKey]["weak"]
    def update(result, key, testKey):
        result[testKey] = (key, dataset[key][testKey]["weak"])

    result = per_test(dataset, compare, update)
    print("Max weak behaviors:")
    for key in result:
        print(key + ": " + str(result[key][1]) + " in iteration " + result[key][0])

def harmonic_mean(data):
    if sum(data) == 0:
        return 0
    recips = []
    for v in data:
        if v != 0:
            recips.append(1/v)
    print(recips)
    return round(len(data)/sum(recips), 3)

def max_rate_per_test(dataset):
    """
    Finds the max rate of weak behaviors per test
    """
    def compare(result, key, testKey):
        value = dataset[key][testKey]["weak"]
        time = dataset[key][testKey]["durationSeconds"]
        rate = value/time
        return result[testKey][1] < rate
    def update(result, key, testKey):
        value = dataset[key][testKey]["weak"]
        time = dataset[key][testKey]["durationSeconds"]
        rate = round(value/time, 3)
        result[testKey] = (key, rate)

    result = per_test(dataset, compare, update)
    print("Rate of weak behaviors:")
    #print("[", end='')
    maxed = 0
    weak = []
    weak_caught = 0
    co_weak = []
    co_weak_caught = 0
    co = []
    co_caught = 0
    for key in result:
        #print("{}, ".format(result[key][1]), end='')
        if "Mutations" in key:
            co.append(result[key][1])
            if result[key][1] > 0:
                co_caught += 1
        elif "Coherency" in key:
            co_weak.append(result[key][1])
            if result[key][1] > 0:
                co_weak_caught += 1
        else:
            weak.append(result[key][1])
            if result[key][1] > 0:
                weak_caught += 1
        print(key + ": " + str(result[key][1]) + " weak behaviors per second in iteration " + result[key][0])
        if result[key][1] >= 6.4:
            maxed += 1
    #print("]")
    all_tests = weak + co_weak + co
    print("Weak Mean: {}, Caught: {}".format(round(sum(weak)/len(weak), 3), weak_caught))
    print("Coherence Weak Mean: {}, Caught: {}".format(round(sum(co_weak)/len(co_weak), 3), co_weak_caught))
    print("Coherence Mean: {}, Caught: {}".format(round(sum(co)/len(co), 3), co_caught))
    print("All Mean: {}, Caught: {}".format(round(sum(all_tests)/len(all_tests), 3), weak_caught + co_weak_caught + co_caught))
    print("Reproducible tests: {}".format(maxed))
    print(all_tests)

def total_time(dataset):
    total = 0
    for key in dataset:
        if key != "randomSeed":
            for test in dataset[key]:
                if test != "params":
                    total += dataset[key][test]["durationSeconds"]
    print("Time spent tuning: {} seconds".format(total))

def checksum(dataset, is_si, i):
    matched = True
    for key in dataset:
        if key != "randomSeed":
            w = dataset[key]["params"]["testingWorkgroups"]
            for test in dataset[key]:
                if test != "params":
                    total = dataset[key][test]["seq"] + dataset[key][test]["interleaved"] + dataset[key][test]["weak"]
                    if is_si:
                        expected = i
                    else:
                        expected = w * i * 256;
                    if total != expected:
                        print("Checksum did not match! Iteration: {}, Test: {}, Expected: {}, Actual: {}".format(key, test, expected, total))
                        matched = False
    if matched:
        print("Checksum matched!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_path", help="Path to output to analyze")
    parser.add_argument("--action", default="rate", help="Analysis to perform. Options are 'sum', 'rate', 'time', 'checksum'")
    parser.add_argument("--iterations", default="100", help="Number of iterations to compute checksum against")
    parser.add_argument('--si', action='store_true', help="When computing checksum, signifies this was a single instance run, not parallel")
    args = parser.parse_args()
    dataset = load_stats(args.stats_path)
    if args.action == "sum":
        max_per_test(dataset)
    elif args.action == "rate":
        max_rate_per_test(dataset)
    elif args.action == "time":
        total_time(dataset)
    elif args.action == "checksum":
        checksum(dataset, args.si, int(args.iterations))

if __name__ == "__main__":
    main()
