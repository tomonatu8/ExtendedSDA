from typing import Dict, List, Any, Tuple, Optional

import pytest
import sys
import os
import time
import traceback

sys.path.append(os.path.dirname((os.path.abspath(__file__))).replace("/test",""))
from scripts.esda.unified_ESDA_algorithm import unified_ESDA_algorithm

from test.create_test_instances import create_test_instance_1, create_test_instance_2, create_test_presented_in_Theorem_1



def test_SC_algorithm_1():
    children_dic, daycares_dic, families_dic = create_test_instance_1()
    start_time = time.time()
    try:
        success = unified_ESDA_algorithm(children_dic, daycares_dic, families_dic, "SC", exclude_family=False)
        computation_time = time.time() - start_time
        print("test_SC_algorithm_1:",success, computation_time)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        traceback.print_tb(exception_traceback)
        exit()
        raise Exception(f"Error: {e}")


def test_SC_presented_in_Theorem_1():
    children_dic, daycares_dic, families_dic = create_test_presented_in_Theorem_1()
    start_time = time.time()
    try:
        success = unified_ESDA_algorithm(children_dic, daycares_dic, families_dic, "SC", exclude_family=False)
        computation_time = time.time() - start_time
        print("test_SC_presented_in_Theorem_1:",success, computation_time)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        traceback.print_tb(exception_traceback)
        exit()
        raise Exception(f"Error: {e}")