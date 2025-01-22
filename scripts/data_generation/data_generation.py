from typing import Dict, DefaultDict, List, Any, Tuple, Optional
from collections import defaultdict
import sys 
import os


sys.path.append(os.path.dirname((os.path.abspath(__file__))).replace("/mallows",""))
from scripts.data_generation.generate_agents import generate_child, generate_family, generate_daycare_using_rust
from scripts.data_generation.generate_pref import generate_pref
from scripts.data_generation.generate_original_priority import generate_original_priority

from mallows import generate_mallows_votes  # type: ignore # Rust



def calculate_family_size(total_children: int) -> Tuple[int, int, int, int]:
    two_siblings_families = int((0.2 * total_children * 0.8) / 2)
    three_siblings_families = int((0.2 * total_children * 0.2) / 3)
    
    # 2人兄弟と3人兄弟の子どもの総数を計算
    children_in_larger_families = (two_siblings_families * 2 + 
                                 three_siblings_families * 3)
    
    # 残りを一人っ子家庭に割り当て
    single_child_families = total_children - children_in_larger_families
    
    # 合計家庭数を計算
    total_families = single_child_families + two_siblings_families + three_siblings_families
    
    return total_families, single_child_families, two_siblings_families, three_siblings_families


def data_generation(total_children: int, phi: float, num_instances: int = 100) -> List[Dict]:

    # Calculate family numbers
    total_families, single_child_families, two_siblings_families, three_siblings_families = calculate_family_size(total_children)
    daycare_num = int(0.1 * total_families)  # number of daycares is 10% of total families
    
    instances = []
    recruiting_numbers_list = [5, 5, 1, 1, 1, 1]  # quotas for each age group
    varepsilon = 1.0  # parameter for original priority

    for instance in range(num_instances):
        if instance % 10 == 0:
            print(f"Generating instance {instance+1}/{num_instances}")
            
        children_dic = defaultdict()
        families_dic = defaultdict()

        
        # Generate single-child families
        for i in range(1, single_child_families + 1):
            daycare_list = list(range(100000, 100000 + daycare_num))
            pref = generate_pref(daycare_list, 5)
            
            dict_for_child = generate_child(i, None, pref)
            children_dic[i] = dict_for_child
            
            dic_for_f = generate_family(i, [i], dict_for_child['preference_list'])
            families_dic[i] = dic_for_f
        
        # Start ID for siblings families
        next_family_id = single_child_families + 1
        next_child_id = single_child_families + 1
        
        # Generate two-sibling families
        for i in range(two_siblings_families):
            daycare_total_list = list(range(100000, 100000 + daycare_num))
            l_list = [[0]*2 for _ in range(10)]
            for ind in range(2):
                l0 = generate_pref(daycare_total_list, 10)
                for ind_2 in range(10):
                    l_list[ind_2][ind] = l0[ind_2]
            
            l_tuple_list = [tuple(each_l_list) for each_l_list in l_list]
            children_ids = [next_child_id, next_child_id + 1]
            
            dic_for_f = generate_family(
                next_family_id,
                children_ids,
                generate_pref(l_tuple_list, 10)
            )
            families_dic[next_family_id] = dic_for_f
            
            for j, c_id in enumerate(children_ids):
                pref = [t[j] for t in dic_for_f['pref']]
                dict_for_child = generate_child(c_id, dic_for_f['id'], pref)
                children_dic[c_id] = dict_for_child
            
            next_family_id += 1
            next_child_id += 2
        
        # Generate three-sibling families
        for i in range(three_siblings_families):
            daycare_total_list = list(range(100000, 100000 + daycare_num))
            l_list = [[0]*3 for _ in range(10)]
            for ind in range(3):
                l0 = generate_pref(daycare_total_list, 10)
                for ind_2 in range(10):
                    l_list[ind_2][ind] = l0[ind_2]
            
            l_tuple_list = [tuple(each_l_list) for each_l_list in l_list]
            children_ids = [next_child_id, next_child_id + 1, next_child_id + 2]
            
            dic_for_f = generate_family(
                next_family_id,
                children_ids,
                generate_pref(l_tuple_list, 10)
            )
            families_dic[next_family_id] = dic_for_f
            
            for j, c_id in enumerate(children_ids):
                pref = [t[j] for t in dic_for_f['pref']]
                dict_for_child = generate_child(c_id, dic_for_f['id'], pref)
                children_dic[c_id] = dict_for_child
            
            next_family_id += 1
            next_child_id += 3
        
        # Generate original priority and daycares
        original_priority = generate_original_priority(20, families_dic, varepsilon)
        rust_votes = generate_mallows_votes(
            num_candidates=len(original_priority),
            num_voters=daycare_num,
            phi=phi,
            original_priority=original_priority,
            seed=42
        )

        daycares_dic = defaultdict()
        for i in range(100000, 100000 + daycare_num):
            daycares_dic[i] = generate_daycare_using_rust(
                i, 
                rust_votes[i-100000], 
                children_dic, 
                recruiting_numbers_list
            )
        
        # Package instance data
        instance_data = {
            'children': children_dic,
            'daycares': daycares_dic,
            'families': families_dic,
            'params': {
                'total_children': total_children,
                'total_families': total_families,
                'single_child_families': single_child_families,
                'two_siblings_families': two_siblings_families,
                'three_siblings_families': three_siblings_families,
                'daycare_num': daycare_num,
                'phi': phi,
                'varepsilon': varepsilon,
                'recruiting_numbers': recruiting_numbers_list
            }
        }
        
        instances.append(instance_data)
    
    return instances


# if __name__ == "__main__":
#     # Parameters
#     target_children_sizes = [500, 1000, 3000, 5000, 10000]
#     phi_values = [0.9,1.0]

#     # Create base directory for datasets
#     base_dir = Path('mallows/datasets')
#     base_dir.mkdir(exist_ok=True)

#     # Generate and save data for each configuration
#     for total_children in target_children_sizes:
#         print(f"\nGenerating data for total children: {total_children}")
#         total_families, single_child_families, two_siblings_families, three_siblings_families = calculate_family_size(total_children)
#         print(f"  Families breakdown:")
#         print(f"    Total families: {total_families}")
#         print(f"    Total children: {single_child_families + two_siblings_families * 2 + three_siblings_families * 3}")
#         print(f"    Single child: {single_child_families}")
#         print(f"    Two siblings: {two_siblings_families}")
#         print(f"    Three siblings: {three_siblings_families}")
        
#         for phi in phi_values:
#             print(f"  φ = {phi}")
#             filename = base_dir / f"instances_children_{total_children}_phi_{phi}.pkl.gz"
#             if filename.exists():
#                 print(f"\nSkipping existing file: {filename}")
#                 continue
            
#             # Generate instances
#             instances = generate_data(total_children, phi)
            
#             # Package with metadata
#             dataset = {
#                 'params': {
#                     'total_children': total_children,
#                     'total_families': total_families,
#                     'single_child_families': single_child_families,
#                     'two_siblings_families': two_siblings_families,
#                     'three_siblings_families': three_siblings_families,
#                     'phi': phi,
#                 },
#                 'instances': instances
#             }

#             # Save to compressed pickle file
#             filename = base_dir / f"instances_children_{total_children}_phi_{phi}.pkl.gz"
#             with gzip.open(filename, 'wb') as f:
#                 pickle.dump(dataset, f)
            
#             print(f"    Saved to {filename}")

#     print(f"\nData generation complete!")