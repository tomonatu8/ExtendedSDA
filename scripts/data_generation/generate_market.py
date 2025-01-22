from typing import Dict, DefaultDict, List, Any, Tuple, Optional
from collections import defaultdict
import random

from scripts.data_generation.generate_agents import generate_child, generate_family, generate_daycare_using_rust
from scripts.data_generation.generate_pref import generate_pref
from scripts.data_generation.generate_original_priority import generate_original_priority


from mallows import generate_mallows_votes  # type: ignore # Rust

def generate_synthetic_data(
        fnum: int, 
        siblings_fnum: int, 
        dnum: int, 
        recruiting_numbers_list: List[int], 
        dispersions: float, 
        varepsilon: float
) -> Tuple[
        Dict[int, Dict[str, Any]], 
        Dict[int, Dict[str, Any]], 
        Dict[int, Dict[str, Any]]
    ]:

    children_dic = defaultdict()
    families_dic = defaultdict()
    
    for i in range(0, fnum - siblings_fnum):
        # generate each child
        l = list(range(100000, 100000+dnum))
        pref = generate_pref(l, 5)
        dict_for_child = generate_child(i+1, None, pref)
        children_dic[i+1] = dict_for_child
        # generate each family property
        dic_for_f = generate_family(i+1, [i+1], dict_for_child['preference_list'])
        families_dic[i+1] = dic_for_f
        

    nn = fnum-siblings_fnum
    for i in range(nn, fnum):
        random_number = random.uniform(0,1)
        if random_number<=0.8:
            num_children = 2
        else:
            num_children = 3
        l_list = [[0]*num_children for i in range(10)]
        for ind in range(num_children):
            daycare_total_list = list(range(100000, 100000+dnum))
            l0 = generate_pref(daycare_total_list, 10)
            for ind_2 in range(10):
                l_list[ind_2][ind] = l0[ind_2]
        l_tuple_list = [] 
        for each_l_list in l_list:
            l_tuple_list.append(tuple(each_l_list))

        dic_for_f = generate_family(i+1, list(range(nn + 1, nn + 1 + num_children)), generate_pref(l_tuple_list, 10))
        families_dic[i+1] = dic_for_f
        for j in range(len(dic_for_f['children'])):
            c_id = dic_for_f['children'][j]
            pref = [t[j] for t in dic_for_f['pref']]
            dict_for_child = generate_child(c_id, dic_for_f['id'], pref)
            children_dic[c_id] = dict_for_child
        nn += num_children

    original_priority = generate_original_priority(20, families_dic, varepsilon)

    daycares_dic = defaultdict()

    rust_votes = generate_mallows_votes(
        num_candidates=len(original_priority),
        num_voters=dnum,
        phi=dispersions,
        original_priority=original_priority,
        seed=42
    )

    assert len(rust_votes) == dnum

    for i in range(100000, 100000+dnum):
        # daycares_dic[i] = generate_daycare(i, original_priority, dispersions, children_dic, recruiting_numbers_list)
        daycares_dic[i] = generate_daycare_using_rust(i, rust_votes[i-100000], children_dic, recruiting_numbers_list)
    c_number = 1
    for key in families_dic:
        for c in families_dic[key]["children"]:
            if c != c_number:
                exit()
            c_number += 1
    
    return children_dic, daycares_dic, families_dic