# Risk (game) Monte Carlo Simulator

![Risk board](images/risk_game.jpg)

<center>Risk game map</center>

## Intro

One exciting application of Monte Carlo Simulations is that they allow you to make better decisions when given a range of possible scenarios, which is especially useful in financial sectors such as risk or portfolio management. However, although less useful, its an interesting idea to apply high-level statistical tools such as Monte Carlo Simulation (MCS) to board games such *Risk*.

This repository contains all the code used to develop the Streamlit App and run the simulation locally.

## Quick Start

For a quick start, it is possible to use the simulation tool without any installation by accessing the dashboard hosted by Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://francescomrn-risk-monte-carlo-simulator-app-lheo12.streamlit.app/) 

[Open the Streamlit App](https://francescomrn-risk-monte-carlo-simulator-app-lheo12.streamlit.app/)

## Contents

*   [Getting started](#getting-started)
    *   [Install locally](#install-locally)
    *   [Usage](#usage)
*   [Functionalities and Outcomes](#functionalities-and-outcomes)
*   [Contribute](#contribute)
*   [License](#license)
*   [Conclusion](#conclusion)
*   [References](#references)

## Getting Started

So how do you get this template to work for your project? It is easier than you think.

### Install Locally

Use git to clone this repository into your computer.

```bash
git clone https://github.com/FrancescoMrn/MC_simulation_risk
```

Create a new environment i.e. with conda. Activate it and install the required packages

```bash
conda create -n risk_mc python=3.10 -y
conda activate risk_mc
```

Move into the git repo cloned above and run

```bash
pip install -r requirements.txt
```

### Usage

The main script can be executed by using the following command.

```bash
# Run the main script
python main.py
```

Nevertheless, the script in the current version does not expose any parameters to the command windows. To change the parameters or explore the code, running the script with an IDE is suggested.

## Functionalities and Outcomes

The code is designed to produce for a specific state (number of attackers, number of defenders) the following results:

- Probability of Win of the Attacker (A)
- Probability of Win of the Defender (A)
- Binomial Distribution Standard Deviation
- Number of units that best increase the defense capabilities (given the initial conditions)

Additional to the above results, the code produces three plots, saved inside the folder ```/plots```:

- Win probability and remaining units (for attacker and defender)
- Defender probability of a win for the incremental number of units
- Risk attacker strategy - Overview of how the delta, the difference in units between Attacker/Defender, affects the game

## Contribute

Pull requests are welcome. For significant changes, please open an issue to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Conclusion

To summarise, his repository implements a complete Monte Carlo Simulation of the game *Risk*. Through the simulation, some patterns specific to the game can be highlighted:

**Attackers strategy tip:**

- Aggressive strategies should be preferred over defensive ones
- Attack a territory only with a numerical advantage
- With more than five units than the defender, the probability of a win is ~90%

**Defenders strategy tip:**

- It's better to double up defence on single territories to improve the overall defence capability.
- The best reinforcement strategy is to get your regions up to the number of armies of the attacker.


## References

- Game rules and image [Ultra Board Games](https://www.ultraboardgames.com/risk/game-rules.php)
- [Simulating Risk The Board Game](https://juliangarratt.com/monte-carlo-simulations-simulating-risk-the-board-game/)
