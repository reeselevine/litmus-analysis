import json
import argparse
import math
from os import listdir

class RateSumResult:

    def __init__(self, rate_sum, min_rate):
        self.rate_sum = rate_sum
        self.min_rate = min_rate

    def __str__(self):
        return "Rate Sum: {}, Min Rate: {}".format(self.rate_sum, self.min_rate)

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
    maximized = 0
    maximized_tests = dict()
    min_rates = []
    for stats in all_stats:
        maximized_tests[stats[0]] = 0
    for res in tests.items():
        min_rates.append(res[1][1].min_rate)
        maxed_rates = 0
        print("{}: {} in iteration {}".format(res[0], str(res[1][1]), res[1][0]))
        print ("  Details:")
        for stats in all_stats:
            if calculate_rate(stats, res[1][0], res[0]) >= 6.4:
                maximized_tests[stats[0]] = maximized_tests[stats[0]] + 1
                maxed_rates += 1
            print("    {}: {}".format(stats[0], stats[1][res[1][0]][res[0]]))
        if maxed_rates == len(all_stats):
            maximized += 1
        print()
    print("Maximized: {}".format(maximized))
    print(maximized_tests)
    print(min_rates)

def compare_greater_than(a, b):
    return a >= b

def compare_rate_sum(cur, best):
    if cur.rate_sum == best.rate_sum:
        return cur.min_rate >= best.min_rate
    else:
        return cur.rate_sum > best.rate_sum

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
    def max_rate(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += rate
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    def compare(cur, best):
        if cur.rate_sum == best.rate_sum:
            return cur.min_rate >= best.min_rate
        else:
            return cur.rate_sum > best.rate_sum

    analyze_combined(all_stats, "rate", max_rate, compare_rate_sum, RateSumResult(0, 0))

def max_log_rate(all_stats):
    def max_log(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(rate + 1)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_combined(all_stats, "log rate", max_log, compare_rate_sum, RateSumResult(0, 0))

def max_ceiling_log_rate(all_stats):
    def max_log_ceiling(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(min(rate, 6.4) + 1)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_combined(all_stats, "ceiling log rate", max_log_ceiling, compare_rate_sum, RateSumResult(0, 0))

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
