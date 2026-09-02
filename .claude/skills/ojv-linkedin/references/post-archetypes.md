# OJV Post Archetypes

Five archetypes. Each has a purpose, a native funnel tier, an input trigger, a default CTA tier,
a skeleton, and two worked examples.

**How to read the examples.** Examples marked `VERIFIED 2026-09-03` use facts checked against the
linked primary source during the research pass and can be lifted as voice models. Examples marked
`STRUCTURE DEMO` use `<angle brackets>` wherever a number, name or date must be sourced at draft
time. Never publish a structure demo with the brackets still in it, and never fill a bracket from
memory.

**Archetype and slot are separate decisions.** The native funnel tier below is the archetype's
centre of gravity. The slot sets the actual CTA tier, which often means downgrading. An archetype
A post in Monday's awareness slot ends on a question and does not mention the trek.

---

## Choosing the archetype for a slot

Every post is exactly one archetype. Pick it from evidence, not preference, in this order.

1. **Read the rotation check first.** `python3 scripts/rotation-check.py <monday>` prints which
   archetypes, hook patterns, entities and images are BLOCKED this week. A blocked archetype is
   out, whatever the news says.
2. **Match the input you actually have.** The input trigger decides the archetype, not the other
   way round. Never go hunting for a story to fit a chosen archetype, because that is how invented
   details get in.

   | What landed in front of you | Archetype |
   | --- | --- |
   | Dated China deep-tech news with a checkable number | A |
   | A US or European company with documented traction in Asia, and a named mechanism | B |
   | An Asian company with documented traction in the West, and a named mechanism | C |
   | A funding story with a documented rejection count and a documented raise | D |
   | Something OJV itself did: an event, a workshop, a portfolio move, a partner on stage, a trek update | E |

3. **Fill the slots.** Monday takes a news or story archetype (A, B, C or D) with a soft CTA.
   Wednesday takes a proof archetype (B, C or D) with a medium CTA. Friday defaults to E, and
   takes A instead when a strong China signal is live and the trek is inside eight weeks.
4. **Prefer cold.** Where two archetypes both fit, take the one the rotation check reports as
   never used or longest unused.
5. **Never twice in one week.** Three posts, three different archetypes, always.
6. **If only two archetypes have verified material, ship two posts.** Two sourced posts beat
   three with one invented. Say which slot is empty and why.

### Why E exists

A, B, C and D are all commentary on other people. A page that only comments on others has no
evidence it can do the work. E is the only archetype that carries first-party proof, it is the
only one that can use the partner photos that make up most of the image library, and it is the
only one that still works in a week when the news is thin. It is also where the trek offer and
OJV Educate live once the trek is close.

---

## A. China signal to tour

| Field | Value |
| --- | --- |
| Purpose | Convert Western executives' curiosity about a China headline into the realisation that reading about it is not the same as seeing it, and that OJV runs the seeing. |
| Native funnel tier | Awareness to interest |
| Input trigger | A dated news item from China's deep-tech ecosystem: robotics, EV, battery, semiconductors, AI hardware, biotech, drones. Must carry at least one checkable number. |
| Default CTA tier | Hard on Friday slots (trek dates, DM keyword, enquiry link). Soft on Monday slots (question, no trek mention). |
| Length | 950 to 1,250 characters |
| Image | Factory floor, robotics showroom, Shenzhen street, hardware market, trek group shot |

### Skeleton

```
1. The signal.            One line. The number or the event, plainly. No adjectives.
2. The reframe.           One line. What the number actually is, which is not what it looks like.
3. The misread.           2 to 4 lines. How a Western executive reads this from a desk in London
                          or New York, and why that reading is wrong. Name the wrong conclusion.
4. On the ground.         3 to 5 lines. What this looks like physically in Shenzhen. Concrete
                          nouns: streets, floors, lead times, distances, who you meet. This is the
                          section that only OJV can write, so it carries the post.
5. The generalisation.    One or two lines. The transferable rule, usually a version of "the
                          ecosystem is the product, not the company".
6. Close.                 Question (soft) OR invitation with dates and keyword (hard). Never both.
7. Source line.           `Source: <publisher>, <date>: <UTM-tagged link>`
8. Hashtags.              3 to 5, at the end.
```

### Example A1 `VERIFIED 2026-09-03`

> Unitree closed its first day on the Shanghai exchange up 542%.
>
> That is not a robotics story. It is a supply chain story wearing a robot costume.
>
> Read from a desk in London, the takeaway is "Chinese robotics is a bubble" or "we should buy the
> stock". Both miss it.
>
> The reason a humanoid company can list in Shanghai 73 days after filing, and price at a 61
> billion yuan valuation, is that the hardware it needs is already sitting within an hour's drive
> of its assembly line.
>
> On the ground in Shenzhen this is unremarkable. Actuators on one floor. Reducers two buildings
> over. A machinist who will turn a revised part around before the end of the week, then argue
> with you about the tolerance because they have built the same part for four other robotics
> firms this month.
>
> That is the thing you cannot read in a filing. The company is not the moat. The one-hour radius
> is the moat.
>
> We are taking a small group of operators through that radius in October.
>
> 📍 Hong Kong and Shenzhen
> 🗓 13 to 17 October 2026, with ContraVC as official partner
> 👉 Comment TREK or DM the keyword and we will send the itinerary.
>
> Source: CNBC, 19 August 2026: <UTM-tagged link>
>
> #Shenzhen #DeepTech #Robotics #APAC #ChinaTechTrek

Notes on why this passes: hook is 62 characters, one number, no emoji. Line 2 is the Ashley
reframe pattern. Section 4 is the only part a competitor cannot write. Hard CTA, no closing
question. Every number is in the CNBC piece.

### Example A2 `STRUCTURE DEMO`

> <Company> just shipped <number> units of <thing> in a single quarter.
>
> The number is not the news. The lead time is.
>
> From outside, this looks like state subsidy, or dumping, or a chart that will revert. Those
> arguments are comfortable and they keep being wrong.
>
> What it is, in practice: <specific supply chain fact from the source, with the distance or the
> timeline>.
>
> Walk the <named market or district> and you can watch the loop close. <Concrete observation
> one>. <Concrete observation two>. <Who you end up talking to and what they assume is normal>.
>
> Every Western team we take through has the same moment on day two. The question stops being
> "how are they this cheap" and becomes "how are they this fast".
>
> What would change in your product roadmap if your next revision took nine days instead of nine
> weeks?
>
> Source: <publisher>, <date>: <UTM-tagged link>
>
> #China #Manufacturing #Hardware #APAC

---

## B. West into Asia

| Field | Value |
| --- | --- |
| Purpose | Show that Asia entry succeeds on a specific unlock, not on ambition, and that finding the unlock is the work OJV sells. |
| Native funnel tier | Interest to consideration |
| Input trigger | A US or European company with documented traction in an Asian market, and a named mechanism for it. No mechanism, no post. |
| Default CTA tier | Medium (comment a keyword, or a link to something genuinely useful) |
| Length | 1,000 to 1,300 characters |
| Image | Conference hall, workshop, city shot of the market in question, partner on stage |

### Skeleton

```
1. Hook.                  The counterintuitive fact about the entry, or the question the reader
                          has an opinion about.
2. What they did.         2 to 3 lines. Plain sequence of events with dates.
3. The unlock.            3 to 4 lines. Name it precisely and pick one: local partner, pricing
                          rebuild, distribution, regulatory sequencing, or community. Say what
                          they did NOT do, because the contrast is where the insight is.
4. Why it generalises.    2 to 3 lines. The rule. Tie it to the 15+ ecosystems line where it fits.
5. Our version of it.     2 to 3 lines. How OJV runs this play, named as a service (GTM advisory,
                          lead generation, fundraising support). Mechanism, not boast.
6. Disclosure.            One line if the company is not a client. Non-negotiable.
7. Close.                 Medium CTA or a question.
8. Source line + hashtags.
```

### Example B1 `VERIFIED 2026-09-03`

> Notion's second-biggest market outside the US was Japan before Notion had a Japanese product.
>
> The community got there first. Japanese users ran their own meetups, built their own forums, and
> wrote and self-published their own books about a tool that only spoke English.
>
> Notion localised in October 2021, after the demand existed. In the year before that launch,
> daily active users in Japan grew 500%.
>
> The unlock was sequencing, not translation.
>
> Most Western software teams do it in the opposite order. Localise, then hunt for demand, then
> conclude the market is small when the funnel stays empty. Notion let a market prove itself, then
> paid to serve it properly.
>
> This is the part that generalises across APAC. You are not entering one market, you are entering
> 15+ ecosystems with different rules, cultures and buyer behaviour, and only some of them are
> already pulling on your product. The job is finding which ones are pulling before you spend.
>
> That is most of what our GTM advisory work actually is. Find the pull, sequence the spend.
>
> We have never worked with Notion. This is commentary from the outside.
>
> Comment PULL and we will send you the three questions we use to test whether a market is pulling
> or you are pushing.
>
> Source: Notion, 12 October 2021: <UTM-tagged link>
>
> #GTM #APAC #MarketEntry #Japan #VentureStudio

Notes: the disclosure line sits immediately before the CTA so it cannot be missed. The number
carries a date because it is a 2021 figure being used in 2026, and the copy says so.

### Example B2 `STRUCTURE DEMO`

> <Company> spent <number> months in <market> before it took a single order. That was the plan.
>
> <What they did, with dates, from the source.>
>
> The unlock was regulatory sequencing. They took <licence A> first, which sounds like the small
> one, and it made <licence B> a formality instead of a fight.
>
> They did not open an office first. They did not hire a country head first. They did not run a
> launch campaign into a market where they were not yet allowed to invoice.
>
> Every APAC market has its own version of that ordering problem, and the correct order is
> different in each of the 15+ ecosystems. Getting it wrong costs a year, and the year is usually
> spent on the thing that felt most like progress.
>
> Sequencing is the first thing we map in a GTM engagement, before positioning, before pricing.
>
> We were not involved in <Company>'s expansion. This is commentary.
>
> Which came first in your Asia entry, the licence or the pipeline?
>
> Source: <publisher>, <date>: <UTM-tagged link>
>
> #MarketEntry #APAC #Regulation #GTM

---

## C. Asia into the West

| Field | Value |
| --- | --- |
| Purpose | The mirror case. Reset the assumption that a product good enough for Asia will sell itself in the West, and position OJV on the buyer, pricing and story side. |
| Native funnel tier | Interest to consideration |
| Input trigger | An Asian or Asia-based company with documented traction in the US or Europe, and a named mechanism. |
| Default CTA tier | Medium |
| Length | 1,000 to 1,300 characters |
| Image | Conference hall, Western city shot, partner with a founder, workshop |

**The spine of every C post:** the hard part is rarely the product. It is the buyer, the pricing
and the story. Say it in the post, in those terms.

### Skeleton

```
1. Hook.                  The thing that did not transfer, stated as a surprise.
2. What they had.         1 to 2 lines. The product was already good. Establish this fast so the
                          post cannot be read as "the product was weak".
3. What broke.            3 to 4 lines. Pick from: the buyer was a different person with a
                          different budget; the pricing model did not survive contact with
                          procurement; the story was written for an audience that already knew
                          the category.
4. What they changed.     2 to 3 lines. Specific, from the source.
5. Why it generalises.    2 lines. The buyer, the pricing, the story. Never the product.
6. Our version of it.     2 lines.
7. Disclosure + close.    Medium CTA or a question.
8. Source line + hashtags.
```

### Example C1 `STRUCTURE DEMO`

> <Company> was <number> in <home market> and unknown in Germany eighteen months later. The
> product had not changed.
>
> It did not need to. <One line establishing the product was already strong, from the source.>
>
> What broke was the buyer. In <home market> the decision sat with <role>, who could sign in a
> week. In Germany the same purchase sat with <role>, who needed <the thing they needed> and a
> reference customer in the same industry, in the same country.
>
> So the pricing broke too. A per-seat model that worked at <home market> deal sizes turned into
> a procurement argument about <the thing procurement argued about>.
>
> They fixed it by <specific change from the source>.
>
> This is the pattern in nearly every Asia-to-West move we see. The product is not the problem.
> The buyer is a different person, the pricing has to be rebuilt for how that person buys, and the
> story has to be rewritten for a room that has never heard of the category leader you beat at
> home.
>
> Rebuilding those three is what our GTM advisory work is for.
>
> We were not involved in <Company>'s expansion. This is commentary.
>
> Which of the three broke first for you, the buyer, the pricing or the story?
>
> Source: <publisher>, <date>: <UTM-tagged link>
>
> #GTM #Expansion #APAC #Pricing

### Example C2 `STRUCTURE DEMO`

> Would you bet against an Asian hardware company because Western buyers have not heard of it?
>
> <Company> has <number> of the <category> market by units. In <Western market> its brand
> recognition is <number or qualitative fact from source>.
>
> Both things are true at once, and only one of them is a moat.
>
> <What they did, from source.>
>
> The lesson is not "brands do not matter". It is that a brand advantage is a story advantage, and
> a story can be rewritten faster than a supply chain can be rebuilt.
>
> When we take an Asian founder into a Western market, the first month is not product work. It is
> finding out who signs, what they compare us to, and what they need to hear before they will put
> their own name on the decision.
>
> No relationship with <Company>. Commentary only.
>
> Comment STORY and we will send the one-page brief we use to rewrite a pitch for a Western buyer.
>
> Source: <publisher>, <date>: <UTM-tagged link>
>
> #Hardware #GoToMarket #APAC #Branding

---

## D. Rejection to raise

| Field | Value |
| --- | --- |
| Purpose | Reach a founder who is mid-raise and losing confidence, and land one idea: the problem is usually the list and the framing, not the company. Then position fundraising support. |
| Native funnel tier | Interest to consideration. Runs well in the awareness slot with a soft CTA because the story travels. |
| Input trigger | A founder, ideally Asian or Asia-based, with a **documented** rejection count and a documented raise. Both numbers must be in the source. |
| Default CTA tier | Soft or medium. Rarely hard, because a hard CTA on a rejection story reads as prospecting on someone's pain. |
| Length | 900 to 1,200 characters |
| Image | Partner portrait, workshop, one-to-one session. Never a stock "rejected" visual. |

### Skeleton

```
1. The number.            The rejection count, flat, with the raise or the outcome. One line.
2. What did not change.   1 to 2 lines. The business was the same business. Establish this.
3. What did change.       3 to 5 lines. Narrative, targeting, or warm access. Take it from the
                          source. This is the whole post, so do not compress it.
4. The reframe.           2 lines. A hundred nos to the wrong list is not evidence about the
                          company. It is evidence about the list.
5. Our claim, bounded.    2 to 3 lines. A shorter, better-targeted list. Cut the list, improve
                          the targeting, get to the right rooms. NEVER the yes.
6. Close.                 Soft question, or medium CTA. Never a hard sell.
7. Source line + hashtags.
```

### Example D1 `VERIFIED 2026-09-03`

> More than 100 investors said no to Canva before anyone said yes.
>
> Melanie Perkins spent roughly three years on that, pitching from Perth, and the company she was
> pitching did not change in any meaningful way between the last no and the first yes.
>
> Two things changed.
>
> The framing. She was asking investors to price a category that did not exist yet, so there was
> nothing to benchmark against. Consumer design software read as niche until the pitch stopped
> asking people to believe in a market and started showing them the behaviour.
>
> And the access. The breakthrough conversation happened because an investor was in Perth to
> kitesurf, and she got in front of him there. Not a warm intro from a fund's website. A room she
> managed to be in.
>
> A hundred nos from the wrong list is not information about your company. It is information about
> your list.
>
> This is the part of fundraising support we actually do. We cut the list, we fix who is on it,
> and we work the warm paths into the rooms where your story already makes sense. We do not
> promise the yes, because nobody honest can.
>
> If you are mid-raise: how many of the investors on your list have funded your category in the
> last 18 months?
>
> Source: Inc, on Perkins' 100-plus rejections: <UTM-tagged link>
>
> #Fundraising #Founders #APAC #VentureStudio

Notes: sections 5 and 6 are where this archetype lives or dies. "We cut the list, we fix who is on
it, we work the warm paths" is bounded to things OJV controls. "We do not promise the yes, because
nobody honest can" is the explicit disclaimer, in the voice, not bolted on. The close is a
question, not a pitch.

### Example D2 `STRUCTURE DEMO`

> <Number> nos. Then a <round size> round from <investor or type>, <how long later>.
>
> <Founder> was building the same thing in both halves of that story. Same product, same market,
> mostly the same deck.
>
> What moved was <narrative / targeting / warm access, from the source>.
>
> <Two to three lines of the specific change, from the source. If the source only says "the
> pitch changed", say that and do not embellish it.>
>
> Founders read a long rejection list as a verdict on the company. Usually it is a verdict on the
> match. Fifty funds that do not write cheques in your stage, your geography or your category will
> all say no, and they will all be right to, and none of it tells you anything.
>
> On a raise we would have cut that list hard and spent the time on warm paths into the funds that
> have actually funded this shape of company in the last two years. A shorter, better-targeted list
> beats a longer one. What we can change is who hears the pitch and how it lands, not the answer.
>
> How long is your current investor list, and how many of them have funded your stage this year?
>
> Source: <publisher>, <date>: <UTM-tagged link>
>
> #Fundraising #Founders #APAC #Startups

### Archetype D hard rule: outcome language

Never imply a guaranteed or probable outcome. The claim is process, not result.

**Approved phrasings**
- "We would have cut that list hard."
- "A shorter, better-targeted list beats a longer one."
- "We fix who is on the list and work the warm paths into the right rooms."
- "What we can change is who hears the pitch and how it lands, not the answer."
- "We do not promise the yes, because nobody honest can."
- "This is about improving the targeting, not the odds you were quoted by someone else."
- "Fewer meetings, better matched."
- "We would have got you in front of the funds that actually write cheques at your stage."
- "We shorten the list. The investors still decide."

**Banned phrasings**
- "We would have got you funded."
- "We would have closed this in X weeks."
- "Our founders raise faster." (a claim about outcomes, and unsourceable)
- "We get you the yes."
- "With us, that would not have taken 100 nos."
- "Guaranteed introductions to investors who will fund you."
- "We turn nos into term sheets."
- "X% of our founders raise." (never, unless OJV publishes the audited number, and even then not
  in an archetype D post)
- Any construction where OJV is the subject of a verb whose object is the funding event.

**Test to apply before writing the file.** Underline every sentence where OJV is the subject. If
the object of that verb is an outcome the investor controls, rewrite it so the object is something
OJV controls: the list, the targeting, the access, the framing, the preparation.

---

## E. Inside the room

| Field | Value |
| --- | --- |
| Purpose | Show the super-connector working, with real names, real rooms and real numbers, so the other four archetypes read as evidenced rather than as opinion. This is the only archetype where OJV is the subject. |
| Native funnel tier | Interest to enquiry. It is the natural home for the Friday offer slot. |
| Input trigger | Something OJV actually did. An event held, a workshop run, a portfolio company joined, a partner judging or speaking, a university programme started, a trek update. If OJV did not do it, this is not archetype E. |
| Default CTA tier | Hard on the Friday offer slot. Medium when the post is proof rather than offer. |
| Length | 900 to 1,200 characters. Behind-the-scenes posts may run shorter. |
| Image | **Required.** A named partner's face, or the room itself. A logo is not a face. This is the one archetype where a text-only fallback is not acceptable, because the post is a claim about a room that happened. |

### Skeleton

```
1. The specific, checkable detail.  One line. A number, a date, a room. Not "we had a great
                                    event". The August drinks post worked because it opened on
                                    "August in Hong Kong is supposed to be quiet".
2. What actually happened.          2 to 3 lines. Who was there, what it was, no adjectives.
                                    Name the partners and co-hosts.
3. Why it was built that way.       2 to 4 lines. The deliberate choice. No panels. No pitch
                                    decks. Curated room. This is the section that carries the
                                    positioning, and it is the difference between a photo dump
                                    and a post.
4. The connection to the thesis.    2 lines. Startups do not scale on capital alone, they scale
                                    on access. Our job is to keep building those rooms.
5. Thanks or credit.                One line, only where a real co-host or partner earned it.
                                    Never a wall of tags.
6. Close.                           Hard CTA (next date, keyword, enquiry link) or a question.
                                    Never both.
7. Hashtags.                        3 to 5, at the end.
```

### Example E1 `VERIFIED 2026-09-03` (from OJV's own August event)

> August in Hong Kong is supposed to be the quiet month. Empty calendars, everyone away, nothing
> booked.
>
> We pulled more than 150 signups anyway.
>
> Last month we ran summer drinks with Carta and Endowus. Gelato, cold beer, a room of founders
> and investors.
>
> No panels. No pitch decks. No agenda.
>
> That was the whole design, not a shortcut. A panel gives 40 people permission to sit quietly and
> watch four people talk. Take the panel away and the same 40 people have to actually meet each
> other, which is the only thing any of them came for.
>
> Startups do not scale on capital alone. They scale on access, to the right operators and the
> right partners at the right time. Our job is to keep building the rooms where that happens.
>
> Thanks to Carta and Endowus for co-hosting this one.
>
> The next one is in October, alongside the China Tech Trek week.
>
> 👉 Comment TODO(config: DM keyword) and we will send you the invite.
>
> #HongKong #Founders #APAC #VentureStudio

Notes: the number is first-party, so it is attributed to our own signup list rather than linked.
Section 3 is doing the real work, and it is the part a competitor cannot copy because it is a
reason, not a fact. Five tags cut to four. The original version of this post ran seven.

### Example E2 `STRUCTURE DEMO`

> <Partner name> spent <duration> judging <track> at <event>, <date>.
>
> <One or two lines on what the event was and what the role actually involved.>
>
> <Two to four lines on the pattern they saw across the companies. This is the value of the post.
> A judging slot is not interesting. What <number> pitches in a row taught you is.>
>
> The reason we take these seats is not visibility. It is that you cannot advise founders in a
> market you are not sitting in. APAC is not one market, it is 15+ ecosystems with different rules
> and different buyers, and the recalibration only happens in the room.
>
> <Credit line if a co-host earned it.>
>
> Which APAC market surprised you most this year?
>
> #<Sector> #APAC #Founders #<City>

### First-party numbers in archetype E

Style rule 8 says every number carries a source link. Archetype E is the exception, because our
own numbers have no external link. So:

- Attribute the number in the copy to where it came from: "more than 150 signups" on our own
  signup list, "the room held 40" from the venue booking.
- Never round upward. 150+ is fine when the list says 154. It is not fine when the list says 138.
- **Check every first-party number with the partner who owns it before the post is scheduled.**
  An unchecked internal number is exactly as bad as an unsourced external one, and worse, because
  the people in the room will know.
- No aggregate claims about outcomes. "Companies we have worked with have raised X" does not go
  out without audited numbers and Naman's sign-off, and it does not belong in archetype E anyway.

### Third-party disclosure, all archetypes

Every archetype B, C and D post about a company OJV has not worked with carries an explicit
disclosure line in the body. Approved forms:

- "We have never worked with <Company>. This is commentary from the outside."
- "We were not involved in <Company>'s expansion. This is commentary."
- "No relationship with <Company>. Commentary only."
- "We had nothing to do with this one. We just think it is the clearest example around."

Never rely on implication, and never place the disclosure after the hashtags where it will be
truncated out of view.

Archetype E is the mirror case: it is the only archetype where OJV may claim credit, and it must
claim only what OJV actually did. Co-hosted means co-hosted. A partner judging a track is not OJV
running the event.
