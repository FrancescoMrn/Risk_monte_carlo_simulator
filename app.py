import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from src.game.play import RiskGame, State
from src.simulation.mc import MCSimulation
from src.visualization.plots import plot_histogram_probability, plot_defence_improvements

# Parameters 
DIE  = (1, 2, 3, 4, 5, 6) # define the die 
st.set_page_config(page_title="Risk MC")


st.title('Risk (game) Monte Carlo Simulator')
st.markdown("""<span style="word-wrap:break-word;">\
        This web app simulate the game and calulate \
        the probabilities of winning a round given the initial conditions\
        </span>""", unsafe_allow_html=True)
st.image("images/risk_game.jpg", caption="Risk game map")

st.header("Input the state of the game")
attacker = st.slider("Number of Attacker", 2, 50, 10)
defenders = st.slider("Number of Defenders", 2, 50, 5)
runs = st.slider("Number of Monte Carlo simulations", 100, 3000, 1000)

# Set the initial state of the simulation
state = State(A=attacker, D=defenders)

# Set up the game and the MC Simulation
risk = RiskGame(die=DIE)
mcsim = MCSimulation(riskgame=risk, runs=runs)

# Attacker MC Simulation
simout_attacker = mcsim.simulate_multiple_attack(state=state, normalization=True)
attacker_pwin = mcsim.pwin_probability(simout_attacker)
defender_pwin = mcsim.pwin_probability(simout_attacker, entity="defender")
hist = plot_histogram_probability(simout_attacker, state, save_fig=False)

# Defender MC Simulation
simout_defender = mcsim.simulate_defense_improvement(n_defenders = state.D, n_attacker = state.A, max_defenders = state.A * 2)
defender_additional_units, marginal_gain = mcsim.marginal_defence_improvement(simout_defender)
bars= plot_defence_improvements(simout_defender, state, marginal_gain, save_fig=False)

st.header("Simulation summary results")
st.markdown("""**Cumulative probabilities**""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Attacker P Win", attacker_pwin.p_win)
col2.metric("Denfender P Win", defender_pwin.p_win)
col3.metric("Binomial Distr. Std", attacker_pwin.sim_std_value)

st.markdown("""**Attacker Position Desciption:**""", unsafe_allow_html=True)
st.write("The aggregated probability of win for the attacker is:", attacker_pwin.p_win, "💣")
st.write("including the estimated ±3sigma (standard deviation) we obtain the range:") 
st.write("- highest probability of winning is:", attacker_pwin.p_win_high)
st.write("- lowest probability of winning is:", attacker_pwin.p_win_low)

st.markdown("""**Defender Position Desciption:**""", unsafe_allow_html=True)
st.write("The aggregated probability of win for the defender is:", defender_pwin.p_win, "🏰")
st.write("including the estimated ±3sigma (standard deviation) we obtain the range:") 
st.write("- highest probability of winning is:", defender_pwin.p_win_high)
st.write("- lowest probability of winning is:", defender_pwin.p_win_low)

st.write("👉 The best defence improvement is obtained with", defender_additional_units, "additional units 👈")

st.subheader("Visualizations")
st.pyplot(hist)
st.pyplot(bars)

col1, col2, col3= st.columns([.35, .3, .35])
with col2:
    st.write("[GitHub Repository](https://github.com/FrancescoMrn/MC_simulation_risk)💡")
