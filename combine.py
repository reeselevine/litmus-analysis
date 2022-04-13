import json
import argparse
import math
import statistics
from os import listdir

class RateSumResult:

    def __init__(self, rate_sum, min_rate):
        self.rate_sum = rate_sum
        self.min_rate = min_rate

    def __str__(self):
        return "Rate Sum: {}, Min Rate: {}".format(self.rate_sum, self.min_rate)

class MaxTestsResult:

    def __init__(self, rep_tests, min_rate):
        self.rep_tests = rep_tests
        self.min_rate = min_rate


    def __str__(self):
        return "Reproducible Tests: {}, Min Rate: {}".format(self.rep_tests, self.min_rate)

def compare_max_tests_results(cur, best):
        if cur.rep_tests == best.rep_tests:
            return cur.min_rate > best.min_rate
        else:
            return cur.rep_tests > best.rep_tests

def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def get_range(data):
    minimum = None
    maximum = None
    for value in data:
        if minimum == None or value < minimum:
            minimum = value
        if maximum == None or value > maximum:
            maximum = value
    return (minimum, maximum)

def get_average(data):
    return round(sum(data)/len(data))

def get_median(data):
    return round(statistics.median(data))

def merge(all_stats):
    best_envs = []
    for dataset in all_stats:
        res = dict()
        for key in dataset[1]:
            if key != "randomSeed":
                for testKey in dataset[1][key]:
                    if testKey != "params":
                        value = dataset[1][key][testKey]["weak"]
                        time = dataset[1][key][testKey]["durationSeconds"]
                        rate = round(value/time, 3)
                        if testKey not in res:
                            res[testKey] = (key, rate)
                        elif res[testKey][1] < rate:
                            res[testKey] = (key, rate)
        best_envs.append(res)
    all_params = dict()
    for i in range(len(best_envs)):
        stats = all_stats[i][1]
        envs = best_envs[i]
        for test in envs.keys():
            (i, rate) = envs[test]
            if rate > 0:
                for key in stats[i]["params"]:
                    if key not in all_params:
                        all_params[key] = [stats[i]["params"][key]]
                    else:
                        all_params[key].append(stats[i]["params"][key])
    merged_params = dict()
    keys_to_average = ["shufflePct", "barrierPct", "memStressPct", "preStressPct", "memStride", "stressLineSize", "memStressIterations", "preStressIterations", "stressStrategyBalancePct", "memStressStoreFirstPct", "memStressStoreSecondPct", "preStressStoreFirstPct", "preStressStoreSecondPct", "stressTargetLines", "maxWorkgroups", "testingWorkgroups"]
    for key in keys_to_average:
        merged_params[key] = get_average(all_params[key])
    merged_params["minTestingWorkgroups"] = merged_params["testingWorkgroups"]
    merged_params["minStressTargetLines"] = merged_params["stressTargetLines"]
    merged_params["scratchMemorySize"] = 32 * merged_params["stressTargetLines"] * merged_params["stressLineSize"]
    with open('merged_params.json', 'w') as f:
        json.dump(merged_params, f, indent=4)

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
    rates = dict()
    log_rates = []
    for stats in all_stats:
        maximized_tests[stats[0]] = 0
        rates[stats[0]] = []
    for test in testKeys:
        maxed_rates = 0
        for stats in all_stats:
            rate = calculate_rate(stats, best_iter, test)
            rates[stats[0]].append(rate)
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
    for stats in all_stats:
        print("Average rate for {}: {}".format(stats[0], round(sum(rates[stats[0]])/len(rates[stats[0]]), 3)))

def analyze_combined(all_stats, to_max, calculate, compare, initial_best, ceiling_rate):
    tests = {}
    min_rate = 100000000
    total_ti = 0
    total_time = 0
    for key in all_stats[0][1]["0"]:
        if key != "params":
            tests[key] = ('0', initial_best)
    for key in all_stats[0][1]:
        if key != "randomSeed":
            for testKey in tests.keys():
                for stats in all_stats:
                    total_ti += stats[1][key][testKey]["seq"] + stats[1][key][testKey]["interleaved"] + stats[1][key][testKey]["weak"]
                    total_time += stats[1][key][testKey]["durationSeconds"]
                    rate = stats[1][key][testKey]["weak"] / stats[1][key][testKey]["durationSeconds"]
                    if rate > 0 and rate < min_rate:
                        min_rate = rate
                result = calculate(all_stats, key, testKey)
                if compare(result, tests[testKey][1]):
                    tests[testKey] = (key, result)
    print("Average rate across tuning: {}, total time tuning: {}".format(total_ti/total_time, total_time))
    print("Average number of instances per iteration: {}".format(total_ti/1920000))
    print("Maximizing {} of weak behaviors".format(to_max))
    print("Ceiling rate: {}".format(ceiling_rate))
    maximized = 0
    maximized_tests = dict()
    total_maxed = 0
    total_ti = 0
    total_time = 0
    ratios = dict()
    for stats in all_stats:
        maximized_tests[stats[0]] = 0
        ratios[stats[0]] = dict()
    for res in tests.items():
        maxed_rates = 0
        for stats in all_stats:
            ratios[stats[0]][res[0]] = (res[1][0], stats[1][res[1][0]][res[0]])
            total_ti += stats[1][res[1][0]][res[0]]["seq"] + stats[1][res[1][0]][res[0]]["interleaved"] + stats[1][res[1][0]][res[0]]["weak"]
            total_time += stats[1][res[1][0]][res[0]]["durationSeconds"]
            rate = calculate_rate(stats, res[1][0], res[0])
            print("Rate for {} on {} in iteration {}: {}".format(res[0], stats[0], res[1][0], rate))
            if calculate_rate(stats, res[1][0], res[0]) >= ceiling_rate:
                maximized_tests[stats[0]] = maximized_tests[stats[0]] + 1
                maxed_rates += 1
                total_maxed += 1
        if maxed_rates == len(all_stats):
           maximized += 1
    print("Max Time To See One: {}".format(1/min_rate))
    print("Number of Tests Reproducible on All Devices: {}".format(maximized))
    print("Number of Tests Reproducible: {}".format(total_maxed))
    print("Averaged instance rate for best strategy: {}".format(round(total_ti/total_time), 3))
    print(maximized_tests)
    with open("rates.json", "w") as f:
        json.dump(ratios, f, indent=4)
    return maximized_tests


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

def calculate_test_instance_rate(stats, key, testKey):
    total_instances = stats[1][key][testKey]["seq"] + stats[1][key][testKey]["interleaved"] + stats[1][key][testKey]["weak"]
    time = stats[1][key][testKey]["durationSeconds"]
    return round(total_instances/time, 3)


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
        result = MaxTestsResult(0, 0)
        rate_sum = 0
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            result.log_of_rest += math.log(rate + 1)
            if rate > 0:
                result.rep_tests += 1
        return result

    analyze_combined(all_stats, "log rate", max_log, compare_max_tests_results, MaxTestsResult(0, 0), ceiling_rate)

def max_ceiling_rate(all_stats, ceiling_rate):
    def max_ceiling(all_stats, key, testKey):
        result = MaxTestsResult(0, 10000000000)
        for stats in all_stats:
            rate = calculate_rate(stats, key, testKey)
            if rate >= ceiling_rate:
                result.rep_tests += 1
            if rate > 0:
                result.min_rate = min(result.min_rate, rate)
        return result

    return analyze_combined(all_stats, "ceiling rate", max_ceiling, compare_max_tests_results, MaxTestsResult(0, 10000000000), ceiling_rate)

def max_ceiling_rate_all(all_stats, rep):
    budgets = [1/1024, 1/512, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16, 32, 64, 128]
    total_res = dict()
    total_res["all"] = []
    for stats in all_stats:
        total_res[stats[0]] = []
    for b in budgets:
        ceiling_rate = get_ceiling_rate(rep, b)
        results = max_ceiling_rate(all_stats, ceiling_rate)
        total = 0
        for key in results.keys():
            total += results[key]
            total_res[key].append(results[key])
        total_res["all"].append(total)
    print(total_res)


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
        result = MaxTestsResult(0, 0)
        for stats in all_stats:
            for testKey in testKeys:
                rate = calculate_rate(stats, key, testKey)
                result.log_of_rest += math.log(rate + 1)
                if rate > 0:
                    result.rep_tests += 1
        return result

    analyze_global(all_stats, "global log rate", max_log_ceiling, compare_max_tests_results, MaxTestsResult(0, 0), ceiling_rate)

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
    parser.add_argument("--action", default="log-rate", help="Analysis to perform. Options are 'rate', 'log-rate', 'ceiling-log-rate', 'ceiling-rate', 'global-log-rate' , 'global-ceiling-log-rate', 'global-ceiling-rate', 'merge', 'ceiilng-rate-all'")
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
    elif args.action == "merge":
        merge(all_stats)
    elif args.action == "ceiling-rate-all":
        max_ceiling_rate_all(all_stats, float(args.rep)/100)

if __name__ == "__main__":
    main()
