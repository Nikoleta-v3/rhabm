rhabm
=====

A rhino poaching agent based simulation tool written in Python. "🌲🦏🔪🚓"

## Installation

Either download or clone this repo:

```
$ git clone https://github.com/Nikoleta-v3/rhabm.git
```

## How to use

```python
>>> import rhabm 

>>> width = 10
>>> height = 10
>>> number_of_rhinos = 10
>>> number_of_poachers = 5
>>> number_of_security_agents = 6
>>> number_of_selective_poachers = 2
>>> clock = 100
>>> keep_history = True

>>> simulation = rhabm.simulate(width=width,
....                            height=height,
....                            number_of_rhinos=number_of_rhinos,
....                            number_of_poachers=number_of_poachers,
....                            number_of_security_agents=number_of_security_agents,
....                            number_of_selective_poachers=number_of_security_agents,
....                            clock=100,
....                            keep_history=keep_history)

>>> simulation
[🦏, '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲']
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲']
['🌲', '🌲', '🌲', ⛓️, '🌲', 🦏, '🌲', '🌲', '🌲', '🌲']
['🌲', '🌲', '🌲', '🌲', 💀, '🌲', '🌲', '🌲', 🚓, '🌲']
['🌲', '🌲', '🌲', 🦏, 🚓, '🌲', '🌲', '🌲', '🌲', 🚓]
['🌲', 🦏, '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲']
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', 🚓, '🌲', ⛓️, '🌲']
[🚓, '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', 🦏, '🌲', '🌲']
['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', 🚓, ⛓️]
['🌲', '🌲', 🦏, '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲']
```

## Licence

Under MIT [licence](LICENCE).

## Contributions
All contributions are welcome 🎉.