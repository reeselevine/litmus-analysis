import json
import argparse
import math
from os import listdir

class LogSumRateResult:

    def __init__(self, log_sum_rate, min_rate):
        self.log_sum_rate = log_sum_rate
        self.min_rate = min_rate

    def __str__(self):
        return "Log Sum Rate: {}, Min Rate: {}".format(self.log_sum_rate, self.min_rate)

def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def analyze_combined(all_stats, to_max, calculate, compare, initial_best=0):
    tests = {}
    for key in all_stats[0][1]["0"]:
        if key != "params":
            tests[key] = (None, initial_best)
    for key in all_stats[0][1]:
        if key != "randomSeed":
            for testKey in tests.keys():
                result = calculate(all_stats, key, testKey)
                if compare(result, tests[testKey][1]):
                    tests[testKey] = (key, result)
    print("Maximizing {} of weak behaviors".format(to_max))
    for res in tests.items():
        print("{}: {} in iteration {}".format(res[0], str(res[1][1]), res[1][0]))
        print ("  Details:")
        for stats in all_stats:
            print("    {}: {}".format(stats[0], stats[1][res[1][0]][res[0]]))
        print()

def compare_greater_than(a, b):
    return a >= b

def maximize_sum(calculate):
    def func(all_stats, key, testKey):
        result = 0
        for stats in all_stats:
            result += calculate(stats, key, testKey)
        return result
    return func

def maximize_min(calculate):
    def func(all_stats, key, testKey):
        result = None
        for stats in all_stats:
            cur = calculate(stats, key, testKey)
            if result == None or cur < result:
                result = cur
        return result
    return func

def calculate_total(stats, key, testKey):
    value = stats[1][key][testKey]["weak"]
    return value

def calculate_rate(stats, key, testKey):
    value = stats[1][key][testKey]["weak"]
    time = stats[1][key][testKey]["durationSeconds"]
    rate = round(value/time, 3)
    return rate

def max_sum(all_stats):
    analyze_combined(all_stats, "sum", maximize_sum(calculate_total), compare_greater_than)

def max_log_sum(all_stats):
    def calculate(stats, key, testKey):
        return math.log(calculate_total(stats, key, testKey) + 1, 2)
    analyze_combined(all_stats, "log sum", maximize_sum(calculate), compare_greater_than)

def max_rate(all_stats):
    analyze_combined(all_stats, "rate", maximize_sum(calculate_rate), compare_greater_than)

def max_log_rate(all_stats):
    def max_log(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(rate + 1, 2)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return LogSumRateResult(rate_sum, min_rate)

    def compare(cur, best):
        if cur.log_sum_rate == best.log_sum_rate:
            return cur.min_rate >= best.min_rate
        else:
            return cur.log_sum_rate > best.log_sum_rate

    analyze_combined(all_stats, "log rate", max_log, compare, LogSumRateResult(0, 0))

def max_ceiling_log_rate(all_stats):
    def max_log_ceiling(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(min(rate, 6.4) + 1, 2)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return LogSumRateResult(rate_sum, min_rate)

    def compare(cur, best):
        if cur.log_sum_rate == best.log_sum_rate:
            return cur.min_rate >= best.min_rate
        else:
            return cur.log_sum_rate > best.log_sum_rate

    analyze_combined(all_stats, "ceiling log rate", max_log_ceiling, compare, LogSumRateResult(0, 0))

def max_tanh_rate(all_stats):
    def calculate(stats, key, testKey):
        return math.tanh(calculate_rate(stats, key, testKey))
    analyze_combined(all_stats, "tanh rate", maximize_sum(calculate), compare_greater_than)

def max_min_rate(all_stats):
    analyze_combined(all_stats, "max min rate", maximize_min(calculate_rate), compare_greater_than)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_dir", help="Directory of stats files to combine")
    parser.add_argument("--action", default="log-rate", help="Analysis to perform. Options are 'sum', 'rate', 'log-sum', 'log-rate', 'tanh-rate', 'min-rate', 'ceiling-log-rate'")
    args = parser.parse_args()
    all_stats = []
    for stats_file in listdir(args.stats_dir):
        all_stats.append((stats_file.split(".")[0], load_stats(args.stats_dir + "/" + stats_file)))
    if args.action == "sum":
        max_sum(all_stats)
    elif args.action == "log-sum":
        max_log_sum(all_stats)
    elif args.action == "rate":
        max_rate(all_stats)
    elif args.action == "log-rate":
        max_log_rate(all_stats)
    elif args.action == "tanh-rate":
        max_tanh_rate(all_stats)
    elif args.action == "min-rate":
        max_min_rate(all_stats)
    elif args.action == "ceiling-log-rate":
        max_ceiling_log_rate(all_stats)

if __name__ == "__main__":
    main()
