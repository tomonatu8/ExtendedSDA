from typing import Dict, List, Tuple, Optional
from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family
from scripts.esda.update_permutaion import update_pi

def check_restart(
        pi: List[int],
        pi_index: int,
        evicted_children: Dict[SDA_Child, SDA_Daycare],
        matched_families_with_siblings: List[SDA_Family],
        having_siblings_families: List[SDA_Family]
) -> Tuple[
        bool, 
        List[int]
]:
    restart_bool = False
    new_pi = []
    for c in evicted_children:
        if c.family in matched_families_with_siblings:
            j = pi.index(having_siblings_families.index(c.family))
            i = pi_index
            new_pi = update_pi(pi, j, i)
            restart_bool = True
    return restart_bool, new_pi
