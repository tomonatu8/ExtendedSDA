import random
from typing import Dict, DefaultDict, List, Any, Tuple, Optional

def generate_pref(
        list_0: List[int], 
        length: int
) -> List[int]:
        return random.sample(list_0, length)

