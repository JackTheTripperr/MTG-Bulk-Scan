# MTG Bulk Scan

![MTG Bulk Scan in action](./.assets/demo.gif)

MTG Bulk Scan is a project born from the frusteration of manually entering Magic: The Gathering cards into an online database and spending far too long finding the right card, then finding the right set, then finding the right art, then marking the card for trade, then...

You get the idea! I found myself putting off the entering of new cards into the online collection tracker I use (deckbox.org) because I found the process tedious. Before long, I'd have been to a couple of FNM's, maybe a pre-release or two and I'd have a literal mountain of cards sitting on my dining room table that needed to be entered. Looking at the pile only made me put off entering the cards even longer! I let this happen long enough that my wife took notice and suddenly I was facing a whole new, much more serious problem. 

Faced with catching up on of months of card entry, I figured there ought to be a way to make the process go a little faster. Coincidentally, around the same time I had been playing with various LLM's like ChatGPT and Claude, and I was dying to find a way to use this technology to make my life a little bit easier. These circumstances all collided in my head and gave birth to the baby that was born as MTG Bulk Scan.

## Features

- Automated processing of your MTG cards for quick and easy entry into Deckbox.org.
- Very little human input required. Snap a quick picture of your new cards and let the scanner do the rest.
- Photos are resized during processing to ensure efficient API use.
- By default, a deckbox.org formatted CSV is made with prepopulated Count, Tradelist Count, Name, Edition, Edition Code, Card Number, Condition, and Language fields. With these fields filled, you no longer have to hunt for the right set, card number, art work, etc. Just import from the CSV and you're done.
- In addition to the above fields, you can also customize Foil, Signed, Artist Proof, and Tags for the batch of cards you're working on.
- Debug mode included to help you trouble shoot if any issues pop up.
- For cards that can't be indentified or otherwise entered into the CSV automatically, an error log is generated so you can quickly identify which cards got left out.

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

5. Enter .env details:
   - Copy the `.env.example` file to `.env`.
   - Open the `.env` file and:
     - replace `your_api_key_here` with your actual OpenAI API key.
     - replace `path\to\card-pics` with the path to folder containing pictures of your cards.

## Usage

1. Snap a photo of each of your cards and place the card images in the folder you setup in the .env file.

2. Run the script with desired options:
   ```bash
   python mtg_bulk_scan.py [OPTIONS]
   ```
   Running the script without options will consider all cards as Near Mint, non-foil, and English. Use the option flags to customize the CSV fields. For example, setting the condition to LP (Lightly Played) will mark all cards in that batch as LP.

```
usage: main.py [-h] [-s] [-f {yes,no}] [-t {yes,no}] [-c {M,NM,LP,PL,HP,P,PX}] [-l LANGUAGE] [-S {yes,no}]
               [-ap {yes,no}] [-aa {yes,no}] [-m {yes,no}] [-T TAGS] [--debug]

Use photos of your cards to populate a CSV for 1-click import into deckbox.org

options:
  -h, --help            show this help message and exit
  -s, --strict          Disables fuzzy searching and only populates the CSV if the script feels confident it has found
                        the correct printing of the card
  -f {yes,no}, --foil {yes,no}
                        Specify if the batch of cards is foiled
  -t {yes,no}, --tradelist {yes,no}
                        Specify if the card batch should be marked for trade
  -c {M,NM,LP,PL,HP,P,PX}, --condition {M,NM,LP,PL,HP,P,PX}
                        Specify the condition of the card batch
  -l LANGUAGE, --language LANGUAGE
                        Specify the language of the card batch
  -S {yes,no}, --signed {yes,no}
                        Specify if the batch of cards has been signed
  -ap {yes,no}, --artist-proof {yes,no}
                        Specify if the batch of cards are proofs
  -aa {yes,no}, --altered-art {yes,no}
                        Specify if the batch of cards have altered art
  -m {yes,no}, --misprint {yes,no}
                        Specify if the batch of cards is misprinted
  -T TAGS, --tags TAGS  User specified tags for the card batch
  --debug               Enable debug logging
```

4. After the script finishes, you'll find a `DATE_TIME.csv` file in the projects root directory, ready for import into deckbox.org. If the script wasn't confident about the card details it found, the cards entry will be prefaced with "***". Quickly check these entries to ensure they are accurate an then delete the "***" once you're satsified. If the script wasn't able to accurately parse the information from a card, you'll find a copy of it's picture in the "card-errors" folder in the projects root directory, as well as an "errors_DATE-TIME.csv which contains any additional info about the error. 

## Example

Process all cards as Good (Lightly Played) condition, English language, mark them all for trade:
```bash
python mtg_bulk_scan.py --condition LP --tradelist yes
```
## How does it work?

The script sends a picture of each card off to the Open AI GPT-4o API and requests that the card name, collector number, and set code be returned in JSON format. With my limited "programming" skills and the incredibly small text the collector number and set code is printed in, I've found this technique to be significantly more accurate at parsing the required text than more traditional OCR techniques. This data is then cross referenced with data from Scryfall to confirm the correct details were obtained. if everytghing looks good, the card is entered into the CSV and the next card is processed. If there is a mismatch, data for each unique printing of the card being proccessed is requested from Scryfall and the Open AI API is called again to try and deduce which printing of the card is correct. If this step fails, the card is considered an error and the script moves on. Otherwise, the card data is entered into the CSV. If there were any mismatches during this process, that card entry will be prefaced with "***" in the CSV so you can quickly confirm whether the correct details were entered or not.

## Limitations

The script has trouble with card styles in which the name of the card isn't found in the traditional location or cards in which the set code and collector number are not located in the bottom left corner of the card. In addition, the script has trouble with Tokens. Keep these limitations in mind when sending batched of cards through the script.

## Roadmap

- Option to rename resized images as CardName-Set-CardNumber for ready-to-upload pictures.
- CSV compatibility for import into other collection managers.
- Optimizations
- Compatability with free LLM APIs.
- Suggestions or requests?

## Troubleshooting

If any cards fail to process, check the `errors_DATE-Time.csv` file in the project's root folder for details. You can also run the script with the `--debug` flag for more verbose output that can help you pinpoint the origin of some issues.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. In particular, I'd love help with forgoing the LLM technique and moving over to OCR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC or deckbox.org. This is an independent project created to assist Magic: The Gathering players in managing their collections.
