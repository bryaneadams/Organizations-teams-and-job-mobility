import pandas as pd
import uuid
import math
from typing import Union


def build_team_dict(df: pd.DataFrame) -> dict:
    """Provide a data frame of data for a given month of data
    and get back dict of the teams found in that month

    Args:
        df (pd.DataFrame): One month of data in a pd.DataFrame

    Returns:
        dict: dict of teams found that month
    """
    # creates a list of unique supervisors
    supervisor_keys = build_supervisor_list(df)

    team_dict = {}

    for i in supervisor_keys:
        uid = str(uuid.uuid4()).replace("-", "")[:10]
        while uid in team_dict:
            uid = str(uuid.uuid4()).replace("-", "")[:10]

        # Determine if a team is terminal
        team_members = determine_terminal_teams(df, i, supervisor_keys)

        if team_members:
            # Start the team
            team_dict[uid] = {}

            # Add supervisor
            team_dict[uid]["supervisor"] = i

            # Add team members

            team_dict[uid]["team_members"] = team_members

            # Get list of UICs for team members in the event they are different

            temp_uic = list(set(df[df["MASTERKEY"].isin(team_members)]["UIC"]))
            # Sort uics and remove NaN
            temp_uic = sorted([x for x in temp_uic if not isinstance(x, float)])
            team_dict[uid]["uic"] = temp_uic
            # Determine if the supervisor UIC is different
            try:
                supervisor_uic = df[df["MASTERKEY"] == i].iloc[0]["UIC"]
                if supervisor_uic not in team_dict[uid]["uic"]:
                    if not isinstance(supervisor_uic, float):
                        team_dict[uid]["uic"].append(supervisor_uic)

            except:
                pass

            # Add team size and include supervisor
            team_dict[uid]["team_size"] = len(team_dict[uid]["team_members"]) + 1

            # Make a unique hash
            team_dict[uid]["hash"] = hash(
                (
                    team_dict[uid]["supervisor"],
                    str(team_dict[uid]["team_members"]),
                    str(team_dict[uid]["uic"]),
                )
            )

    return team_dict


def build_supervisor_list(df: pd.DataFrame) -> list:
    """Generates a list of supervisors for a dataframe

    Args:
        df (pd.DataFrame): One month of data

    Returns:
        list: list of supervisors with NaN removed
    """

    supervisor_keys = list(df["SUPERVISOR MASTERKEY"].unique())
    supervisor_keys = list(filter(lambda x: not math.isnan(x), supervisor_keys))
    return supervisor_keys


def determine_terminal_teams(
    df: pd.DataFrame, supervisor: Union[int, float, str], supe_keys: list
) -> Union[list, None]:
    """This function determines if a team is terminal. If any team member is also a supervisor
    This function will return None, otherwise it will return a list of the team members.
    It has also been modified to remove supervisors only supervising themselves from the list of
    team members.

    Args:
        df (pd.DataFrame): data for a given month
        supervisor (Union[int, float, str]): The supervisor of the team
        supe_keys (list): list of supervisor keys

    Returns:
        Union[list, None]: list of team members' MASTERKEY if a team is terminal otherwise None
    """
    team_members = list(df[df["SUPERVISOR MASTERKEY"] == supervisor]["MASTERKEY"])
    # There were some use cases where the supervisor was part of the team
    # and a supervisor who only supervised themselves
    team_members = [tm for tm in team_members if tm != supervisor]

    if len(team_members) == 0:
        return None

    if len(set(team_members).intersection(set(supe_keys))) > 0:
        return None

    return team_members


def create_linked_team(team_dict: dict, month: str, uid: str) -> dict:
    """Generates a new entry required for linking teams. The body initially
    created is then updated as months are looped through. This function is used
    to initiate the linked_teams and used again to add a new team

    Args:
        team_dict (dict): the dict of teams by month
        month (str): The month of interest
        uid (str): the uid of the team of interest

    Returns:
        dict: The dict of a new team to add to the linked_teams dict.
    """
    linked_team = {
        "last_hash": team_dict[month][uid]["hash"],
        "team_uuids": [uid],
        "last_supervisor": team_dict[month][uid]["supervisor"],
        "last_uic": team_dict[month][uid]["uic"],
        "last_team_members": team_dict[month][uid]["team_members"],
        "last_month_matched": month,
    }
    return linked_team


def update_team(lt: dict, td: dict) -> dict:
    """
    This function is used to update the running "last team dict."

    Args:
        lt (dict): The linked team dict that will be updated.
        td (dict): Team dict that will be used to update the running linked team dict

    Returns:
        dict: The updated running linked team dict.
    """
    lt["last_supervisor"] = td["supervisor"]
    lt["last_hash"] = td["hash"]
    lt["last_uic"] = td["uic"]
    lt["last_team_members"] = td["team_members"]
    return lt


class LinkedTeams:
    def __init__(self, df_dict, month_list):
        self.df_dict = df_dict
        self.month_list = month_list
        self.lineage_dict_departure = {}
        self.lineage_dict_arrival = {}
        self.team_dicts_by_month = {}

    def create_team_dicts(self):
        for month, df in self.df_dict.items():
            print("building month - {}".format(month))
            self.team_dicts_by_month[month] = build_team_dict(df)

    def determine_coordinated(
        self, people: list, month: str, departure: bool = True
    ) -> bool:
        """This is designed to see if there is a coordinated move. Your provide the function the team members that departed the team and the month they departed. We then look to see who their supervisors are the following month. If there is a supervisor match between the group, we return True - that it is a coordinated move, if not we return False - that it is not a coordinated move.

        Args:
            group (list): List of team members that departed
            month (str): month the team members departed
            departure (bool): used to determine which month to look at, for arrivals you need to look at where the difference came from and make sure they did not come from the same team, if departure, you need to look at where they went to.

        Returns:
            bool: True if it is coordinated, False if it is not coordinated
        """

        supe_list = {True: self.new_supes, False: self.last_supes}

        if not departure:
            month_index = self.month_list.index(month)
            month = self.month_list[month_index - 1]

        # Used to check for coordinated arrivals with a supervisor and
        # their subordinate
        supe_arrivals = set(people).intersection(supe_list[departure])
        if len(supe_arrivals) > 0:
            for supe in supe_arrivals:
                subordinates = set(
                    self.df_dict[month][
                        self.df_dict[month]["SUPERVISOR MASTERKEY"] == supe
                    ]["MASTERKEY"].to_list()
                )

                if len(subordinates.intersection(set(people))) > 0:
                    return True

        supervisor_list = self.df_dict[month][
            self.df_dict[month]["MASTERKEY"].isin(people)
        ]["SUPERVISOR MASTERKEY"].to_list()

        coordinated = len(supervisor_list) != len(set(supervisor_list))

        return coordinated

    def find_optimal_match(
        self, prior: str, possible_teams: list[str], month: str
    ) -> Union[str, None]:
        """At times there is a need to find a match for a team that has changed based on a supervisor change

        Args:
            prior (str): team dictionary
            possible_teams (list[str]): Other teams
            month (str): current month

        Returns:
            Union[str, None]: matched team or None (None is no longer used)
        """
        prior_team = set(self.linked_teams[prior]["last_team_members"])
        prior_supervisor = self.linked_teams[prior]["last_supervisor"]
        possible_size_matches = {}

        for team in possible_teams:
            possible_team = set(self.team_dicts_by_month[month][team]["team_members"])
            possible_size_matches[team] = len(prior_team.intersection(possible_team))

        possible_matches = [
            key for key, value in possible_size_matches.items() if value > 1
        ]
        # print(possible_matches)
        if len(possible_matches) == 1:
            return possible_matches[0]
        else:
            for team in possible_teams:
                if (
                    self.team_dicts_by_month[month][team]["supervisor"]
                    == prior_supervisor
                ):
                    return team
        return None

    def build_linked_team_dict(self) -> dict:
        """This is the logic used to create linked teams

        Args:
            team_dicts_by_month (dict): the teams found by month

        Returns:
            dict: a dict of all the teams that have been linked
        """
        # self.team_dicts_by_month = team_dicts_by_month
        month_keys = sorted(self.team_dicts_by_month)

        # Create the initial set of teams
        self.linked_teams = {}
        start_month = month_keys[0]
        for uid in self.team_dicts_by_month[start_month].keys():
            self.linked_teams[uid] = create_linked_team(
                self.team_dicts_by_month, start_month, uid
            )

        # Used to check if an unmatched team
        # Can be matched using a Jaccard Index
        new_teams_by_month = {}
        month_count = 1
        possible_teams = {}
        for month in month_keys[1:]:
            print("linking month - {}".format(month))

            # TODO can this help with a coordinated move with supervisor
            self.last_supes = set(
                self.df_dict[month_keys[month_count - 1]][
                    "SUPERVISOR MASTERKEY"
                ].to_list()
            )
            self.new_supes = set(self.df_dict[month]["SUPERVISOR MASTERKEY"].to_list())

            month_count += 1
            # create the month key for new teams and initialize as an empty dict
            # The dit will consist of uid: team_make_up
            new_teams_by_month[month] = {}

            possible_teams[month] = {}

            month_index = self.month_list.index(month)
            last_month = self.month_list[month_index - 1]

            # iterate through the teams in a given month
            # for key, value in self.team_dicts_by_month[month].items():
            for key in self.team_dicts_by_month[month].keys():
                # This is used to keep track of if the team is matched
                matched = False

                # iterate through the team to check for matching criteria
                for k, v in self.linked_teams.items():

                    # Check if the team was linked the previous month
                    # If not you want to pass over it because it died
                    if v["last_month_matched"] == last_month:
                        # keep track of new teams that could be linked if
                        # on criteria is not met.

                        # Check to see if two or more team members left the team
                        prior_team = set(self.linked_teams[k]["last_team_members"])
                        possible_new_team = set(
                            self.team_dicts_by_month[month][key]["team_members"]
                        )

                        team_departed = prior_team - prior_team.intersection(
                            possible_new_team
                        )

                        team_diff = prior_team ^ possible_new_team
                        team_overlap = prior_team.intersection(possible_new_team)
                        team_arrival = possible_new_team - prior_team

                        # link if the hash matches, i.e. same team composition
                        if (
                            self.team_dicts_by_month[month][key]["hash"]
                            == self.linked_teams[k]["last_hash"]
                        ):
                            self.linked_teams[k] = update_team(
                                self.linked_teams[k],
                                self.team_dicts_by_month[month][key],
                            )
                            self.linked_teams[k]["last_month_matched"] = month
                            self.linked_teams[k]["team_uuids"].append(key)
                            matched = True
                            break

                        # Link if they have the same team membership
                        elif (
                            self.team_dicts_by_month[month][key]["team_members"]
                            == self.linked_teams[k]["last_team_members"]
                        ):
                            # Have the same supervisor and different UICs as this could signal a reorganization at UIC level

                            self.linked_teams[k] = update_team(
                                self.linked_teams[k],
                                self.team_dicts_by_month[month][key],
                            )
                            self.linked_teams[k]["last_month_matched"] = month
                            self.linked_teams[k]["team_uuids"].append(key)
                            matched = True
                            break

                        # Checks if the team difference is less than 2 and that they
                        # Have the same supervisor, if the supervisor is not equal
                        # there could be a coordinated departure
                        elif len(team_diff) < 2:
                            if (
                                self.team_dicts_by_month[month][key]["supervisor"]
                                == self.linked_teams[k]["last_supervisor"]
                            ):
                                self.linked_teams[k] = update_team(
                                    self.linked_teams[k],
                                    self.team_dicts_by_month[month][key],
                                )
                                self.linked_teams[k]["last_month_matched"] = month
                                self.linked_teams[k]["team_uuids"].append(key)
                                matched = True

                                break

                        # this looks to see if there is some overlap between the possible
                        # teams and makes a list, that can be use later for identifying
                        # possible work unit links

                        elif len(team_overlap) > 0:
                            # This looks at month t+1 to make sure the difference did not
                            # go to the same team
                            coordinated = self.determine_coordinated(
                                list(team_departed), month
                            )
                            # Check if those that left are coordinated, i.e. go to same team
                            if not coordinated:
                                coordinated_arrival = self.determine_coordinated(
                                    list(team_arrival), month, departure=False
                                )
                                if not coordinated_arrival:
                                    if k not in possible_teams[month]:
                                        possible_teams[month][k] = [key]
                                    else:
                                        possible_teams[month][k].append(key)

                        if matched == True:
                            break

                # If the team is not linked to a previous team append it to the list for that month
                if matched == False:
                    new_teams_by_month[month][key] = self.team_dicts_by_month[month][
                        key
                    ]

            # Go through possible matched and identify if
            # there is an optimal match based on the provide criteria.
            for k, v in possible_teams[month].items():
                best_match = self.find_optimal_match(k, v, month)
                if best_match:
                    self.linked_teams[k] = update_team(
                        self.linked_teams[k],
                        self.team_dicts_by_month[month][best_match],
                    )
                    self.linked_teams[k]["last_month_matched"] = month
                    self.linked_teams[k]["team_uuids"].append(best_match)
                    matched = True

                    new_teams_by_month[month].pop(best_match)

            # Add unmatched teams as new team
            current_uids = list(self.linked_teams.keys())

            for uid in new_teams_by_month[month].keys():
                # if uid is not in the current uids, add
                if uid not in current_uids:
                    self.linked_teams[uid] = create_linked_team(
                        new_teams_by_month, month, uid
                    )
                    current_uids.append(uid)
                # if uid is in current uids, generate new uid until it is not
                else:
                    new_uid = str(uuid.uuid4()).replace("-", "")[:10]
                    while new_uid in current_uids:
                        new_uid = str(uuid.uuid4()).replace("-", "")[:10]
                    self.linked_teams[new_uid] = create_linked_team(
                        new_teams_by_month, month, uid
                    )
                    current_uids.append(new_uid)

        return self.linked_teams
