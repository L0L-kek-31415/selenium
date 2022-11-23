import argparse
from parser.siteservice import SiteService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=2, help="workers")
    parser.add_argument("--pages", type=int, default=2, help="pages")
    parser.add_argument(
        "--database",
        type=str,
        default="mongo",
        help="mongo - MongoDB, pg - Postgres, txt - TXT_file",
    )
    args = parser.parse_args()
    workers = args.workers
    pages = args.pages
    database = args.database
    reddit = SiteService(pages, workers, "https://reddit.com/top", database)
    reddit.start()


if __name__ == "__main__":
    main()
