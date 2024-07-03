# MTG Bulk Scan

![MTG Bulk Scan in action](./.assets/demo.gif)

MTG Bulk Scan is a project born from the frusteration of manually entering Magic: The Gathering cards into an online database and spending far too long finding the right card, then finding the right set, then finding the right art, then marking the card for trade, then...

You get the idea! I found myself putting off the entering of new cards into the online collection tracker I use (deckbox.org) because I found the process tedious. Before long, I'd have been to a couple of FNM's, maybe a pre-release or two and I'd have a literal mountain of cards sitting on my dining room table that needed to be entered. Looking at the pile only made me put off entering the cards even longer! I let this happen long enough that my wife took notice and suddenly I was facing a whole new, much more serious problem. 

Faced with catching up on of months of card entry, I figured there ought to be a way to make the process go a little faster. Coincidentally, around the same time I had been playing with various LLM's like ChatGPT and Claude, and I was dying to find a way to use this technology to make my life a little bit easier. These circumstances all collided in my head and gave birth to the baby that was born as MTG Bulk Scan.

## Features

- Automated processing of your MTG cards for quick and easy entry into Deckbox.org.
- Very little human input required. Snap a quick picture of your new cards and let the scanner do the rest.
- Photos are resized during processing to ensure efficient API use.
- By default, a deckbox.org formatted CSV is made with prepopulated Count, Tradelist Count, Name, Edition, Edition Code, Card Number, Condition, and Language fields. With these fields filled, you no longer have to hunt for the right set, card number, art work, etc. Just import from the CSV and your done.
- In addition to the above fields, you can also customize Foil, Signed, Artist Proof, Altered Art, Misprint,Promo, Textless, Printing ID, Printing Note, Tags, and My Price for the batch of cards you're working on.
- If you're looking to save even more time, let the AI detect which cards are foil and have the CSV correctly populated with that data, too (this feature is experimental, but has suprisingly accurate results).
- Debug mode included to help you trouble shoot if any issues pop up.
- For cards that can't be indentified or otherwise entered into the CSV automatically, a error log is generated so you can quickly identify which cards got left out.

## Prerequisites

- OpenAI API key (uses the GPT-4o API). Obtain your key at platform.openai.com.
- Python 3.7 or higher.
- A way to take pictures of your cards (a smartphone works fine).

## Installation

1. Star the repository and follow for the latest updates.

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mtg-bulk-scan.git
   cd mtg-bulk-scan
   ```

3. (Optional) Create a virtual environment to avoid dependency conflicts:
   - For Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your OpenAI API key:
   - Copy the `.env.example` file to `.env`.
   - Open the `.env` file and replace `your_api_key_here` with your actual OpenAI API key.

## Usage

1. Snap a photo of each of your cards and place the card images in the `card-pics` folder.

2. Run the script with desired options:
   ```bash
   python mtg_bulk_scan.py [OPTIONS]
   ```
   Running the script without options will consider all cards as Near Mint, non-foil, and English. Use the option flags to customize the CSV fields. For example, setting the condition to LP (Lightly Played) will mark all cards in that batch as LP.

   Available options:
   - `--condition`: Set the condition of the cards in this batch (M, NM, LP, PL, HP, PR, PX, B)
   - `--language`: Set the language of the cards in this batch
   - `--my-price`: Set "My Price" for the cards in this batch
   - `--tradelist-count`: Set the tradelist count for this batch
   - `--signed`: Mark cards as signed
   - `--artist-proof`: Mark cards as artist proofs
   - `--altered-art`: Mark cards as altered art
   - `--misprint`: Mark cards as misprints
   - `--promo`: Mark cards as promos
   - `--textless`: Mark cards as textless
   - `--printing-note`: Add a printing note to this batch of cards
   - `--tags`: Add a custom tag to this batch of cards
   - `--foil {yes, auto}`: Set foil status (experimental)
   - `--debug`: Enable debug mode for detailed logging

3. After the script finishes, you'll find a `card-list.csv` file in the root directory, ready for import into deckbox.org.

## Example

Process all cards in Good (Lightly Played) condition, English language, and mark them all as foil:
```bash
python mtg_bulk_scan.py --condition LP --foil yes
```

## Roadmap

- Option to rename resized images as CardName-Set-CardNumber for ready-to-upload pictures.
- CSV compatibility for import into other collection managers.
- Optimizations
- Compatibility with other LLM APIs
- Suggestions or requests?

## Troubleshooting

If any cards fail to process, check the `error_log.txt` file in the project's root folder for details. You can also run the script with the `--debug` flag for more detailed logging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC or deckbox.org. This is an independent project created to assist Magic: The Gathering players in managing their collections.
