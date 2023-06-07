# Streamlit Application

# Imports
import streamlit as st

# Import the functions from ethereum.py
from sothebys import addlisting
from sothebys import purchase

################################################################################

# Import the functions from sothebys.sol
art_listing = addlisting()
purchase = purchase()


################################################################################
# Streamlit Code

# Streamlit application headings
st.markdown("# NFT Art Bidding")
st.text("\n")
st.markdown("## Purchase")

# Write the Ethereum account address to the Streamlit page
st.write(purchase)