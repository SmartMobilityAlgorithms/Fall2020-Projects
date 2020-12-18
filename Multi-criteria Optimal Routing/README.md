# Multi-Criteria Optimal Routing Problem

## Introduction

The _bio-inspired algorithms_ we chose to solve the Multi-Criteria Optimal Routing Problem are __Genetic Algorithm (GA)__ and __Particle Swarm Optimization (PSO)__. Additionally, we have designed __adaptive versions__ of above algorithms using Tabu List.

## Dataset
- data/uoft-highway-factors-fixed.osm
- data/large_data.osm

## Experiment Implementation
#### 1. Data preparation (search space)

#### 2. Prepare dataset for multi-criteria:
- Cost of distance on a route
- Cost of travel time on a route

#### 3. Prepare attributes for soft constraints
- Number of traffic signs
- Number of bus stops
- Close to any shop

#### 4. Define source and destination nodes
#### 5. Run Genetic Algorithm
#### 6. Run Practicle Swarm Optimization
#### 7. Apply different hyper-parameters
#### 8. Analysis and Comparison:
- Quality
- Converge time
- Compare within and between algorithms

## Adaptive Algorithm Experiment
Include a Tabu List with respect to runtime status to automatically adjust between _diversification_ and _intensification_. Compare the performance between non-adaptive version and adaptive version.

## Code
- Running GA and PSO on Small dataset: `Project_Fixed_Small_Dataset.ipynb`
- Running GA and PSO on Large dataset: `Project_Fixed_Large_Dataset.ipynb`
- Running Adaptive versions of GA and PSO: `Project_Adaptive.ipynb`
