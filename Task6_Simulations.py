#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Update on Sun Jan 18 21:14:12 2026

@author: rarrayaIU (Roberto Arraya)

DLMAIIAC01
Causality and Inference

Task 6 - Advanced Workbook

Problem Statement: 
Task 6: A company wants to get feedback on their product and uses a voluntary survey to ask their customers. 
For example, we can imagine that the company runs a webservice and customers use a web-browser or app to use this service. 
The link to the survey is placed on the webpage and inside the app, but customers are not required to fill in the survey at any point of using the product. 
As part of the survey, the customers are asked to rate their satisfaction with the product on a scale of 1 (very satisfied) to 6 (not satisfied). 
To present the findings of the feedback to the management, the feedback should be mapped to a simple visualization such as a traffic light whether the customers are happy, or action is required.
Discuss which bias(es) may arise due to the setup of the way the feedback is acquired and outline potential paths to mitigate them.
How is the “traffic light” indicator for the management affected if the probability of taking the survey depends on the satisfaction? 
Create a numerical simulation to illustrate the result. For simplicity, assume that we can model the results of the survey using a Poisson distribution where we map any value greater than 6 to 6 (not satisfied).
   
"""
#IMPORT RElEVANT Libraries
import numpy as np
import pandas as pd
from pgmpy.readwrite import BIFReader
import networkx as nx
import matplotlib.pyplot as plt 
from scipy.special import logit #, expit

#TEMP
#import os
#os.getcwd()
#

# -----------------------------
# USER CHOICES
# -----------------------------

populationSize = 50000  # population size represents the number of possible survey takers

# Choose target response rate (e.g., 0.10 = 10%)
target_response_rate = 0.10

# Choose satisfaction selection bias strength. This affects how strongly dissatisfaction affects response
# Options: "small", "medium", "large"
satisfaction_selection_bias = "large"

# Choose selection mechanism.This affects whether latent traits affect the response
# Options: "outcome_only" or "outcome_and_latent"
#selection_type = "outcome_only"
selection_type = "outcome_and_latent"

# Choose green and red thresholds on scale of 1 to 6
thres_green = 2.5
thres_red = 4 

# Poisson rate is function of L lambda(i) = exp(beta0 + betaL x L)
"""
beta0
• −0.5 → population mostly satisfied (mean ≈ 1.5–2.0)
• 0.0 → population moderately satisfied (mean ≈ 2.0–2.5)
• 0.5 → population mixed (mean ≈ 2.5–3.5)
• 1.0 → population leaning dissatisfied (mean ≈ 3.5–4.5)
betaL
• 0.0 → no latent heterogeneity
• −0.2 → mild heterogeneity
• −0.3 → moderate heterogeneity
• −0.6 → strong heterogeneity
"""
beta0 = 0.5 # higher values yield more dissatisfaciton
betaL = -0.3 # higherL means slightly better satisfaction


###############################################################################
# RUN SIMULATION
###############################################################################

# -----------------------------
# MAP USER CHOICES TO PARAMETERS, note some values may be arbitrary to the simulation
# -----------------------------

# Back-calculate α0 from target response rate
# We want: expit(α0) = target_response_rate  when S=0, L=0
alpha0 = logit(target_response_rate)

# Choose αS based on bias strength
if satisfaction_selection_bias == "small":
    alphaS = 0.2
elif satisfaction_selection_bias == "medium":
    alphaS = 0.5
elif satisfaction_selection_bias == "large":
    alphaS = 1.0
else:
    raise ValueError("Invalid satisfaction_selection_bias option")

# Choose αU based on selection type
if selection_type == "outcome_only":
    alphaL = 0.0
    dagName = 'TrafficLightDAG_OutcomeOnly.bif'
elif selection_type == "outcome_and_latent":
    alphaL = 0.3
    dagName = 'TrafficLightDAG.bif'
else:
    raise ValueError("Invalid selection_type option")
    

# Create the DAG and group Latent traits in L
# This DAG represents the outcome and latent option only. Outcome only would remove causality from L to R. 

#folderPath = ('/Users/rarraya/anaconda_projects/Python Files/Causality and Inference')
#os.chdir(folderPath)
##print(os.listdir())
#reader = BIFReader(folderPath + dagName)
reader = BIFReader(dagName)
model = reader.get_model()
model.check_model()


# L represents the set of latent variables grouped into one category
# These can be user characteristics, patience, tech affinity, mood, even current transactional experience
L = np.random.normal(0, 1, populationSize)

# Poisson rate is function of L lambda(i) = exp(beta0 + betaL x L)
lambda_poisson = np.exp(beta0 + betaL * L)
#Unbounded Poisson satisfaction value without truncation

# S represents actual satisfaction modeled via Poisson with truncation
S_star = np.random.poisson(lambda_poisson)
#Truncate values to 1 - 6
S_actual = np.clip(S_star, 1, 6)
#Pass model values to Satisfaction Node
S = S_actual  

print("Total Range for S:", S.min(), " - ", S.max())

#print("Value counts (true):")

print("Mean S (Real-world):", S.mean())

# Selection mechanism
# More negative means fewer people respond
# More positive means more people respond

#alpha0 = -1.0
#alphaS = 0.5   # dissatisfied more likely to respond
#alphaL = 0.3
#print(alpha0)
#print(alphaS)
#print(alphaL)

#Generate Response Node
logit_p = alpha0 + alphaS * S + alphaL * L
p = 1 / (1 + np.exp(-logit_p))
R = np.random.binomial(1, p)

# Compute number of respondents
num_respondents = R.sum()
# Compute means
response_rate = R.mean()
S_real_world_mean = S.mean()
S_observed_mean = S[R == 1].mean()

print()
print("##########################################")
print("#         SIMULATION RESULTS           ##")
print("##########################################")
print()
print("Number of respondents:", num_respondents)
print()
print("Response rate:", response_rate)
print()
print(pd.Series(S).value_counts().sort_index())
print()
print('Entire Population Satisfaction Score: ' + str(round(S_real_world_mean,3)))
print()
print('Survey Taker Satisfaction Score: ' + str(round(S_observed_mean,3)))
print()

# Map to traffic light
def traffic_light(m,threshold_green,threshold_red):
    if m < threshold_green:
        return "green"
    elif m > threshold_red:
        return "red"
    else:
        return "yellow"

#Define 
real_world_light = traffic_light(S_real_world_mean,thres_green,thres_red)
observed_light = traffic_light(S_observed_mean,thres_green,thres_red)

print('Real World Traffic Light result: ' + str(real_world_light))
print()
print('Observed Traffic Light result: ' + str(observed_light))
print()
print()
print("##########################################")
print("#         SIMULATION END                ##")
print("##########################################")

#Build Causal Graph
G = model  

#print(G.nodes())
#print(G.edges())

G = nx.DiGraph()
G.add_nodes_from(model.nodes())
G.add_edges_from(model.edges())

plt.figure(figsize=(7, 7))
pos = nx.spring_layout(G, seed=42)   # stable layout
nx.draw(
    G, pos,
    with_labels=True,
    node_size=2000,
    node_color='lightblue',
    arrows=True,
    font_size=12
)
plt.show()
