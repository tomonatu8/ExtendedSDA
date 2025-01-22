from typing import Dict, List, Any, Tuple
from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family

def get_agent(
        agent_id: int, 
        agents: List[Any]
) -> Any:
    '''
    return an agent instance for given id (including child / daycare / families)
    '''
    agent = next((x for x in agents if x.id == agent_id), None)
    
    return agent

def create_children(
        children_dic: Dict[int, Dict[str, Any]]
) -> List[SDA_Child]:
    '''
    Parameters
    ----------
    children_dic : Dict[int, Dict[str, int]]

    Returns
    -------
    result : List[Child]
    '''
    children: List[SDA_Child] = []
    for c_id in children_dic.keys():
        c_id = children_dic[c_id]['id']
        age = children_dic[c_id]['age']
        if children_dic[c_id]['family_id'] == None: 
            family_id = children_dic[c_id]['id'] 
            # family_id = children_dic[c_id]['id'] + 10000 # for an only child, set c.family as c.id + 10000
        else:
            family_id = children_dic[c_id]['family_id']
        if children_dic[c_id]['initial_daycare_id'] == None:
            initial_daycare_id = 9999 # convert None into 9999
        else:
            initial_daycare_id = children_dic[c_id]['initial_daycare_id']
        if children_dic[c_id]['actual_daycare_id'] == None:
            actual_daycare_id = 9999 # convert None into 9999
        else:
            actual_daycare_id = children_dic[c_id]['actual_daycare_id']
        preference_list = children_dic[c_id]['preference_list']
        
        # create a Child instance
        c = SDA_Child(c_id, age, family_id, initial_daycare_id, actual_daycare_id, preference_list)
        children.append(c)
    return children



def create_daycares(
        daycares_dic: Dict[int, Dict[str, Any]]
) -> List[SDA_Daycare]:
    '''
    Parameters
    ----------
    daycares_dic : Dict[int, Dict[str, int]]

    Returns
    -------
    result : list[Daycare]
    '''
    daycares: List[SDA_Daycare] = []
    
    for d_id in daycares_dic.keys():
        
        # retrive the data of each daycare
        d_id = daycares_dic[d_id]['id']
        recruiting_numbers_list = daycares_dic[d_id]['recruiting_numbers_list']
        priority_child_id_list = daycares_dic[d_id]['priority_child_id_list']
        priority_score_list = daycares_dic[d_id]['priority_score_list']
        
        # create a Daycare instance
        d = SDA_Daycare(d_id, recruiting_numbers_list, priority_child_id_list, priority_score_list)
        daycares.append(d)
        
    dummy_id = 9999
    recruiting_numbers_list = [9999 for i in range(6)]
    priority_child_id_list = []
    priority_score_list = []
    dummy = SDA_Daycare(dummy_id , recruiting_numbers_list, priority_child_id_list, priority_score_list)
    daycares.append(dummy)
        
    return daycares


def create_families(
        families_dic: Dict[int, Dict[str, Any]]
) -> List[SDA_Family]:
    '''
    Parameters
    ----------
    families_dic : dict[dict]

    Returns
    -------
    result : list[Family]
    '''
    families: List[SDA_Family] = []
    for f_id in families_dic.keys():
        
        # retrive the data of each family
        f_id = families_dic[f_id]['id'] 
        children_id_list = families_dic[f_id]['children'] 
        pref_list = families_dic[f_id]['pref'] 
        assignment = None
        
        f = SDA_Family(f_id, children_id_list, pref_list, assignment)
        families.append(f)
        
    return families




def update_children_attributes(
        children: List[SDA_Child], 
        families: List[SDA_Family], 
        daycares: List[SDA_Daycare]
):
    for c in children:
        pref_list_c=[]
        for d_id in c.pref:
            for daycare in daycares:
                if d_id == daycare.id:
                    pref_list_c.append(daycare)
            if pref_list_c == []:
                print('Daycare whose id is '+str(d_id)+' was not found.')
        c.pref = pref_list_c

        if c.initial_daycare != 9999:
            for daycare in daycares:
                if daycare.id == c.initial_daycare:
                    if daycare not in c.pref:
                        c.pref.append(daycare)


        a=0
        for f in families:
            if c.family == f.id:
                c.family = f
                a+=1
                if f.has_siblings:
                    c.has_siblings = True
        if a == 0:
            print('Family whose id is '+str(c.family)+' was not found.')
        
def update_families_attributes(
        families: List[SDA_Family], 
        children: List[SDA_Child], 
        daycares: List[SDA_Daycare]
):
    for f in families:
        c_list = []
        for c_id in f.children:
            for child in children:
                if c_id == child.id:
                    c_list.append(child)
            if c_list == []:
                print('Child whose id is '+str(c_id)+' was not found.')
        f.children = c_list


        pref_list_f=[]

        if f.has_siblings:
            for d_tuple in f.pref:
                d_tuple_list=[]
                for d_id in d_tuple:
                    for daycare in daycares:
                        if d_id == daycare.id:
                            d_tuple_list.append(daycare)
                pref_list_f.append(tuple(d_tuple_list))
                if pref_list_f == []:
                    print('Daycare whose id is '+str(d_id)+' was not found.')
        else:
            for d_id in f.pref:
                for daycare in daycares:
                    if d_id == daycare.id:
                        pref_list_f.append(tuple([daycare]))
                if pref_list_f == []:
                    print('Daycare whose id is '+str(d_id)+' was not found.')
        f.pref = pref_list_f

def update_daycares_attributes(
        children: List[SDA_Child], 
        daycares: List[SDA_Daycare]
):
    for d in daycares:
        c_priority_list = []
        for c_id in d.priority:
            for child in children:
                if c_id == child.id:
                    c_priority_list.append(child)
            if c_priority_list == []:
                print('Child whose id is '+str(c_id)+' was not found.')
        d.priority = c_priority_list
    
        d.update_priority_age_dic(children)
        
    # update d.total_numbers
    for c in children:
        if c.initial_daycare != 9999:
            for d in daycares:
                if d.id == c.initial_daycare:
                    if c in d.priority:
                        d.priority.remove(c)
                        d.priority.insert(0,c)
                    else:
                        d.priority.insert(0,c)

    for c in children:
        initial = get_agent(c.initial_daycare, daycares)
        initial.total_numbers[c.age] += 1
        
    d9999 = get_agent(9999, daycares)
    for c in children:
        d9999.priority.append(c)
        d9999.score_list.append(1)



def create_agents(
        children_dic: Dict[int, Dict[str, Any]],
        daycares_dic: Dict[int, Dict[str, Any]],
        families_dic: Dict[int, Dict[str, Any]]
) -> Tuple[List[SDA_Child], List[SDA_Daycare], List[SDA_Family]]:
    children = create_children(children_dic)
    daycares = create_daycares(daycares_dic)
    families = create_families(families_dic)
    update_children_attributes(children, families, daycares)
    update_families_attributes(families, children, daycares)
    update_daycares_attributes(children, daycares)

    return children, daycares, families
