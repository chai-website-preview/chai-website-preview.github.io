---
title: Mitigating Generative Agent Social Dilemmas
slug: mitigating-generative-agent-social-dilemmas
date: '2023-12-04 10:48:00'
status: publish
author: dalereed
wp_id: 4997
original_url: https://humancompatible.ai/news/2023/12/04/mitigating-generative-agent-social-dilemmas/
excerpt: The authors of this paper find evidence that social dilemmas involving generative agents can be mitigated with contracting and negotiation.
categories:
- news
featured_image: ../../assets/featured/2023/12/2023-12-12-223009-1.png
---

In their paper published on 11/07/2023 titled [Mitigating Generative Agent Social Dilemmas](https://openreview.net/pdf?id=5TIdOk7XQ6), Julian Yocum, Phillip J.K. Christoffersen, Mehul Damani, Justin Svegliato, Dylan Hadfield-Menell, and Stuart Russell consider the design of generative agents that can overcome social dilemmas in multi-agent settings.

Multi-agent interactions with automatic decision makers are complex, hard to predict, and can cause harm. For example, the flash crash of 2010 involved relatively simple agents whose interaction led to the largest intraday collapse in Dow Jones history. Despite this, as AI cognitive abilities continue to grow and scale to more complex tasks, the authors expect to see more AI agents in decision-making roles that interact with each other.

---

> ## **Abstract:**
>
> In social dilemmas, individuals would be better off cooperating but fail to do so due to conflicting interests that discourage cooperation. Existing work on social dilemmas in AI has focused on standard agent design paradigms, most recently in the context of multi-agent reinforcement learning (MARL). However, with the rise of large language models (LLMs), a new design paradigm for AI systems has started to emerge---generative agents, in which actions performed by agents are chosen by prompting LLMs. This paradigm has seen recent success, such as Voyager, a highly capable Minecraft agent. In this work, we perform an initial study of outcomes that arise when deploying generative agents in social dilemmas. To do this, we build a multi-agent Voyager framework with a contracting and judgement mechanism based on formal contracting, which has been effective in mitigating social dilemmas in MARL. We then construct social dilemmas in Minecraft as the testbed for our open-source framework. Finally, we conduct preliminary experiments using our framework to provide evidence that contracting helps improve outcomes for generative agents in social dilemmas.
