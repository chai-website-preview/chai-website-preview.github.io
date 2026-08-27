---
title: Discovering User-Interpretable Capabilities of Black-Box Planning Agents
slug: discovering-user-interpretable-capabilities-of-black-box-planning-agents-2
date: '2022-09-09 08:05:00'
status: publish
author: rosaliefaddoul
wp_id: 3763
original_url: https://humancompatible.ai/news/2022/09/09/discovering-user-interpretable-capabilities-of-black-box-planning-agents-2/
excerpt: Several approaches have been developed for answering users’ specific questions about AI behavior and for assessing their core functionality in terms of primitive executable actions
categories:
- news
featured_image: ../../assets/featured/2022/09/KR2022-1.png
summary_html: Pulkit Verma and Siddharth Srivastava from CHAI along with Shashank Marpally published a <a href="https://proceedings.kr.org/2022/36/kr2022-0036-verma-et-al.pdf">paper</a> on Discovering User-Interpretable Capabilities of Black-Box Planning Agents at<a href="https://kr2022.cs.tu-dortmund.de/"> the Knowledge Representation and Reasoning, KR 2022</a>.
---

Pulkit Verma and Siddharth Srivastava from CHAI along with Shashank Marpally published a [paper](https://proceedings.kr.org/2022/36/kr2022-0036-verma-et-al.pdf) on Discovering User-Interpretable Capabilities of Black-Box Planning Agents at [the Knowledge Representation and Reasoning, KR 2022](https://kr2022.cs.tu-dortmund.de/).

They argue that several approaches have been developed for answering users’ specific questions about AI behavior and for assessing their core functionality in terms of primitive executable actions. However, the problem of summarizing an AI agent’s broad capabilities for a user has received little research attention. This is aggravated by the fact that users may not know which questions to ask in order to understand the limits and capabilities of a system. This paper presents an algorithm for discovering from scratch the suite of high-level “capabilities” that an AI system with arbitrary internal planning algorithms/policies can perform. It computes conditions describing the applicability and effects of these capabilities in user-interpretable terms. Starting from a set of user-interpretable state properties, an AI agent, and a simulator that the agent can interact with, using arbitrary decision-making paradigms over primitive operations (unknown to the user), our algorithm returns a set of high-level capabilities with capability descriptions in the user’s vocabulary. Empirical evaluation on several game-based scenarios shows that this approach efficiently learns interpretable descriptions of various types of AI agents in deterministic, fully observable settings. User studies show that such interpretable descriptions are easier to understand and reason with than the agent’s primitive actions.
