// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract Counter {
    uint8 private counter;
    address public owner;
    mapping(address => bool) public whitelist;

    event CounterModified(address indexed by, string operation, uint8 newValue);

    constructor() {
        owner = msg.sender;
        whitelist[owner] = true;
    }

    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "Not authorized: not in whitelist");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can manage whitelist");
        _;
    }

    function addToWhitelist(address _address) external onlyOwner {
        whitelist[_address] = true;
    }

    function removeFromWhitelist(address _address) external onlyOwner {
        delete whitelist[_address];
    }

    function increment() external onlyWhitelisted {
        counter += 1;
        emit CounterModified(msg.sender, "increment", counter);
    }

    function decrement() external onlyWhitelisted {
        counter -= 1;
        emit CounterModified(msg.sender, "decrement", counter);
    }
}
