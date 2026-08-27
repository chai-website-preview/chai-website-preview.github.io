---
title: NeurIPS 2019 Accepts CHAI Researchers’ Paper “On the Utility of Learning about Humans for Human-AI Coordination”
slug: utility_learning
date: '2019-09-28 12:00:00'
status: publish
author: Chris Northwood
wp_id: 80
original_url: https://humancompatible.ai/news/2019/09/28/utility_learning/
categories:
- news
featured_image: ../../assets/featured/2019/09/neurips_2019.jpg
---

The paper authored by Micah Carroll, Rohin Shah, Tom Griffiths, Pieter Abbeel, and Anca Dragan, along with two other researchers not affiliated with CHAI, was accepted to NeurIPS 2019. An ArXiv link for the paper will be available shortly.

The paper is about how recently, deep reinforcement learning has been used to play Dota and Starcraft, using methods like self-play and population-based training, which create agents that are very good at coordinating with themselves. They “expect” their partners to be similar to them and are unable to predict what human partners would do. In competitive games, this is fine: if the human deviates from optimal play, even if you don’t predict it you will still beat them. However, in cooperative settings, this can be a big problem. This paper demonstrates this with a simple environment that requires strong coordination based on the popular game Overcooked. It shows that agents specifically trained to play alongside humans perform much better than self-play or population-based training when paired with humans, particularly by adapting to suboptimal human gameplay.
