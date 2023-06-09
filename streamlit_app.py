# Streamlit app code for Auction House NFTs

import streamlit as st
from web3 import Web3
import time
import json
import os
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

################################################################################
# Load_Contract Function
################################################################################
def load_contract():

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS") #'0x4a46A8464DE04b9Ae6310B77792F5088b89993Dc' 
    
    # read file with ABI json
    with open('json/contract_ABI.json', 'r') as myfile:
        contract_json = myfile.read()
    
    contract_abi = json.loads(contract_json)

    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    
    return contract

# Load the contract
contract = load_contract()

###############################################################################
# Helper functions to pin files and json to Pinata
################################################################################

# Set Streamlit theme
st.set_page_config(layout="wide", page_title="Auction House NFTs")

# Title
st.title("Auction House NFTs")

# Token ID
token_id = st.number_input('Enter token ID', min_value=1, step=1)

# Get image and fable
image_path = Path("Images/frog_king_1.png")# replace with your actual path
#fable_path = f"nft_art_bidding/Fable_Fiction.ipynb/{token_id}.ipynb"  # replace with your actual path

if os.path.exists(image_path): #and os.path.exists(fable_path):
    # Display image
    image = Image.open(image_path)
    st.image(image, caption=f"Token ID: {token_id}", use_column_width=True)

    # Display fable
    with open(fable_path, 'r') as f:
        fable = json.load(f)
    st.markdown(f"## Fable")
    st.markdown(fable['cells'][0]['source'][0])  # assuming the fable is in the first cell of the notebook

    # Get auction details
    auction = contract.functions.Auctions(token_id).call()
    st.markdown(f"## Current Highest Bid: {web3.fromWei(auction[3], 'ether')} ETH")

    # Calculate time left
    current_block = web3.eth.blockNumber
    end_block = auction[1]
    blocks_left = end_block - current_block
    # Assuming ~15 seconds per block
    time_left = blocks_left * 15
    st.markdown(f"## Time Left: {time.strftime('%H:%M:%S', time.gmtime(time_left))}")
else:
    st.markdown("## Invalid token ID or the files do not exist.")
