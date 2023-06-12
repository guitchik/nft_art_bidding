# Streamlit app code for Auction House NFTs and Pinata Helper Functions

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
# Load_Contract Function for ABI and Ganache smart contract address
################################################################################
def load_contract():

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")  
    
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
###############################################################################

def pin_bid(artwork_file, selected_artwork_name):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)

    # Build a token metadata file for the artwork
    token_json = {
        "name": selected_artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_bid_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

################################################################################
# STREAMLIT CODE FOR FRONTEND!!!
################################################################################

# Set Streamlit theme and page title
#st.set_page_config(layout="wide", page_title="Auction House NFTs")

# Set Title 
st.markdown("<h1 style='text-align: center; color: white;'>Auction House NFTs</h1>", unsafe_allow_html=True)

st.markdown("---")




# Choose your Favorite Image to Bid On
st.markdown("## Choose your Favorite Art to Bid On")

# Specify the directory where your images are
image_dir = 'Images2'

# List all files in the directory
image_files = os.listdir(image_dir)

# Remove extensions from file names
image_names = [os.path.splitext(file)[0] for file in image_files]

# Create a dictionary to map image names to their files
image_dict = dict()
for i, image_name in enumerate(image_names):
    image_dict[image_name] = image_files[i]

# Create a selectbox for the image names
selected_artwork_name = st.selectbox('Choose an image', image_names)

# Get the corresponding image file
artwork_file = image_dict[selected_artwork_name]

# Display the selected image
st.image(os.path.join(image_dir, artwork_file))

st.markdown("---")




# Select Wallet, Bidder's Name, Initial Bid, and Pin artwork to bid"
st.markdown("## Choose a wallet account to start bidding!")

accounts = web3.eth.accounts
#tokens = contract.functions.totalSupply().call()

bidder = st.selectbox("Select Account", options=accounts)
#token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
newbid = st.text_input("Enter your initial bid (in Ether)")


if st.button("Start Bidding!"):
    # Use the `pin_bid` helper function to pin the file to IPFS
    artwork_ipfs_hash, token_json = pin_bid(artwork_file, selected_artwork_name)

    artwork_uri = f"ipfs://{artwork_ipfs_hash}"

    tx_hash = contract.functions.bidOnAuction(
        #token_id,
        bidder,
        int(newbid),
        #artwork_uri,
        #token_json['image']
    ).transact({'from': bidder, 'gas': 1000000})
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    #st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    #st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    #st.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

st.markdown("---")
