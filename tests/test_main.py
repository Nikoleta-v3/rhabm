import rhabm


def test_simulate_returns_park():
    width = 5
    height = 5
    number_of_rhinos = 2
    number_of_poachers = 2
    number_of_security_agents = 1
    clock = 5

    simulation = rhabm.simulate(
        width=width,
        height=height,
        number_of_rhinos=number_of_rhinos,
        number_of_poachers=number_of_poachers,
        number_of_security_agents=number_of_security_agents,
        clock=clock,
    )

    assert isinstance(simulation, rhabm.Park)
    assert simulation.height == height
    assert simulation.width == width
    assert isinstance(simulation.__repr__(), str)


def test_simulate_with_history():
    width = 5
    height = 5
    number_of_rhinos = 2
    number_of_poachers = 2
    number_of_security_agents = 1
    clock = 5
    keep_history = True

    simulation = rhabm.simulate(
        width=width,
        height=height,
        number_of_rhinos=number_of_rhinos,
        number_of_poachers=number_of_poachers,
        number_of_security_agents=number_of_security_agents,
        clock=clock,
        keep_history=keep_history,
    )

    assert isinstance(simulation, rhabm.Park)
    assert simulation.height == height
    assert simulation.width == width
    assert len(simulation.history) == clock


def test_simulate_with_non_symmetrical_park():
    width = 1
    height = 2
    number_of_rhinos = 0
    number_of_poachers = 0
    number_of_security_agents = 0

    simulation = rhabm.simulate(
        width=width,
        height=height,
        number_of_rhinos=number_of_rhinos,
        number_of_poachers=number_of_poachers,
        number_of_security_agents=number_of_security_agents,
    )

    assert isinstance(simulation, rhabm.Park)
    assert simulation.height == height
    assert simulation.width == width
    assert simulation.coordinates == [(0, 0), (1, 0)]
