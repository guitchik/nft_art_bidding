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
   mapping(uint256 => Artwork) public Gallery;
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
}