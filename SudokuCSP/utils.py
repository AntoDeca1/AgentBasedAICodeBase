def domains_filter(domains, variables_to_fix):
    """
    :param domains:
    :param variables_to_fix: tuple(var,value)
    :return:
    """
    new_domains = dict(domains)
    for var, val in variables_to_fix:
        del new_domains[var]
    return new_domains


def state_filter(state, variables_to_fix):
    new_state = dict(state)
    for var, val in variables_to_fix:
        new_state[var] = val
    return new_state


