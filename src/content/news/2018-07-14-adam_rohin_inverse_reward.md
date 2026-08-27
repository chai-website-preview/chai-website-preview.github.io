---
title: CHAI’s Adam Gleave and Rohin Shah Present “Active Inverse Reward Design”
slug: adam_rohin_inverse_reward
date: '2018-07-14 12:00:00'
status: publish
author: Chris Northwood
wp_id: 211
original_url: https://humancompatible.ai/news/2018/07/14/adam_rohin_inverse_reward/
categories:
- news
summary_html: 'Two of CHAI’s researchers presented this paper at the 1st Workshop on Goal Specifications for Reinforcement Learning, FAIM 2018. The abstract reads:'
---

Two of CHAI’s researchers presented this paper at the 1st Workshop on Goal Specifications for Reinforcement Learning, FAIM 2018. The abstract reads:

Reward design, the problem of selecting an appropriate reward function for an AI system, is both critically important, as it encodes the task the system should perform, and challenging, as it requires reasoning about and understanding the agent’s environment in detail. AI practitioners often iterate on the reward function for their systems in a trial-and-error process to get their desired behavior. Inverse reward design (IRD) is a preference inference method that infers a true reward function from an observed, possibly misspecified, proxy reward function. This allows the system to determine when it should trust its observed reward function and respond appropriately. This has been shown to avoid problems in reward design such as negative side-effects (omitting a seemingly irrelevant but important aspect of the task) and reward hacking (learning to exploit unanticipated loopholes). In this paper, we actively select the set of proxy reward functions available to the designer. This improves the quality of inference and simplifies the associated reward design problem. We present two types of queries: discrete queries, where the system designer chooses from a discrete set of reward functions, and feature queries, where the system queries the designer for weights on a small set of features. We evaluate this approach with experiments in a personal shopping assistant domain and a 2D navigation domain. We find that our approach leads to reduced regret at test time compared with vanilla IRD. Our results indicate that actively selecting the set of available reward functions is a promising direction to improve the efficiency and effectiveness of reward design.
