import pytest
from typing import List
import sys
import os
import pickle

sys.path.append(os.path.dirname((os.path.abspath(__file__))).replace("/test",""))


from scripts.esda.agent_class import SDA_Child, SDA_Daycare, SDA_Family


from scripts.data_generation.data_generation import data_generation


def test_imple():
    total_children = 1000
    phi = 0.5
    instances = data_generation(total_children, phi)
