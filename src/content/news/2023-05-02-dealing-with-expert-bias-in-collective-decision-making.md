---
title: Dealing with expert bias in collective decision-making
slug: dealing-with-expert-bias-in-collective-decision-making
date: '2023-05-02 14:15:19'
status: publish
author: rosaliefaddoul
wp_id: 4012
original_url: https://humancompatible.ai/news/2023/05/02/dealing-with-expert-bias-in-collective-decision-making/
excerpt: In their paper published in the AI journal, CHAI Tom Lenaerts and Axel Abels argue that quite some real-world problems can be formulated as decision-making problems wherein one must repeatedly make an appropriate choice from a set of alternatives.
categories:
- news
featured_image: ../../assets/featured/2023/05/expert-bias-climbing-to-knowledge.png
---

In their [paper published in the AI journal](https://www.sciencedirect.com/science/article/abs/pii/S000437022300067X?via%3Dihub), CHAI Tom Lenaerts and Axel Abels argue that quite some real-world problems can be formulated as decision-making problems wherein one must repeatedly make an appropriate choice from a set of alternatives. They explain that multiple expert judgments, whether human or artificial, can help in taking correct decisions, especially when exploration of alternative solutions is costly. As expert opinions might deviate, the problem of finding the right alternative can be approached as a collective decision making problem (CDM) via aggregation of independent judgments. Current state-of-the-art approaches focus on efficiently finding the optimal expert, and thus perform poorly if all experts are not qualified or if they display consistent biases, thereby potentially derailing the decision-making process. In this paper, they propose a new algorithmic approach based on contextual multi-armed bandit problems (CMAB) to identify and counteract such biased expertise. They explore homogeneous, heterogeneous and polarized expert groups and show that this approach is able to effectively exploit the collective expertise, outperforming state-of-the-art methods, especially when the quality of the provided expertise degrades. Their novel CMAB-inspired approach achieves a higher final performance and does so while converging more rapidly than previous adaptive algorithms.
