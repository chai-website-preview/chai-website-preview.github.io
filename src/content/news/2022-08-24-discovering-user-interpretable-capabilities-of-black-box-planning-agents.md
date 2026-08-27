---
title: Discovering User-Interpretable Capabilities of Black-Box Planning Agents
slug: discovering-user-interpretable-capabilities-of-black-box-planning-agents
date: '2022-08-24 09:19:09'
status: publish
author: rosaliefaddoul
wp_id: 3681
original_url: https://humancompatible.ai/news/2022/08/24/discovering-user-interpretable-capabilities-of-black-box-planning-agents/
excerpt: Pulkit Verma and Siddharth Srivastava from CHAI co-wrote this paper with Shashank Marpally. Both Verma and Srivastava are affiliates of CHAI.
categories:
- news
featured_image: ../../assets/featured/2022/01/CHAI-360x230-1.png
summary_html: Pulkit Verma and Siddharth Srivastava from CHAI co-wrote this paper with Shashank Marpally. Both Verma and Srivastava are affiliates of CHAI.
---

Pulkit Verma and Siddharth Srivastava from CHAI co-wrote this paper with Shashank Marpally. Both Verma and Srivastava are affiliates of CHAI.

Several approaches have been developed for answering users’ specific questions about AI behavior and for assessing their core functionality in terms of primitive executable actions. However, the problem of summarizing an AI agent’s broad capabilities for a user has received little research attention. This is aggravated by the fact that users may not know which questions to ask in order to understand the limits and capabilities of a system. This paper presents an algorithm for discovering from scratch the suite of high-level “capabilities” that an AI system with arbitrary internal planning algorithms/policies can perform. It computes conditions describing the applicability and effects of these capabilities in user-interpretable terms. Starting from a set of user-interpretable state properties, an AI agent, and a simulator that the agent can interact with, using arbitrary decision-making paradigms over primitive operations (unknown to the user), our algorithm returns a set of high-level capabilities with capability descriptions in the user’s vocabulary. Empirical evaluation on several game-based scenarios shows that this approach efficiently learns interpretable descriptions of various types of AI agents in deterministic, fully observable settings. User studies show that such interpretable descriptions are easier to understand and reason with than the agent’s primitive actions.

You can find the published paper [here](https://arxiv.org/abs/2207.10192).
