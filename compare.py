import json
import argparse
import math

def load_stats(stats_path):
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def time_to_rep(test_dur, observed, needed):
    if observed == 0:
        return -1
    else:
        return (test_dur/observed) * needed

def update_keys(totals, value):
    if value != -1:
        if value > totals["parallelTime"]:
            totals["parallelTime"] = value
        totals["sequentialTime"] += value
        totals["totalKilled"] += 1

def print_totals(strat, totals):
    print("Using {} strategy: Longest Time: {}, Sequential Time: {}, Score: {}".format(strat, totals["parallelTime"], totals["sequentialTime"], totals["totalKilled"]))

def compare(p_rates, si_rates, rep):
    needed = math.ceil(-math.log(1 - rep))
    keys = ["parallelTime", "sequentialTime", "totalKilled"]
    p_totals = dict()
    si_totals = dict()
    si_extra_totals = dict()
    for key in keys:
        p_totals[key] = 0
        si_totals[key] = 0
        si_extra_totals[key] = 0
    for device in p_rates.keys():
        for i in range(len(p_rates[device].keys())):
            p_test = list(p_rates[device].keys())[i]
            si_test = list(si_rates[device].keys())[i]
            p_total_instances = p_rates[device][p_test]["seq"] + p_rates[device][p_test]["interleaved"] + p_rates[device][p_test]["weak"]
            si_total_instances = si_rates[device][si_test]["seq"] + si_rates[device][si_test]["interleaved"] + si_rates[device][si_test]["weak"]

            si_rate = si_total_instances/si_rates[device][si_test]["durationSeconds"]

            p_time_to_rep = time_to_rep(p_rates[device][p_test]['durationSeconds'], p_rates[device][p_test]['weak'], needed)
            si_time_to_rep = time_to_rep(si_rates[device][si_test]["durationSeconds"], si_rates[device][si_test]["weak"], needed)

            if p_rates[device][p_test]["weak"] == 0:
                si_extra_time_to_rep = -1
            else:
                p_iter_per_weak = p_total_instances/p_rates[device][p_test]["weak"]
                extra_time = p_iter_per_weak/si_rate
                si_extra_time_to_rep = extra_time * needed

            update_keys(p_totals, p_time_to_rep)
            update_keys(si_totals, si_time_to_rep)
            update_keys(si_extra_totals, si_extra_time_to_rep)
            print("{} on {}: Parallel Time Needed: {}, Single Instance Time Needed: {}, Single Instance Extrapolated: {}".format(p_test, device, p_time_to_rep, si_time_to_rep, si_extra_time_to_rep))

    print_totals("Parallel", p_totals)
    print_totals("Single Instance", si_totals)
    print_totals("Single Instance Extrapolated", si_extra_totals)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("p_rates", help="File containing parallel rate information")
    parser.add_argument("si_rates", help="File containing single instance rate information")
    parser.add_argument("--rep", default="99.999", help="Level of reproducibility.")
    args = parser.parse_args()
    p_rates = load_stats(args.p_rates)
    si_rates = load_stats(args.si_rates)
    compare(p_rates, si_rates, float(args.rep)/100)

if __name__ == "__main__":
    main()
