import requests
from datetime import datetime

def get_balance_and_tx_details(address):
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
            "funded": funded * 0.00000001,    # Convert to Bitcoin
            "spent": spent * 0.00000001       # Convert to Bitcoin
        }

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def save_to_file(address, details):
    with open("results.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Date & Time: {timestamp}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Current Balance: {details['balance']} BTC\n")
        file.write(f"Total Received: {details['funded']} BTC\n")
        file.write(f"Total Spent: {details['spent']} BTC\n")
        file.write("-" * 40 + "\n")

if __name__ == "__main__":
    address = input("Enter the Bitcoin address: ")
    details = get_balance_and_tx_details(address)

    if details is not None:
        print("\n" + "-" * 40)
        print(f"Address: {address}")
        print(f"Current balance: {details['balance']} BTC")
        print(f"Total Received: {details['funded']} BTC")
        print(f"Total Spent: {details['spent']} BTC")
        print("-" * 40 + "\n")
        
        save_to_file(address, details)
    else:
        print(f"Couldn't retrieve details for address {address}.")

        # futre features
        # 1.List all transactions with the amount and history
        # 2. see if any transactions are consistent and try to connect them (possible fraud/ laundering)
        # 3.add multiple input addresses
        # 4. add gui or add colors to console
        # 5. add error handling instead of just displaying
        # 6. currency selector


        #USE ADRUINO TO DISPLAY CURRENT PORTFOLIO VALUE BASED ON CURRENT PRICE
