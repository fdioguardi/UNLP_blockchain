import pytest

from brownie import Ballot
from scripts.utils import get_account

CANDIDATES = ["Alice", "Bob", "Charlie"]


@pytest.fixture
def ballot():
    return Ballot.deploy(CANDIDATES, {"from": get_account()})


def test_deploy(ballot):
    assert ballot.getCandidateCount() == len(CANDIDATES)
    assert ballot.candidates(0) == (CANDIDATES[0], 0)
    assert ballot.candidates(1) == (CANDIDATES[1], 0)
    assert ballot.candidates(2) == (CANDIDATES[2], 0)
    assert ballot.isOpen()


def test_close_ballot(ballot):
    assert ballot.isOpen()
    ballot.closeBallot()
    assert not ballot.isOpen()


def test_simple_vote(ballot):
    ballot.vote(0)
    assert ballot.candidates(0) == (CANDIDATES[0], 1)
    assert ballot.candidates(1) == (CANDIDATES[1], 0)
    assert ballot.candidates(2) == (CANDIDATES[2], 0)


def test_unique_vote(ballot):
    ballot.vote(0)
    with pytest.raises(Exception):
        ballot.vote(0)
    with pytest.raises(Exception):
        ballot.vote(1)


def test_vote_out_of_range(ballot):
    with pytest.raises(Exception):
        ballot.vote(3)


def test_vote_after_closed(ballot):
    ballot.closeBallot()
    with pytest.raises(Exception):
        ballot.vote(0)


def test_get_winner(ballot):
    ballot.vote(1)
    assert ballot.getWinner() == CANDIDATES[1]
