---
title: Getting By Goal Misgeneralization With a Little Help From a Mentor
slug: getting-by-goal-misgeneralization-with-a-little-help-from-a-mentor
date: '2024-10-10 09:19:23'
status: publish
author: chaiadmin
wp_id: 5776
original_url: https://humancompatible.ai/news/2024/10/10/getting-by-goal-misgeneralization-with-a-little-help-from-a-mentor/
categories:
- news
featured_image: ../../assets/featured/2023/10/chai-logo_a729cbef.png
---

Khanh Nguyen, Mohamad Danesh, Ben Plaut, and Alina Trinh wrote [this paper](https://arxiv.org/pdf/2410.21052) which was presented at Towards Safe & Trustworthy Agents Workshop at NeurIPS 2024.

While reinforcement learning (RL) agents often perform well during training, they can struggle with distribution shift in real-world deployments. One particularly severe risk of distribution shift is goal misgeneralization, where the agent learns a proxy goal that coincides with the true goal during training but not during deployment. In this paper, we explore whether allowing an agent to ask for help from a supervisor in unfamiliar situations can mitigate this issue.
