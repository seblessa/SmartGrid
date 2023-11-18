# Multi-Agent System for Smart Grid Management

#### Python versions used:

`Python 3.11.5`
`Python 3.9.18`


## List of users on our server

| Username                                | Password    |
|-----------------------------------------|-------------|
| `admin@localhost`                       | `SmartGrid` | 
| `grid_controller@localhost`             | `SmartGrid` |
| `green_power_generator@localhost`       | `SmartGrid` |
| `wind_energy_generator@localhost`       | `SmartGrid` |
| `solar_energy_generator@localhost`      | `SmartGrid` |
| `hydro_energy_generator@localhost`      | `SmartGrid` |
| `energy_consumer@localhost`             | `SmartGrid` |
| `NeighborhoodControllerAgent@localhost` | `SmartGrid` |



## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 main.py
```


## Explanation of our thought process

We started by creating two agents `GridControllerAgent` and `PowerGeneratorAgent` and `EnergyConsumerAgent`.
Then we tested the messaging system between the three agents.
After that we created an environment for the agents to interact with each other.

## Interesting for our project

- Ter os agentes a comunicar entre si e não com o ambiente onde existem (ambiente multi-agente)
- Centralização vs Descentralização.
- Contract net
