import telegram.ext as tg_ext 
import argparse
from src import handlers

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    aplication = tg_ext.Application.builder().token(args.token).build()

    handlers.setup_hendlers(aplication)

    aplication.run_polling()

if __name__ == "__main__":
    main()
