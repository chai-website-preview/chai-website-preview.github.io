---
title: Conditional Abstraction Trees for Sample-Efficient Reinforcement Learning
slug: conditional-abstraction-trees-for-sample-efficient-reinforcement-learning
date: '2023-08-31 15:44:00'
status: publish
author: dalereed
wp_id: 4558
original_url: https://humancompatible.ai/news/2023/08/31/conditional-abstraction-trees-for-sample-efficient-reinforcement-learning/
excerpt: In many real-world problems, the learning agent needs to learn a problem’s abstractions and solution simultaneously. However, most such abstractions need to be designed and refined by hand for different problems and domains of application.
categories:
- news
featured_image: ../../assets/featured/2023/09/taxi-2023-09-08-160318.png
---

In this paper published on 07/31/2023 titled [Conditional Abstraction Trees for Sample-Efficient Reinforcement Learning](https://aair-lab.github.io/Publications/dns_uai23.pdf), Siddharth Srivastava, Mehdi Dadvar, Rashmeet Kaur Nayyar develop a novel approach for online learning of abstractions that improve the sample efficiency and scalability of reinforcement learning in long-horizon, sparse-reward tasks. Empirical analysis shows that this approach improves sample efficiency of Q-learning to the point where it can outperform SOTA DRL approaches even when including the samples used for learning the abstraction. Additionally, it shows that the learned abstractions effectively capture semantic subtask structures in long-horizon, sparse-reward stochastic planning problems.

This paper develops a new way of learning abstraction hierarchies while carrying out reinforcement learning. Such methods can allow AI systems to accomplish long-horizon tasks where user preferences are sparse and cannot be used to provide continual feedback on the agent's actions. This approach can also be used to autonomously extract high-level actions and improve the efficiency of planning in stochastic environments.
