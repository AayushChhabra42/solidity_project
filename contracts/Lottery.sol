//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";


contract Lottery is VRFConsumerBase{
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public UsdEntry_Fee;
    AggregatorV3Interface internal ethusdpricefeed;
    enum Lottery_State{
        Open,
        Closed,
        Calculating_Winner
    }
    Lottery_State public lottery_state;
    //Thes states in enum are represented by numbers,(0,1,2,respectively).
    uint256 public fee;
    bytes32 public keyhash;
    event requestrandomness(bytes32 RequestID);

    constructor(address _pricefeedaddress , address vrf_coordinator,  address link , uint256 _fee, bytes32 _keyhash) public VRFConsumerBase(vrf_coordinator,link){
        UsdEntry_Fee = 5 * (10 ** 18);
        ethusdpricefeed = AggregatorV3Interface(_pricefeedaddress);
        lottery_state=Lottery_State.Closed;
        fee=_fee;
        keyhash=_keyhash;
    }
    function enter() public payable{
        // minimum price of 50 dollars
        require(lottery_state==Lottery_State.Open,"Lottery Not Open yet");
        require(msg.value >= Get_Entrance_fee(),"Not Enough Eth!");
        players.push(msg.sender);

    }

    function Get_Entrance_fee() public view returns (uint256){
        (,int price,,,) = ethusdpricefeed.latestRoundData();
        uint256 adjustedprice = uint256(price) * 10**10; //18 decimals
        uint256 costtoenter = (UsdEntry_Fee * 10 ** 18)/adjustedprice;
        return costtoenter;
    }

    function StartLottery() public {
        require(lottery_state==Lottery_State.Closed,"sorry can't open lottery yet");
        lottery_state=Lottery_State.Open;
    }

    function EndLottery() public {
        lottery_state=Lottery_State.Calculating_Winner;
        bytes32 RequestID = requestRandomness(keyhash,fee);
        emit requestrandomness(RequestID);
    }
    function fulfillRandomness(bytes32 _RequestID, uint256 _randomness) internal override {
        require(lottery_state==Lottery_State.Calculating_Winner,"Lottery not done yet");
        require(_randomness>0,"Random-not-found");
        uint256 IndexOfWinner = _randomness % players.length;
        recentWinner = players[IndexOfWinner];
        recentWinner.transfer(address (this).balance);
        //reset
        players = new address payable[](0);
        lottery_state=Lottery_State.Closed;
        randomness = _randomness;
    }

}