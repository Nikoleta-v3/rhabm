import random

import rhabm


def simulate(
    width,
    height,
    number_of_rhinos,
    number_of_poachers,
    number_of_selective_poachers=0,
    value_threshold=0.5,
    number_of_devalued_rhinos=0,
    devalued_value=0.2,
    target_value=1,
    number_of_security_agents=2,
    clock=200,
    keep_history=False,
    seed=0,
):

    park = rhabm.Park(width=width, height=height)
    agents = [
        rhabm.Rhino(park)
        for _ in range(number_of_rhinos - number_of_devalued_rhinos)
    ]
    agents += [
        rhabm.Rhino(park, devalued_value)
        for _ in range(number_of_devalued_rhinos)
    ]
    agents += [
        rhabm.Poacher(park, target_value=target_value)
        for _ in range(number_of_poachers - number_of_selective_poachers)
    ]
    agents += [
        rhabm.Poacher(
            park,
            minimum_horn_value_threshold=value_threshold,
            target_value=target_value,
        )
        for _ in range(number_of_selective_poachers)
    ]
    agents += [
        rhabm.SecurityOfficer(park) for _ in range(number_of_security_agents)
    ]

    if keep_history:
        park.history = []

    random.seed(seed)
    for tick in range(clock):
        random.shuffle(agents)
        if keep_history:
            park.history.append(park.__repr__())

        for agent in agents:
            agent.move()

    return park
