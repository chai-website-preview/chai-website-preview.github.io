---
title: 'NeurIPS Paper: Scalable Online Planning via Reinforcement Learning Fine-Tuning 12-6'
slug: neurips-paper-scalable-online-planning-via-reinforcement-learning-fine-tuning-12-6
date: '2021-11-18 03:06:00'
status: publish
author: andrewpereira
wp_id: 3302
original_url: https://humancompatible.ai/news/2021/11/18/neurips-paper-scalable-online-planning-via-reinforcement-learning-fine-tuning-12-6/
excerpt: CHAI’s Arnaud Fickinger and Stuart Russell co-authored the paper with Noam Brown, Brandon Amos, and Hengyuan Hu.
categories:
- news
featured_image: ../../assets/featured/2021/11/neurIPS.jpeg
---

CHAI’s Arnaud Fickinger and Stuart Russell co-authored the [paper](https://arxiv.org/pdf/2109.15316.pdf) with Noam Brown, Brandon Amos, and Hengyuan Hu. They replace tabular search (MCTS, SPARTA, etc.) with neural network fine-tuning via deep reinforcement learning and obtain state-of-the-art results in the cooperative game Hanabi. Read the abstract here:

Lookahead search has been a critical component of recent AI successes, such as in the games of chess, go, and poker. However, the search methods used in these games, and in many other settings, are tabular. Tabular search methods do not scale well with the size of the search space, and this problem is exacerbated by stochasticity and partial observability. In this work we replace tabular search with online model-based fine-tuning of a policy neural network via reinforcement learning, and show that this approach outperforms state-of-the-art search algorithms in benchmark settings. In particular, we use our search algorithm to achieve a new state-of-the-art result in self-play Hanabi, and show the generality of our algorithm by also showing that it outperforms tabular search in the Atari game Ms. Pacman.
