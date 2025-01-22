from typing import List

def update_pi(
        pi: List[int], 
        j: int, 
        i: int
) -> List[int]:
    """
    Swaps the elements at indices i and j in the permutation pi to create a new permutation pi_prime.
    
    Parameters:
    - pi: The original list representing a permutation.
    - j: The index of the first element to swap.
    - i: The index of the second element to swap.

    Returns:
    - A new list representing the permutation after the swap.
    """
    pi_prime: List[int] = []
    for _ in range(len(pi)):
        pi_prime.append(0)
    for ind in range(0,j):
        pi_prime[ind]=pi[ind]
    pi_prime[j] = pi[i]
    for ind in range(j+1,i+1):
        pi_prime[ind] = pi[ind-1]
    for ind in range(i+1,len(pi)):
        pi_prime[ind] = pi[ind]

    return pi_prime