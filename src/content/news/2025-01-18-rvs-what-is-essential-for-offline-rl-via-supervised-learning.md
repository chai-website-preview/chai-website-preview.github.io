---
title: 'RvS: What is Essential for Offline RL via Supervised Learning?'
slug: rvs-what-is-essential-for-offline-rl-via-supervised-learning
date: '2025-01-18 09:55:12'
status: publish
author: chaiadmin
wp_id: 5816
original_url: https://humancompatible.ai/news/2025/01/18/rvs-what-is-essential-for-offline-rl-via-supervised-learning/
categories:
- news
featured_image: ../../assets/featured/2021/03/emmons-square-1.jpg
---

Scott Emmons, PhD student, was an author on "RvS: What is Essential for Offline RL via Supervised Learning?"

Recent work has shown that supervised learning alone, without temporal difference (TD) learning, can be remarkably effective for offline RL. When does this hold true, and which algorithmic components are necessary? Through extensive experiments, we boil supervised learning for offline RL down to its essential elements. In every environment suite we consider, simply maximizing likelihood with a two-layer feedforward MLP is competitive with state-of-the-art results of substantially more complex methods based on TD learning or sequence modeling with Transformers. Carefully choosing model capacity (e.g., via regularization or architecture) and choosing which information to condition on (e.g., goals or rewards) are critical for performance. These insights serve as a field guide for practitioners doing Reinforcement Learning via Supervised Learning (which we coin "RvS learning"). They also probe the limits of existing RvS methods, which are comparatively weak on random data, and suggest a number of open problems.

Link to paper: <https://arxiv.org/abs/2112.10751>
