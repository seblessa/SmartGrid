# Multi-Agent System for Smart Grid Management

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

Time Agent: time_agent@localhost

| Username                                | Password    |
|-----------------------------------------|-------------|
| `grid_controller@localhost`             | `SmartGrid` |
| `fossil_fuel_power_generator@localhost` | `SmartGrid` |
| `green_power_controller@localhost`      | `SmartGrid` |
| `wind_energy_controller@localhost`      | `SmartGrid` |
| `wind_energy_generator@localhost`       | `SmartGrid` |
| `solar_energy_controller@localhost`     | `SmartGrid` |
| `solar_energy_generator@localhost`      | `SmartGrid` |
| `hydro_energy_generator@localhost`      | `SmartGrid` |
| `hospital_demander@localhost`           | `SmartGrid` |
| `fire_station_demander@localhost`       | `SmartGrid` |
| `police_station_demander@localhost`     | `SmartGrid` |
| `neighborhood_controller@localhost`     | `SmartGrid` |
| `school_demander@localhost`             | `SmartGrid` |
| `house_demander@localhost`              | `SmartGrid` |

### Comunication of each agent

| Agent Name                  | Receives Information from                                                           | Sends Information         |
|-----------------------------|-------------------------------------------------------------------------------------|---------------------------|
| grid_controller             | `green_power_controller`, `fossil_fuel_power_generator`                             | `energy_controller`       |
| fossil_fuel_power_generator | Doesn't receive information from another agent                                      | `grid_controller`         |
| green_power_controller      | `wind_energy_controller`,    `solar_energy_controller`   , `hydro_energy_generator` | `grid_controller`         |
| wind_energy_controller      | `wind_energy_generator`                                                             | `green_power_controller`  |
| wind_energy_generator       | Doesn't receive information from another agent                                      | `wind_energy_controller`  |
| solar_energy_controller     | `solar_energy_generator`                                                            | `green_power_controller`  |
| solar_energy_generator      | Doesn't receive information from another agent                                      | `solar_energy_controller` |
| hydro_energy_generator      | Doesn't receive information from another agent                                      | `green_power_controller`  |
| hospital_demander           | Doesn't receive information from another agent                                      | `grid_controller`         |
| fire_station_demander       | Doesn't receive information from another agent                                      | `grid_controller`         |
| police_station_demander     | Doesn't receive information from another agent                                      | `grid_controller`         |
| neighborhood_controller     | `school_demander`          , `house_demander`                                       | `grid_controller`         |
| school_demander             | Doesn't receive information from another agent                                      | `neighborhood_controller` |
| house_demander              | Doesn't receive information from another agent                                      | `neighborhood_controller` |




## Interesting for our project

- Ter os agentes a comunicar entre si e não com o ambiente onde existem (ambiente multi-agente)
- Centralização vs Descentralização.
- Contract net


To do list
- Class 