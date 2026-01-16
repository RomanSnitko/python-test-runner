import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("tests")
    parser.add_argument("--timeout", type=float, default=2.0)
    return parser.parse_args()
