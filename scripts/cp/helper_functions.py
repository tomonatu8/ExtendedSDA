from scripts.cp.CP_agents import CP_Daycare, CP_Child, CP_Family

def get_agent(agent_id, agents):
    '''
    return a CP_agent instance for given id (including child / daycare / families)
    '''
    agent = next((x for x in agents if x.id == agent_id), None)
    return agent

def create_children(children_dic):
    '''
    create a list of CP_child instances from data stored in children_dic
    '''
    children = []
    for c_id in children_dic.keys():
        c_id = children_dic[c_id]['id']
        age = children_dic[c_id]['age']
        if children_dic[c_id]['family_id'] == None:
            family_id = children_dic[c_id]['id']
        else:
            family_id = children_dic[c_id]['family_id']
        initial_daycare_id = 9999 if children_dic[c_id]['initial_daycare_id'] == None else children_dic[c_id]['initial_daycare_id']
        actual_daycare_id = 9999 if children_dic[c_id]['actual_daycare_id'] == None else children_dic[c_id]['actual_daycare_id']
        preference_list = children_dic[c_id]['preference_list']
        # create a CP_Child instance
        c = CP_Child(c_id, age, family_id, initial_daycare_id, actual_daycare_id, preference_list)
        children.append(c)
    return children

def create_daycares(daycares_dic):
    '''
    create a list of CP_Daycare instances from data stored in daycares_dic
    '''
    daycares = []
    for d_id in daycares_dic.keys():
        d_id = daycares_dic[d_id]['id']
        recruiting_numbers_list = daycares_dic[d_id]['recruiting_numbers_list']
        share_ages_list = daycares_dic[d_id]['share_ages_list']
        priority_child_id_list = daycares_dic[d_id]['priority_child_id_list']
        priority_score_list = daycares_dic[d_id]['priority_score_list']
        # create a CP_Daycare instance
        d = CP_Daycare(d_id, recruiting_numbers_list, share_ages_list, priority_child_id_list, priority_score_list)
        daycares.append(d)
    # create a dummy daycare for being unmatched
    dummy_id = 9999
    recruiting_numbers_list = [9999 for i in range(6)]
    share_ages_list = []
    priority_child_id_list = []
    priority_score_list = []
    dummy = CP_Daycare(dummy_id , recruiting_numbers_list, share_ages_list, priority_child_id_list, priority_score_list)
    daycares.append(dummy)
    return daycares


def create_families(families_dic):
    '''
    create a list of CP_family instances from data stored in families_dic
    '''
    families = []
    for f_id in families_dic.keys():
        f_id = families_dic[f_id]['id']
        children_id_list = families_dic[f_id]['children']
        pref_list = families_dic[f_id]['pref']
        assignment = None
        # create a CP_Family instance
        f = CP_Family(f_id, children_id_list, pref_list, assignment)
        families.append(f)
    return families

def update_families_attributes(families):
    '''
    for families with an only child,
        1) convert f.pref: list[int] into f.pref list[tuple(int)]
        2) convert None into 9999
    '''
    for f in families:
        if f.has_siblings == False:
            f.pref = [tuple([d_id]) for d_id in f.pref]
        for pos in range(len(f.pref)):
            new = []
            tup_p = f.pref[pos]
            for item in tup_p:
                if item == None:
                    new.append(9999)
                else:
                    new.append(item)
            f.pref[pos]=tuple(new)

def update_children_attributes(children, families):
    '''
    1) c.projected_pref is induced from f.pref
    2) c.all_daycare_ids is calulated from c.projected_pref
    '''
    # update c.projected_pref
    for f in families:
        for pos in range(len(f.pref)):
            tup_p = f.pref[pos]
            for index, d_id in enumerate(tup_p):
                f_c = get_agent(f.children[index], children)
                f_c.projected_pref.append(tup_p[index])
    # update c.all_daycare_ids
    for c in children:
        c_d_ids = []
        for d_id in c.projected_pref:
            if d_id not in c_d_ids:
                c_d_ids.append(d_id)
        c.all_daycare_ids = c_d_ids

def update_daycares_attributes(children, daycares):
    '''
    1) update the priority ordering / score list of dummy daycare 9999
    2) update d.priority_age_dic & d.priority_age_share_dic
    3）update d.total_numbers & d.total_numbers_share
    '''
    # update dummy.priority
    dummy = get_agent(9999, daycares)
    for c in children:
        if 9999 in c.projected_pref and c.id not in dummy.priority:
            dummy.priority.append(c.id)

    # update dummy.score_list
    dummy.score_list = [100 for x in range(len(dummy.priority))]

    # update d.priority_age_dic & d.priority_age_share_dic & d.total_numbers
    for d in daycares:
        d.update_priority_age_dic(children)
        d.update_priority_age_share_dic(children)

    # update d.total_numbers
    for c in children:
        initial = get_agent(c.initial_daycare, daycares)
        initial.total_numbers[c.age] += 1

    # update d.total_numbers_share
    for d in daycares:
        ############################################################
        # modify on 23.05.28
        d.total_numbers_share = [x for x in d.total_numbers]
        ############################################################
        if len(d.all_shared_ages) > 0:
            for ages in d.share_ages_list:
                quota_ages = 0
                for age in ages:
                    quota_ages += d.total_numbers[age]
                for age in ages:
                    d.total_numbers_share[age] = quota_ages

def create_agents(children_dic, daycares_dic, families_dic):
    '''
    Don't change the order of the following functions
    '''
    children = create_children(children_dic)
    daycares = create_daycares(daycares_dic)
    families = create_families(families_dic)
    update_families_attributes(families)
    update_children_attributes(children, families)
    update_daycares_attributes(children, daycares)
    return children, daycares, families

def check_IR(children):
    non_IR_children = []
    for c in children:
        if c.initial_daycare != 9999 and c.assigned_daycare == 9999:
            non_IR_children.append(c.id)

    if len(non_IR_children) == 0:
        print('the outcome satisfies IR')
    else:
        print('the outcome does not satisfy IR')

    return non_IR_children

def check_feasibility(children, daycares, share_bool):

    infeasible_daycare_ids = []

    # number of matched children by age
    outcome_daycares = {}
    for d in daycares:
        outcome_daycares[d.id] = [0 for g in range(6)]
    for c in children:
        if c.assigned_daycare != None:
            outcome_daycares[c.assigned_daycare][c.age] += 1

    # check feasibility
    if share_bool == False:
        for d in daycares:
            for g in range(6):
                if outcome_daycares[d.id][g] > d.total_numbers[g] and d.id not in infeasible_daycare_ids:
                    infeasible_daycare_ids.append(d.id)
    else:
        for d in daycares:
            for g in range(6):
                if g in d.all_shared_ages:
                    related_ages = d.return_related_ages(g)
                    sum_matched = 0
                    for x in related_ages:
                        sum_matched += outcome_daycares[d.id][x]

                    if sum_matched > d.total_numbers_share[g] and d.id not in infeasible_daycare_ids:
                        infeasible_daycare_ids.append(d.id)
                else:
                    if outcome_daycares[d.id][g] > d.total_numbers[g] and d.id not in infeasible_daycare_ids:
                        infeasible_daycare_ids.append(d.id)


    if len(infeasible_daycare_ids) == 0:
        print('the outcome is feasible')
    else:
        print('the outcome is NOT feasible')

    return infeasible_daycare_ids

def check_bp(children_dic, daycares_dic, families_dic, outcome_f):

    # create CP_agents
    children, daycares, families = create_agents(children_dic, daycares_dic, families_dic)

    # update f.assignment & c.assigned_dacayre
    for f in families:
        for p in range(len(f.pref)):

            # 注意： outcome_f　は重要だ！！！
            if outcome_f[f.id, p] == 1:
                f.assignment = p

                for cid in f.children:
                    c = get_agent(cid, children)
                    c.assigned_daycare = c.projected_pref[p]

        if f.assignment == None:
            f.assignment = len(f.pref)

    # blocking coalition
    bp_dic = {}
    for f in families:
        bp_dic[f.id] = []

    for f in families:
        # ignore all families who are matched to their top choice
        if f.assignment != 0:
            # check every position prior to f.assignment
            for p in range(f.assignment):
                # D(f, p)
                D_fp = f.return_daycare_id_for_certain_position(p)
                bool_all = 0

                for d in D_fp:
                    # default all 0 (could accept C_fpd)
                    bool_fpd = [0 for i in range(6)]
                    # C(f,p,d)
                    C_fpd = f.return_children_for_certain_position_and_daycare(p, d)
                    for g in range(6):
                        # C(f,p,d,g)
                        C_fpdg = f.return_siblings_for_certain_position_daycare_age(p, d, g, False, children, daycares)
                        if len(C_fpdg) != 0:
                            w_fpd = f.return_lowest_sibling_for_certain_position_daycare_age(p, d, g, False, children, daycares)
                            daycare = get_agent(d, daycares)
                            better_cid = daycare.return_weak_better_children_than_child_excluding_siblings(w_fpd, children, False, True, 0)
                            better_number = 0
                            for x in better_cid:
                                xc = get_agent(x, children)
                                if xc.assigned_daycare == d:
                                    better_number += 1

                            if better_number + len(C_fpdg) > daycare.recruiting_numbers[g]:
                                bool_fpd[g] = 1

                    if sum(bool_fpd) == 0:
                        bool_all += 1

                if bool_all == len(D_fp):
                    if p not in bp_dic[f.id]:
                        bp_dic[f.id].append(p)

    num_bp = 0
    for key in bp_dic.keys():
        num_bp += len(bp_dic[key])

    if num_bp == 0:
        print('the outcome is stable')
    else:
        print('the outcome is NOT stable')

    return bp_dic

def check_outcome(children_dic, daycares_dic, families_dic, outcome_children_dic, outcome_f, share_bool):

    children, daycares, families = create_agents(children_dic, daycares_dic, families_dic)

    for c in children:
        c.assigned_daycare = outcome_children_dic[c.id]['CP']

    non_IR_children = check_IR(children)
    infeasible_daycare_ids = check_feasibility(children, daycares, share_bool)
    bp_dic = check_bp(children_dic, daycares_dic, families_dic, outcome_f)

    return non_IR_children, infeasible_daycare_ids, bp_dic
