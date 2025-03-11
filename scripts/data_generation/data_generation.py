from typing import Dict, DefaultDict, List, Any, Tuple
from collections import defaultdict
import random

from scripts.data_generation.generate_agents import generate_child, generate_family, generate_daycare_using_rust
from scripts.data_generation.generate_pref import generate_pref
from scripts.data_generation.generate_original_priority import generate_original_priority

from mallows import generate_mallows_votes  # type: ignore # Rust



def generate_multi_child_preferences(
        daycare_ids: List[int],
        num_children: int,
        pref_length: int,
        seed: int
) -> List[Tuple[int, ...]]:
    """
    Generate preference lists for multi-child families.
    
    Parameters
    -----------
    daycare_ids : List[int]
        List of daycare IDs to choose from
    num_children : int
        Number of children in the family (2 or 3)
    pref_length : int
        Length of preference list to generate
    seed : int
        Random seed for reproducibility
        
    Returns
    --------
    List[Tuple[int, ...]]
        List of preference tuples, where each tuple contains daycare IDs for siblings
    """
    # Create a matrix to hold daycare preferences for each child
    preferences_per_sibling = [[0] * num_children for _ in range(pref_length)]
    
    # Create a deterministic seed sequence for each sibling
    sibling_seeds = [seed + i for i in range(num_children)]
    
    # Generate individual preferences for each sibling
    for sibling_idx in range(num_children):
        # Get random daycare preferences for this child using the sibling-specific seed
        sibling_prefs = generate_pref(daycare_ids, pref_length, sibling_seeds[sibling_idx])
        for pref_idx in range(pref_length):
            preferences_per_sibling[pref_idx][sibling_idx] = sibling_prefs[pref_idx]
    
    # Convert to tuples
    return [tuple(pref_set) for pref_set in preferences_per_sibling]




def data_generation(
        num_of_total_children: int,
        num_of_total_families: int, 
        num_of_single_child_families: int, 
        num_of_two_siblings_families: int, 
        num_of_three_siblings_families: int,
        num_of_total_daycares: int,
        capacity: List[int],
        varepsilon: float,
        phi: float,
        single_child_pref_length: int,
        multi_child_pref_length: int,
        daycare_priority_length: int,
        age_distribution: List[float],
        num_instances: int,
        seed: int,
) -> List[Dict]:
    """
    Generate synthetic data for daycare assignment problem.
    
    This function creates a dataset containing children, families, and daycares with their preferences,
    which can be used for two-sided matching problem with siblings.
    

    Parameters
    -----------
    num_of_total_children : int
        Total number of children across all families
    num_of_total_families : int
        Total number of families to generate
    num_of_single_child_families : int
        Number of families with exactly one child
    num_of_two_siblings_families : int
        Number of families with exactly two children
    num_of_three_siblings_families : int
        Number of families with exactly three children
    num_of_total_daycares : int
        Number of daycares to generate
    capacity : List[int]
        Quota for each age group in daycares
    varepsilon : float
        Parameter for generating original priority
    phi : float
        Parameter for Mallows model (lower values create preferences closer to the reference ranking)
    single_child_pref_length : int
        Maximum preference list length for single-child families
    multi_child_pref_length : int
        Maximum preference list length for multi-child families
    daycare_priority_length : int
        Length of the original priority ranking
    age_distribution : List[float]
        Probability distribution for ages 0-5. Should sum to 1.0.
    num_instances : int
        Number of data instances to generate
    seed : int
        Random seed for reproducibility
        
    Returns
    --------
    instances : List[Dict]
        List of generated instances, each containing children, families, daycares data and parameters
    """
    
    # Verify family distribution and parameter validity
    assert num_of_total_families == num_of_single_child_families + num_of_two_siblings_families + num_of_three_siblings_families, \
        "Total families must equal the sum of single-child, two-siblings, and three-siblings families"
    
    assert num_of_total_children == num_of_single_child_families + 2 * num_of_two_siblings_families + 3 * num_of_three_siblings_families, \
        "Total children must equal single-child families + 2*(two-siblings families) + 3*(three-siblings families)"
    
    assert single_child_pref_length <= num_of_total_daycares, \
        "Single child preference length cannot exceed the number of daycares"
    
    assert multi_child_pref_length <= num_of_total_daycares, \
        "Multi-child preference length cannot exceed the number of daycares"
    
    assert daycare_priority_length <= num_of_total_children, \
        "Original priority length cannot exceed the number of children"


    # Set the base random seed
    random.seed(seed)
    instance_seeds = [seed + i * 1000 for i in range(num_instances)]

    instances = []
    daycare_id_start = max(100000, num_of_total_children * 10) 
    daycare_ids = list(range(daycare_id_start, daycare_id_start + num_of_total_daycares))
    

    for instance_idx in range(num_instances):
        if instance_idx % 10 == 0:
            print(f"Generating instance {instance_idx+1}/{num_instances}")
            
        children_dic = defaultdict()
        families_dic = defaultdict()
        instance_seed = instance_seeds[instance_idx]

        
        # ----- Step 1: Generate single-child families -----
        for family_id in range(1, num_of_single_child_families + 1):
            family_seed = instance_seed + family_id
            daycare_preferences = generate_pref(daycare_ids, single_child_pref_length, family_seed)
            child_id = family_id
            child_data = generate_child(child_id, None, daycare_preferences, age_distribution, family_seed)
            children_dic[child_id] = child_data
            
            family_data = generate_family(family_id, [child_id], child_data['preference_list'])
            families_dic[family_id] = family_data
        # ----- Step 1: Generate single-child families -----

        
        next_family_id = num_of_single_child_families + 1
        next_child_id = num_of_single_child_families + 1
        
        # ----- Step 2: Generate two-sibling families -----
        for i in range(num_of_two_siblings_families):
            family_id = num_of_single_child_families + 1 + i
            family_seed = instance_seed + family_id
            multi_prefs = generate_multi_child_preferences(
                daycare_ids, 
                2, 
                multi_child_pref_length, 
                family_seed
            )
            children_ids = [next_child_id, next_child_id + 1]
            family_data = generate_family(
                next_family_id,
                children_ids,
                multi_prefs  # Pass the preference tuples directly without using generate_pref
            )
            families_dic[next_family_id] = family_data
            
            # Create each child with their own preferences
            for idx, child_id in enumerate(children_ids):
                # Extract this child's preferences from family preference tuples
                child_preferences = [preference_tuple[idx] for preference_tuple in family_data['pref']]
                child_data = generate_child(
                    child_id, 
                    family_data['id'], 
                    child_preferences, 
                    age_distribution,
                    family_seed + idx
                )
                children_dic[child_id] = child_data
            # ----- Step 2: Generate two-sibling families -----
            
            next_family_id += 1
            next_child_id += 2
        
        # ----- Step 3: Generate three-sibling families -----
        for i in range(num_of_three_siblings_families):
            family_id = num_of_single_child_families + num_of_two_siblings_families + 1 + i
            family_seed = instance_seed + family_id
            
            # Generate combined preferences for siblings
            multi_prefs = generate_multi_child_preferences(
                daycare_ids, 
                3, 
                multi_child_pref_length, 
                family_seed
            )
            
            # Create family with three children
            children_ids = [next_child_id, next_child_id + 1, next_child_id + 2]
            family_data = generate_family(
                next_family_id,
                children_ids,
                multi_prefs  # Pass the preference tuples directly without using generate_pref
            )
            families_dic[next_family_id] = family_data
            
            # Create each child with their own preferences
            for idx, child_id in enumerate(children_ids):
                child_preferences = [preference_tuple[idx] for preference_tuple in family_data['pref']]
                child_data = generate_child(
                    child_id, 
                    family_data['id'], 
                    child_preferences, 
                    age_distribution,
                    family_seed + idx
                    )
                children_dic[child_id] = child_data
            # ----- Step 3: Generate three-sibling families -----
            
            next_family_id += 1
            next_child_id += 3


        # ----- Step 4: Generate daycare priorities for children -----
        # Create base priority ordering for all daycares
        priority_seed = instance_seed + 10000
        original_priority = generate_original_priority(
            daycare_priority_length, 
            families_dic, 
            varepsilon, 
            priority_seed
        )
        
        # Generate variations of the priority for each daycare using Mallows model
        votes_seed = instance_seed + 20000
        daycare_votes = generate_mallows_votes(
            num_candidates=len(original_priority),
            num_voters=num_of_total_daycares,
            phi=phi,
            original_priority=original_priority,
            seed=votes_seed
        )
        # ----- Step 4: Generate daycare priorities for children -----

        # ----- Step 5: Create daycare records -----
        daycares_dic = defaultdict()
        for idx, daycare_id in enumerate(daycare_ids):
            daycares_dic[daycare_id] = generate_daycare_using_rust(
                daycare_id, 
                daycare_votes[idx], 
                children_dic, 
                capacity
            )
        # ----- Step 5: Create daycare records -----
        
        # ----- Step 6: Package data into a complete instance -----
        instance_data = {
            'children_dic': children_dic,
            'daycares_dic': daycares_dic,
            'families_dic': families_dic,
            'params': {
                'total_children': num_of_total_children,
                'total_families': num_of_total_families,
                'single_child_families': num_of_single_child_families,
                'two_siblings_families': num_of_two_siblings_families,
                'three_siblings_families': num_of_three_siblings_families,
                'daycare_num': num_of_total_daycares,
                'phi': phi,
                'varepsilon': varepsilon,
                'recruiting_numbers': capacity,
                'single_child_pref_length': single_child_pref_length,
                'multi_child_pref_length': multi_child_pref_length
            }
        }
        # ----- Step 6: Package data into a complete instance -----
        
        instances.append(instance_data)

    return instances

