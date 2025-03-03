import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir.replace("/test", ""))


from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family
from scripts.esda.unified_ESDA_algorithm import unified_ESDA_algorithm
from scripts.cp.CP_algo import CP
from scripts.data_generation.data_generation import data_generation





def test_imple():
    """
    Test function that runs various matching algorithms on generated data.
    """


    # Data generation parameters
    num_of_total_children = 100
    num_of_total_families = 82
    num_of_single_child_families = 69
    num_of_two_siblings_families = 8
    num_of_three_siblings_families = 5
    num_of_total_daycares = 15

    single_child_pref_length = 5
    multi_child_pref_length = 10
    daycare_priority_length = 20 

    num_instances = 100
    capacity = [5, 5, 1, 1, 1, 1]
    varepsilon = 1.0  
    phi = 0.5
    age_distribution = [0.3, 0.3, 0.15, 0.15, 0.05, 0.05]
    seed = 100

    # Print configuration
    print("================ DATA GENERATION SETTINGS ================")
    print(f"Children: {num_of_total_children}  |  Families: {num_of_total_families}")
    print(f"Family distribution: {num_of_single_child_families} single, {num_of_two_siblings_families} two-child, {num_of_three_siblings_families} three-child")
    print(f"Daycares: {num_of_total_daycares}  |  Capacity: {capacity}")
    print(f"Preference lengths: {single_child_pref_length} (single), {multi_child_pref_length} (multi)")
    print(f"Parameters: φ={phi}, ε={varepsilon}")
    print(f"Age distribution: {age_distribution}")
    print(f"Generating {num_instances} instances with seed {seed}")
    print("========================================================")

    print("\nGenerating instances...")
    instances = data_generation(
        num_of_total_children,
        num_of_total_families, 
        num_of_single_child_families, 
        num_of_two_siblings_families, 
        num_of_three_siblings_families,
        num_of_total_daycares,
        capacity,
        varepsilon,
        phi,
        single_child_pref_length,
        multi_child_pref_length,
        daycare_priority_length,
        age_distribution,
        num_instances,
        seed
    )
    print(f"Generated {len(instances)} instances successfully\n")
    
    # Track results
    sc_results = []
    sda_results = []
    esda_results = []
    cp_results = []
    
    # Test SC algorithm
    print("================ RUNNING SC ALGORITHM ================")
    for i, instance in enumerate(instances):
        if i % 20 == 0:
            print(f"Testing instance {i+1}/{num_instances}...")
        
        children_dic = instance['children_dic']
        daycares_dic = instance['daycares_dic']
        families_dic = instance['families_dic']
        
        success = unified_ESDA_algorithm(children_dic, daycares_dic, families_dic, "SC", exclude_family=False)
        sc_results.append(success)
    
    sc_success_count = sum(sc_results)
    print(f"SC Algorithm: {sc_success_count}/{len(sc_results)} successful ({sc_success_count/len(sc_results)*100:.1f}%)")
    
    # Test SDA algorithm
    print("\n================ RUNNING SDA ALGORITHM ================")
    for i, instance in enumerate(instances):
        if i % 20 == 0:
            print(f"Testing instance {i+1}/{num_instances}...")
        
        children_dic = instance['children_dic']
        daycares_dic = instance['daycares_dic']
        families_dic = instance['families_dic']
        
        success = unified_ESDA_algorithm(children_dic, daycares_dic, families_dic, "SDA", exclude_family=False)
        sda_results.append(success)
    
    sda_success_count = sum(sda_results)
    print(f"SDA Algorithm: {sda_success_count}/{len(sda_results)} successful ({sda_success_count/len(sda_results)*100:.1f}%)")
    
    # Test ESDA algorithm
    print("\n================ RUNNING ESDA ALGORITHM ================")
    for i, instance in enumerate(instances):
        if i % 20 == 0:
            print(f"Testing instance {i+1}/{num_instances}...")
        
        children_dic = instance['children_dic']
        daycares_dic = instance['daycares_dic']
        families_dic = instance['families_dic']
        
        success = unified_ESDA_algorithm(children_dic, daycares_dic, families_dic, "ESDA", exclude_family=True)
        esda_results.append(success)
    
    esda_success_count = sum(esda_results)
    print(f"ESDA Algorithm: {esda_success_count}/{len(esda_results)} successful ({esda_success_count/len(esda_results)*100:.1f}%)")
    
    # Test CP algorithm
    print("\n================ RUNNING CP ALGORITHM ================")
    for i, instance in enumerate(instances):
        if i % 20 == 0:
            print(f"Testing instance {i+1}/{num_instances}...")
        
        children_dic = instance['children_dic']
        daycares_dic = instance['daycares_dic']
        families_dic = instance['families_dic']
        
        try:
            solver_status, _, _, _, _ = CP(
                children_dic, 
                daycares_dic, 
                families_dic, 
                share_bool=False, 
                bp_num=0, 
                solver_time=1000, 
                exclude_bool=False, 
                search_depth=0
            )
            success = solver_status != "INFEASIBLE"
            cp_results.append(success)
        except Exception as e:
            print(f"  Error in instance {i+1}: {e}")
            cp_results.append(False)
    
    cp_success_count = sum(cp_results)
    print(f"CP Algorithm: {cp_success_count}/{len(cp_results)} successful ({cp_success_count/len(cp_results)*100:.1f}%)")
    
    # Summary
    print("\n================ SUMMARY ================")
    print(f"SC Algorithm:  {sc_success_count}/{len(sc_results)} ({sc_success_count/len(sc_results)*100:.1f}%)")
    print(f"SDA Algorithm: {sda_success_count}/{len(sda_results)} ({sda_success_count/len(sda_results)*100:.1f}%)")
    print(f"ESDA Algorithm: {esda_success_count}/{len(esda_results)} ({esda_success_count/len(esda_results)*100:.1f}%)")
    print(f"CP Algorithm:  {cp_success_count}/{len(cp_results)} ({cp_success_count/len(cp_results)*100:.1f}%)")
    print("=====================================")
    
