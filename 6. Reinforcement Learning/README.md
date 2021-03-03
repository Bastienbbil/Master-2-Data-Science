# Reinforcement Learning Course

This course was taught by E. Le Pennec (Polytechnique)

The pratical work consisted in working on an article through an analysis, discussion and implementation. 

For this, we worked in a group of 3 students on the article [*Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model*](https://arxiv.org/abs/1911.08265v2). The result of our work is contained in this repository with the following elements:

* The paper studied on the MuZero algorithm (Mastering-Atari-Go-Chess-and-Shogi-by-Planning-with-a-Learned-Model-.pdf)

* The co-written report of our analysis containing a theoretical explanation and ddiscussion of the article, a link with our implementation and a comparison with the AlphaZero algorithm (Rapport_Reinforcement_Learning.pdf)

* The implemented work which consists in a practical implementation of the MuZero algorithm and its components with an application to the CartPole game from the Gym environment. The code we started it with comes from [J. Gras](https://github.com/johan-gras/MuZero) (Implémentation_MuZero_Projet_Reinforcement_Learning.ipynb)

The work has been done in French. 

## The MuZero Algorithm 

The MuZero algorithm presented in the original paper is a model-based Reinforcement Learning algorithm. The principal motivation of the authors in defining the solution was to propose a model-based algorithm that achieved performance of state-of-the-art models in both strategic games such as chess, Go and Shogi (where model-based algorithms such as AlphaZero was state-of-the-art) and visually rich domains such as Atari 2006 (where model-free models were state-of-the-art). 