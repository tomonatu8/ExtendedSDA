# (1) SYY stability (Sun, Yokoyama, and Yokoo)
# (2) ABH stability (Ashlagi, Braverman, and Hassidim)

from typing import Dict, List, Tuple, Optional

from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family

def choice_function_of_daycare(
        daycare: SDA_Daycare, 
        children_list: List[SDA_Child],
) -> Tuple[
        List[SDA_Child], 
        List[SDA_Child]
    ]:
    """ Choice function of a daycare
    
    Args:
        daycare: 
        children_list: List of children who are applying to the daycare
        
    Returns:
        Tuple[List[SDA_Child], List[SDA_Child]]: (accepted_children, rejected_children)
    """
    children_by_age = [[] for _ in range(6)]
    for child in children_list:
        if child in daycare.priority:
            children_by_age[child.age].append(child)
    
    accepted_children = []
    rejected_children = []
    
    for age in range(6):
        age_group = children_by_age[age]
        if not age_group:
            continue
            
        age_group.sort(key=lambda c: daycare.priority.index(c))

        capacity = daycare.total_numbers[age]
        accepted_children.extend(age_group[:capacity])
        rejected_children.extend(age_group[capacity:])
    
    return accepted_children, rejected_children



def check_acceptance_base(
        family_children_pref_dict: Dict[SDA_Child, SDA_Daycare],
        exclude_family: bool  # SYY stability -> True, ABH stability -> False
) -> Tuple[
        bool, # A bool indicating if the application is accepted　
        Dict[SDA_Child, SDA_Daycare]  #  evicted children by a daycare (will be used for checking cycles in XDA)
    ]:
    daycares = list(set(family_children_pref_dict.values()))
    
    is_accepted = True
    evicted_children = {}

    for daycare in daycares:
        current_children = []
        for age in range(6):
            if exclude_family:  # SYY stability -> (μ(d) \setminus C_f)
                for c in daycare.assigned_children[age]:
                    if c not in family_children_pref_dict:
                        current_children.append(c)
            else:  # ABH stability -> μ(d)
                current_children.extend(daycare.assigned_children[age])
            
        # \cup C(≻_f, j, d)
        applying_children = [c for c, d in family_children_pref_dict.items() if d == daycare]
        all_children = current_children + applying_children

        accepted_children, rejected_children = choice_function_of_daycare(daycare, all_children)
        for c in rejected_children:
            if c in applying_children:
                is_accepted = False
            evicted_children[c] = daycare
        
    return is_accepted, evicted_children


def check_acceptance_based_on_SYY(
        family_children_pref_dict: Dict[SDA_Child, SDA_Daycare]
) -> Tuple[
        bool, # A bool indicating if the application is accepted　
        Dict[SDA_Child, SDA_Daycare]  #  evicted children by a daycare (will be used for checking cycles in XDA)
    ]:    
    """SYY stability 
    Ch_d((μ(d) \\setminus C_f) \\cup C(≻_f, j, d))
    """
    return check_acceptance_base(family_children_pref_dict, exclude_family=True)


def check_acceptance_based_on_ABH(
        family_children_pref_dict: Dict[SDA_Child, SDA_Daycare]
) -> Tuple[
        bool, # A bool indicating if the application is accepted　
        Dict[SDA_Child, SDA_Daycare]  #  evicted children by a daycare (will be used for checking cycles in XDA)
    ]:
    """ABH stability 
    Ch_d(μ(d) \\cup C(≻_f, j, d))
    """
    return check_acceptance_base(family_children_pref_dict, exclude_family=False)