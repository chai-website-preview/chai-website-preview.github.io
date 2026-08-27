---
title: Anca Dragan Publishes “Probabilistically Safe Robot Planning with Confidence-Based Human Predictions”
slug: anca_safe_robot
date: '2018-05-31 12:00:00'
status: publish
author: Chris Northwood
wp_id: 223
original_url: https://humancompatible.ai/news/2018/05/31/anca_safe_robot/
categories:
- news
---

The paper published in arXiv and supported by the National Science Foundation deals with human-computer interaction and having robots be able to navigate around moving people properly. The abstract reads:

In order to safely operate around humans, robots can employ predictive models of human motion. Unfortunately, these models cannot capture the full complexity of human behavior and necessarily introduce simplifying assumptions. As a result, predictions may degrade whenever the observed human behavior departs from the assumed structure, which can have negative implications for safety. In this paper, we observe that how “rational” human actions appear under a particular model can be viewed as an indicator of that model’s ability to describe the human’s current motion. By reasoning about this model confidence in a real-time Bayesian framework, we show that the robot can very quickly modulate its predictions to become more uncertain when the model performs poorly. Building on recent work in provably-safe trajectory planning, we leverage these confidence-aware human motion predictions to generate assured autonomous robot motion. Our new analysis combines worst-case tracking error guarantees for the physical robot with probabilistic time-varying human predictions, yielding a quantitative, probabilistic safety certificate. We demonstrate our approach with a quadcopter navigating around a human.
