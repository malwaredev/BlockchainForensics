import requests

def get_block_height_range_addresses_and_txids(start_block, end_block):
    addresses = set()
    txids = set()
    
    for block_height in range(start_block, end_block + 1):
        block_url = f"https://blockchain.info/rawblock/{block_height}"
        response = requests.get(block_url)
        block_data = response.json()
        
        for tx in block_data["tx"]:
            txids.add(tx["hash"])
            for input in tx["inputs"]:
                if "prev_out" in input and "addr" in input["prev_out"]:
                    addresses.add(input["prev_out"]["addr"])
            for output in tx["out"]:
                if "addr" in output:
                    addresses.add(output["addr"])
    
    return addresses, txids

# Prompt the user for the starting and ending block heights
start_block = int(input("Enter the starting block height: "))
end_block = int(input("Enter the ending block height: "))

try:
    # Get the list of addresses and transaction IDs
    addresses, txids = get_block_height_range_addresses_and_txids(start_block, end_block)
    
    # Save the output to a text file
    output_file = "blockchain_output.txt"
    with open(output_file, "w") as file:
        file.write("Addresses in the specified block height range:\n")
        for address in addresses:
            file.write(address + "\n")
        file.write("\nTransaction IDs in the specified block height range:\n")
        for txid in txids:
            file.write(txid + "\n")
    
    print(f"Output saved to {output_file}")
except KeyError as e:
    print(f"Error: {e}")
    print("The API response format may have changed. Please check the script and try again later.")
