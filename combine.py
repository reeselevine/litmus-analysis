import json
import argparse

def load_stats(stats_path):
    """
    Load the file with the test run output
    """
    with open(stats_path, "r") as stats_file:
        dataset = json.loads(stats_file.read())
        return dataset

def analyze_combined(all_stats, to_max, calculate):
    tests = {}
    for key in all_stats[0][1]["0"]:
        if key != "params":
            tests[key] = (None, 0)
    for key in all_stats[0][1]:
        if key != "randomSeed":
            for testKey in tests.keys():
                result = calculate(all_stats, testKey)
                if result > tests[testKey][1]:
                    tests[testKey] = (key, result)
    print("Maximizing {} of weak behaviors".format(to_max))
    for res in tests.items():
        print("{}: {} in iteration {}".format(res[0], str(res[1][1]), res[1][0]))
        print ("  Details:")
        for stats in all_stats:
            print("    {}: {}".format(stats[0], stats[1][res[1][0]][res[0]]))

def max_sum(all_stats):
    def calculate(all_stats, testKey):
        total = 0
        for stats in all_stats:
            total += stats[1][key][testKey]["weak"]
        return total
    analyze_combined(all_stats, to_max, calculate)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_files", nargs="+", help="List of stats files to combine")
    args = parser.parse_args()
    all_stats = []
    for stats_file in args.stats_files:
        all_stats.append((stats_file.split(".")[0], load_stats(stats_file)))
    analyze_combined(all_stats)

if __name__ == "__main__":
    main()



