---
title: 'NeurIPS Paper: Replay-Guided Adversarial Environment Design 12-6'
slug: neurips-paper-replay-guided-adversarial-environment-design-12-6
date: '2021-11-10 12:52:00'
status: publish
author: andrewpereira
wp_id: 3297
original_url: https://humancompatible.ai/news/2021/11/10/neurips-paper-replay-guided-adversarial-environment-design-12-6/
excerpt: CHAI’s Michael Dennis co-authored the paper together with Minqi Jiang, Jack Parker-Holder, Jakob Foerster, Edward Grefenstette, and  Tim Rocktäschel.
categories:
- news
featured_image: ../../assets/featured/2021/11/neurIPS.jpeg
---

CHAI’s Michael Dennis co-authored the [paper](https://arxiv.org/pdf/2110.02439.pdf) together with Minqi Jiang, Jack Parker-Holder, Jakob Foerster, Edward Grefenstette, and  Tim Rocktäschel. Read the abstract here:

Deep reinforcement learning (RL) agents may successfully generalize to new settings if trained on an appropriately diverse set of environment and task configurations. Unsupervised Environment Design (UED) is a promising self-supervised RL paradigm, wherein the free parameters of an underspecified environment are automatically adapted during training to the agent's capabilities.  This approach leads to the emergence of diverse training environments which challenge the policy to be more robust and generalizable.  This paper casts Prioritized Level Replay (PLR) as a method for UED, arguing that by curating completely random levels can generate novel and complex levels. Furthermore, the paper theoretically motivates a counterintuitive improvement to PLR, improving performance by training on less data. The experiments confirm that our new method, PLR⊥, obtains better results on a suite of out-of-distribution, zero-shot transfer tasks, in addition to demonstrating that PLR⊥ improves the performance of PAIRED, from which it inherited its theoretical framework.
