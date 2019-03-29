import random

import rhabm


def simulate(
    width,
    height,
    number_of_rhinos,
    number_of_poachers,
    number_of_security_agents,
    number_of_selective_poachers=0,
    value_threshold=0.5,
    number_of_devalued_rhinos=0,
    devalued_value=0.2,
    target_value=1,
    clock=200,
    keep_history=False,
    seed=None
):
    """ A function for running the simulation.

    Parameters
    ==========

    width : `int`
        The width of the park.
    height : `int`
        The height of the park.
    number_of_rhinos : `int`
        Number of rhino agents in the park.
    number_of_poachers : `int`
        Number of poacher agents in the park.
    number_of_security_agents : `int`
        Number of security officers in the park.
    number_of_selective_poachers : `int`
        The number of poacher that will behave selectively.
    value_threshold=0.5 : `int`
        The value horn threshold for which poachers will behave selectively.
    number_of_devalued_rhinos : `int`
        The number of devalued rhinos in the park.
    devalued_value : `float`
        The amount of horn left on devalued rhinos.
    target_value : `int`
        The amount of horn value a poacher must gain before leaving the park.
    clock : `int`
        The time units for which the simulation is run.
    keep_history : `bool`
        Keep tracks of history if True. False otherwise.
    seed : `int`
        The seed of the experiment.
    """

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

    if seed:
        random.seed(seed)
    for tick in range(clock):
        random.shuffle(agents)
        if keep_history:
            park.history.append(park.__repr__())

        for agent in agents:
            agent.move()

    return park
