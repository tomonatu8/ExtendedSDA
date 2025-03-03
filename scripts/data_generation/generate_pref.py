import random
from typing import TypeVar, Union, Generic, Any, cast, Sequence, List

T = TypeVar('T')


def generate_pref(
        items: List[T],
        length: int,
        seed: int
) -> List[T]:
    """
    Generate a preference list by randomly sampling from a list of options.
    
    This function works with both lists of integers and lists of tuples.
    
    Parameters
    -----------
    items : List[T]
        List of items to choose from (can be integers or tuples)
    length : int
        Number of items to select
    seed : int, optional
        Random seed for reproducibility
        
    Returns
    --------
    List[T]
        Random sample of length items from the input list
    """
    rng = random.Random(seed)
    
    if len(items) <= length:
        return items.copy() 
    
    return rng.sample(items, length)