pragma solidity ^0.7.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract Sothebys {
    mapping(address => mapping(uint256 => listing)) public listings;
    mapping(address => uint256) public balances;

    // Current state of the auction.
    address public highestBidder;
    uint public highestBid;

    struct listing {
        uint price;
        address seller;
        string title;
        bool auctionEnded;
    }

    function addListing(address contractAddr, uint price) public {
        ERC721 token = ERC721(contractAddr);
        require(token.balanceOf(msg.sender) > 0, "No token to add");
        require(token.isApprovedForAll(msg.sender, address(this)), "Token not approved for transfer");
        listings[contractAddr][token.tokenOfOwnerByIndex(msg.sender, 0)] = listing(price, msg.sender, "Title", false);
    }

    function bid(address contractAddr, uint256 tokenId) public payable {
        listing storage item = listings[contractAddr][tokenId];
        require(!item.auctionEnded, "Auction already ended");
        require(msg.value > item.price, "There already is a higher bid");

        if (item.price != 0) {
            // Refund the previous bidder.
            balances[highestBidder] += highestBid;
        }
        highestBidder = msg.sender;
        highestBid = msg.value;
        item.price = msg.value;
    }

    function purchase(address contractAddr, uint256 tokenId) public payable {
        listing memory item = listings[contractAddr][tokenId];
        require(msg.value >= item.price, "Insufficient funds");
        balances[item.seller] += msg.value;

        ERC721 token = ERC721(contractAddr);
        token.safeTransferFrom(item.seller, msg.sender, tokenId);
        item.auctionEnded = true;
    }
}
