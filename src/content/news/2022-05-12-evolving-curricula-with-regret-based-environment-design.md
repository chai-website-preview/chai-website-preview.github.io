---
title: Evolving Curricula with Regret-Based Environment Design
slug: evolving-curricula-with-regret-based-environment-design
date: '2022-05-12 13:27:00'
status: publish
author: andrewpereira
wp_id: 3574
original_url: https://humancompatible.ai/news/2022/05/12/evolving-curricula-with-regret-based-environment-design/
excerpt: In this YouTube video, authors Jack Parker-Holder, Minqi Jiang, CHAI's Michael Dennis, Mikayel Samvelyan, Jakob Foerster, Edward Grefenstette, and Tim Rocktäschel present ACCELL.
categories:
- news
featured_image: ../../assets/featured/2022/06/Screen-Shot-2022-06-08-at-1.35.34-PM.png
---

In this [YouTube video](https://www.youtube.com/watch?v=povBDxUn1VQ), authors Jack Parker-Holder, Minqi Jiang, CHAI's Michael Dennis, Mikayel Samvelyan, Jakob Foerster, Edward Grefenstette, and Tim Rocktäschel present ACCELL.

Unsupervised Environment Design(UED) is a field which aims to automatically generate environments which are appropriate to train agents in. UED's ability to promote transfer to unknown environments is an invaluable asset to safety, as well its ability to empower the AI designer to have more control over the resulting policy through controlling the training distribution.

Two important insights in Unsupervised Environment Design (UED) are:   
* High Regret Levels promote efficient learning and transfer (See PAIRED, Robust PLR)   
* Evolution is more efficient at optimizing environments than RL (See POET)

In this work, the authors combine these two threads, curating level edits to maximize regret, and allowing evolution to compound this effect over time.

ACCELL achieves state of the art performance in every domain tested including:   
* Bipedal Walker (used in POET)   
* Minigrid and Car Racing environments (used in PAIRED and Robust PLR)

You can stress test their method yourself with the interactive demo right in your browser! (<https://accelagent.github.io/>)
