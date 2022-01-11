import json
import argparse

def load_stats(stats_path):
     with open(stats_path, "r") as stats_file:
         stats = json.loads(stats_file.read())
         return stats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_path", help="Path to output to analyze")
    args = parser.parse_args()
    stats = load_stats(args.stats_path)
    print(stats["0"])

if __name__ == "__main__":
    main()
