// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

struct Candidate {
    string name;
    uint8 voteCount;
}

contract Ballot {
    Candidate[] public candidates;
    bool public isOpen = true;
    mapping(address => bool) public hasVoted;

    event Voted(address indexed by, string candidate);

    constructor(string[] memory candidateNames) {
        for (uint256 i = 0; i < candidateNames.length; i++) {
            candidates.push(Candidate({name: candidateNames[i], voteCount: 0}));
        }
    }

    function vote(uint256 candidateIndex) external {
        require(isOpen, "Voting is closed");
        require(!hasVoted[msg.sender], "You have already voted");
        require(candidateIndex < candidates.length, "Invalid candidate index");

        candidates[candidateIndex].voteCount += 1;
        hasVoted[msg.sender] = true;

        emit Voted(msg.sender, candidates[candidateIndex].name);
    }

    function closeBallot() external {
        isOpen = false;
    }

    function getWinner() public view returns (string memory) {
        uint256 winningVoteCount = 0;
        uint256 winningCandidateIndex = 0;

        for (uint256 i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > winningVoteCount) {
                winningVoteCount = candidates[i].voteCount;
                winningCandidateIndex = i;
            }
        }

        return candidates[winningCandidateIndex].name;
    }

    function getCandidateCount() public view returns (uint256) {
        return candidates.length;
    }
}
