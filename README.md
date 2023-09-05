# Connecting NDVI, Groundwater, and Stream Disconnection During Drought: Case Study along the Rio Grande
#### Repo for Data Challenge
#### Written by Danielle Tadych

The purpose of this repository is to be a hub for working with Planet Data and also a final deliverable for the data challenge 2023.

In this repository there is:
 - DataChallengeReport_RioGrandeAnalysis.ipynb: A python notebook for analyzing Planet data and creating NDVI Products.  This also contains final Results
 - RioGrandeAnalysis_Expanded.ipynb: This is a python notebook similar to the "DataChallengeReport...", however it is expanded to include the ability to create areas of interest and order data from planet.
 - AOI: Files for areas of interest
 - data: place to store order files from planet
 - Tutorials: Tutorials from Planet Jupyter notebooks repository
 - outputfiles: Location of output files from analysis

### Workflow for working on Virtual Machines:
1. Launch virtual machine on cyverse
2. Navigate to /home/jovyan/data-store
3. git clone repo
4. install environment if planet environment is not currently activated
    - Launching Planet Jupyter Labs on cyverse automatically activates planet environment
      * update:* lies, to activate the environment paste
      conda install -f ../environment.yml
      
      
Quick access committing:
    git commit -m "words here about what crimes you committed"
