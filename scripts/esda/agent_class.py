from typing import Dict, List, Any, Optional

class SDA_Child():
    """
    Attributes
    ----------
    id : int
        child id
    age : int
        age (0-5)
    family : int = Family.id
    initial_daycare : int 
    actual_daycare : int
    pref : list[int]
    assigned_daycare_id : int
    """
    def __init__(
            self, 
            c_id:int, 
            age:int, 
            family_id:int, 
            initial_daycare_id:int, 
            actual_daycare_id:int, 
            preference_list: List[int]
        ): 
        # attributes from dictionary
        self.id = c_id
        self.age = age
        self.family = family_id
        self.initial_daycare = initial_daycare_id
        self.actual_daycare = actual_daycare_id
        self.pref = [d_id if d_id != None else 9999 for d_id in preference_list] 
        self.assigned_daycare: Optional[SDA_Family] = None
        self.projected_pref: List[int] = []
        self.all_daycare_ids: List[int] = []      
        self.has_siblings = False
        
    def __str__(self):
        return f'child {self.id}'
    def __repr__(self):
        return f'child {self.id}'
    


class SDA_Daycare():
    """
    Attributes
    ----------
    id: int
        daycare id, a dummy daycare with id=9999 for unmatched children 
    recruiting_numbers_list: list[int]
        the number of recruiting children by age, where each position represents one age
    priority_child_id_list: list[int]
        priority list of each daycare
        only store child.id
    priority_score_list: list[float]
    total_numbers: list[int]
        the number of children who prefer transfers by age
    priority_age_dic: dict
    priority_age_share_dic: dict
    """
    def __init__(
            self, 
            d_id:int, 
            recruiting_numbers_list:list[int],  
            priority_child_id_list: list[int], 
            priority_score_list: list[float]
        ):
        
        # attributes from dictionary
        self.id = d_id
        self.recruiting_numbers = recruiting_numbers_list
        self.priority = priority_child_id_list
        self.score_list = priority_score_list
        self.total_numbers = [x for x in self.recruiting_numbers]
        self.priority_age_dic: Dict[int,List[int]] = {}
        self.priority_age_share_dic = {}
        self.assigned_children = [[] for _ in range(6)]
        
    def __str__(self):
        return f'daycare {self.id}'
    def __repr__(self):
        return f'daycare {self.id}'

    def update_priority_age_dic(self, children):
        '''
        create a priority dictionary by age from self.priority_list
        '''
        self.priority_age_dic = {}
        for age in range(6):
            self.priority_age_dic[age] = []
        for c in self.priority:
            
            if c not in self.priority_age_dic[c.age]:
                self.priority_age_dic[c.age].append(c)



class SDA_Family():
    """
    Attributes
    ----------
    id: int
    children: list[int]
    pref: list[tuple[int]]
    assignment: tuple[int]
    """

    def __init__(
            self, 
            f_id:int, 
            children_id_list:list=[int], 
            pref_list:list=[int], 
            assignment_daycare_id_list = None
        ):
        
        self.id = f_id
        self.children = children_id_list
        self.pref = pref_list
        self.assignment = assignment_daycare_id_list
        self.has_siblings = len(self.children) > 1
        
    def __str__(self):
        return f'family {self.id}'
    def __repr__(self):
        return f'family {self.id}'