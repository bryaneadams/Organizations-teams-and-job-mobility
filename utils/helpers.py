def build_teams_over_time(
    linked_teams: dict, team_dicts_by_month: dict, month_keys: list
) -> dict:
    """creates the teams over time

    Args:
        linked_teams (dict): set of linked teams
        team_dicts_by_month (dict): team dictionaries by month
        month_keys (list): lis tof months

    Returns:
        dict: teams over time
    """
    teams_over_time = {}
    team_num = 0
    for value in linked_teams.values():
        teams_over_time[team_num] = {}

        for key in month_keys:
            for uid in value["team_uuids"]:
                try:
                    temp = {key: team_dicts_by_month[key][uid]}
                    teams_over_time[team_num] = {
                        **teams_over_time[team_num],
                        **temp,
                    }
                    break
                except:
                    continue

        team_num += 1
    return teams_over_time
