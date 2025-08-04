import pandas as pd

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
