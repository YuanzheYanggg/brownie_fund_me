// SPDX-License-Identifier: MIT

// 2:37:06
pragma solidity ^0.6.0;

// we import path from @chainlink
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // only needed for any solidity version under 0.8.0
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;

    address[] public addressArray;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        // grab ETH/USD conversion rate through Rinkeby test net
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    // notice when we change the state of blockchain, either when we deploy a new contract
    // or we make transactions instead of calls.
    // we can choose to deploy the massage with some value other than gas fee

    function fund() public payable {
        // we require that if user want to write fund function, a value of at least 50 dollars need to be sent with the transaction
        // we still need 8 decimals
        uint256 minNum = 50 * 1e8;
        require(
            // since normally our sending value have unit as gwei, but get conversionRate need amount in wei
            getConversionRate(msg.value * 1e9) >= minNum,
            "You need to spend more ETH."
        );
        addressToAmountFunded[msg.sender] += msg.value;
        addressArray.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // we need the address of the interface to perform our operation
        // since the interface that on the testnet or mainnet can give what we want.
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // we need to casting the answer to our demanded return type
        // we need to multiply by 1e9 because we need to convert ether to gwei
        // since the default decimal number is 8
        // which means the return value will in 1200 * 1e8 if current price is 1200 usd per eth
        return uint256(answer);
    }

    // we need a function to calculate the converted certain amount of ETH wei to US dollars
    function getConversionRate(uint256 _amount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        // ethPrice from previous calculation we got 2000 * 1e17
        // _amount is the amount of ether wei
        // still we have 8 decimals here
        uint256 ethAmountInUSD = (ethPrice * _amount) / 1e18;
        return ethAmountInUSD;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 1e8;
        uint256 price = getPrice();
        uint256 precision = 1 * 1e18;
        // it will return how many wei will satisfy the lowest amount of entrance fee
        return (mimimumUSD * precision) / price;
    }

    function withdrawAll() public payable onlyOwner {
        //require(msg.sender == owner, "Only owner can withdraw all the money.");
        msg.sender.transfer(address(this).balance);
        // we need to reset the addressToAmount to 0
        for (
            uint256 funderIndex = 0;
            funderIndex < addressArray.length;
            funderIndex++
        ) {
            addressToAmountFunded[addressArray[funderIndex]] = 0;
        }
        // we need 0 as a initializer to of our new address array, it representing 0x0
        // since in blockchain, addresses can only be contract address or other users account address
        addressArray = new address[](0);
    }
}
