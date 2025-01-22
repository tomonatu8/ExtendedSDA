def create_test_instance_1():
    children_dic = {
        1: {
            'id': 1,
            'age': 3,
            'family_id': 1,
            'initial_daycare_id': 1,
            'actual_daycare_id': 1,
            'preference_list': [2, 1]
        },
        2: {
            'id': 2,
            'age': 3,
            'family_id': 2,
            'initial_daycare_id': 2,
            'actual_daycare_id': 2,
            'preference_list': [1, 2]
        },
        3: {
            'id': 3,
            'age': 4,
            'family_id': 2,
            'initial_daycare_id': 2,
            'actual_daycare_id': 2,
            'preference_list': [1, 2]
        }
    }
    daycares_dic = {
        1: {
            'id': 1,
            'recruiting_numbers_list': [2, 1, 1, 1, 1, 1],
            'priority_child_id_list': [1, 2, 3],
            'priority_score_list': [1.0, 0.8, 0.9],
            'share_ages_list': []
        },
        2: {
            'id': 2,
            'recruiting_numbers_list': [2, 1, 1, 1, 1, 1],
            'priority_child_id_list': [2, 1, 3],
            'priority_score_list': [1.0, 0.9, 0.8],
            'share_ages_list': []
        }
    }
    families_dic = {
        1: {
            'id': 1,
            'children': [1],
            'pref': [2, 1]
        },
        2: {
            'id': 2,
            'children': [2, 3],
            'pref': [(1, 1), (2, 2)]
        }
    }
    return children_dic, daycares_dic, families_dic


def create_test_instance_2():
    children_dic = {
        1: {
            'id': 1,
            'age': 3,
            'family_id': 1,
            'initial_daycare_id': 1,
            'actual_daycare_id': 1,
            'preference_list': [2, 1]
        },
        2: {
            'id': 2,
            'age': 3,
            'family_id': 2,
            'initial_daycare_id': 2,
            'actual_daycare_id': 2,
            'preference_list': [1, 2]
        },
        3: {
            'id': 3,
            'age': 4,
            'family_id': 2,
            'initial_daycare_id': 2,
            'actual_daycare_id': 2,
            'preference_list': [1, 2]
        }
    }
    daycares_dic = {
        1: {
            'id': 1,
            'recruiting_numbers_list': [2, 1, 1, 1, 1, 1],
            'priority_child_id_list': [1, 2, 3],
            'priority_score_list': [1.0, 0.8, 0.9],
            'share_ages_list': []
        },
        2: {
            'id': 2,
            'recruiting_numbers_list': [2, 1, 1, 1, 1, 1],
            'priority_child_id_list': [2, 1, 3],
            'priority_score_list': [1.0, 0.9, 0.8],
            'share_ages_list': []
        }
    }
    families_dic = {
        1: {
            'id': 1,
            'children': [1],
            'pref': [2, 1]
        },
        2: {
            'id': 2,
            'children': [2, 3],
            'pref': [(1, 1), (2, 2)]
        }
    }
    return children_dic, daycares_dic, families_dic




def create_test_presented_in_Theorem_1():
    children_dic = {
        1: {
            'id': 1,
            'age': 0,
            'family_id': 1,
            'initial_daycare_id': None,
            'actual_daycare_id': None,
            'preference_list': []
        },
        2: {
            'id': 2,
            'age': 0,
            'family_id': 1,
            'initial_daycare_id': None,
            'actual_daycare_id': None,
            'preference_list': []
        },
        3: {
            'id': 3,
            'age': 0,
            'family_id': 2,
            'initial_daycare_id': None,
            'actual_daycare_id': None,
            'preference_list': [2]
        }
    }
    daycares_dic = {
        1: {
            'id': 1,
            'recruiting_numbers_list': [1, 1, 1, 1, 1, 1],
            'priority_child_id_list': [1, 3, 2],
            'priority_score_list': [1.0, 0.9, 0.8],
            'share_ages_list': []
        },
        2: {
            'id': 2,
            'recruiting_numbers_list': [1, 1, 1, 1, 1, 1],
            'priority_child_id_list': [1, 3, 2],
            'priority_score_list': [1.0, 0.9, 0.8],
            'share_ages_list': []
        },
        3: {
            'id': 3,
            'recruiting_numbers_list': [1, 1, 1, 1, 1, 1],
            'priority_child_id_list': [1, 3, 2],
            'priority_score_list': [1.0, 0.9, 0.8],
            'share_ages_list': []
        }
    }
    families_dic = {
        1: {
            'id': 1,
            'children': [1,2],
            'pref': [(1, 2), (2, 3)]
        },
        2: {
            'id': 2,
            'children': [3],
            'pref': [2]
        }
    }
    return children_dic, daycares_dic, families_dic