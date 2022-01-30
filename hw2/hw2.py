def parse_args():
    print("parse argv")

def sniff_traffic():
    print("sniff trafic")

def calculate_rates():
    print("calculate rates")

def print_summary(results):
    print("print results")

def main():
    args       = parse_args()
    hash_table = sniff_traffic()
    results    = calculate_rates()
    print_summary(results)

if __name__ == "__main__":
    main()

