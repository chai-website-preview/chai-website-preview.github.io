---
title: The Prosocial Ranking Challenge – $60,000 in prizes for better social media algorithms
slug: the-prosocial-ranking-challenge-60000-in-prizes-for-better-social-media-algorithms
date: '2024-01-18 11:23:43'
status: publish
author: jonathanstray
wp_id: 5064
original_url: https://humancompatible.ai/news/2024/01/18/the-prosocial-ranking-challenge-60000-in-prizes-for-better-social-media-algorithms/
categories:
- news
featured_image: ../../assets/featured/2024/01/The-Prosocial-Ranking-Challenge-Logo-Idea-Green-on-Black.png
summary_html: <strong>Deadline extended! First round submissions now due April 15th. See below. </strong>
---

![](/app/uploads/2024/01/The-Prosocial-Ranking-Challenge-Logo-Light-Green-Cropped-2-e1705607009111.png)

**Deadline extended! First round submissions now due April 15th. See below.**

Do you wish you could test what would happen if people saw different content on social media? Now you can!

The Prosocial Ranking Challenge is soliciting post ranking algorithms to test, with $60,000 in prize money split among up to ten finalists. Finalists will be scored by a panel of expert judges, who will then pick up to five winners to be tested experimentally.

Each winning algorithm will be tested for four months using a browser extension that can re-order, add, or remove content on Facebook, X, and Reddit. We collect data on a variety of conflict, well-being, and informational outcomes, including attitudes (via surveys) and behaviors (such as engagement) in a pre-registered, controlled experiment with consenting participants. Testing one ranker costs about $50,000 to recruit and pay enough participants for statistical significance (see below), which we will fund for up to five winning teams.

## Keep Informed

For updates on the Prosocial Ranking Challenge — including contest details, science development, and technical resources — [subscribe to our blog](https://rankingchallenge.substack.com/). Or join our [discord](https://discord.gg/JRmuHSj8XK).

## Why?

Many people believe that what social media algorithms choose to show have effects on what people know, how they feel, and how they relate. This challenge will test ways to mitigate problems or harms, and can also demonstrate new ways to design these systems toward socially desirable ends.

There is no shortage of ideas about how to do better, but these are hard to test if you don’t work at a platform. So, we’re using a custom browser extension to do the next best thing: fetch as many posts as we can when the page loads and reorder, remove, or add content. And we’re inviting all of you to write new ranking algorithms for it.

## Timelines

Because of the work required to create a usable ranker, the challenge will be split into two phases. The first round submissions will require only a simple prototype. From these, we will select up to ten finalists, each of whom will receive $1,000 and have one month to make their classifiers production ready. We’ll split the remaining $50,000 among those finalists who deliver a ranker that conforms to our API, performance and security specifications. Then we’ll pick up to five of the best and test them (meaning you will share in the prize money if you successfully submit a production ranker, even if that ranker is not selected for testing.)

**April 15, 2024: Submissions due**

Each submission will include documentation describing how the algorithm works, what outcome(s) it is expected to change, and why it is desirable to test, plus a prototype implementation (running as a live API endpoint that you host).

**May 1st: Ten finalists will be announced**

We will choose up to ten finalists. Each gets a $1000 prize, and one month to create a production-ready version of their algorithm. Our judges will try to give useful suggestions on how to strengthen your approach.

**June 1st: Finalist submissions due**

This time your ranker will need to be delivered in a Docker container and meet certain performance and security requirements. $50,000 in prize money will be split between all submissions that meet the technical requirements (see below).

**June 15th: Winners announced, experiment** **begins**

While we will award prize money to up to ten finalists, it is expensive to run a ranker, so unfortunately we can’t test all of them. We will select up to five rankers to test based on scientific merit and technical readiness (including performance and stability).

**June – October: Experiment runs**

We will test the winning rankers with real users across three different platforms for five months.

**December: Initial results available**

Winning teams will be invited to co-author the resulting paper, for publication in 2025.

## Technical requirements

We will call your ranker with a list of posts, including their ID, text content, author, engagement, etc (basically everything available in the normal UI, but no images). You must return an ordered list of IDs. You can also remove items by not including them in the ID list, or add items by filling out the fields of a new post.

For first round submissions, you must provide a working API endpoint, running your own server somewhere. There is no limit on execution time, or external services you can call. We will test this on public social media data.

For second round submissions, you must provide a Docker container which implements the same API as a REST endpoint. It must meet stringent latency requirements (basically, it has to run within 100ms) and cannot call external services due to privacy concerns. But we will provide some other ways you can do things like pre-processing, walking the social graph, etc.

For full specifications and sample code, see our [github repo](https://github.com/HumanCompatibleAI/ranking-challenge).

## Team matchmaking service

Do you have a great idea but aren’t up to this level of software development?  Are you an engineer who wants a side project experimenting with how AI can be used for good? Find each other in the #matchmaking channel on our [discord](https://discord.gg/JRmuHSj8XK).

## How to submit

Here’s the [submission form](https://forms.gle/tcRvtoFyhGeFyZup7) There’s not that much to it – probably you want to look at our [technical specifications](https://github.com/HumanCompatibleAI/ranking-challenge). Submissions are due on April 15th and June 1st (for finalists), anywhere on Earth.

## FAQ:

**What do you mean by “ranking algorithm”?**

A program that takes a set of posts and re-orders them. It can also remove posts or add entirely new posts.

**Who is eligible to enter?**

Any person or team of people, with a few exceptions (conflicts of interest, live in a country we can’t legally pay money to, etc.)

**What outcomes will you test in the experiment?**

A battery of both survey and behavioral outcomes related to conflict, well-being, and informativeness. We are developing this list, based on a set used in a previous study. Do you have a specific recommendation? Let us know.

There will be about 1500 people in each arm, which will allow us to find effect sizes of 0.1 Standard Deviations  with 80% probability. Each user will use the extension for four months, with surveys at 0, 2, and 4 months.

**What are you looking for when judging rankers?**

Scientific merit, meaning that 1) the ranker is based on a plausible theory of how exposure to different content on Facebook, X, and Reddit, can change one of our informational, well-being, or conflict related outcomes, and 2) there’s a reason to believe the effect will be large enough to detect with the sample size we can afford.

Desirability, meaning that the change you want to make seems like a good idea, something that would improve current designs.

Technical requirements, meaning that you meet the technical specification at each stage of the competition. These concern API conformance, maximum latency, and security.

One tricky issue here, really the limiting factor in what you can do, is that your content changes can’t make people want to stop participating in the experiment. The experience should be mostly transparent, so that we don’t get differential attrition between arms which could cause selection bias problems. We’ll be looking for that in our data analysis.

**Can we use LLMs in the ranker?**

Definitely, though for privacy reasons you cannot rely on any external services in the final submission. This means, for example, that you can submit a first round prototype built using GPT4 or Claude but cannot use these in your production code. We will provide sample code for a Mistral-based production ranker. See the [repo](https://github.com/HumanCompatibleAI/ranking-challenge).

**What data can the ranker use?**

Your ranker gets to see the text content of all posts the user sees, but not store them. You cannot call external APIs or services, but you can run a background process that imports or scrapes public social media data. See the [technical details](https://github.com/HumanCompatibleAI/ranking-challenge).

**Will the results be good science?**

We are making the method as strong as we can manage, including pre-registration, multiple control arms, manipulation and robustness checks, and appropriate statistical analysis.

The major limitations are that we can only sort the top few hundred posts (the most we can retrieve at once from what has already been selected for the user), that it’s desktop only, and that there will be a slight delay when loading posts (we hope to keep this to less than a second), and that we will only have 1,500 participants per arm.

However, this experiment is multi-platform, long term, and ecologically valid – we will be testing real users on real platforms.

**Are there any ethical considerations?**

Yes, because we are experimenting on people and collecting their data. We believe this research readily meets the [standards](https://web.stanford.edu/class/siw198q/websites/reprotech/New%20Ways%20of%20Making%20Babies/EthicVoc.htm) of autonomy, beneficence, non-maleficence, and justice. That is, we think this research will produce valuable information that can make things better for others in the future without exposing anyone to unreasonable risk or harm.

We are following standard research practices including appropriate institutional approvals. We will include your algorithm in our IRB submission, and may decline to test your ranker if we cannot get ethics approval for it. We have received approval for a similarly structured study before. Participants will be debriefed and paid for their time. We are addressing relevant privacy and security concerns with appropriate procedural and technical approaches.

Questions or ideas? Please talk to us!

**Who will be authors on the paper?**

The project team, the judges, and winning teams.

**Who is running this experiment?**

The experiment is being run out of the UC Berkeley Center for Human-compatible AI, but it’s an interdisciplinary team effort.

- Jonathan Stray – UC Berkeley (computer science)
- Julia Kamin – Civic Health Project (political science)
- Kylan Rutherford – Columbia University (political science)
- Ceren Budak – University of Michigan (computational social science)
- George Beknazar-Yuzbashev – Columbia University (economics)
- Mateusz Stalinski – University of Warwick (economics)
- Ian Baker – UC Berkeley (engineering)

**Who will judge the entries?**

The following astounding individuals have volunteered their time and expertise both to advise us on this project, and judge the entries:

- Mark Brandt, Michigan State
- Amy Bruckman, Georgia Tech
- Andy Guess, Princeton
- Dylan Hadfield-Mennell, MIT
- Alex Landry, Stanford
- Yph Lelkes, U Penn
- Paul Resnick, U Michigan
- Lisa Schirch, U Notre Dame
- Joshua Tucker, NYU
- Robb Willer, Stanford
- Magdalena Wojcieszak, UC Davis

Submissions will be anonymized, and any judges with conflicts of interest will be recused from individual entries.

**Who is funding the challenge?**

UC Berkeley CHAI

Jonathan Stray is receiving financial support for this project as a [Project Liberty Fellow](https://www.projectliberty.io/), powered by *Common Era.*
