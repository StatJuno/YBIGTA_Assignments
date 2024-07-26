from argparse import ArgumentParser
from datetime import datetime
from hankyung_scraper import HanKyungScraper


def create_parser() -> ArgumentParser:
    today = datetime.today().strftime("%Y%m%d")

    parser = ArgumentParser()
    parser.add_argument("-s", "--start_date", type=str, required=True, help="example: 20240504")
    parser.add_argument("-e", "--end_date", type=str, default=today, help=f"example: {today}")
    parser.add_argument("-o", "--output", type=str, default="", help="output json file path")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    scraper = HanKyungScraper(args.start_date, args.end_date, args.output)
    scraper.scrape()
    