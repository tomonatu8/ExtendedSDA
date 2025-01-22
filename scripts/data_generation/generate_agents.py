from typing import Dict, DefaultDict, List, Any, Tuple, Optional
from collections import defaultdict
import random


def generate_child(
        id: int, 
        family_id: Optional[int], 
        pref: List[int]
) -> DefaultDict[str, Any]:

    dict_for_child: DefaultDict[str, Any] = defaultdict()

    dict_for_child['id'] = id
    
    random_number = random.uniform(0,1)
    if random_number<=0.3:
        dict_for_child['age'] = 0
    elif random_number<=0.6:
        dict_for_child['age'] = 1
    elif random_number<=0.75:
        dict_for_child['age'] = 2
    elif random_number<=0.9:
        dict_for_child['age'] = 3
    elif random_number<=0.95:
        dict_for_child['age'] = 4
    else:
        dict_for_child['age'] = 5

    dict_for_child['family_id'] = family_id
    dict_for_child['initial_daycare_id'] = None
    dict_for_child['actual_daycare_id'] = None
    dict_for_child['preference_list'] = pref

    return dict_for_child


def generate_family(
        id: int, 
        children_list: List[int], 
        pref: List[int]
) -> DefaultDict[str, Any]:

    dic_for_f: DefaultDict[str, Any] = defaultdict()
    dic_for_f['id'] = id
    dic_for_f['children'] = children_list
    dic_for_f['pref'] = pref
    return dic_for_f



def generate_daycare_using_rust(
        id: int, 
        rust_votes_i: List[int], 
        children_dic: DefaultDict[int, DefaultDict[str, Any]], 
        recruiting_numbers_list: List[int]
) -> DefaultDict[str, Any]:
    
    dic_for_d: DefaultDict[str, Any] = defaultdict()
    dic_for_d['id'] = id
    dic_for_d['recruiting_numbers_list'] = recruiting_numbers_list

    daycares_priority = rust_votes_i
    
    chil_list = []
    for c_id in daycares_priority:
        if id in children_dic[c_id]['preference_list']:
            chil_list.append(c_id)
    dic_for_d['priority_child_id_list'] = chil_list 

    dic_for_d['share_ages_list'] = []

    dic_for_d['priority_score_list'] = [1000000000.0 - k for k in range(len(chil_list))]

    return dic_for_d
