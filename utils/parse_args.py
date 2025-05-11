import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--fast", action="store_true")
    return parser.parse_args()
