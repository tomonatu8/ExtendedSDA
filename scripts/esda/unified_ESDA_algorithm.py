from typing import Dict, List, Any, Tuple, Optional

from scripts.esda.setup_inputs import create_agents
from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family

from scripts.esda.children_DA import DA_for_no_siblings_families
from scripts.esda.check_acceptance import check_acceptance_based_on_SYY, check_acceptance_based_on_ABH
from scripts.esda.check_restart import check_restart
from scripts.esda.update_assignment import update_assignment
from scripts.esda.check_stability import check_stability


def unified_ESDA_algorithm(
        children_dic: Dict[int, Dict[str, Any]],
        daycares_dic: Dict[int, Dict[str, Any]],
        families_dic: Dict[int, Dict[str, Any]],
        algorithm_type: str, 
        exclude_family: bool = True  # True -> SYY stability, False -> ABH stability 
) -> bool:

    assert algorithm_type in ["SC", "SDA", "ESDA"]

    check_acceptance = check_acceptance_based_on_SYY if exclude_family else check_acceptance_based_on_ABH

    children, daycares, families = create_agents(children_dic, daycares_dic, families_dic)

    no_siblings_families = [f for f in families if not f.has_siblings]
    having_siblings_families = [f for f in families if f.has_siblings]

    Pi_set: List[List[int]] = []
    pi = [i for i in range(len(having_siblings_families))]
    if algorithm_type in ["SDA", "ESDA"]:
        Pi_set.append(pi)

    algorithm_terminated = False
    while not algorithm_terminated:
        # initialization
        for daycare in daycares:
            daycare.assigned_children = [[] for _ in range(6)]
        for child in children:
            child.assigned_daycare = None
        for family in families:
            family.assignment = None
        family_next_rank = {family.id: 0 for family in families}

        # DA for families with no siblings
        no_siblings_families, daycares, family_next_rank = DA_for_no_siblings_families(no_siblings_families, daycares, family_next_rank)
        matched_families_with_siblings = []

        pi_index = 0
        restart_bool = False
        second_restart_bool = False
        while pi_index < len(pi):
            current_family = having_siblings_families[pi[pi_index]]

            while not restart_bool and not second_restart_bool:
                if current_family.assignment is not None:
                    break
                if family_next_rank[current_family.id] >= len(current_family.pref):
                    break

                #### Proposal ####
                daycare_tuple = current_family.pref[family_next_rank[current_family.id]]
                family_children_pref_dict = {
                    child: daycare_tuple[i] 
                    for i, child in enumerate(current_family.children)
                }
                #### Proposal ####
                is_accepted, evicted_children = check_acceptance(family_children_pref_dict)
                family_next_rank[current_family.id] += 1

                restart_bool, new_pi = check_restart(pi, pi_index, evicted_children, matched_families_with_siblings, having_siblings_families)
                if restart_bool:
                    if algorithm_type == "SC":  
                        return False
                    if new_pi in Pi_set:
                        return False
                    Pi_set.append(new_pi)
                    pi = new_pi
                    break

                if is_accepted:
                    matched_families_with_siblings.append(current_family)
                    current_family.assignment = family_next_rank[current_family.id] - 1
                    update_assignment(family_children_pref_dict, evicted_children)

                    children_to_process = []
                    for child in evicted_children:
                        if child not in children_to_process:
                            children_to_process.append(child)

                    # Stabilization
                    while children_to_process:
                        displaced_child = children_to_process.pop(0)
                        if displaced_child.assigned_daycare is not None:
                            continue

                        f = displaced_child.family

                        while family_next_rank[f.id] < len(f.pref):
                            if f.assignment is not None:
                                break

                            #### Proposal ####
                            single_application = {displaced_child: f.pref[family_next_rank[f.id]][0]}
                            #### Proposal ####
                            new_is_accepted, new_evicted_children = check_acceptance(single_application)
                            family_next_rank[f.id] += 1

                            second_restart_bool, new_pi = check_restart(pi, pi_index, new_evicted_children, matched_families_with_siblings, having_siblings_families)
                            if second_restart_bool:
                                if algorithm_type == "SC": 
                                    return False
                                if new_pi in Pi_set:
                                    return False
                                Pi_set.append(new_pi)
                                pi = new_pi
                                break

                            if new_is_accepted:
                                f.assignment = family_next_rank[f.id] - 1
                                update_assignment(single_application, new_evicted_children)

                        if second_restart_bool:
                            break

                    # Checking blocking pairs (ESDA only)
                    if algorithm_type == "ESDA":
                        if not check_stability(current_family, exclude_family):
                            return False

                if second_restart_bool:
                    break

            if restart_bool or second_restart_bool:
                break

            pi_index += 1

            if pi_index >= len(pi):
                return True

    return False