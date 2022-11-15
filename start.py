import argparse
from main import SiteService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=2, help="workers")
    parser.add_argument("--pages", type=int, default=2, help="pages")
    args = parser.parse_args()
    workers = args.__dict__["workers"]
    pages = args.__dict__["pages"]
    reddit = SiteService(pages, workers, "https://reddit.com/top")
    reddit.start()


if __name__ == "__main__":
    main()
