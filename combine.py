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

class MaxTestsResult:

    def __init__(self, rep_tests, log_of_rest):
        self.rep_tests = rep_tests
        self.log_of_rest = log_of_rest


    def __str__(self):
        return "Reproducible Tests: {}, Log Sum of Rest: {}".format(self.rep_tests, self.log_of_rest)

def compare_max_tests_results(cur, best):
        if cur.rep_tests == best.rep_tests:
            return cur.log_of_rest > best.log_of_rest
        else:
            return cur.rep_tests > best.rep_tests

def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def analyze_global(all_stats, to_max, calculate, compare, initial_best, ceiling_rate):
    testKeys = []
    best = initial_best
    best_iter = None
    for key in all_stats[0][1]["0"]:
        if key != "params":
            testKeys.append(key)
    for iteration in all_stats[0][1]:
        if iteration != "randomSeed":
            result = calculate(all_stats, iteration,  testKeys)
            if compare(result, best):
                best = result
                best_iter = iteration
    print("Maximizing {} of weak behaviors".format(to_max))
    maximized = 0
    maximized_tests = dict()
    total_maxed = 0
    rates = []
    log_rates = []
    for stats in all_stats:
        maximized_tests[stats[0]] = 0
    for test in testKeys:
        maxed_rates = 0
        for stats in all_stats:
            rate = calculate_rate(stats, best_iter, test)
            if rate >= ceiling_rate:
                maximized_tests[stats[0]] = maximized_tests[stats[0]] + 1
                maxed_rates += 1
                total_maxed += 1
        if maxed_rates == len(all_stats):
            maximized += 1
    print(maximized_tests)
    print("Best: {} in iteration {}".format(best, best_iter))
    print("Number of Tests Reproducible on All Devices: {}".format(maximized))
    print("Number of Tests Reproducible: {}".format(total_maxed))


def analyze_combined(all_stats, to_max, calculate, compare, initial_best, ceiling_rate):
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
    total_maxed = 0
    for stats in all_stats:
        maximized_tests[stats[0]] = 0
    for res in tests.items():
        maxed_rates = 0
        #print("{}: {} in iteration {}".format(res[0], str(res[1][1]), res[1][0]))
        #print ("  Details:")
        for stats in all_stats:
            if calculate_rate(stats, res[1][0], res[0]) >= ceiling_rate:
                maximized_tests[stats[0]] = maximized_tests[stats[0]] + 1
                maxed_rates += 1
                total_maxed += 1
            #print("    {}: {}".format(stats[0], stats[1][res[1][0]][res[0]]))
        if maxed_rates == len(all_stats):
            maximized += 1
        #print()
    print("Number of Tests Reproducible on All Devices: {}".format(maximized))
    print("Number of Tests Reproducible: {}".format(total_maxed))
    print(maximized_tests)


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

def max_rate(all_stats, ceiling_rate):
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

    analyze_combined(all_stats, "rate", max_rate, compare_rate_sum, RateSumResult(0, 0), ceiling_rate)

def max_log_rate(all_stats, ceiling_rate):
    def max_log(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(rate + 1)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_combined(all_stats, "log rate", max_log, compare_rate_sum, RateSumResult(0, 0), ceiling_rate)

def max_ceiling_rate(all_stats, ceiling_rate):
    def max_ceiling(all_stats, key, testKey):
        result = MaxTestsResult(0, 0)
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            if rate >= ceiling_rate:
                result.rep_tests += 1
            else:
                result.log_of_rest += math.log(rate + 1)
        return result

    analyze_combined(all_stats, "ceiling rate", max_ceiling, compare_max_tests_results, MaxTestsResult(0, 0), ceiling_rate)


def max_ceiling_log_rate(all_stats, ceiling_rate):
    def max_log_ceiling(all_stats, key, testKey):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            rate_sum += math.log(min(rate, ceiling_rate) + 1)
            if min_rate == None or rate < min_rate:
                min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_combined(all_stats, "ceiling log rate", max_log_ceiling, compare_rate_sum, RateSumResult(0, 0), ceiling_rate)


def max_global_ceiling_rate(all_stats, ceiling_rate):
    def max_ceiling(all_stats, key, testKeys):
        result = MaxTestsResult(0, 0)
        for stats in all_stats:
            for testKey in testKeys:
                rate = calculate_rate(stats, key, testKey)
                if rate >= ceiling_rate:
                    result.rep_tests += 1
                else:
                    result.log_of_rest += math.log(rate + 1)
        return result

    analyze_global(all_stats, "global ceiling rate", max_ceiling, compare_max_tests_results, MaxTestsResult(0, 0), ceiling_rate)

def max_global_log_rate(all_stats, ceiling_rate):
    def max_log_ceiling(all_stats, key, testKeys):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            for testKey in testKeys:
                rate = calculate_rate(stats, key, testKey)
                rate_sum += math.log(rate + 1)
                if min_rate == None or rate < min_rate:
                    min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_global(all_stats, "global log rate", max_log_ceiling, compare_rate_sum, RateSumResult(0, 0), ceiling_rate)

def max_global_ceiling_log_rate(all_stats, ceiling_rate):
    def max_log_ceiling(all_stats, key, testKeys):
        rate_sum = 0
        min_rate = None
        for stats in all_stats:
            for testKey in testKeys:
                rate = calculate_rate(stats, key, testKey)
                rate_sum += math.log(min(rate, ceiling_rate) + 1)
                if min_rate == None or rate < min_rate:
                    min_rate = rate
        return RateSumResult(rate_sum, min_rate)

    analyze_global(all_stats, "global ceiling log rate", max_log_ceiling, compare_rate_sum, RateSumResult(0, 0), ceiling_rate)


def get_ceiling_rate(reproducibility, time_budget):
    num_weak_behaviors = math.ceil(-math.log(1 - reproducibility))
    return num_weak_behaviors/time_budget

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_dir", help="Directory of stats files to combine")
    parser.add_argument("--action", default="log-rate", help="Analysis to perform. Options are 'rate', 'log-rate', 'ceiling-log-rate', 'ceiling-rate', 'global-log-rate' , 'global-ceiling-log-rate', 'global-ceiling-rate'")
    parser.add_argument("--rep", default="99.999", help="Level of reproducibility.")
    parser.add_argument("--budget", default="3", help="Time budget per test (seconds)")
    args = parser.parse_args()
    all_stats = []
    for stats_file in listdir(args.stats_dir):
        all_stats.append((stats_file.split(".")[0], load_stats(args.stats_dir + "/" + stats_file)))
    ceiling_rate = get_ceiling_rate(float(args.rep)/100, float(args.budget))
    if args.action == "rate":
        max_rate(all_stats, ceiling_rate)
    elif args.action == "log-rate":
        max_log_rate(all_stats, ceiling_rate)
    elif args.action == "ceiling-log-rate":
        max_ceiling_log_rate(all_stats, ceiling_rate)
    elif args.action == "global-log-rate":
        max_global_log_rate(all_stats, ceiling_rate)
    elif args.action == "global-ceiling-log-rate":
        max_global_ceiling_log_rate(all_stats, ceiling_rate)
    elif args.action == "global-ceiling-rate":
        max_global_ceiling_rate(all_stats, ceiling_rate)
    elif args.action == "ceiling-rate":
        max_ceiling_rate(all_stats, ceiling_rate)

if __name__ == "__main__":
    main()
