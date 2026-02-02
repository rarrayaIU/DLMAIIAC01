# DLMAIIAC01
Inference and Causality Course IU
Task 6 Simulation
Prior to running script, verify you have the following files: 
1) TrafficLightDAG_OutcomeOnly.bif
2) TrafficLightDAG.bif
3) Task6_Simulation.py
4) environment_minimal.yml
5) environment_Full.yml

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
  
STEPS to Execute Code 
Prerequisites: 
- CONDA
- Python Version >= 3.10
- Some extra libraries may be required
- Download Files locally

In terminal, navigate to folder location where files are located. 

OPTION I ) MINIMAL EXECUTION 
-------------------------------
1) Generate minimal environment to ensure version compatibility
conda env create -f environment_minimal.yml
2) Activate minimal environment
conda activate trafficlight-simulation-minimal
3) Choose variables by editing the python file in an editor of choice. 
4) Run Simulation 
python Task6_Simulations.py

******** NOTE ***********
* ONLY execute if minimal installation does not provide required packages
*************************

OPTION II ) MINIMAL EXECUTION 
-------------------------------
If Simulation fails, please attempt to install the full environment
1) Generate full environment to ensure version compatibility
conda env create -f environment_Full.yml
2) Activate full environment
conda activate trafficlight-simulation-full-env
3) Choose variables by editing the python file in an editor of choice.
4) Run Simulation 
python Task6_Simulations.py

**************************



