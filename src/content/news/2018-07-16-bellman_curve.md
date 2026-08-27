---
title: Stuart Russell and Anca Dragan Publish Paper on “An Efficient, Generalized Bellman Update For Cooperative Inverse Reinforcement Learning”
slug: bellman_curve
date: '2018-07-16 12:00:00'
status: publish
author: Chris Northwood
wp_id: 203
original_url: https://humancompatible.ai/news/2018/07/16/bellman_curve/
categories:
- news
featured_image: ../../assets/featured/2018/07/rl.png
---

CHAI PI Stuart Russell and co-PI Anca Dragan, with a number of other authors from Berkeley’s School of Electrical Engineering and Computer Science, published “An Efficient, Generalized Bellman Update For Cooperative Inverse Reinforcement Learning” in the Proceedings of the 35th International Conference on Machine Learning in Stockholm, Sweden back in July 2018. The paper’s abstract states that:

Our goal is for AI systems to correctly identify and act according to their human user’s objectives. Cooperative Inverse Reinforcement Learning
(CIRL) formalizes this value alignment problem as a two-player game between a human and
robot, in which only the human knows the parameters of the reward function: the robot needs
to learn them as the interaction unfolds. Previous work showed that CIRL can be solved as a
POMDP, but with an action space size exponential in the size of the reward parameter space. In this work, we exploit a specific property of CIRL—the human is a full information agent—to derive an optimality-preserving modification to the standard Bellman update; this reduces the complexity of the problem by an exponential factor and allows us to relax CIRL’s assumption of human rationality. We apply this update to a variety of POMDP solvers and find that it enables us to scale CIRL to non-trivial problems, with larger reward parameter
spaces, and larger action spaces for both robot and human. In solutions to these larger problems, the human exhibits pedagogic behavior, while the robot interprets it as such and attains higher value for the human.
