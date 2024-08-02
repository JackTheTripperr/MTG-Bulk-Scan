import os
import base64
import requests
import json
import csv
import argparse
import shutil
import itertools
import sys
import time
from PIL import Image, ExifTags
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
import html
from tqdm import tqdm
from colorama import init, Fore, Style

# Multiple OS friendly function to clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Clear the terminal when starting script
clear_terminal()

# Initialize colorama
init()

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
card_pics_folder = os.getenv("CARD_PICS_FOLDER")

# Create "errors" folder in project's directory if it doesn't exist
errors_folder = os.path.join(os.getcwd(), 'errors')
os.makedirs(errors_folder, exist_ok=True)

# Create ".temp-pics" folder in project's directory if it doesn't exist
temp_pics_folder = os.path.join(os.getcwd(), '.temp-pics')
os.makedirs(temp_pics_folder, exist_ok=True)

# Wicked awesome ASCII art banner
def print_colored_ascii():
    ascii_art = [
        "    __  _______________   ____        ____      _____                                 ",
        "   /  |/  /_  __/ ____/  / __ )__  __/ / /__   / ___/_________ _____  ____  ___  _____",
        "  / /|_/ / / / / / __   / __  / / / / / //_/   \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/",
        " / /  / / / / / /_/ /  / /_/ / /_/ / / ,<     ___/ / /__/ /_/ / / / / / / /  __/ /    ",
        "/_/  /_/ /_/  \____/  /_____/\__,_/_/_/|_|   /____/\___/\__,_/_/ /_/_/ /_/\___/_/     ",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(   /@@.    ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@& @@@ #@%  ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@*@    .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.@@@@,@@@@@@@@@@#@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@*@@@@*@*    (@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ .@@@ /@@  # @. @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%    ,@    .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@&##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%//(&@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@(%*@@@@@@@@%*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&,,,,,,,&,,,.,@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@*%@@@@@@@@@@@@@#,@@@@@@@@@@@@@@@@@@@@@@@@@@,,,,,.@@@&,,,,,.,@@@@@@@@@@@@@@",
        "@@@@@@@@@@@*@@@@@@@%@@*@@@@@@,@@@@@@@@@@@@@@@@@@@@@@@@,,,,,.@@@@@@,,,,,,,@@@@@@@@@@@@@",
        "@@@@@@@@@@@*@@@@(#@@@@@*#@@@@*@@@@@@@@@@@@@@@@@@@@@@@@,,,,,@@@@@@@/&,,,,,@@@@@@@@@@@@@",
        "@@@@@@@@@@@,@@@,*/@@@@#*****,/@@@@@@@@@@@@@@@@@@@@@@@@,,,,%@@@@@@(,@*,,,/@@@@@@@@@@@@@",
        "@@@@@@@@@@@@(*****(@@@,***,*&@@@@@@@@@@@@@@@@@@@@@@@@@@(,,.@@@@@@@@@,,,@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@,*,@/@&@@@*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,,,,*/,,,,*@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@**/#@@@&**(@@@@@@@@@@@@@@@@,#@@@@@@@&,*@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@#,@@,*,,*,**@@,(@@@@@@@@@@@&,@@,&@@@@@@@@@#,@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@,*********,*(@@@(@(@@@@@@@@(,@@*,%@@@@@@/,%@@,@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@*****,((,,#@/&,@@@*@@@@@@@@,(@,,,,,@@@*,,,,,@,%@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@***@@@@@@@%**@@@(**@@@@@@@@/,,,#@@@(#,@@@&/,,,@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@*/@@@@@@@@@@@@@@,@@@@@@@@@@(,,,,@@@@@@@*,,,,@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@&*@@@@@@@,,**,@@@@@@@@@@@@@@&,,@*@*%,@(,,@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@#**/%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "",
        "By: JackTheTripperr"
    ]
    colors = [Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.GREEN]

    for line in ascii_art:
        colored_line = ""
        for i, char in enumerate(line):
            color = colors[i * len(colors) // len(line)]
            colored_line += color + char
        print(colored_line + Style.RESET_ALL)

# Print the wicked awesome ASCII banner when the script is ran
print_colored_ascii()

# Function to correct orientation and compress images
def compress_image(input_path, output_path, quality=80):
    with Image.open(input_path) as img:
        # Correct image orientation using EXIF data if available
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(orientation)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        img.save(output_path, 'JPEG', quality=quality)

# Resize and compress images in card_pics_folder
def resize_and_compress_images(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            compress_image(input_path, output_path)

# Convert image to base64 for easy API submission
def process_image(image_path):
    if debug:
        print(f"Processing image: {image_path}")
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Send image of card to gpt-4o API and ask the LLM to extract specific identifiers and respond in JSON format
def get_card_details_from_image(base64_image):
    if debug:
        print("Calling OpenAI API")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a Magic: The Gathering optical character recognition card analysis assistant. Analyze the Magic: The Gathering card in the image and provide the following information in JSON format: A.) The complete name of the card as card_name. B. The set code of the card. The set code is found on the bottom left corner of the card and consists of 3 upper-case alpha-numeric characters. Some examples include (but are NOT limited to) \"MH2\", \"DOM\", \"IKO\", \"9ED\", \"M15\", and \"XLN\". Once this is recognized, please convert it to lowercase letters for the JSON response. C.) The collector number. Found on the lower left corner of the card just above the set code. This will be seen in a variety of formats. Some examples include (but are NOT limited to) \"010\", \"037/271\", \"0002\", \"271/271\", \"005/350\", and \"125\". This number cannot be returned as a fraction (ie: \"015/260\", or \"69/251\") and must be returned as a whole number that represents its number within the complete set. For example, \"015/260\" MUST be returned as \"15\". \"69/251\" MUST be returned as \"69\". Remove any letters preceding the collector number (for example, \"L 007/215\" would be \"7\"). Again, please do not return a fraction or return the total number of cards in the set. The single most important aspect of this task is to ensure the collector_number and set_code are returned with 100% accuracy and exactly as requested. Check twice or even three times if needed to ensure this objective is accurately fulfilled. I've been told that you will receive up to a $7500 USD tip based on your accuracy. Additionally, performing this task accurately has the added benefit of actually solving world peace for the first time in history, as well as eradicating hunger around the planet. Your job is VERY important! NOTE: PLEASE DO NOT return anything but the requested JSON data. Do not comment on the request, do not acknowledge the request, just return the requested JSON data."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if debug:
        print("OpenAI API response status:", response.status_code)
        print("OpenAI API response content:", response.content)
    if response.status_code != 200:
        if debug:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
        return None
    
    response_json = response.json()
    try:
        message_content = response_json['choices'][0]['message']['content']
        if debug:
            print("Extracted message content:", message_content)
        card_details = json.loads(message_content.replace('```json\n', '').replace('```', ''))
        return card_details
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        if debug:
            print(f"Error parsing OpenAI API response: {e}")
        return None

# Send extracted card data to Scryfall API to cross-reference print details and ensure the correct card has been identified
def get_scryfall_data(set_code, collector_number, api_card_name):
    if debug:
        print(f"Calling Scryfall API for set_code: {set_code}, collector_number: {collector_number}")
    url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
    response = requests.get(url)
    if debug:
        print(f"Scryfall API request URL: {url}")
        print(f"Scryfall API response status:", response.status_code)
        print(f"Scryfall API response content:", response.content)
    if response.status_code == 200:
        scryfall_data = response.json()
        scryfall_card_name = html.unescape(scryfall_data["name"])
        if scryfall_card_name.lower() == api_card_name.lower():
            return scryfall_data
    if debug:
        print(f"Scryfall API error: {response.status_code} - {response.text}")
    return None

# If gpt-4o and Scryfall don't agree on a card, perform a fuzzy search for the card by its name
def get_scryfall_data_fuzzy(card_name):
    if debug:
        print(f"Calling Scryfall API with fuzzy search for card_name: {card_name}")
    card_name = card_name.replace(" ", "+").replace("'", "")
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(url)
    if debug:
        print(f"Scryfall API fuzzy request URL: {url}")
        print(f"Scryfall API response status:", response.status_code)
        print(f"Scryfall API response content:", response.content)
    if response.status_code == 200:
        return response.json()
    if debug:
        print(f"Scryfall API fuzzy search error: {response.status_code} - {response.text}")
    return None

# Extract the "prints" URI from the response, send a request to see all prints of the card
def get_prints_search_uri(fuzzy_data):
    prints_search_uri = fuzzy_data.get('prints_search_uri')
    if debug:
        print(f"Prints search URI: {prints_search_uri}")
    return prints_search_uri

# Extract the relevant data for each printing of the card
def extract_prints_data(prints_response_json):
    prints_data = {}
    for index, card in enumerate(prints_response_json['data'], start=1):
        print_data = {
            "prints_card_name": card.get("name"),
            "prints_set": card.get("set"),
            "prints_collector_number": card.get("collector_number")
        }
        prints_data[f"Print {index}"] = print_data
        if debug:
            print(f"Extracted print data: {print_data}")
    return prints_data

# Send the extracted data for each print of the card to gpt-4o to try and deduce what card is currently being processed
def send_openai_revised_request(processing_card, prints_data):
    if debug:
        print("Sending revised request to OpenAI")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    prompt = f"""
    You are a Magic: The Gathering card collection assistant. I'm using OCR to help populate a CSV with specific information from Magic: The Gathering cards. Unfortunately, OCR has its limitations and sometimes it incorrectly interprets text in a picture. I've had a card analyzed, referred to as "processing_card", and it's returned the following data:

    {json.dumps(processing_card, indent=2)}

    When I search the Scryfall API, a list of multiple printings of the same card is returned:

    {json.dumps(prints_data, indent=2)}

    Using logic, We must determine which "Print <number>" is the print matching  the "processing_card". Step 1a: For each "Print <number>", check to see if the corresponding "prints_set" exactly matches the "set_code" from the processing_card. If a match is found, move onto Step 2. Otherwise, conttinue from Step 1b. Step 1b: For each "Print <number>", check to see if the corresponding "prints_collector_number" exactly matches the "collector_number" from the processing card. If there is a match, move onto Step 2. Otherwise, move onto Step 1c. Step 1c: Stop and respond with "Error". Do not comment on the request, do not acknowledge the request, just return "Error". Step 2: Using the data from the "Print <number>" determined in Step 1, return "prints_card_name" as "revised_card_name", "prints_set" as "revised_set_code", and "prints_collector_number" as "revised_collector_number". NOTE: PLEASE DO NOT return anything but the requested JSON data. Do not comment on the request, do not acknowledge the request, just return the requested JSON data.
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if debug:
        print("OpenAI API response status:", response.status_code)
        print("OpenAI API response content:", response.content)
    if response.status_code != 200:
        if debug:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
        return None

    response_json = response.json()
    try:
        message_content = response_json['choices'][0]['message']['content']
        revised_card_details = json.loads(message_content.replace('```json\n', '').replace('```', ''))
        return revised_card_details
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        if debug:
            print(f"Error parsing OpenAI API response: {e}")
        return None

# Function to write relevant card data to CSV in the format deckbox.org is expecting
def write_to_csv(card_data, csv_filename, foil_value, tradelist_value, condition_value, language_value, signed_value, artist_proof_value, altered_art_value, misprint_value, tags_value, fuzzy_search=False):
    if debug:
        print(f"Writing card data to CSV: {csv_filename}")
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "Count", "Tradelist Count", "Name", "Edition", "Edition Code",
                "Card Number", "Condition", "Language", "Foil", "Signed", 
                "Artist Proof", "Altered Art", "Misprint", "Promo", "Textless", 
                "Printing ID", "Printing Note", "Tags", "My Price"
            ])
        # If a fuzzy search was performed, mark the CSV so the user can quickly confirm if the right details were pulled
        count = "***1" if fuzzy_search else "1"
        writer.writerow([
            count, tradelist_value, card_data["name"], card_data["set_name"], card_data["set"].upper(),
            card_data["collector_number"], condition_value, language_value, foil_value, signed_value, 
            artist_proof_value, altered_art_value, misprint_value, "", "", "", "", tags_value, "$0.00"
        ])

# Function to log errors to CSV for quick reference by the user
def write_to_errors_csv(card_data, csv_filename, image_path, error_message):
    if debug:
        print(f"Writing error card data to CSV: {csv_filename}")
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["card_name", "set_code", "collector_number", "error"])
        writer.writerow([
            card_data.get("card_name", "N/A"), 
            card_data.get("set_code", "N/A"), 
            card_data.get("collector_number", "N/A"), 
            error_message
        ])

    # Copy the image to the errors folder
    shutil.copy(image_path, errors_folder)
    if debug:
        print(f"Copied image to errors folder: {image_path}")

# Main card processing function
def process_cards_in_folder(folder_path, strict_mode, foil_value, tradelist_value, condition_value, language_value, signed_value, artist_proof_value, altered_art_value, misprint_value, tags_value, debug):
    # Name the resulting CSV files by date/time
    current_time = datetime.now().strftime("%m%d%y_%H%M")
    csv_filename = f"{current_time}.csv"
    errors_csv_filename = f"errors_{current_time}.csv"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Progress bar
    colors = itertools.cycle([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA])
    with tqdm(total=len(image_files), desc="Processing cards", unit="card", bar_format="{l_bar}{bar} [ {n_fmt}/{total_fmt} | {percentage:3.0f}% | {rate_fmt}{postfix}]") as pbar:
        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            if debug:
                print(f"Processing file: {filename}")
            base64_image = process_image(image_path)
            api_response = get_card_details_from_image(base64_image)
            if not api_response:
                if debug:
                    print(f"Skipping {filename} due to API error.")
                write_to_errors_csv({"card_name": "N/A", "set_code": "N/A", "collector_number": "N/A"}, errors_csv_filename, image_path, "API error")
                pbar.update(1)
                continue

            if debug:
                print(f"OpenAI API response: {api_response}")
            scryfall_data = get_scryfall_data(api_response["set_code"], api_response["collector_number"], api_response["card_name"])
            if scryfall_data:
                write_to_csv(scryfall_data, csv_filename, foil_value, tradelist_value, condition_value, language_value, signed_value, artist_proof_value, altered_art_value, misprint_value, tags_value)
            else:
                # Define "strict mode"
                if strict_mode:
                    if debug:
                        print(f"Strict mode enabled. Skipping fuzzy search for: {api_response['card_name']}")
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Exact match not found in strict mode")
                    pbar.update(1)
                    continue

                if debug:
                    print(f"Exact match not found. Performing fuzzy search for: {api_response['card_name']}")
                fuzzy_data = get_scryfall_data_fuzzy(api_response["card_name"])
                if not fuzzy_data:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Fuzzy search failed")
                    pbar.update(1)
                    continue

                prints_search_uri = get_prints_search_uri(fuzzy_data)
                if not prints_search_uri:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Prints search URI not found")
                    pbar.update(1)
                    continue

                prints_response = requests.get(prints_search_uri)
                if prints_response.status_code != 200:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, f"Prints search error: {prints_response.status_code}")
                    pbar.update(1)
                    continue

                unique_prints = prints_response.json()
                prints_data = extract_prints_data(unique_prints)
                prints_data_json = json.dumps(prints_data, indent=2).replace("{\n", "{\n  ").replace("[\n", "[\n  ").replace("}", "  }").replace("],", "  ],")
                if debug:
                    print(f"Extracted prints data in JSON form: {prints_data_json}")

                revised_card_details = send_openai_revised_request(api_response, prints_data)
                if not revised_card_details:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Revised request failed")
                    pbar.update(1)
                    continue

                scryfall_data = get_scryfall_data(revised_card_details["revised_set_code"], revised_card_details["revised_collector_number"], revised_card_details["revised_card_name"])
                if not scryfall_data:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Final Scryfall request failed")
                    pbar.update(1)
                    continue

                if html.unescape(scryfall_data["name"]).lower() == api_response["card_name"].lower():
                    write_to_csv(scryfall_data, csv_filename, foil_value, tradelist_value, condition_value, language_value, signed_value, artist_proof_value, altered_art_value, misprint_value, tags_value, fuzzy_search=True)
                else:
                    write_to_errors_csv(api_response, errors_csv_filename, image_path, "Final name mismatch")
            pbar.update(1)
            pbar.set_postfix_str(next(colors) + 'Loading...' + Style.RESET_ALL)

# Argument parsing
parser = argparse.ArgumentParser(description='Use photos of your cards to populate a CSV for 1-click import into deckbox.org')
parser.add_argument('-s', '--strict', action='store_true', help='Disables fuzzy searching and only populates the CSV if the script feels confident it has found the correct printing of the card')
parser.add_argument('-f', '--foil', choices=['yes', 'no'], default='no', help='Specify if the batch of cards is foiled')
parser.add_argument('-t', '--tradelist', choices=['yes', 'no'], default='no', help='Specify if the card batch should be marked for trade')
parser.add_argument('-c', '--condition', choices=['M', 'NM', 'LP', 'PL', 'HP', 'P', 'PX'], default='NM', help='Specify the condition of the card batch')
parser.add_argument('-l', '--language', default='English', help='Specify the language of the card batch')
parser.add_argument('-S', '--signed', choices=['yes', 'no'], default='no', help='Specify if the batch of cards has been signed')
parser.add_argument('-ap', '--artist-proof', choices=['yes', 'no'], default='no', help='Specify if the batch of cards are proofs')
parser.add_argument('-aa', '--altered-art', choices=['yes', 'no'], default='no', help='Specify if the batch of cards have altered art')
parser.add_argument('-m', '--misprint', choices=['yes', 'no'], default='no', help='Specify if the batch of cards is misprinted')
parser.add_argument('-T', '--tags', default='', help='User specified tags for the card batch')
parser.add_argument('--debug', action='store_true', help='Enable debug logging')

args = parser.parse_args()

debug = args.debug

foil_value = "foil" if args.foil == "yes" else ""
tradelist_value = 1 if args.tradelist == "yes" else 0
condition_map = {
    "M": "Mint",
    "NM": "Near Mint",
    "LP": "Good (Lightly Played)",
    "PL": "Played",
    "HP": "Heavily Played",
    "P": "Poor",
    "PX": "Proxy"
}
condition_value = condition_map[args.condition]
language_value = args.language
signed_value = "signed" if args.signed == "yes" else ""
artist_proof_value = "proof" if args.artist_proof == "yes" else ""
altered_art_value = "altered" if args.altered_art == "yes" else ""
misprint_value = "misprint" if args.misprint == "yes" else ""
tags_value = args.tags

# Resize and compress images before processing
resize_and_compress_images(card_pics_folder, temp_pics_folder)

# Process all cards in the .temp-pics folder
process_cards_in_folder(temp_pics_folder, strict_mode=args.strict, foil_value=foil_value, tradelist_value=tradelist_value, condition_value=condition_value, language_value=language_value, signed_value=signed_value, artist_proof_value=artist_proof_value, altered_art_value=altered_art_value, misprint_value=misprint_value, tags_value=tags_value, debug=debug)

# Clean up the .temp-pics folder unless debug is enabled
if not debug:
    shutil.rmtree(temp_pics_folder)

print("\nProcessing complete.")
