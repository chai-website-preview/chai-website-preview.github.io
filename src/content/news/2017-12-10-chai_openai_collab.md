---
title: CHAI and OpenAI Work Together on Inverse Reward Design
slug: chai_openai_collab
date: '2017-12-10 12:00:00'
status: publish
author: Chris Northwood
wp_id: 246
original_url: https://humancompatible.ai/news/2017/12/10/chai_openai_collab/
categories:
- news
featured_image: ../../assets/featured/2017/12/openai.png
summary_html: 'CHAI PI Stuart Russell and co-PI Anca Dragan, with a number of other authors from Berkeley’s School of Electrical Engineering and Computer Science and one from OpenAI, published “Inverse Reward Design” in the 31st Conference on Neural Information Processing Systems held in Long Beach, California back in last December. The abstract reads:'
---

CHAI PI Stuart Russell and co-PI Anca Dragan, with a number of other authors from Berkeley’s School of Electrical Engineering and Computer Science and one from OpenAI, published “Inverse Reward Design” in the 31st Conference on Neural Information Processing Systems held in Long Beach, California back in last December. The abstract reads:

Autonomous agents optimize the reward function we give them. What they don’t know is how hard it is for us to design a reward function that actually captures what we want. When designing the reward, we might think of some specific training scenarios, and make sure that the reward will lead to the right behavior in those scenarios. Inevitably, agents encounter new scenarios (e.g., new types of terrain) where optimizing that same reward may lead to undesired behavior. Our insight is that reward functions are merely observations about what the designer actually wants, and that they should be interpreted in the context in which they were designed. We introduce inverse reward design (IRD) as the problem of inferring the true objective based on the designed reward and the training MDP. We introduce approximate methods for solving IRD problems, and use their solution to plan risk-averse behavior in test MDPs. Empirical results suggest that this approach can help alleviate negative side effects of misspecified reward functions and mitigate reward hacking.
