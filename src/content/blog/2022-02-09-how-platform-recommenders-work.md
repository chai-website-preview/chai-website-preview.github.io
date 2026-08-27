---
title: How Platform Recommenders Work
slug: how-platform-recommenders-work
date: '2022-02-09 10:11:22'
status: publish
author: jonathanstray
wp_id: 3331
original_url: https://humancompatible.ai/blog/2022/02/09/how-platform-recommenders-work/
excerpt: A recommender system (or simply ‘recommender’) is an algorithm that takes a large set of items and determines which of those to display to a user—think the Facebook News Feed, the Twitter timeline, Google News, or the YouTube homepage. Recommenders are necessary tools to help navigate the sheer volume of content produced each day, but their scale and rapid development can cause unintended consequences. Facebook’s algorithms have been blamed for radicalizing users, TikTok’s for inundating teens with eating-disorder videos, and Twitter’s for political bias.
categories:
- blog
---

by [Luke Thorburn](https://lukethorburn.com/), [Priyanjana Bengani](https://twitter.com/acookiecrumbles), and [Jonathan Stray](https://twitter.com/jonathanstray)

A recommender system (or simply ‘recommender’) is an algorithm that takes a large set of items and determines which of those to display to a user—think the Facebook News Feed, the Twitter timeline, Google News, or the YouTube homepage. Recommenders are necessary tools to help navigate the sheer volume of content produced each day, but their scale and rapid development can cause unintended consequences. Facebook’s algorithms have been blamed for [radicalizing users](https://www.nbcnews.com/tech/tech-news/facebook-knew-radicalized-users-rcna3581), TikTok’s for [inundating teens with eating-disorder videos](https://www.wsj.com/articles/how-tiktok-inundates-teens-with-eating-disorder-videos-11639754848), and Twitter’s for [political bias](https://blog.twitter.com/en_us/topics/company/2021/rml-politicalcontent).

Understanding how to mitigate such effects requires knowledge of how these systems work. At first glance this might seem impossible, because the algorithms used by each platform are proprietary. However, they share common principles. This post is based on public information found in company blog posts, academic papers written by platform employees, journalistic investigations and leaked documents. Each of these sources has limitations, but taken together they show repeating patterns of design and operation. While details can be scarce, the basic operation of these systems is not mysterious.

### A Typical Recommender

Modern recommenders are pipelines with multiple stages. All recommenders start with the entire set of items available to be displayed – whether that’s every post from your Facebook friends, every news article published today, or every song on Spotify. This set is first filtered by **moderation**, where items belonging to certain undesirable categories are identified and removed. The remaining set is still intractably large, so a **candidate generation** algorithm selects a subset of items that are plausible candidates for recommendation. These candidates are **ranked** according to a primary metric, usually a measure of how likely the user is to engage with the item. The items are often partially **re-ranked** to improve secondary objectives such as diversity in the types of content recommended. Finally, the top items are shown to the user. This final set of items is called a *slate*.

![](/app/uploads/external/26989cd4-1_UkYAN0UJOvdEFGPIfjdx-Q.png)
**A typical recommender pipeline, along with the approximate number of items retained at each stage for a large platform.**

### Moderation

The first stage is moderation, in which undesirable items are removed from the pool or flagged for special treatment.

The word “moderation” encompasses a complex process that determines what items are allowed on platforms, including policy-making, human content raters, automated classifiers, and an appeals process. All these steps influence what items users see, but only some operate within the core recommender pipeline. In this post, we use “moderation” to refer to the automated processes that remove items from the pool of content eligible for recommendation. Depending on the country, companies can be held liable for hosting content relating to a variety of issues such as copyright, defamation, [CSAM](https://en.wikipedia.org/wiki/Child_pornography) or hate speech. Most platforms also have policies (such as those of [Facebook](https://transparency.fb.com/en-gb/features/approach-to-ranking/types-of-content-we-demote/), [YouTube](https://support.google.com/youtube/answer/9288567), or [Twitter](https://help.twitter.com/en/rules-and-policies)) to filter out content that is believed to cause harm, such as nudity, [coordinated inauthentic behavior](https://about.fb.com/news/2018/12/inside-feed-coordinated-inauthentic-behavior/), or public health misinformation.

The bulk of such moderation is performed by a series of automated filters designed to catch different categories of undesirable content. What happens to items caught in these filters [will differ](https://www.niemanlab.org/2021/06/shadow-bans-fact-checks-info-hubs-the-big-guide-to-how-platforms-are-handling-misinformation-in-2021/) depending on the category of content and platform policy. Among other possibilities, they may be removed from the pool of items eligible for recommendation, or flagged for down-ranking in a later stage of the pipeline.

### Candidate generation

In the candidate generation stage the full set of items available on the platform (potentially millions) is efficiently filtered to a set of [500 or so](https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/) that are plausibly of interest to the user.

Some recommenders mostly choose items from people or groups a user follows. In these contexts, the candidate items are the posts that have been created by these sources since that user last logged in, along with items ranked highly in previous sessions that they haven’t yet seen. This is the case for the Twitter [timeline](https://blog.twitter.com/engineering/en_us/topics/insights/2017/using-deep-learning-at-scale-in-twitters-timelines) and the Facebook [News Feed](https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/).

Other recommenders regularly show items from sources that users haven’t explicitly followed. Indeed, on some platforms (e.g. Google News, Netflix) there is no concept of “following”. In these contexts, candidates are typically chosen using a simpler, less accurate, but more computationally efficient version of the full algorithm used in the ranking stage. For example, if the ranking stage uses a large, computationally intensive model (e.g. a neural network) to predict the probability of a user engaging with the item, the candidate generation stage might work similarly, just with a much smaller model that can be applied to a larger set of items. This reduced model may have been trained to emulate the behavior of the full model used in the ranking stage as best it can. This is roughly how candidate generation is performed on the YouTube [homepage](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf) and in the [Explore view](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/) on Instagram.

### Ranking

In the ranking stage each item is assigned a number intended to capture the value of showing it to a particular user in a particular context. Every recommender serves [multiple stakeholders](https://www.researchgate.net/profile/Himan-Abdollahpouri/publication/338516177_Multistakeholder_recommendation_Survey_and_research_directions/links/5e191200299bf10bc3a34635/Multistakeholder-recommendation-Survey-and-research-directions.pdf), so this will be some combination of value to the user, the content provider, the platform, and society. The items are then sorted by their score from largest to smallest. We will use the term *value model* to describe the formula used to compute these scores, a name that is used by some platforms. Other platforms call this a *scoring function*.

In most platform recommenders, the value model is primarily a weighted sum of the predicted probabilities that the user will interact with the item in different ways, such as clicking, commenting, sharing etc. These interactions are informally known as *engagement*.

For example, consider a feed or timeline on a social media platform. There are multiple ways a user can engage with an item. These include explicit inputs such as liking, commenting, and sharing, but also more implicit data such as whether a user clicks on links to specific domains and how much time they spend looking at an item (known as “dwell time”).

For any given user and any given post, the platform has a model that predicts Pr(*like*), Pr(*comment*), Pr(*share*) and so on, the probabilities that the user will engage with the post if it is shown to them. These probabilities are produced by machine learning models trained to predict how a particular *user* will interact with a particular *item* in a given *context* (see e.g. [YouTube](https://dl.acm.org/doi/pdf/10.1145/3298689.3346997), [Twitter](https://dl.acm.org/doi/pdf/10.1145/3394486.3403370)). These models are trained on historical engagement data, and their objective is predictive accuracy.

The core value model is a weighted combination of these probabilities. In its simplest form, it might look something like

![](/app/uploads/external/30d30f6a-1_VZw0d-eAEHZRXXsaEyzabw.png)

The use of engagement terms in this value model is what is meant by the phrase “optimizing for engagement.” The weights in front of the probabilities are intended to capture the degree to which different types of engagement are valuable. The weights can be selected in a variety of ways, and may be:

• Skewed towards particular types of engagement (e.g. YouTube prioritizes [watch time](https://blog.youtube/news-and-events/youtube-now-why-we-focus-on-watch-time/) of videos, TikTok prioritizes [retention and time spent](https://www.nytimes.com/2021/12/05/business/media/tiktok-algorithm.html) using the app).

• Negative, if the corresponding type of engagement indicates disapproval (e.g. clicking “See Fewer Posts Like This” on [Instagram](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/)).

• Personalized to each user (as in the Facebook [News Feed](https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/)).

• Chosen algorithmically to optimize a single overriding metric, such as retention, that isn’t optimized for directly (e.g. [Google](https://dl.acm.org/doi/pdf/10.1145/3097983.3098043), [LinkedIn](https://www.usenix.org/conference/opml20/presentation/gupta)).

• Regularly adjusted to respond to changes in priorities, or changes in the user interface that alter the significance of different types of engagement (as in the Instagram [Explore view](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/)). For example, if the ‘like’ button is made bigger, people are more likely to click it and so it loses significance as a signal of value.

The value model typically includes additional terms that are not predictions. That is, no real platform optimizes solely for engagement. For example, there might be additional terms added to boost or penalize items that were flagged during the moderation stage. These “‘integrity signals” might include probabilities that the item is [low quality news or ad farm content](https://www.protocol.com/policy/facebook-papers-integrity-holdouts). So the value model will look more like:

![](/app/uploads/external/4ca1003d-1_ltANKtFhc-rvZY9Jzz1_xQ.png)

In real recommender systems the equation will be more complex, with a larger number of engagement types and integrity signals being included. But the basic structure seems to be standard practice in all the major news and social media recommenders about which information is publicly available. Scores of this sort are used to rank items in the Facebook [News Feed](https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/), Twitter [notifications](https://arxiv.org/abs/2008.12623), YouTube [watch next suggestions](https://dl.acm.org/doi/10.1145/3298689.3346997), the Instagram [Explore view](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/), and on [TikTok](https://www.nytimes.com/2021/12/05/business/media/tiktok-algorithm.html).

### Re-ranking

So far, this approach to ranking does not take into account the relationships between items in the ranked list—the position of each item is determined independently of the others. This can lead to the top-ranked items being too homogeneous. For example, they may all relate the same political story, if that story causes outrage and thus high engagement.

Thus, a re-ranking stage is used to tweak the positions of the items in the ranked list to improve the quality of the recommendations in their final context. In this phase, items aren’t selected based on individual appeal, but the appeal of the whole slate of items to the user, which depends on the overall mix. The re-ranking stage might aim to position complementary items near one another, prevent boredom by improving diversity in the item topics, promote fairness by improving diversity in the accounts presented, or counter popularity bias (the tendency of the ranking stage to unduly prioritize popular, “mainstream” items).

For example, the Instagram [Explore view](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/) increases the diversity of accounts represented by adding a penalty factor to “successive posts from the same author or seed account”. YouTube has [experimented](https://dl.acm.org/doi/pdf/10.1145/3269206.3272018) with ensuring that at most *n* out of every *m* items can fall within a certain similarity distance of each other.

The exact properties sought depend on the context. There are, for example, legitimate cases in which a user should be served similar items, such as during a breaking news event when information is continually arriving, on a music streaming service when the user has requested a particular genre, or when recommending groups a user might want to join.

Following the re-ranking stage, the top items in the re-ranked list are selected as the slate shown to the user. The ranked list of content may also be interleaved with targeted ads, which are selected by a different recommender system.

### The Recommender Pipeline

The diagram below shows how items flow through a typical recommender pipeline. At left is every item eligible for recommendation. This could be a huge number of items, as on YouTube, or it could be only the posts from a user’s friends. Moderation is typically performed once, removing the same items for all users, while candidate generation, ranking, and re-ranking are personalized to a particular user and context.

![](/app/uploads/external/457dc5d4-1_EHsfx4DEZXib4-616Fi4Yw.png)
**An example of how items flow through a recommender pipeline. In reality, the stages toward the left include huge numbers of items, which are gradually filtered down to the final slate.**

Particular systems will differ in their specifics. For example, moderation (the removal of items) may be performed at multiple points throughout the pipeline, and adjacent stages may be performed in conjunction and not easily separated at the algorithmic level. But this description is accurate in its broad strokes. There is no need for recommender systems to be mysterious – they all work on the same basic principles.
