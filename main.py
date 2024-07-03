import os
import base64
import csv
import json
import requests
import logging
import re
import argparse
import shutil
import time
import sys
import rawpy
from dotenv import load_dotenv
from PIL import Image
import io
from colorama import init, Fore, Back, Style

def print_colored_char(char, color):
    sys.stdout.write(color + char + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(0.001)  # Adjust this value to change the printing speed

def print_banner():
    banner = """
            ███╗   ███╗████████╗ ██████╗                                                         
            ████╗ ████║╚══██╔══╝██╔════╝                                                         
            ██╔████╔██║   ██║   ██║  ███╗                                                        
            ██║╚██╔╝██║   ██║   ██║   ██║                                                        
            ██║ ╚═╝ ██║   ██║   ╚██████╔╝                                                        
            ╚═╝     ╚═╝   ╚═╝    ╚═════╝                                                         
                                                                                                 
██████╗ ██╗   ██╗██╗     ██╗  ██╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║   ██║██║     ██║ ██╔╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██║     █████╔╝     ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██║     ██╔═██╗     ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝███████╗██║  ██╗    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                                 
 ╦┌─┐┌─┐┬┌─╔╦╗┬ ┬┌─┐╔╦╗┬─┐┬┌─┐┌─┐┌─┐┬─┐┬─┐  ┌─┐  ╔═╗┬┌┬┐┬ ┬┬ ┬┌┐ 
 ║├─┤│  ├┴┐ ║ ├─┤├┤  ║ ├┬┘│├─┘├─┘├┤ ├┬┘├┬┘  │└┘  ║ ╦│ │ ├─┤│ │├┴┐
╚╝┴ ┴└─┘┴ ┴ ╩ ┴ ┴└─┘ ╩ ┴└─┴┴  ┴  └─┘┴└─┴└─  └──  ╚═╝┴ ┴ ┴ ┴└─┘└─┘
    """
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA]
    color_index = 0
    for char in banner:
        if char != '\n':
            print_colored_char(char, colors[color_index])
            color_index = (color_index + 1) % len(colors)
        else:
            sys.stdout.write('\n')
    print(Style.RESET_ALL)

def print_progress(message, progress, total):
    bar_length = 50
    filled_length = int(bar_length * progress / total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percentage = progress / total * 100
    sys.stdout.write(f'\rProcessing {message: <30} [{bar}] {percentage:5.1f}%')
    sys.stdout.flush()

def condition_map(value):
    condition_mapping = {
        'M': 'Mint',
        'NM': 'Near Mint',
        'LP': 'Lightly Played (Good Condition)',
        'PL': 'Played',
        'HP': 'Heavily Played',
        'PR': 'Poor',
        'PX': 'Proxy',
        'B': ''
    }
    return condition_mapping.get(value.upper(), value)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process pictures of your Magic: The Gathering cards and create a CSV file for quick and easy import to deckbox.com. Take a clean picture of the cards you wish to add to your deckbox.org collection and place the pictures in the \"card-pics\" folder. Run the script. Once it's complete, you'll find a card-list.csv in the root folder that you can use to quickly import all of the cards to your deckbox.org collection.")
    parser.add_argument("--condition", type=condition_map, default="Near Mint", 
                        help="Condition of the imported cards. Options: M (Mint), NM (Near Mint), LP (Lightly Played), PL (Played), HP (Heavily Played), PR (Poor), PX (Proxy), B (Blank). Defaults to Near Mint.")
    parser.add_argument("--language", default="English", help="Language of the imported cards. Defaults to English.")
    parser.add_argument("--my-price", default="$0.00", help="Set My Price of the imported cards. Defaults to $0.00")
    parser.add_argument("--tradelist-count", default="0", help="Tradelist Count of the imported cards. Defaults to 0. Change to 1 to automatically mark every card imported available for trade.")
    parser.add_argument("--signed", default="", help="Signed status of the imported cards. Defaults to blank.")
    parser.add_argument("--artist-proof", default="", help="Artist Proof status of the imported cards. Defaults to blank.")
    parser.add_argument("--altered-art", default="", help="Altered Art status of the imported cards. Defaults to blank.")
    parser.add_argument("--misprint", default="", help="Misprint status of the imported cards. Defaults to blank.")
    parser.add_argument("--promo", default="", help="Promo Status of the imported cards. Defaults to blank.")
    parser.add_argument("--textless", default="", help="Textless status of the imported cards. Defaults to blank.")
    parser.add_argument("--printing-note", default="", help="Printing Note of the imported cards. Defaults to blank.")
    parser.add_argument("--tags", default="", help="Set Tags for the imported cards. Defaults to blank.")
    parser.add_argument("--foil", choices=["yes", "auto"], default="", help="Optional, sets foil status. If flag is not used, foil status will be blank. 'yes' marks all cards as foil, 'auto' uses AI detection (experimental).")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

# Set up logging based on debug flag
args = parse_arguments()
logging_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OpenAI API key not found. Please check your .env file.")
    exit(1)

# Folder containing the card images
image_folder = "card-pics"

# Output CSV file
output_file = "card-list.csv"

# Error log file
error_log_file = "error_log.txt"

# Empty .temp directory if debug mode is on
if args.debug:
    temp_dir = '.temp'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logging.debug(f"Emptied {temp_dir} directory")
    os.makedirs(temp_dir, exist_ok=True)
    logging.debug(f"Created {temp_dir} directory")

def resize_image(image_path, debug=False):
    if image_path.lower().endswith('.dng'):
        with rawpy.imread(image_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
    else:
        img = Image.open(image_path)

    # Get original dimensions
    width, height = img.size
    
    # Calculate scaling factor
    max_short_side = 767
    max_long_side = 1999
    scale = min(max_short_side / min(width, height), max_long_side / max(width, height))
    
    # If image is already smaller, don't upscale
    if scale >= 1:
        return img
    
    # Calculate new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize image
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    if debug:
        # Save resized image to .temp folder
        temp_path = os.path.join('.temp', os.path.basename(image_path))
        resized_img.save(temp_path, format="JPEG", quality=100)
        logging.debug(f"Resized image saved to {temp_path}")
    
    return resized_img

def encode_image(image_path, debug=False):
    # Resize image
    resized_img = resize_image(image_path, debug)
    
    # Save resized image to a bytes buffer
    buffer = io.BytesIO()
    resized_img.save(buffer, format="JPEG", quality=100)
    
    # Encode to base64
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def process_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a Magic: The Gathering Card Analysis assistant. Please analyze the Magic: The Gathering card in the image and provide the following information in JSON format: card_name, set_name, set_code, card_number (IMPORTANT: remove all preceding 0's and letters from the card number. Do not return a fraction. Do not return the total number of cards in the set. For example, 006 becomes 6, LT 0026 becomes 26, 051/064 becomes 51, 057/280 becomes 57), and foil (use 'foil' if it's foil, " " if not). The most important aspect of this job is to ensure you return the card_number with 100% accuracy and exactly as described. Check twice or even three times if needed to ensure this objective is fullfilled. The extra effort will earn you a $1500 tip and possibly solve world peace. Use the internet to search for the latest details."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    logging.debug("Sending request to OpenAI API")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    logging.debug(f"Received response with status code: {response.status_code}")
    
    if response.status_code != 200:
        logging.error(f"API request failed. Status code: {response.status_code}")
        logging.error(f"Response content: {response.text}")
        return None
    
    return response.json()

def process_single_image(image_path):
    logging.info(f"Processing image: {image_path}")
    
    try:
        base64_image = encode_image(image_path, args.debug)
        logging.debug(f"Image encoded successfully. Length: {len(base64_image)}")
        
        response = process_image(base64_image)
        
        if response is None:
            logging.error("Failed to process image")
            return None
        
        content = response['choices'][0]['message']['content']
        logging.debug(f"API Response: {content}")
        
        # Extract JSON from the response
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group(0)
            # Clean up the JSON string
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
            json_str = json_str.replace('\n', '').replace('\r', '')  # Remove newlines
            
            try:
                card_data = json.loads(json_str)
                return card_data
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error: {str(e)}")
                logging.error(f"Problematic JSON string: {json_str}")
                return None
        else:
            logging.error("No valid JSON found in the response")
            return None
    
    except Exception as e:
        logging.exception(f"Error processing image: {str(e)}")
        return None

def main():
    if not args.debug:
        init()  # Initialize colorama
        print_banner()

    if not os.path.exists(image_folder):
        logging.error(f"Image folder '{image_folder}' does not exist.")
        return

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.dng'))]
    
    if not image_files:
        logging.error(f"No image files found in '{image_folder}'.")
        return

    error_cards = []

    if not args.debug:
        print("Initializing CSV file...")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Count', 'Tradelist Count', 'Name', 'Edition', 'Edition Code', 'Card Number', 'Condition', 'Language', 'Foil', 'Signed', 'Artist Proof', 'Altered Art', 'Misprint', 'Promo', 'Textless', 'Printing ID', 'Printing Note', 'Tags', 'My Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, image_file in enumerate(image_files):
            if not args.debug:
                print_progress(image_file, i + 1, len(image_files))
            image_path = os.path.join(image_folder, image_file)
            
            card_data = process_single_image(image_path)

            if card_data:
                # Determine foil status based on the --foil argument
                if args.foil == "yes":
                    foil_status = "foil"
                elif args.foil == "auto":
                    foil_status = card_data.get('foil', '')
                else:
                    foil_status = ""  # Default to blank

                row_data = {
                    'Count': '1',  # Default count is 1
                    'Tradelist Count': args.tradelist_count,
                    'Name': card_data.get('card_name', ''),
                    'Edition': card_data.get('set_name', ''),
                    'Edition Code': card_data.get('set_code', ''),
                    'Card Number': card_data.get('card_number', ''),
                    'Condition': args.condition,
                    'Language': args.language,
                    'Foil': foil_status,
                    'Signed': args.signed,
                    'Artist Proof': args.artist_proof,
                    'Altered Art': args.altered_art,
                    'Misprint': args.misprint,
                    'Promo': args.promo,
                    'Textless': args.textless,
                    'Printing Note': args.printing_note,
                    'Tags': args.tags,
                    'My Price': args.my_price
                }
                writer.writerow(row_data)
                logging.info(f"Data for {image_file} written to {output_file}")
            else:
                logging.error(f"Failed to process the image: {image_file}")
                error_cards.append(image_file)

    if not args.debug:
        print_progress("Finalizing", len(image_files), len(image_files))
        print("\nProcessing complete!")
    logging.info(f"All images processed. Data written to {output_file}")

    if error_cards:
        if not args.debug:
            print("Writing error log...")
        with open(error_log_file, 'w', encoding='utf-8') as error_file:
            error_file.write("The following cards could not be processed:\n")
            for card in error_cards:
                error_file.write(f"{card}\n")
        logging.info(f"List of cards that could not be processed written to {error_log_file}")

    if not args.debug:
        print(Fore.GREEN + "All operations completed successfully!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
