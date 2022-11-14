import argparse
from main import main as kek


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1, help="how many workers")

    parser.add_argument("--pages", type=int, default=5, help="how many pages")
    args = parser.parse_args()
    workers = args.__dict__["workers"]
    pages = args.__dict__["pages"]
    kek(pages, workers)


if __name__ == "__main__":
    main()
