from typing import Dict, List, Tuple, Optional

from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family



def DA_for_no_siblings_families(
        no_siblings_families: List[SDA_Family], 
        daycares: List[SDA_Daycare], # all daycares
        family_next_rank: Dict[int, int]
) -> Tuple[List[SDA_Family], List[SDA_Daycare], Dict[int, int]]:
    
    # Check if all families have only one child
    for family in no_siblings_families:
        assert len(family.children) == 1, f"Family {family.id} has more than one child"

    # Temporary assignment 
    tmp = dict()
    for daycare in daycares:
        tmp[daycare.id] = [[] for _ in range(6)]


    # Flag to indicate when all proposals are done
    done: bool = False
    while not done:
        done = True

        for family in no_siblings_families:
            child = family.children[0] 
            if child.assigned_daycare is not None:
                continue
            if family_next_rank[family.id] >= len(family.pref):
                continue
            
            done = False
            daycare = family.pref[family_next_rank[family.id]][0]
            
            if child in daycare.priority:
                age = child.age
                current_count = len(tmp[daycare.id][age])
                total_capacity = daycare.total_numbers[age]
                if current_count < total_capacity:
                    # when the capacity is not full
                    tmp[daycare.id][age].append(child)
                    tmp[daycare.id][age].sort(key=lambda c: daycare.priority.index(c))
                    child.assigned_daycare = daycare
                elif current_count == total_capacity:
                    # when the capacity is full, replace the lowest priority child
                    lowest_priority_child = tmp[daycare.id][age][-1]
                    if daycare.priority.index(child) < daycare.priority.index(lowest_priority_child):
                        # when the child has higher priority than the lowest priority child
                        lowest_priority_child.assigned_daycare = None
                        tmp[daycare.id][age].pop()
                        tmp[daycare.id][age].append(child)
                        tmp[daycare.id][age].sort(key=lambda c: daycare.priority.index(c))
                        child.assigned_daycare = daycare
            family_next_rank[family.id] += 1

    for daycare in daycares:
        daycare.assigned_children = tmp[daycare.id]

    return no_siblings_families, daycares, family_next_rank


def make_no_siblings_families_list(
        families: List[SDA_Family]
) -> Tuple[List[SDA_Family], List[SDA_Family]]:
    """
    Output 
    (i) the set of children which do not have siblings
    (ii) the set of families which have siblings
    """
    no_siblings_families = [f for f in families if not f.has_siblings]
    having_siblings_families = [f for f in families if f.has_siblings]
    
    return no_siblings_families, having_siblings_families