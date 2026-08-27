---
title: 'SMCP3: Sequential Monte Carlo with Probabilistic Program Proposals'
slug: smcp3-sequential-monte-carlo-with-probabilistic-program-proposals
date: '2023-07-21 01:11:33'
status: publish
author: rosaliefaddoul
wp_id: 4459
original_url: https://humancompatible.ai/news/2023/07/21/smcp3-sequential-monte-carlo-with-probabilistic-program-proposals/
excerpt: This paper introduces SMCP3, a new family of sequential Bayesian inference algorithms.
categories:
- news
featured_image: ../../assets/featured/2023/07/Screenshot-2023-07-21-at-10.09.56-AM.png
summary_html: To develop aligned AI systems which can make accurate inferences about people’s objectives, and then act on those objectives, we need AI to understand when it is uncertain about what people want. In cases where it is uncertain, an AI should act cautiously, and seek more information about the preferences of the person the AI is trying to assist (for instance, by asking the person a question). To build AI systems which can do this, we need robust methods enabling AIs to reason about their own uncertainty in a calibrated way.
---

To develop aligned AI systems which can make accurate inferences about people’s objectives, and then act on those objectives, we need AI to understand when it is uncertain about what people want. In cases where it is uncertain, an AI should act cautiously, and seek more information about the preferences of the person the AI is trying to assist (for instance, by asking the person a question). To build AI systems which can do this, we need robust methods enabling AIs to reason about their own uncertainty in a calibrated way.

[This paper](https://proceedings.mlr.press/v206/lew23a/lew23a.pdf), written by Alexander K. Lew, George Matheos, Tan Zhi-Xuan, Matin Ghavamizadeh, Nishad Gothoskar, Stuart Russell and Vikash Mansinghka for the 26th International Conference on Artificial Intelligence and Statistics, introduces SMCP3, a new family of sequential Bayesian inference algorithms. This can be used to develop agents which can reason about their own uncertainty, and maintain calibrated estimates of their uncertainty over time. The paper also contributes software which can automate the implementation of SMCP3 algorithms, given a probabilistic program defining the agent’s mental model of the world, and probabilistic programs describing algorithms for updating hypothesized world states in light of new data.
