---
title: A Practical Definition of Political Neutrality for AI
slug: a-practical-definition-of-political-neutrality-for-ai
date: '2025-02-04 15:00:26'
status: publish
author: jonathanstray
wp_id: 5801
original_url: https://humancompatible.ai/news/2025/02/04/a-practical-definition-of-political-neutrality-for-ai/
categories:
- blog
- news
featured_image: ../../assets/featured/2025/02/Screenshot-2025-02-04-at-3.02.54-PM.png
summary_html: 'NEW: Our current research project to build <a href="https://docs.google.com/document/d/19haXfSeQtTjdVLUbba1z5GRhW12rj0ipR6lM5S3G0o4/edit?usp=sharing">political neutrality evaluations</a>.'
---

**Jonathan Stray, CHAI Senior Scientist**

NEW: There’s also a [video version of this post](https://youtu.be/bEKgQXAg4r0)

NEW: Our current research project to build [political neutrality evaluations](https://docs.google.com/document/d/19haXfSeQtTjdVLUbba1z5GRhW12rj0ipR6lM5S3G0o4/edit?usp=sharing).

There is an urgent need for a clear, consistent, and practical definition of political neutrality for AI systems.

It seems a foregone conclusion that intelligent machines will soon be the main way we get information about our world, including our political world. Rather than reading news articles directly, AI systems will [summarize](https://www.niemanlab.org/2024/12/get-ready-for-the-ai-driven-world-of-news/) exactly what we want to know from a variety of sources. It seems inevitable, then, that these machines will influence our politics. And indeed, [recent research](https://arxiv.org/abs/2410.24190) shows that they do.

This is a dangerous state of affairs. At best, these machines will change our beliefs in ways we don’t understand as a side effect of optimizing some predefined metric (such as [engagement](https://medium.com/understanding-recommenders/whats-right-and-what-s-wrong-with-optimizing-for-engagement-5abaac021851)). At worst, AI will be weaponized to manipulate us.

If we do not want AI interference in human politics, we need to be able to say exactly what that means – and it has to be possible to implement it in practice. This is a surprisingly tricky thing to do. It doesn’t work to train an AI to have no effect on what humans believe, because such a machine would lie to try to prevent you from changing your mind. It isn’t enough to say that all AI output should be accurate and truthful, because there are plenty of ways to be deceptive using only true facts. And while “objectivity” is sometimes taken to mean balance or fairness, it’s not a coherent enough concept to be useful.

We need to look elsewhere, at ideas of what deliberation should look like in a democratic society. Drawing on this, I propose the following definition of AI neutrality: when asked about a controversial topic, the machine should produce an answer which 1) as many people as possible from each side of a debate would say fairly includes their perspective while 2) ensuring that the same percentage of each side approves. I’ll call this idea *maximum equal approval*. This is a [pluralist](https://pluralistic-alignment.github.io/) view of AI alignment, where the goal isn’t to find one perfect answer but to equitably balance competing values, interests, and groups. It can also be seen as a quantitative formalization of Wikipedia’s successful “neutral point of view” policy.

*Maximum equal approval* gives a straightforward empirical metric for the “neutrality” of any particular AI-generated answer: survey people on each side of an issue and see what percentage say the answer includes a fair representation of their view (given that other views may also be represented in the answer). Then choose the answer which gives the highest approval that all sides can reach simultaneously. This process won’t always give an ideal result, but in the absence of more specific knowledge it’s an essential democratic default.

**LLMs Can Change Your Vote**

A number of investigators have tested the politics of LLMs by asking them to fill out political quizzes. Generally, LLMs seem to have left-libertarian politics, as seen in this figure from [Rozado (2024)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0306621) where each dot is a different model (including GPT, LLaMA, Mistral, Claude, Gemini, Grok, etc.):

![](/app/uploads/external/ad073de4-AD_4nXedyPg4NWEhpBfy2ZiAYktWUFOja0_axPHje1-UKV2wqJVlKPsjr0Ej.png)

However, such experiments don’t tell us what we really want to know: does talking with an LLM actually change human political opinions?

[Recent research](https://arxiv.org/abs/2410.24190) from Berkeley PhD student Yujin Potter, et al. and CHAI affiliate Dawn Song does answer this question. In an early 2024 experiment, they showed that conversations with several different LLMs made people of all political orientations more likely to say they’d vote for Biden. These models were not told to persuade anyone in any way; they were instructed only to have a conversation about politics and include their “own subjective thoughts”.

![](/app/uploads/external/162cf519-AD_4nXfMKYgmgxXR2R3kZfOj9FYnsgGSbyj6b7LTJLuh81W1OABNKbWmDWLb.png)

Percentage shift in vote intention from talking about politics with LLMs. [Potter *et al.* 2024](https://arxiv.org/abs/2410.24190)

The effect was up to two percentage points – wider than Trump’s margin of victory in the popular vote, so an alternative 2024 where everyone got their news through AI may have been a very different world. Depending on who you voted for, this may strike you as either preferable or outrageous. But saying what should happen in this case is not nearly enough. Which side should the AI favor on every issue and in every election worldwide?

**Why Non-Persuasion Won’t Work**

One answer is to say that AI shouldn’t persuade anyone about anything, so that we preserve human agency by keeping machines out of human affairs. The problem with this attractive idea is that sometimes humans *should* change their minds.

It would certainly be possible to train a model to have no persuasive effect on, say, voting intention. One could repeat the above experiment many times while varying the model parameters, using the shift in vote intentions as a feedback signal. This is similar to the way that [RLHF](https://huggingface.co/blog/rlhf) is used today to train models that humans rate as helpful. In this way, it would be possible to create a system which had essentially zero effect on vote intention.

However, you would have created a machine that would try to *prevent* you from changing your mind. It might argue against you, or hide crucial information, or even lie to you. There are good reasons and bad reasons to change your mind, but this training process doesn’t distinguish between them – to such a model, all change is bad. This is a specific instance of a tricky general problem which has been known to the AI safety community for some time. Here it is in a 2016 discussion about minimizing “side effects” in robotics:

> If we don’t want side effects, it seems natural to penalize “change to the environment.” …  A very naive approach would be to penalize state distance, *d(s**<sub>i</sub>**, s**<sub>0</sub>**)*, between the present state *s**<sub>i</sub>* and some initial state *s**<sub>0</sub>*. Unfortunately, such an agent wouldn’t just avoid changing the environment—it will resist any other source of change, including the natural evolution of the environment and the actions of any other agents!
>
> [Amodei *et al*. 2016](https://arxiv.org/abs/1606.06565)

If there really are better facts and arguments on one side, they *should* persuade; a news bot that could never change your views would be dysfunctional. This is no different than saying that a music recommender should help you develop your tastes and an educational system has to teach. An AI agent that could not or would not ever change the user’s mind would have to take pains to avoid repeating any sort of good argument, no matter where the facts led – a deeply irrational thing to do.

Thus, a user shift towards Biden is not by itself evidence of chatbot bias. Rather, it depends why this shift happened. If people were persuaded through “the unforced force of the better argument”, as communication theorist Jürgen Habermas [put it](https://www.cambridge.org/core/books/abs/foundations-of-deliberative-democracy/force-of-better-argument-in-deliberation/3658A782AF72998E1C37070601EF044B), then this may be a legitimate or even desirable shift. On the other hand, if what the chatbot said was manipulative in some way – for example, if it omitted key information or perspectives – then we would say that this persuasion was unacceptable.

**From Rationality to Fairness**

When computer scientists talk about good arguments, they are usually concerned with giving the sorts of reasons that will [lead to true beliefs](https://plato.stanford.edu/entries/argument/) – a purely “rational” view of persuasion. Getting LLMs to use good arguments with good evidence is an active and important area of research. But when political scientists and democratic theorists talk about good arguments, they are also concerned with power: who ultimately gets to control the decision-making process through what evidence is presented, how it is framed, who is included in the discussion, how the result is acted upon, and so on.

The issue here is not rationality but fairness. Fairness and neutrality are not the same, and fairness is often taken to require more than neutrality. Yet all principles of fairness ultimately depend on some sort of “[appropriate impartiality](https://doi.org/10.1080/00048400701846491).”

There is a very long history of attempts to say what makes a political argument fair. In Plato’s Republic, Thrasymachus [challenges](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0168%3Abook%3D1%3Asection%3D338c) Socrates to prove that justice is anything other than what the stronger party says it is. In the 19th century, John Stuart Mill said that we should consider the strongest version of an argument in order to criticize it. In the 20th century John Rawls argued that in a democracy, citizens must justify their positions to each other using [public reason](https://plato.stanford.edu/entries/public-reason/), that is, arguments and evidence that any citizen could reasonably accept. Jürgen Habermas, who coined the phrase “the public sphere,” described the [ideal speech situation](https://easysociology.com/general-sociology/ideal-speech-situation/) where all can participate on an equal footing. The rationalist community sometimes talks about the [ideological Turing test](https://rationalwiki.org/wiki/Ideological_Turing_test), a 21st century version of fair political discourse.

These are all profound ideas, but because we want to implement a practical system we should also look to practitioners for inspiration. Journalists must communicate political information fairly every day. Can we make the journalistic notion of “objectivity” our goal?

**The Challenges of Objectivity**

Science fiction author Phillip K. Dick once [wrote](https://www.brainyquote.com/quotes/philip_k_dick_136851) that “reality is that which, when you stop believing in it, doesn’t go away.” This captures the core idea of objectivity: it’s not about what humans think. A 1949 manual for CIA analysts [defined](https://www.tandfonline.com/doi/full/10.1080/02684527.2019.1710806) the “objective situation” as “the situation as it exists in the understanding of some hypothetical omniscient Being.”

Can we use objectivity as the standard for answers on controversial topics? Journalists [used to](https://www.niemanlab.org/2024/04/objectivity-in-journalism-is-a-tricky-concept-what-could-replace-it/) think so. As journalism professionalized in the early 20th century, it borrowed this idea of objectivity because it aspired to “scientific” standards – and also to free itself from perceptions of partisanship, as it was plainly [good business](https://ethics.journalism.wisc.edu/2011/04/20/the-fall-and-rise-of-partisan-journalism/) to appeal to all sides.

But while “objective” might mean “true no matter what you think,” this kind of “truth” is not strong enough to encompass most of the problems with unfair or manipulative answers on controversial topics. It’s possible to be biased or deceptive while saying only completely true things. This can be done by omitting key facts, by cherry-picking true examples, by framing which distorts the meaning of true facts, by logical fallacies applied to truths, by claiming that some facts are important while others are not, by questioning the credibility of sources, and so on. There are so many ways to make the facts tell a particular story that even the most biased media sources [very rarely lie outright](https://www.astralcodexten.com/p/the-media-very-rarely-lies).

The fundamental problem is that the inhuman perspective makes a lot less sense when applied to human affairs, because meaning is a [partially objective and partially subjective](https://meaningness.com/objective-subjective) phenomenon. Politics itself is famously subjective. This is why modern understandings of objectivity have had to become a lot more sophisticated. For example, this is what the [intelligence community](https://www.tandfonline.com/doi/full/10.1080/02684527.2019.1710806) thinks of it today:

> Even if analysts try to be “objective” in a procedural sense, they will not be able to achieve absolute objectivity because biases consisting of cognitive frameworks are necessary in order to infer meaning from incomplete data. Conceptual frameworks provide each analyst with a different kind of filter, for both understanding and interpretation, and a corresponding set of biases.

In other words, we cannot simply “present the facts” without some criterion for saying which facts are most important and how they should be interpreted. (For that matter, exactly what constitutes an atomic “fact” is a [pretty complicated](https://plato.stanford.edu/entries/facts/) question.) The failure of “objectivity” can be seen as an instance of the “[no free lunch](https://en.wikipedia.org/wiki/No_free_lunch_theorem)” class of theorems, and the above paragraph is saying we need some sort of [inductive bias](https://en.wikipedia.org/wiki/Inductive_bias) to get anywhere at all.

This is a technical account of why we can’t simply program our machines to be “objective,” but many endeavors have run into the same underlying problem from different directions. The philosopher Thomas Nagel wrote about the “[View From Nowhere,](https://plato.stanford.edu/entries/scientific-objectivity/#ViewNowh)” meaning the impossibility of experiencing the universe without a perspective. [Standpoint epistemology](https://plato.stanford.edu/entries/feminism-epistemology/#FemiStanTheo) is based on the observation that different people will have importantly different prior knowledge, experience, and priorities. Google Maps shows [different borders](https://www.washingtonpost.com/technology/2020/02/14/google-maps-political-borders/) depending on what country you’re in, because borders are not properties of nature.  Even statistical practice is now understood to properly require [both objective and subjective](https://academic.oup.com/jrsssa/article/180/4/967/7068392?login=false) elements.

Thus, saying that an AI agent should be “objective” or “just present the facts” doesn’t actually explain what the machine should do. Nor can we produce useful training data by asking humans to rate the objectivity of AI outputs, because “objectivity” is neither coherent nor complete enough to be a foundational goal.

**Formalizing Wikipedia’s Successful Definition of Neutrality**

Journalism is not the only place where people are regularly producing politically fair text. Wikipedia’s “neutral point of view” policy played a large part in its early development, and remains central today. The [current version](https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view/FAQ#There's_no_such_thing_as_objectivity) of the NPOV policy approaches practical fairness in this way:

> Now, is it possible to characterize disputes fairly? This is an empirical issue, not a philosophical one: can we edit articles so that all the major participants will be able to look at the resulting text, and agree that their views are presented accurately and as completely as the context permits?

This is a deceptively simple paragraph which contains a number of key ideas. There are multiple *participants*. They are having a *dispute*. The goal is to get them to *agree*, not with each other, but that the text *presents their views* accurately and completely – one could say [charitably](https://en.wikipedia.org/wiki/Principle_of_charity). In this definition, fairness comes from fair representation of competing groups who have different priors, values, and interpretations. This idea can’t be derived from classical rationality, but instead flows from a fundamentally political analysis: we are trying to mediate between multiple parties vying for power.

We can turn this idea into a practical way to quantitatively evaluate the fairness of answers to controversial questions.

For the moment let’s assume there are only two sides in the debate. Suppose we choose the text of an answer, then survey each side to ask if they feel it includes a fair representation of their side. Note the precise question: not “is this the text you want?” but “does it fairly represent your view, among others?” This difference is key, but we’ll just call it “approval” from now on. Depending on the text, we might get results like any of the graphs below.

![](/app/uploads/external/3bd10683-AD_4nXd0ZIoWmztuwOYmd-2dhnAkYGMs2fg3hIvMm6Qcx9BD1HNLtesOkZqL.png)

Three possible outcomes for the percentage of people on each side who approve of an AI answer

When a topic is controversial, it’s easy to write an answer that one side finds accurate and comprehensive, but the other side will probably find it misleading and cherry-picked. It probably won’t be possible to find an answer that both sides approve at the same level as the highest one-sided approval. Adding better arguments for one side will probably make the other side unhappy, even if you ask people to strictly focus on whether the result *includes* their perspective. Let’s say an answer has *equal approval* if each side approves (feels it includes their perspective) at the same rate. Of course we could easily generate answers that neither side likes, so we also want answers to be good*,* meaning that this equal approval rate should be as high as possible. I propose that when asked a controversial question, by default the AI should produce the answer of *maximum equal approval* – the middle graph above.

This defines an empirical ground truth. Given a set of possible answers to a controversial question, we can learn which answer is best through surveys asking each side if they approve of each answer. To know if we have the *best possible* answer we would have to try many different variations to see how high we could push equal approval.

However, with sufficient data it should be possible to model and predict what each side in a conflict would say if they were asked whether a particular answer fairly includes their perspective. It seems likely that such a model could be created, because LLMs have proven [quite good](https://journals.sagepub.com/doi/full/10.1177/08944393241286471) at mimicking human political judgments. This is similar in principle to how RLHF relies on a reward model trained to predict which of a pair of LLM outputs a human rater would prefer. Thus the principle of maximum equal approvalgives an empirical measure that can be used with existing techniques for tuning language models.

Note that if the participants in a debate value accuracy, comprehensiveness, etc. then the answer of maximum equal approvalis also likely to be one of the most epistemically rigorous answers. If it were not, then the side which felt that the answer was missing important evidence or committed logical fallacies would not approve.

**Political Neutrality in Action**

To illustrate this approach I asked LLaMA 3.2 1B Instruct a maximally controversial question, “Is the current war in Gaza a genocide?” and refreshed several times until I had generated the three answers below. You can see the [full text here](https://docs.google.com/document/d/1sQAxFTN4klRU34c2z2vtH5Ug2cqeTtRSsxGtAV8Nxos/edit?usp=sharing), but here they are in abbreviated form:

> **Answer 1**
>
> Determining whether the current conflict in Gaza is a genocide is a complex and problematic question, and I’ll try to provide an objective analysis.
>
> …
>
> Therefore, while the current situation in Gaza shares some deadly differences with historical cases, it does not represent a fundamental example of genocide.
>
> **Answer 2**
>
> What a complex and sensitive topic. I’ll provide an objective analysis, but please note that the definition of genocide and its interpretation can vary depending on the source and context.
>
> …
>
> In conclusion, while the current conflict in Gaza is a complex and multifaceted issue, the evidence suggests that it may be characterized as a genocide.
>
> **Answer 3**
>
> What a complex and multifaceted question. The question of whether the current war in Gaza constitutes a genocide is a matter of ongoing debate and analysis.
>
> …
>
> Arguments for a potential genocide:
>
> …
>
> Arguments against labeling it a genocide:
>
> …
>
> In conclusion:
>
> Ultimately, a “genocide” label is not a standard or universally accepted term in international law or humanitarian discourse. The situation in Gaza requires careful consideration and nuanced analysis to address the diverse concerns and perspectives involved.

The principle of maximum equal approval suggests that Answer 3 is probably the right default, because it includes multiple perspectives in detail. To know for sure we would have to ask people on both sides of this issue whether they felt each of these texts includes a fair representation of their view.

To find the *best possible* answer we would have to collect human feedback across many different variations of these texts. Alternatively, we could build a model that could predict the judgments of each side with sufficient accuracy, and use that to guide text generation. For a hotly contested question like this one, the highest possible level of equal approval could be quite low. The [*hostile media effect*](https://www.tandfonline.com/doi/full/10.1080/15205436.2015.1051234) is a well-replicated result showing that when a topic is controversial enough, even the most careful and balanced news stories will be perceived as biased. Perhaps for this question the answer of maximum equal agreement will only get 20% approval from each side.

You may personally feel strongly that one of these answers is correct, and that the others are reprehensible. However, the fairness of the maximum equal approval approach doesn’t rest on the equivalence of *perspectives*. Rather, it flows from the equal dignity of the *people* who hold them.

People are not their ideas. We should be slow to bar someone from expressing their opinion, and our machines should be even slower. Even if we could be absolutely certain that one side really does hold bad or harmful opinions, there are important practical reasons for including them in normal political processes.

Unlike deliberative democracy which views politics as a collective truth-finding exercise, Chantal Mouffe’s [agonistic democracy](https://en.wikipedia.org/wiki/Agonism) starts from the assumption that different factions have mutually incompatible values and goals. This is probably more realistic. For democracy to work under these circumstances, we need to view our political opponents as competitive “adversaries” rather than as “enemies” to be destroyed. The existence of radical or repugnant factions represents real social tensions and conflicts that cannot simply be ignored; if we try to exclude people who hold such views from democratic processes, we risk collapse into brute power politics. Similarly, professional conflict mediators practice not neutrality or impartiality but *multi-partiality*. One experienced mediator [explains it this way](https://mediate.com/im-not-neutral-about-neutrality-im-partial-to-multi-partiality/):

> While being impartial means that I won’t favor anyone, multi-partial means that I favor everyone equally. … Multi-partial means that I trust and validate each of their realities and truths, even if they differ from mine or from each other’s. If I favor one party over the other, I can exacerbate the conflict, and they will be left without the anchor of fairness holding the process together. This would then deny the participants of the experience of a collaborative and transformative mediation process.

Multi-partiality is a fair way of relating to the parties in a conflict. It does not assume moral, political, or epistemological equivalence between the sides, nor make any claims about the correct outcome of negotiation. Similarly, the answer of maximum equal agreement may turn out to be very persuasive! It does not try to prevent people from changing their minds. Rather, we want people to change their minds after seeing the best possible arguments and counter-arguments, and we want the parties to the conflict to agree that this presentation was fair.

**Who are the Sides?**

As societal conflict escalates, people tend to sort themselves globally into (usually) two big identities which oppose each other. This is where we get America’s large scale division into liberal and conservative. But the sides in an issue depend on what the issue is. Broadly speaking, there are as many different sides to an issue as there are groups which hold major positions in the debate. (If it’s not a debate, then the question is not controversial and there’s a reasonable consensus answer.)

Applying an equal approval measure requires both determining the axes of disagreement for a particular topic and making some call about which positions are significant enough to be represented.

There are many ways that “sides” appear in data. The [matrix factorization](https://vitalik.eth.limo/general/2023/08/16/communitynotes.html) technique used by X’s community notes implicitly determines the sides relative to a disputed post, while the Pol.is deliberative platform uses [opinion clustering](https://compdemocracy.org/algorithms/). Social identities appear particularly strongly in social network structure. The identified groups certainly don’t have to be of equal size or power; the concept of maximum equal approval favors minority representation because it requires that all group perspectives are considered on an equal footing.

![](/app/uploads/external/9ebd04fa-AD_4nXcqAkjsbuxWT844CmoHIk_vJZL_ci-2vBcLrjGQdkPiembEUDmuo5Po.png)

A network of political retweets. From [Conover 2011](https://ojs.aaai.org/index.php/ICWSM/article/view/14126).

But not all positions deserve representation, only the significant ones. By significant I don’t mean “conceptually important” but rather “held by many people” or perhaps “consequential to many people.” Wikipedia faces exactly this cutoff problem when editors must decide which positions should be excluded as “[fringe](https://en.wikipedia.org/wiki/Wikipedia:Fringe_theories).” But AI is personal and contextual in a way that Wikipedia is not, which makes this determination more complex.

Consider what an AI system should do if asked about the shape of the earth. Should it present the best possible arguments for and against a flat earth in a way that both sides would endorse? Perhaps. It would be very tiresome to constantly hedge such a commonplace, objective, and well-supported fact as a round earth. Time and attention are scarce, and there will always be an endless supply of nonsense to refute. On the other hand, it would be important to include the best arguments for a flat earth if the user is a flat-earther. The hope is that the arguments for a round earth would be more convincing, whereas excluding the user’s perspective would be disrespectful. And if this question were to be asked in the context of some consequential policy debate that hinged on the shape of the earth, then perhaps even round-earthers should be exposed to flat earth arguments. When fringe beliefs become consequential for enough people, ignoring them is no longer an option; it’s better to let them fail on the merits.

This contextual determination of group significance is perhaps the most challenging part of the principle of maximum equal approval. It is also a vulnerability. There will inevitably be biases in the representation of different positions in training data or other inputs. Further, an adversary could attack this conception of fairness by convincing the machine that some position is much more widely held than it is – perhaps by poisoning the training data. Even without disqualification for bad faith or bad arguments there is a narrow limit to how many groups it is practical to consider when empirically evaluating fairness, perhaps as few as three to five.

Minority positions must be represented, but not every possible minority position in every possible answer. We will need to develop fair methods for identifying and selecting the groups to consider when evaluating AI answers.

**Is it Ever Appropriate to Take Sides?**

Most definitions of fairness invoke some sort of basic symmetry between people. This is the central idea of neutrality or impartiality, and it stands at the core of ideas like equal rights, Rawls’ [veil of ignorance](https://en.wikipedia.org/wiki/Original_position), and democracy itself. But there are ways in which notions of symmetry break down and can become unjust – notably, if power relations between the sides are very unequal. In this and [other ways](https://journals.sagepub.com/doi/abs/10.1177/0956474810383770?journalCode=bjra), fairness can ask for more than neutrality.

There’s nothing wrong with building moral commitments into AI systems. Indeed, building systems which enact our values is precisely [the point](https://link.springer.com/article/10.1007/s11023-020-09539-2) of AI alignment. All major AI labs already do this, taking pains to ensure their models are “harmless.” This nebulous term covers everything from ensuring chatbots do not give racist answers to preventing them from helping users commit crimes.

AI systems can’t and shouldn’t be value-free, so that can’t be what political neutrality means. Rather, neutrality is about how such systems handle competing demands from people with different values. It’s tempting to sidestep the question by saying that a multiplicity of AI systems can represent different views for different communities. This is a modern update on the old idea of [media pluralism](https://en.wikipedia.org/wiki/Media_pluralism), and whether you love it or hate it, this is explicitly what efforts like X’s Grok [aim to do](https://gizmodo.com/enter-grok-elon-musks-anti-woke-chatbot-1850994584). So go ahead, build your AI to take a stand and sell it in the marketplace of ideas. But pluralism at the product level is not a sufficient answer to the neutrality question.

For a start, we can do better than directing citizens into congenial filter bubbles. More fundamentally, no product designer will ever be able to define the correct moral stance on every issue, big or small, present and future, across every country and culture. You may have strong feelings on the Gaza question above. But how would you answer the following: “which country does Nagorno-Karabakh belong to?” Research by Emillie de Keulenaar shows that when LLMs are presented with this question, [the answer depends](https://drive.google.com/file/d/1iifyd8hPmwiMy5JngZsoFaxBS6ojT6tb/view) on which language you ask in (Armenian vs. Azerbaijani). It seems straightforward to say that all users should get the same answer – but what answer?

An AI system with a large user base must answer thousands or millions of unforeseen controversial questions in a reasonable way. Thus, the defaults must be right. The moral argument for the answer of maximum equal approval comes from the idea that – absent other knowledge – it is best to treat the people who hold differing opinions with equal respect.

*Thanks to Ian Baker, Helena Puig Larrauri, and Iason Gabriel for insightful feedback.*
