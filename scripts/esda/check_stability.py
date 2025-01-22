from typing import Dict, List, Tuple, Optional

from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family
from scripts.esda.check_acceptance import check_acceptance_based_on_SYY, check_acceptance_based_on_ABH


def check_stability(
    current_family: SDA_Family, 
    exclude_family: bool
) -> bool:
    check_acceptance = check_acceptance_based_on_SYY if exclude_family else check_acceptance_based_on_ABH
    for i in range(0, current_family.assignment):
        daycare_tuple = current_family.pref[i]
        family_children_pref_dict = {
            child: daycare_tuple[i] 
            for i, child in enumerate(current_family.children)
        }
        third_is_accepted, third_evicted_children = check_acceptance(family_children_pref_dict)
        if third_is_accepted:
            return False
    return True