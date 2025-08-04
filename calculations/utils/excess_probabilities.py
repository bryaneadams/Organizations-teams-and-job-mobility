import json, pickle
import numpy as np
import pandas as pd
import networkx as nx

from typing import Union


def determine_nc_teams(team_start_stop: dict, left: list, right: list) -> list:
    """Determines teams that span the entire T_< and T_> window.

    Args:
        team_start_stop (dict): dictionary of teams when they start and stop
        left (list): T_<
        right (list): T_>

    Returns:
        list: list of n_c teams
    """

    n_c_teams = []

    for team_id, start_stop_info in team_start_stop.items():
        if start_stop_info["start"] <= int(left[0]):
            if start_stop_info["stop"] >= int(right[-1]):
                n_c_teams.append(team_id)

    n_c_int_teams = [int(team) for team in n_c_teams]

    return n_c_int_teams, n_c_teams


def determine_n_star_teams(two_nets: list, W: int = 1) -> list:
    """Determines N* teams

    Args:
        two_nets (list): E_< and E_> networks
        W (int, optional): weight of edge. Defaults to 1.

    Returns:
        list: list of teams in N*
    """
    # Eps = {k for k, v in nx.get_edge_attributes(two_nets[0], "weight").items() if v >= W}
    Eps = {k for k in two_nets[0].edges()}
    N = set([it1 for it1, it2 in Eps] + [it2 for it1, it2 in Eps])
    # Eps_bar = {k for k, v in nx.get_edge_attributes(two_nets[1], "weight").items()}
    Eps_bar = {k for k in two_nets[1].edges()}
    N_bar = set([it1 for it1, it2 in Eps_bar] + [it2 for it1, it2 in Eps_bar])
    N_star = N.intersection(N_bar)

    return N_star


def build_following_networks(df: pd.DataFrame) -> nx.DiGraph:
    """Builds a network with attributes of following and the person who moved

    Args:
        df (pd.DataFrame): data frame with transition information

    Returns:
        nx.DiGraph: Directed graph with information
    """

    g = nx.DiGraph()

    for idx, row in df.iterrows():
        for col in df.columns[2:]:
            if not pd.isna(row[col]):
                if g.has_edge(row["i"], row["j"]):
                    g[row["i"]][row["j"]]["people"].append(row[col][0])
                    g[row["i"]][row["j"]]["following"].append(row[col][1])
                else:
                    g.add_edge(
                        row["i"],
                        row["j"],
                        people=[row[col][0]],
                        following=[row[col][1]],
                    )

    return g


def create_following_attribute_networks(
    tr_df: pd.DataFrame,
    t: int,
    delta_t: int,
    g: int = 0,
) -> Union[tuple, list]:
    """This function takes several months and creates two networks
    based on the sum of transitions for every pair in the corresponding
    T< and T>

    Args:
        tr_df (pd.DataFrame): a dataframe that contains the transitions between two locations
        t (int): month t which will be the center of the interval of observed
        months. in case of a gap, it will be the end of T<
        delta_t (int): the width of the interval
        g (int, optional): a gap between T< and T>. Defaults to 0.
        debug (bool, optional): returns more information for debug purposes. Defaults to False.

    Returns:
        Union[tuple,list]: list of networkx DiGraph directed networks for T< and T>
    """

    left = [str(i) for i in range(t - delta_t + 1, t + 1) if str(i) in tr_df.columns]
    right = [
        str(i) for i in range(t + 1 + g, t + delta_t + g + 1) if str(i) in tr_df.columns
    ]

    temp_left = tr_df[["i", "j"] + left]
    temp_right = tr_df[["i", "j"] + right]

    left_g = build_following_networks(temp_left)
    right_g = build_following_networks(temp_right)

    return left_g, right_g, left, right


def build_ocs_networks(df: pd.DataFrame) -> nx.DiGraph:
    """Builds a network with ocs tuple for the person that moved. The tuple is (from, to)

    Args:
        df (pd.DataFrame): data frame with transition information

    Returns:
        nx.DiGraph: Directed graph with information
    """

    g = nx.DiGraph()

    for idx, row in df.iterrows():
        for col in df.columns[2:]:
            if not pd.isna(row[col]):
                if g.has_edge(row["i"], row["j"]):
                    g[row["i"]][row["j"]]["ocs_transition"].append(row[col])
                else:
                    g.add_edge(row["i"], row["j"], ocs_transition=[row[col]])

    return g


def create_ocs_attribute_networks(
    tr_df: pd.DataFrame,
    t: int,
    delta_t: int,
    g: int = 0,
) -> Union[nx.DiGraph, nx.DiGraph, list, list]:
    """creates networks for Occ. Series

    Args:
        tr_df (pd.DataFrame): transition dataframe
        t (int): $t$
        delta_t (int): $\delta_t
        g (int, optional): gap parameter. Defaults to 0.

    Returns:
        Union[nx.DiGraph, nx.DiGraph,list, list]
    """

    left = [str(i) for i in range(t - delta_t + 1, t + 1) if str(i) in tr_df.columns]
    right = [
        str(i) for i in range(t + 1 + g, t + delta_t + g + 1) if str(i) in tr_df.columns
    ]

    temp_left = tr_df[["i", "j"] + left]
    temp_right = tr_df[["i", "j"] + right]

    left_g = build_ocs_networks(temp_left)
    right_g = build_ocs_networks(temp_right)

    return left_g, right_g, left, right


## rewires


def preserve_strength(
    G, use_seed=None, tol=30, report_lost=False, with_self_loops: bool = False
):
    """Rewire a weighted directed network, preserving its node strength
    distribution.

    Parameters
    ----------
    G : networkx DiGraph with weights
        directed network produced with networkx
    use_seed : int, optional
        calls numpy's random number generator seed (default is None)
    tol : int, optional
        number of times to reattempt the rewiring before destroying
        some of the progress and try again (Default is 30)
    report_lost : bool, optional
        a flag for explicitly creating a list for lost links in the
        output

    Returns
    -------
    networkx DiGraph
        a new directed graph preserving the number of nodes, at least
        the majority of links, and the strength distribution of the
        original network
    """

    theseed = np.random.default_rng(seed=use_seed)
    newG = nx.DiGraph()
    istubs = []
    jstubs = []
    for i, j in G.edges:
        w = int(G[i][j]["weight"])
        istubs += [i for _ in range(w)]
        jstubs += [j for _ in range(w)]
    theseed.shuffle(istubs)
    theseed.shuffle(jstubs)
    unused_i = []
    unused_j = []
    for idx in range(len(istubs)):
        if not with_self_loops:
            if istubs[idx] == jstubs[idx]:
                unused_i.append(istubs[idx])
                unused_j.append(jstubs[idx])
            elif (istubs[idx], jstubs[idx]) in newG.edges:
                newG[istubs[idx]][jstubs[idx]]["weight"] += 1
            else:
                newG.add_edge(istubs[idx], jstubs[idx], weight=1)
        else:
            if (istubs[idx], jstubs[idx]) in newG.edges:
                newG[istubs[idx]][jstubs[idx]]["weight"] += 1
            else:
                newG.add_edge(istubs[idx], jstubs[idx], weight=1)
    num_tries = 0
    theseed.shuffle(unused_i)
    theseed.shuffle(unused_j)
    while (len(unused_i) > 0) and (num_tries < tol):
        unused_i_loc = []
        unused_j_loc = []
        for idx in range(len(unused_i)):
            if not with_self_loops:
                if unused_i[idx] == unused_j[idx]:
                    unused_i_loc.append(unused_i[idx])
                    unused_j_loc.append(unused_j[idx])
                elif (unused_i[idx], unused_j[idx]) in newG.edges:
                    newG[unused_i[idx]][unused_j[idx]]["weight"] += 1
                else:
                    newG.add_edge(unused_i[idx], unused_j[idx], weight=1)
            else:
                if (unused_i[idx], unused_j[idx]) in newG.edges:
                    newG[unused_i[idx]][unused_j[idx]]["weight"] += 1
                else:
                    newG.add_edge(unused_i[idx], unused_j[idx], weight=1)

        unused_i = unused_i_loc
        unused_j = unused_j_loc
        num_tries += 1
        if len(unused_i) > 0:
            theseed.shuffle(unused_i)
            theseed.shuffle(unused_j)
    if report_lost:
        return {
            "net": newG,
            "lost": len(unused_i),
            "missing_per": len(unused_i) / G.number_of_edges(),
        }
    else:
        return newG


def preserve_strength_and_following(
    G,
    possible_destinations: dict,
    use_seed=None,
    selection_limit: int = 1,
    report_lost=False,
) -> Union[dict, nx.DiGraph]:
    """Preserve strength and reuniting

    Args:
        G (_type_): network
        possible_destinations (dict): possible destinations
        use_seed (_type_, optional): random seed to use for testing. Defaults to None.
        selection_limit (int, optional): Used for development. Defaults to 1.
        report_lost (bool, optional): used for more statistics. Defaults to False.

    Returns:
        Union[dict,nx.DiGraph]
    """

    the_seed = np.random.default_rng(seed=use_seed)

    new_g = nx.DiGraph()

    i_studs_following = []
    i_studs_non_following = []
    i_studs_followoing_id = []
    i_studs_non_followoing_id = []

    j_studs_following = []
    j_studs_non_following = []

    for i, j in G.edges:
        edge_info = G[i][j]

        for idx, is_following in enumerate(edge_info["following"]):
            if is_following == 1:
                i_studs_following.append((i, edge_info["people"][idx], "y"))
                i_studs_followoing_id.append(i)
                j_studs_following.append(j)
            else:
                i_studs_non_following.append((i, edge_info["people"][idx], "n"))
                i_studs_non_followoing_id.append(i)
                j_studs_non_following.append(j)

    all_i_studs = i_studs_following + i_studs_non_following
    all_j_studs = j_studs_following + j_studs_non_following

    # Shuffle studs
    the_seed.shuffle(all_i_studs)
    the_seed.shuffle(all_j_studs)

    missed_i = []

    # Used to keep following

    for i_studs in [i_studs_following, i_studs_non_following]:
        # for i in all_i_studs:
        for i in i_studs:

            # determine if it is following or not
            if i[2] == "y":

                # Find a list of possible teams
                possible_teams = possible_destinations[i[0]][i[1]]
                possible_teams = list(
                    set(possible_teams) & set(all_j_studs) - set([i[0]])
                )
                # possible_teams = all_j_studs

                # If there are any left select from the list
                if len(possible_teams) >= selection_limit:

                    j = np.random.choice(possible_teams)

                    if (i[0], j) in new_g.edges:
                        new_g[i[0]][j]["weight"] += 1
                        new_g[i[0]][j]["following"].append(1)

                    else:
                        new_g.add_edge(i[0], j, weight=1, following=[1])

                    all_j_studs.remove(j)

                else:
                    missed_i.append(i)

            else:

                # Find a list of possible teams
                possible_teams = possible_destinations[i[0]][i[1]]
                possible_teams = list(set(all_j_studs) - set(possible_teams))
                # possible_teams = all_j_studs

                if len(possible_teams) >= selection_limit:
                    j = np.random.choice(possible_teams)

                    if (i, j) in new_g.edges:
                        new_g[i][j]["weight"] += 1
                        new_g[i][j]["following"].append(0)

                    else:
                        new_g.add_edge(i[0], j, weight=1, following=[0])

                    all_j_studs.remove(j)

                else:
                    missed_i.append(i)

    if report_lost:
        return new_g, missed_i
    else:
        return new_g


def preserve_strength_and_ocs(g: nx.digraph) -> nx.digraph:
    """creates random rewires of a network using ocs keys for from, to

    Args:
        g (nx.digraph): Network from T_>

    Returns:
        nx.digraph: Random network that preserves the ocs transitions
    """

    i_dict = {}
    j_dict = {}

    # create locations where edges are able to go
    for edge in g.edges:
        for transition in g[edge[0]][edge[1]]["ocs_transition"]:
            if transition not in i_dict:
                i_dict[transition] = [edge[0]]
                j_dict[transition] = [edge[1]]
            else:
                i_dict[transition].append(edge[0])
                j_dict[transition].append(edge[1])

    # shuffle edges
    for v in i_dict.values():
        np.random.shuffle(v)

    for v in j_dict.values():
        np.random.shuffle(v)

    new_g = nx.DiGraph()
    for transition, i_stubs in i_dict.items():

        for i in i_stubs:
            j = j_dict[transition][0]
            j_dict[transition] = j_dict[transition][1:]

            if (i, j) in new_g.edges:
                new_g[i][j]["weight"] += 1
            else:
                new_g.add_edge(i, j, weight=1)

    return new_g


## calculations
def calculate_z_m(
    left_g: nx.DiGraph, right_g: nx.DiGraph, rewired_g: nx.DiGraph, n_c_teams: list
):
    """calculates z_m

    Args:
        left_g (nx.DiGraph): T_<
        right_g (nx.DiGraph): T_>
        rewired_g (nx.DiGraph): rewired graph
        n_c_teams (list): teams

    Returns:
        z_m calculations
    """

    extra_ones = 0
    numerator_total = 0
    denominator_total = 0

    for team in n_c_teams:

        left_degree = left_g.degree(team) if left_g.has_node(team) else 0
        right_degree = right_g.degree(team) if right_g.has_node(team) else 0

        if left_degree == 0:
            if right_degree == 0:
                extra_ones += 1
                continue

            # otherwise the denominator in the summation would be 0
            left_neighbors = 1

        else:
            # fine |E_<|
            left_neighbors = len(
                set(left_g.successors(team)) | set(left_g.predecessors(team))
            )

        # find neighbors from S for both <- and ->
        if team in rewired_g:
            rw_in_neighbors = set(rewired_g.predecessors(team))
            rw_out_neighbors = set(rewired_g.successors(team))
        else:
            rw_in_neighbors = set()
            rw_out_neighbors = set()

        # find neighbors from E_< for both <- and ->
        if left_degree != 0:
            left_in_neighbors = set(left_g.predecessors(team))
            left_out_neighbors = set(left_g.successors(team))
        else:
            left_in_neighbors = set()
            left_out_neighbors = set()

        # find neighbors from E_> for both <- and ->
        if right_degree != 0:
            right_in_neighbors = set(right_g.predecessors(team))
            right_out_neighbors = set(right_g.successors(team))
        else:
            right_in_neighbors = set()
            right_out_neighbors = set()

        # Find [(E_< -> intersect S ->) + (E_< <- intersect S <-)]/|E_<|
        temp_numerator = (
            len(left_out_neighbors.intersection(rw_out_neighbors))
            + len(left_in_neighbors.intersection(rw_in_neighbors))
        ) / (left_neighbors)

        # Find [(E_< -> intersect E_> ->) + (E_< <- intersect E_> <-)]/|E_<|
        temp_denominator = (
            len(left_out_neighbors.intersection(right_out_neighbors))
            + len(left_in_neighbors.intersection(right_in_neighbors))
        ) / (left_neighbors)

        # update running total
        numerator_total += temp_numerator
        denominator_total += temp_denominator

    return (numerator_total + extra_ones) / (
        denominator_total + extra_ones
    ), numerator_total / denominator_total


def calculate_y_m_numerator(left_g: nx.DiGraph, rewired_g: nx.DiGraph) -> int:

    return len(set(left_g.edges).intersection(set(rewired_g.edges)))


def calculate_x_m_value(right_g: nx.DiGraph, rewired_g: nx.DiGraph) -> float:
    """
    Calculates x_m value for given graphs.

    Args:
        right_g (nx.DiGraph): T_>
        rewired_g (nx.DiGraph): rewired graph

    Returns:
        float: x_m
    """
    denominator = len(set(right_g.edges).intersection(set(rewired_g.edges))) / len(
        right_g.edges
    )

    return denominator


def calculate_z_m_alt(
    left_g: nx.DiGraph, right_g: nx.DiGraph, rewired_g: nx.DiGraph, n_c_teams: list
):
    """This one I am changing the direction of the rewiring. The original rewires T_> but this will use rewires
    of T_< and compare with E_> in numerator

    Args:
        left_g (nx.DiGraph): T_<
        right_g (nx.DiGraph): T_>
        rewired_g (nx.DiGraph): rewired graph
        n_c_teams (list): teams

    Returns:
        z_m calculations
    """

    extra_ones = 0
    numerator_total = 0
    denominator_total = 0

    for team in n_c_teams:

        left_degree = left_g.degree(team) if left_g.has_node(team) else 0
        right_degree = right_g.degree(team) if right_g.has_node(team) else 0

        # if left_degree == 0:
        #     if right_degree == 0:
        #         extra_ones+=1
        #         continue

        ## Update - same as above changed only for my own understanding
        if right_degree == 0:
            if left_degree == 0:
                extra_ones += 1
                continue

            # otherwise the denominator in the summation would be 0
            # left_neighbors = 1
            right_neighbors = 1

        else:
            # fine |E_<|
            # left_neighbors = len(set(left_g.successors(team)) | set(left_g.predecessors(team)))

            ## Update
            # fine |E_>|
            right_neighbors = len(
                set(right_g.successors(team)) | set(right_g.predecessors(team))
            )

        # find neighbors from S for both <- and ->
        ## No change as this is rewires
        if team in rewired_g:
            rw_in_neighbors = set(rewired_g.predecessors(team))
            rw_out_neighbors = set(rewired_g.successors(team))
        else:
            rw_in_neighbors = set()
            rw_out_neighbors = set()

        # find neighbors from E_< for both <- and ->
        ## No change
        if left_degree != 0:
            left_in_neighbors = set(left_g.predecessors(team))
            left_out_neighbors = set(left_g.successors(team))
        else:
            left_in_neighbors = set()
            left_out_neighbors = set()

        # find neighbors from E_> for both <- and ->
        # No change
        if right_degree != 0:
            right_in_neighbors = set(right_g.predecessors(team))
            right_out_neighbors = set(right_g.successors(team))
        else:
            right_in_neighbors = set()
            right_out_neighbors = set()

        # # Find [(E_< -> intersect S ->) + (E_< <- intersect S <-)]/|E_<|
        # temp_numerator = (len(left_out_neighbors.intersection(rw_out_neighbors)) +
        #                       len(left_in_neighbors.intersection(rw_in_neighbors)))/(left_neighbors)

        ## Update
        # Find [(E_> -> intersect S ->) + (E_> <- intersect S <-)]/|E_>|
        temp_numerator = (
            len(right_out_neighbors.intersection(rw_out_neighbors))
            + len(right_in_neighbors.intersection(rw_in_neighbors))
        ) / (right_neighbors)

        # Find [(E_< -> intersect E_> ->) + (E_< <- intersect E_> <-)]/|E_<|
        # temp_denominator = (len(left_out_neighbors.intersection(right_out_neighbors)) +
        #                     len(left_in_neighbors.intersection(right_in_neighbors)))/(left_neighbors)

        ## Update
        # Find [(E_< -> intersect E_> ->) + (E_< <- intersect E_> <-)]/|E_>|
        temp_denominator = (
            len(left_out_neighbors.intersection(right_out_neighbors))
            + len(left_in_neighbors.intersection(right_in_neighbors))
        ) / (right_neighbors)

        # update running total
        numerator_total += temp_numerator
        denominator_total += temp_denominator

    return (numerator_total + extra_ones) / (
        denominator_total + extra_ones
    ), numerator_total / denominator_total


def calculate_y_m_numerator_alt(right_g: nx.DiGraph, rewired_g: nx.DiGraph) -> int:
    """
    Calculates the number of matching edges between the right graph and the rewired graph.

    Args:
        right_g (nx.DiGraph): The original directed graph representing E_>.
        rewired_g (nx.DiGraph): The rewired directed graph.

    Returns:
        int: The count of edges that are present in both the right graph and the rewired graph.
    """

    # return len(set(left_g.edges).intersection(set(rewired_g.edges)))
    ## update

    return len(set(right_g.edges).intersection(set(rewired_g.edges)))
