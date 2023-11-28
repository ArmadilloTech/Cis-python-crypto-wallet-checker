import requests
from datetime import datetime
import time
import sys

# ANSI color codes
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
ENDC = '\033[0m'

def typing_effect(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def display_arm_logo():
    arm_logo = """
     █████╗ ██████╗ ███╗   ███╗
    ██╔══██╗██╔══██╗████╗ ████║
    ███████║██████╔╝██╔████╔██║
    ██╔══██║██╔══██╗██║╚██╔╝██║
    ██║  ██║██║  ██║██║ ╚═╝ ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
        ₿₿₿ BTC Checker ₿₿₿
    """
    typing_effect(arm_logo)

def get_current_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"]
    except requests.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def get_balance_and_tx_details(address, btc_to_usd):
    url = f"https://blockstream.info/api/address/{address}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        funded = data["chain_stats"]["funded_txo_sum"]
        spent = data["chain_stats"]["spent_txo_sum"]

        balance = funded - spent

        return {
            "balance": balance * 0.00000001,  # Convert to Bitcoin
            "balance_usd": balance * 0.00000001 * btc_to_usd,  # Convert to USD
            "funded": funded * 0.00000001,    # Convert to Bitcoin
            "funded_usd": funded * 0.00000001 * btc_to_usd,    # Convert to USD
            "spent": spent * 0.00000001,      # Convert to Bitcoin
            "spent_usd": spent * 0.00000001 * btc_to_usd       # Convert to USD
        }

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def save_to_file(address, details):
    with open("results.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Date & Time: {timestamp}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Current Balance: {details['balance']} BTC (${details['balance_usd']:.2f} USD)\n")
        file.write(f"Total Received: {details['funded']} BTC (${details['funded_usd']:.2f} USD)\n")
        file.write(f"Total Spent: {details['spent']} BTC (${details['spent_usd']:.2f} USD)\n")
        file.write("-" * 40 + "\n")

if __name__ == "__main__":
    display_arm_logo()  # Display the ARM logo with animation
    btc_to_usd = get_current_btc_price()
    if btc_to_usd is not None:
        address = input("Enter the Bitcoin address: ")
        details = get_balance_and_tx_details(address, btc_to_usd)

        if details is not None:
            print("\n" + "-" * 40)
            print(f"{YELLOW}Address: {address}{ENDC}")
            print(f"{GREEN}Current balance: {details['balance']} BTC (${details['balance_usd']:.2f} USD){ENDC}")
            print(f"{BLUE}Total Received: {details['funded']} BTC (${details['funded_usd']:.2f} USD){ENDC}")
            print(f"{RED}Total Spent: {details['spent']} BTC (${details['spent_usd']:.2f} USD){ENDC}")
            print("-" * 40 + "\n")
            
            save_to_file(address, details)
        else:
            print(f"Couldn't retrieve details for address {address}.")
    else:
        print("Failed to fetch the current Bitcoin price.")
