pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract Sothebys {
    mapping(address => mapping(uint256 => listing)) public listings;
    mapping(address => uint256) public balances;

    struct listing {
        uint price;
        address seller;
        string title;
    }

    function addlisting(address contractAddr, uint price) public {
        ERC721 token = ERC721(contractAddr);
        require(token.balanceOf(msg.sender) > 0, "No token to add");
        require(token.isApprovedForAll(msg.sender, address(this)), "Token Sold");
    }

    function purchase(address contractAddr, uint256 tokenId) public payable {
        listing memory item = listings[contractAddr][tokenId];
        require(msg.value >= item.price, "Insufficient funds");
        balances[item.seller] += msg.value;

        ERC721 token = ERC721(contractAddr);
        token.safeTransferFrom(item.seller, msg.sender, tokenId);
    }

}