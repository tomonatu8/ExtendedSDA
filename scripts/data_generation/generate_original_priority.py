import numpy as np
import random
from typing import Dict, DefaultDict, List, Any, Tuple, Optional
from collections import defaultdict

def generate_original_priority(
        n: int, 
        families_dic: DefaultDict[int, DefaultDict[str, Any]], 
        varepsilon: float
) -> List[int]:
    
    original_priority: List[int] = []
    for key in families_dic:
        if len(families_dic[key]['children']) == 1:
            original_priority.append(families_dic[key]['children'][0])
        else:
            if random.random() < 1.0/(n**(1+varepsilon)):
                for c in families_dic[key]['children']:
                    original_priority.append(c)
            else:
                original_priority.append(- 1 * key)
    original_priority = np.random.permutation(original_priority)
    new_original_priority: List[int] = []
    for id in original_priority:
        if id<0:
            for c in families_dic[-1 * id]['children']:
                new_original_priority.append(c)
        else:
            new_original_priority.append(id)

    return new_original_priority