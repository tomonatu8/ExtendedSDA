from typing import Dict, DefaultDict, List, Any, Tuple, Optional
from collections import defaultdict
import random


def generate_child(
        id: int, 
        family_id: Optional[int], 
        pref: List[int],
        age_distribution: Optional[List[float]],
        seed: int
) -> DefaultDict[str, Any]:

    dict_for_child: DefaultDict[str, Any] = defaultdict()

    dict_for_child['id'] = id

    rng = random.Random(seed)

    if age_distribution is None:
        age_distribution = [0.3, 0.3, 0.15, 0.15, 0.05, 0.05]
    
    # Validate age distribution
    if len(age_distribution) != 6:
        raise ValueError("Age distribution must have exactly 6 values (for ages 0-5)")
    
    if abs(sum(age_distribution) - 1.0) > 0.0001:
        raise ValueError("Age distribution probabilities must sum to 1.0")
    
    # Generate cumulative probability thresholds
    cum_prob = [sum(age_distribution[:i+1]) for i in range(len(age_distribution))]

    
    # Assign age based on the distribution
    random_number = rng.uniform(0, 1)
    for age, threshold in enumerate(cum_prob):
        if random_number <= threshold:
            dict_for_child['age'] = age
            break

    dict_for_child['family_id'] = family_id
    dict_for_child['initial_daycare_id'] = None
    dict_for_child['actual_daycare_id'] = None
    dict_for_child['preference_list'] = pref

    return dict_for_child



def generate_family(
        id: int, 
        children_list: List[int], 
        pref: List[Tuple[int, ...]],
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
