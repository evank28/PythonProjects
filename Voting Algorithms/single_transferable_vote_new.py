
import math
import operator
import sys
from copy import copy
from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Set, Tuple


def format_results(results_dict: dict) -> str:
    """
    Returns a multiline string to represent the numeric results of a tally that
    was stored and passed to the function as a dictionary.
    >>> format_results({'Mary Jane': 25, 'Alex Brown':52, 'John Smith':43})
    Mary Jane: 25
    Alex Brown: 52
    John Smith: 43
    """
    return "\n".join(f"{candidate}: {result}" for candidate, result in results_dict.items())


class Ballot:
    uid: str
    active_choice: int = 1
    rejected: bool = False
    ranking: Dict[int, str]

    def __init__(self, uid: str, ranking: Dict[int, str]):
        self.uid = uid
        self.ranking = ranking

    def __repr__(self):
        return f"{self.uid}: {self.ranking}"


def count_stv_for_one_winner(ballots: Dict[str, Ballot], candidates_in: Dict[str, int],
                             eliminated_in: Set[str], details: bool) -> Tuple[str, str]:
    """
       Takes a dictionary of ballots and
       returns the winner(s) per the Single Transferable Vote algorithm, as well as
       the details if requested.
       """
    # tabulates any rejected ballots
    rejected = {k: v for k, v in ballots.items() if not v}
    # deletes any rejected ballots, and makes a copy of the ballots
    ballots = {k: copy(v) for k, v in ballots.items() if v}
    candidates = copy(candidates_in)

    cur_ballot_count = 1    # Is this the first round of balloting? The second?
    winner_found = False
    detailed_results = ""
    eliminated = copy(eliminated_in)
    late_rejected_ballots = {}
    # loop through the ballots dictionary
    # if len(candidates) == 1:
    #     winner = list(candidates.keys())[0]
    #     result_string = f"As the only candidate (left), {winner} is declared winner immediately."
    #     result_string += format_results(len(ballot for ballot ))
    #     return ,  winner
    while not winner_found and len(candidates) >= 1:
        for uid, ballot in ballots.items():
            # iterate through the ballots dictionary,
            # calculating/recalculating the sum
            viable_ballot = False  # actually we don't know at this stage
            while not viable_ballot:
                # count the first place vote on each ballot and sum it in
                # another dictionary with all the values called options
                choice = ballot.ranking[ballot.active_choice]
                # any time a ballot is encountered where the first place vote
                # has been eliminated, iterate down the ballot until an option
                # that has not been eliminated is available
                if choice == "Abstain":
                    ballot.rejected = True
                    break

                if choice in eliminated:
                    ballot.active_choice += 1
                    if ballot.active_choice > len(ballot.ranking):
                        ballot.rejected = True
                        break
                else:
                    candidates[choice] += 1
                    viable_ballot = True

            if not viable_ballot:
                # if all options on the ballot have been eliminated, remove the
                # ballot from the ballots dictionary and add it to the
                # late_rejected_ballots dictionary
                if ballot.active_choice == 1:
                    rejected.setdefault(uid, ballot)
                else:
                    late_rejected_ballots.setdefault(uid, ballot)
                # late_rejected_ballots.setdefault(uid, ballot)

        for uid in chain(late_rejected_ballots.keys(), rejected.keys()):
            if uid in ballots:
                del ballots[uid]

        detailed_results += "\n##########\n" + "COUNT {} RESULTS:\n".format(
            cur_ballot_count) + format_results(candidates)
        if cur_ballot_count == 1:
            detailed_results += "\nRejected: " + str(len(rejected)) + "\n"
            # detailed_results += "\nTotal Turnout: " + str(len()) + "\n"
        late_rejects = len(late_rejected_ballots)
        if late_rejects >= 1:
            detailed_results += "\nLate Rejected: " + str(late_rejects) + "\n"
        # if the top option has over 50% of the eligible votes, declare it the
        # winner and break from the loop

        if max(candidates.values()) >= (math.floor(len(ballots) / 2) + 1):
            winner_found = True
            winner = max(candidates.items(), key=operator.itemgetter(1))[0]
            detailed_results += f"\n* {winner} is declared as the winner.\n"
        # otherwise, pop out the minimum option and add it's key to the list
        # eliminated. Continue looping through
        else:
            to_eliminate = min(candidates.items(), key=operator.itemgetter(1))[0]
            eliminated.add(to_eliminate)
            try:
                del candidates[to_eliminate]
            except:
                print(f"Error deleting {to_eliminate} on count #{cur_ballot_count}",
                      file=sys.stderr)
            detailed_results += f"\n* {to_eliminate} was eliminated.\n"
            cur_ballot_count += 1
            for key in candidates:
                candidates[key] = 0

    if winner_found:
        if details:
            return f"{winner} is the winner. \n\n {detailed_results}", winner
        return f"{winner} is the winner.", winner
    # if the ballots dictionary is empty and no winner has been declared,
    # log an error
    else:
        return f"ERROR: No winner found. \n {detailed_results}", None


def count_stv(ballots: Dict[str, Ballot],
              candidates_in: Dict[str, int],
              details: bool,
              number_of_winners: int = 1) -> Tuple[List[str], str]:
    """
    Takes a dictionary of ballots and
    returns the winner(s) per the Single Transferable Vote algorithm, as well as
    the details if requested.
    """
    cumulative_results = ""
    candidates_declared = 0
    candidates = copy(candidates_in)
    eliminated = set()
    winners = []
    while candidates_declared < number_of_winners:
        results, winner = count_stv_for_one_winner(ballots, candidates, eliminated, details)
        cumulative_results += f"RESULT FOR WINNER #{candidates_declared + 1}:\n"
        cumulative_results += results
        eliminated.add(winner)
        winners.append(winner)
        if winner in candidates:
            del candidates[winner]
        candidates_declared += 1

        if candidates_declared < number_of_winners:
            cumulative_results += f"Before the next count, " \
                                  f"already-declared winner {winner} is eliminated.\n\n"
    return winners, cumulative_results

