# MTG Bulk Scan

MTG Bulk Scan is a Python script that automates the process of adding Magic: The Gathering cards to your deckbox.org collection. It uses OpenAI's GPT-4 Vision model to analyze images of cards and extract relevant information, creating a CSV file ready for import into deckbox.org.

## Features

- Process multiple card images at once
- Automatic resizing of images to meet API requirements
- Customizable card condition, language, and other attributes
- Option to mark cards as foil or use AI detection
- Debug mode for troubleshooting
- Error logging for failed card processes

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/mtg-bulk-scan.git
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
- Copy the `.env.example` file to `.env`
- Open the `.env` file and replace `your_api_key_here` with your actual OpenAI API key

## Usage

1. Place your Magic: The Gathering card images in the `card-pics` folder.

2. Run the script with desired options:
```
python mtg_bulk_scan.py [OPTIONS]
```

Available options:
- `--condition`: Set the condition of the cards (M, NM, LP, PL, HP, PR, PX, B)
- `--language`: Set the language of the cards
- `--my-price`: Set your price for the cards
- `--tradelist-count`: Set the tradelist count
- `--signed`: Mark cards as signed
- `--artist-proof`: Mark cards as artist proofs
- `--altered-art`: Mark cards as altered art
- `--misprint`: Mark cards as misprints
- `--promo`: Mark cards as promos
- `--textless`: Mark cards as textless
- `--printing-note`: Add a printing note
- `--tags`: Add tags to the cards
- `--foil`: Set foil status (yes, auto)
- `--debug`: Enable debug mode

3. After processing, you'll find a `card-list.csv` file in the root directory, ready for import into deckbox.org.

## Example

Process all cards in Near Mint condition, English language, and mark them all as foil:
```
python mtg_bulk_scan.py --condition NM --language English --foil yes
```

## Troubleshooting

If any cards fail to process, check the `error_log.txt` file for details. You can also run the script with the `--debug` flag for more detailed logging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC or deckbox.org. This is an independent project created to assist Magic: The Gathering players in managing their collections.


