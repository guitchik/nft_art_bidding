pragma solidity ^0.5.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
contract Etsy is ERC721Full {
    constructor() public ERC721Full("Art Registery Token", "ART") {}
    struct Artwork {
        string name;
        string artist;
        string description;
        uint256 appraisalValue;
        string artJson;
    }
    struct Auction {
        uint256 startPrice;
        uint256 endBlock;
        address highestBidder;
        uint256 highestBid;

        //new
        //event Auction(uint256 tokenID, uint256 highestBid, address bidder);
    }
    mapping(uint256 => Artwork) public Gallery;
    mapping(uint256 => Auction) public Auctions;

    event Appraisal(uint256 tokenID, uint256 appraisalValue, string reportURI, string artJson);
    function imageURI(
        uint tokenID
    ) public view returns (string memory imageJson) {
        return Gallery[tokenID].artJson;
    }
    function registerArt(
        address owner,
        string memory name,
        string memory artist,
        string memory description,
        uint256 initialAppraisalValue,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenID = totalSupply();
        _mint(owner, tokenID);
        _setTokenURI(tokenID, tokenURI);
        Gallery[tokenID] = Artwork(name, artist, description, initialAppraisalValue, tokenJSON);
        return tokenID;
    }
    function newAppraisal(
        uint256 tokenID,
        uint256 newAppraisalValue,
        string memory reportURI,
        string memory tokenJSON
    ) public returns (uint256) {
        Gallery[tokenID].appraisalValue = newAppraisalValue;
        emit Appraisal(tokenID, newAppraisalValue, reportURI, tokenJSON);
        return (Gallery[tokenID].appraisalValue);
    }
    function startAuction(uint256 tokenID, uint256 startPrice, uint256 endBlock, address bidder) public {
        require(msg.sender == ownerOf(tokenID), "Only owner can start auction");
        // startPrice == highestBid;
        bidder == msg.sender;
        require(endBlock > block.number, "End block must be in the future");
        Auctions[tokenID] = Auction(startPrice, endBlock, address(0), 0);
    }
    function bidOnAuction(uint256 tokenID, address bidder, uint256 newbid) public payable {
        require(Auctions[tokenID].endBlock > block.number, "Auction has ended");
        require(newbid > Auctions[tokenID].startPrice, "Bid must be higher than current highest bid");
        Auctions[tokenID].highestBidder = bidder;
        Auctions[tokenID].highestBid = newbid;
        
    }
    function endAuction(uint256 tokenID, address owner) public {
        require(Auctions[tokenID].endBlock == block.number, "Auction is not yet ended");
        require(owner == ownerOf(tokenID), "Only owner can end auction");
        // Transfer the token to the highest bidder
        _transferFrom(ownerOf(tokenID), Auctions[tokenID].highestBidder, tokenID);
        // Transfer the bid amount to the previous owner
        msg.sender.transfer(Auctions[tokenID].highestBid);
    }
}