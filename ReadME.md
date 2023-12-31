# Multi-Agent System for Smart Grid Management

**Authors**
- [Margarida Vila Chã](https://github.com/margaridavc/)
- [Sebastião Santos Lessa](https://github.com/seblessa/)

#### Python versions used:

`Python 3.11.5`
`Python 3.9.18`

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

## Explanation of our thought process

#### We started by creating the environment and the agents.

The environment is the following:

- Class _**SmartGridEnvironment**_ in `enviroment.py`


The agents are the following:

### List of users on our server


| Username                                | Password    |
|-----------------------------------------|-------------|
| `grid_controller@localhost`             | `SmartGrid` |
| `time_agent@localhost`                  | `SmartGrid` |
| `fossil_fuel_power_generator@localhost` | `SmartGrid` |
| `green_power_controller@localhost`      | `SmartGrid` |
| `wind_energy_controller@localhost`      | `SmartGrid` |
| `solar_energy_controller@localhost`     | `SmartGrid` |
| `hydro_energy_generator@localhost`      | `SmartGrid` |
| `hospital_demander@localhost`           | `SmartGrid` |
| `fire_station_demander@localhost`       | `SmartGrid` |
| `police_station_demander@localhost`     | `SmartGrid` |
| `neighborhood_controller@localhost`     | `SmartGrid` |
| `school_demander@localhost`             | `SmartGrid` |
| `house_demander@localhost`              | `SmartGrid` |
| `map_drawer@localhost`                  | `SmartGrid` |
