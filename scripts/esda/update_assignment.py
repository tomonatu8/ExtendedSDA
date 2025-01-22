from typing import Dict, List, Tuple, Optional

from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family
from scripts.esda.update_permutaion import update_pi


def update_assignment(
        family_children_pref_dict: Dict[SDA_Child, SDA_Daycare],
        evicted_children: Dict[SDA_Child, SDA_Daycare],
):
    for child in family_children_pref_dict:
        child.assigned_daycare = family_children_pref_dict[child]
        family_children_pref_dict[child].assigned_children[child.age].append(child)
    for child in evicted_children:
        child.assigned_daycare = None
        evicted_children[child].assigned_children[child.age].remove(child)
