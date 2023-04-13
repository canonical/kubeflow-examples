# SC2 MLFlow demo

This is an MLFlow for SC2 model training demo for Kubecon US 2022

# Environment preparation

Install Starctaft 2 game as this is what we will be playing
> http://us.battle.net/sc2/en/legacy-of-the-void/

Install Conda and create Python 3.7 or higher env

Install SC2 API and OpenAI baselines

> pip install git+https://github.com/deepmind/pysc2

> pip install git+https://github.com/openai/baselines

use requirements.txt for all other dependencies

# 1_basicSC2python.py
This shows a simple binding to a SC2 game instance and running a bot

# 2_combat.py
This shows a combat between 2 players

# 3_generatingTactics.py
This shows an automated "tactics", where the bot tries to build certain units in certain order. Now we can control the bot.

# 4_generatingData.py
If we want to train a model we need an agent that will gather some more data for us. This shows an agent gathering an plotting information

# 5_botVsBot.py
We cannot play alone - this shows how to run 2 agents against each other, one a simple game bot and the other training itself with every iteration using RL and a QLearningTable

# 6_training
Training the RL model

# MLFlow notebook
This shows how to use MLFlow to make our lives easier while training multiple iterations

Run by
> jupyter lab

and select the MLFlow.ipynb file there