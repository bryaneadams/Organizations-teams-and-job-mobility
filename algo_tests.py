import pytest
import pandas as pd

import utils.helpers as hp
import utils.build_teams as bt


def remove_hash(data: dict) -> dict:
    """removes the has key for testing

    Args:
        data (dict): teams over time dictionary

    Returns:
        dict: teams over time dictionary without the hash key
    """
    cleaned_dict = {}
    for id, comp in data.items():
        cleaned_dict[id] = {}
        for date, data in comp.items():
            cleaned_dict[id][date] = data.copy()
            cleaned_dict[id][date].pop("hash")

    return cleaned_dict


### Terminal testing ####

non_terminal_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 244],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 244],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 344, 344, 344, 344],
            "UIC": [1, 1, 1, 2, 2, 2, 2],
        }
    ),
}

becoming_non_terminal_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 244],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 344, 344, 344, 344, 344],
            "UIC": [1, 1, 1, 2, 2, 2, 2, 2],
        }
    ),
}


def test_non_terminal():
    """Runs test to check the following:

    1. Not add non terminal teams
    2. Kill a team if it becomes non-terminal

    """
    linked_teams = bt.LinkedTeams(non_terminal_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1, 2],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35],
                "uic": [1, 2],
                "team_size": 4,
            },
        }
    }

    linked_teams = bt.LinkedTeams(
        becoming_non_terminal_df_dict, ["20120131", "20120228"]
    )
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35],
                "uic": [1, 2],
                "team_size": 4,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            }
        },
    }


### Uncoordinated Testing ####

uncoordinated_move_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 344, 344, 344, 344],
            "UIC": [1, 1, 1, 2, 2, 2, 2],
        }
    ),
}
supervisor_departure_move_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [644, 644, 644, 644, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
}
supe_swap_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [344, 344, 344, 344, 244, 244, 244],
            "UIC": [1, 1, 1, 2, 2, 2, 2],
        }
    ),
}
two_uncoordinated_departure_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 50, 51],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 444, 444],
            "UIC": [1, 1, 1, 1, 2, 2, 2, 3, 3],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 50, 51],
            "SUPERVISOR MASTERKEY": [244, 244, 444, 344, 344, 344, 344, 444, 444],
            "UIC": [1, 1, 3, 2, 2, 2, 2, 3, 3],
        }
    ),
}

two_uncoordinated_arrival_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 50, 51],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 444, 444],
            "UIC": [1, 1, 1, 1, 2, 2, 2, 3, 3],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 50, 51],
            "SUPERVISOR MASTERKEY": [244, 244, 444, 344, 344, 344, 444, 444, 444],
            "UIC": [1, 1, 3, 2, 2, 2, 2, 3, 3],
        }
    ),
}


def test_uncoordinated():
    """Test uncoordinated transitions

    1. Single uncoordinated move
    2. Supervisor uncoordinated move
    3. Supervisor swap
    4. Two uncoordinated departures
    5. Two uncoordinated arrivals and two uncoordinated departures
    """

    linked_teams = bt.LinkedTeams(uncoordinated_move_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35],
                "uic": [1],
                "team_size": 4,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [36, 37, 38, 39],
                "uic": [2],
                "team_size": 5,
            },
        },
    }

    linked_teams = bt.LinkedTeams(
        supervisor_departure_move_df_dict, ["20120131", "20120228"]
    )
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 644,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }

    linked_teams = bt.LinkedTeams(supe_swap_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [33, 34, 35, 36],
                "uic": [1, 2],
                "team_size": 5,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }

    linked_teams = bt.LinkedTeams(
        two_uncoordinated_departure_df_dict, ["20120131", "20120228"]
    )
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34],
                "uic": [1],
                "team_size": 3,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [36, 37, 38, 39],
                "uic": [2],
                "team_size": 5,
            },
        },
        2: {
            "20120131": {
                "supervisor": 444,
                "team_members": [50, 51],
                "uic": [3],
                "team_size": 3,
            },
            "20120228": {
                "supervisor": 444,
                "team_members": [35, 50, 51],
                "uic": [3],
                "team_size": 4,
            },
        },
    }

    linked_teams = bt.LinkedTeams(
        two_uncoordinated_arrival_df_dict, ["20120131", "20120228"]
    )
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34],
                "uic": [1],
                "team_size": 3,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [36, 37, 38],
                "uic": [2],
                "team_size": 4,
            },
        },
        2: {
            "20120131": {
                "supervisor": 444,
                "team_members": [50, 51],
                "uic": [3],
                "team_size": 3,
            },
            "20120228": {
                "supervisor": 444,
                "team_members": [35, 39, 50, 51],
                "uic": [2, 3],
                "team_size": 5,
            },
        },
    }


### Coordinated tests ###

coordinated_move_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 344, 344, 344, 344, 344],
            "UIC": [1, 1, 2, 2, 2, 2, 2],
        }
    ),
}

coordinated_with_supe_move_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 244],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 17],
            "UIC": [1, 1, 1, 1, 2, 2, 2, 1],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 244],
            "SUPERVISOR MASTERKEY": [644, 644, 644, 344, 344, 344, 344, 344],
            "UIC": [1, 1, 1, 2, 2, 2, 2, 2],
        }
    ),
}


def test_coordinated():
    """Test coordinated moves

    1. a coordinated move within the workforce
    2. a coordinated move with a supervisor and team member

    """

    linked_teams = bt.LinkedTeams(coordinated_move_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            }
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            }
        },
        2: {
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34],
                "uic": [1],
                "team_size": 3,
            }
        },
        3: {
            "20120228": {
                "supervisor": 344,
                "team_members": [35, 36, 37, 38, 39],
                "uic": [2],
                "team_size": 6,
            }
        },
    }

    linked_teams = bt.LinkedTeams(
        coordinated_with_supe_move_df_dict, ["20120131", "20120228"]
    )
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            }
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            }
        },
        2: {
            "20120228": {
                "supervisor": 644,
                "team_members": [33, 34, 35],
                "uic": [1],
                "team_size": 4,
            }
        },
        3: {
            "20120228": {
                "supervisor": 344,
                "team_members": [36, 37, 38, 39, 244],
                "uic": [2],
                "team_size": 6,
            }
        },
    }


### Arrivals and exits ###
dual_arrival_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 100, 101],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 244, 244],
            "UIC": [1, 1, 1, 2, 2, 2, 2, 1, 1],
        }
    ),
}
dual_exit_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 344, 344, 344],
            "UIC": [1, 1, 2, 2, 2],
        }
    ),
}

supe_leave_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [644, 644, 644, 644, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
}


def test_arrivals_departures():
    """Test arrivals and departures

    1. Dual arrival
    2. Dual exit
    3. Supervisor leaving

    """

    linked_teams = bt.LinkedTeams(dual_arrival_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36, 100, 101],
                "uic": [1, 2],
                "team_size": 7,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }

    linked_teams = bt.LinkedTeams(dual_exit_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34],
                "uic": [1],
                "team_size": 3,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }

    linked_teams = bt.LinkedTeams(supe_leave_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 644,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }


### New team
new_team_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 37, 38, 39, 100, 101],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 344, 344, 344, 444, 444],
            "UIC": [1, 1, 1, 2, 2, 2, 3, 3],
        }
    ),
}


def test_new_team():
    """Test the creation of a new team"""
    linked_teams = bt.LinkedTeams(new_team_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35],
                "uic": [1],
                "team_size": 4,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
        2: {
            "20120228": {
                "supervisor": 444,
                "team_members": [100, 101],
                "uic": [3],
                "team_size": 3,
            }
        },
    }


### Other tests

splinter_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 644, 744, 844, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
}

team_split_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 744, 744, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
}

team_merger_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39],
            "SUPERVISOR MASTERKEY": [844, 844, 844, 844, 844, 844, 844],
            "UIC": [1, 1, 1, 1, 2, 2, 2],
        }
    ),
}

self_supervisor_df_dict = {
    "20120131": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 888],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 888],
            "UIC": [1, 1, 1, 1, 2, 2, 2, 3],
        }
    ),
    "20120228": pd.DataFrame(
        {
            "MASTERKEY": [33, 34, 35, 36, 37, 38, 39, 344],
            "SUPERVISOR MASTERKEY": [244, 244, 244, 244, 344, 344, 344, 344],
            "UIC": [1, 1, 1, 1, 2, 2, 2, 2],
        }
    ),
}


def test_other():
    """Test other situations

    1. A team splintering
    2. A team dividing
    3. Two teams merging
    4. Self-supervising
    """

    linked_teams = bt.LinkedTeams(splinter_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33],
                "uic": [1],
                "team_size": 2,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
        2: {
            "20120228": {
                "supervisor": 644,
                "team_members": [34],
                "uic": [1],
                "team_size": 2,
            }
        },
        3: {
            "20120228": {
                "supervisor": 744,
                "team_members": [35],
                "uic": [1],
                "team_size": 2,
            }
        },
        4: {
            "20120228": {
                "supervisor": 844,
                "team_members": [36],
                "uic": [1],
                "team_size": 2,
            }
        },
    }

    linked_teams = bt.LinkedTeams(team_split_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            }
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
        2: {
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34],
                "uic": [1],
                "team_size": 3,
            }
        },
        3: {
            "20120228": {
                "supervisor": 744,
                "team_members": [35, 36],
                "uic": [1],
                "team_size": 3,
            }
        },
    }

    linked_teams = bt.LinkedTeams(team_merger_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            }
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            }
        },
        2: {
            "20120228": {
                "supervisor": 844,
                "team_members": [33, 34, 35, 36, 37, 38, 39],
                "uic": [1, 2],
                "team_size": 8,
            }
        },
    }

    linked_teams = bt.LinkedTeams(self_supervisor_df_dict, ["20120131", "20120228"])
    linked_teams.create_team_dicts()
    temp_link_teams = linked_teams.build_linked_team_dict()
    teams_over_time = hp.build_teams_over_time(
        temp_link_teams, linked_teams.team_dicts_by_month, ["20120131", "20120228"]
    )

    assert remove_hash(teams_over_time) == {
        0: {
            "20120131": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
            "20120228": {
                "supervisor": 244,
                "team_members": [33, 34, 35, 36],
                "uic": [1],
                "team_size": 5,
            },
        },
        1: {
            "20120131": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
            "20120228": {
                "supervisor": 344,
                "team_members": [37, 38, 39],
                "uic": [2],
                "team_size": 4,
            },
        },
    }
