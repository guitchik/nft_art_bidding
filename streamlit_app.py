# Streamlit app code for Auction House NFTs

import streamlit as st
from web3 import Web3
import time
import json
import os
from PIL import Image
from pathlib import Path

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Contract address and ABI
contract_address = '0xe242c4Bb7EE83C615Ef53b49c42d33937BF21Ef7'  # replace with your contract address
    
contract_abi = '''
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "to",
				"type": "address"
			},
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "tokenID",
				"type": "uint256"
			},
			{
				"name": "bidder",
				"type": "address"
			},
			{
				"name": "newbid",
				"type": "uint256"
			}
		],
		"name": "bidOnAuction",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "tokenID",
				"type": "uint256"
			},
			{
				"name": "owner",
				"type": "address"
			}
		],
		"name": "endAuction",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "tokenID",
				"type": "uint256"
			},
			{
				"name": "newAppraisalValue",
				"type": "uint256"
			},
			{
				"name": "reportURI",
				"type": "string"
			},
			{
				"name": "tokenJSON",
				"type": "string"
			}
		],
		"name": "newAppraisal",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "owner",
				"type": "address"
			},
			{
				"name": "name",
				"type": "string"
			},
			{
				"name": "artist",
				"type": "string"
			},
			{
				"name": "description",
				"type": "string"
			},
			{
				"name": "initialAppraisalValue",
				"type": "uint256"
			},
			{
				"name": "tokenURI",
				"type": "string"
			},
			{
				"name": "tokenJSON",
				"type": "string"
			}
		],
		"name": "registerArt",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "from",
				"type": "address"
			},
			{
				"name": "to",
				"type": "address"
			},
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "from",
				"type": "address"
			},
			{
				"name": "to",
				"type": "address"
			},
			{
				"name": "tokenId",
				"type": "uint256"
			},
			{
				"name": "_data",
				"type": "bytes"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "to",
				"type": "address"
			},
			{
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "setApprovalForAll",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "tokenID",
				"type": "uint256"
			},
			{
				"name": "startPrice",
				"type": "uint256"
			},
			{
				"name": "endBlock",
				"type": "uint256"
			},
			{
				"name": "bidder",
				"type": "address"
			}
		],
		"name": "startAuction",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "from",
				"type": "address"
			},
			{
				"name": "to",
				"type": "address"
			},
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "tokenID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "appraisalValue",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "reportURI",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "artJson",
				"type": "string"
			}
		],
		"name": "Appraisal",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "to",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "approved",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "operator",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "ApprovalForAll",
		"type": "event"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Auctions",
		"outputs": [
			{
				"name": "startPrice",
				"type": "uint256"
			},
			{
				"name": "endBlock",
				"type": "uint256"
			},
			{
				"name": "highestBidder",
				"type": "address"
			},
			{
				"name": "highestBid",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "baseURI",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Gallery",
		"outputs": [
			{
				"name": "name",
				"type": "string"
			},
			{
				"name": "artist",
				"type": "string"
			},
			{
				"name": "description",
				"type": "string"
			},
			{
				"name": "appraisalValue",
				"type": "uint256"
			},
			{
				"name": "artJson",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "getApproved",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "tokenID",
				"type": "uint256"
			}
		],
		"name": "imageURI",
		"outputs": [
			{
				"name": "imageJson",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "owner",
				"type": "address"
			},
			{
				"name": "operator",
				"type": "address"
			}
		],
		"name": "isApprovedForAll",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "ownerOf",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "interfaceId",
				"type": "bytes4"
			}
		],
		"name": "supportsInterface",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "tokenByIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "owner",
				"type": "address"
			},
			{
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "tokenOfOwnerByIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "tokenURI",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
'''

contract_abi = json.loads(contract_abi)

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set Streamlit theme
st.set_page_config(layout="wide", page_title="Auction House NFTs")

# Title
st.title("Auction House NFTs")

# Token ID
token_id = st.number_input('Enter token ID', min_value=1, step=1)

# Get image and fable
image_path = f"nft_art_bidding/images/{token_id}.png"  # replace with your actual path
fable_path = f"nft_art_bidding/Fable_Fiction.ipynb/{token_id}.ipynb"  # replace with your actual path

if os.path.exists(image_path) and os.path.exists(fable_path):
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
