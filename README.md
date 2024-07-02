# MTG Bulk Scan

MTG Bulk Scan is a Python script that automates the process of adding Magic: The Gathering cards to your deckbox.org collection. It uses OpenAI's GPT-4o model to analyze images of cards and extract relevant information, creating a CSV file ready for import into deckbox.org. Creates a complete CSV requiring no adjustments after import.

## Features

- Process an entire folder of cards at once and create a CSV file to easily upload your cards to your deckbox.org inventory.
- Automatic resizing of images to meet API requirements
- Customizable card condition, language, and other attributes
- Automatically detects foiled cards and marks them appropriately (beta feature).
- Debug mode for troubleshooting
- Error logging for failed card processes

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```
git clone https://github.com/JackTheTripperr/mtg-bulk-scan.git
cd mtg-bulk-scan
```

2. Create a virtual environment:
- For Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- For macOS and Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
- Make a copy of the `.env.example` rename it to `.env`
- Open the `.env` file and replace `your_api_key_here` with your actual OpenAI API key

## Usage

1. Using your phone or any other camera, snap a quick photo of each card you would like to enter into your database. Place your card images in the `card-pics` folder.

2. Run the script with desired options:
```
python mtg_bulk_scan.py [OPTIONS]
```

Available options:
- `--help`: Prints help message
- `--condition OPTIONS`: Options: M (Mint), NM (Near Mint), LP (Lightly Played), PL (Played), HP (Heavily Played), PR (Poor), PX (Proxy), B (Blank), defaults to Near Mint
- `--language LANGUAGE`: Set the language of the cards
- `--my-price PRICE`: "$X.XX" Set your price for the cards
- `--tradelist-count COUNT`: Set to 1 to automatically mark your cards available for trade, default 0
- `--signed OPTIONS`: Options: signed, mark cards as signed, defaults to blank
- `--artist-proof`: Mark cards as artist proofs, defaults to blank
- `--altered-art`: Mark cards as altered art, defaults to blank
- `--misprint`: Mark cards as misprints, defaults to blank
- `--promo`: Mark cards as promos, defaults to blank
- `--textless`: Mark cards as textless, defaults to blank
- `--printing-note`: Add a printing note, defaults to blank
- `--tags`: Add tags to the cards, defaults to blank
- `--foil`: Options: yes, auto. Set foil status. Defaults to blank. "auto" is in beta.
- `--debug`: Enable debug mode

3. After processing, you'll find a `card-list.csv` file in the root directory, ready for import into deckbox.org.

## Example

Process all cards in Good (Lightly Played) condition and automatically identify and label foils:
```
python mtg_bulk_scan.py --condition LP --foil auto
```

## Troubleshooting

If any cards fail to process, check the `error_log.txt` file for the missed cards. You can also run the script with the `--debug` flag for more detailed logging.

## Patience Please!

I'm very new to Python and programming in general. Please bear with me as I experience some growing pains.

## What's Next?

- CSV formatting for other websites
- Automatic renaming of pictures for easy upload to your sales pages
- Better command line args/instructions
- Optimizations
- Support for other APIs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC or deckbox.org. This is an independent project created to assist Magic: The Gathering players in managing their collections.


