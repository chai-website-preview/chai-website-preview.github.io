---
title: Reinforcement Learning with Human Feedback and Active Teacher Selection (RLHF and ATS)
slug: reinforcement-learning-with-human-feedback-and-active-teacher-selection-rlhf-and-ats
date: '2024-04-30 09:00:00'
status: publish
author: sandy
wp_id: 5303
original_url: https://humancompatible.ai/news/2024/04/30/reinforcement-learning-with-human-feedback-and-active-teacher-selection-rlhf-and-ats/
categories:
- news
featured_image: ../../assets/featured/2024/04/Screenshot-2024-05-14-at-12.57.05-AM.png
---

CHAI PhD graduate student, Rachel Freedman gave a presentation at Stanford University on critical new developments in AI safety, focusing on problems and potential solutions with Reinforcement Learning from Human Feedback (RLHF).

RLHF aims to train AI systems to behave in alignment with human preferences by learning a reward function from human feedback on the AI's outputs. However, Freedman highlighted several key issues that must be addressed for RLHF to achieve safe and beneficial AI:

- Misspecification in modeling human preferences, such as incorrectly assuming choices are made from a uniform choice set
- The "expertise problem" of feedback coming from multiple teachers/humans with differing knowledge levels
- Challenges in aggregating diverse preferences from different people

To tackle the expertise problem, Freedman proposed a novel "Active Teacher Selection" (ATS) approach. ATS models the problem as a variant of the multi-armed bandit problem called a "Hidden-Utility Bandit." The AI actively selects which teachers to query for feedback in order to most efficiently learn the true reward function.

Experiments showed ATS significantly outperforms random teacher selection and heuristics, enabling more sample-efficient and robust reward learning from groups of teachers with heterogeneous expertise. Freedman also demonstrated how ATS could optimize the allocation of COVID tests that vary in accuracy to most rapidly identify the best vaccine.

While not a complete solution, this work represents important progress in overcoming critical obstacles to making RLHF a viable path to beneficial AI systems that reliably do what humans want. Further work is still needed on other issues like choice set misspecification and social choice for preference aggregation.
