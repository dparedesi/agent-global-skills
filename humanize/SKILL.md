---
name: humanize
description: Convert AI-written text to more human-like writing through subtle edits. Use when text reads "too AI", when the user mentions "humanize", "sounds robotic", "AI-written", "make it natural", or when editing for a more conversational voice.
---

# Humanize Text

Make AI-generated content read like it was written by a human through targeted, subtle edits.

**Why?** AI-written text has telltale patterns—formulaic transitions, passive voice, overly balanced sentences—that make it feel mechanical. This skill fixes those patterns without rewriting the whole document.

## Quick Start

1. Read the file → 2. Identify AI patterns → 3. Make targeted edits → 4. Verify variety

## How It Works

### Step 1: Read and Scan for AI Patterns

Read the target file and identify these common AI-writing tells:

| Pattern Type | Examples | Why It Sounds AI |
|--------------|----------|------------------|
| **"By [gerund]" overuse** | **"By implementing...", "By constructing...", "By training..."** | **Creates monotonous explanatory rhythm. SCAN FOR THIS FIRST—it appears in nearly every paragraph of technical AI writing.** |
| Formulaic transitions | "Furthermore,", "Additionally,", "Moreover," (Note: "However" is fine in moderation) | Too consistent, textbook-like |
| "This [verb] that" | "This suggests that...", "This demonstrates that...", "This indicates that..." | Most common AI fingerprint |
| **Em-dashes** | "The result—faster inference—was surprising" | Humans rarely use em-dashes; AI overuses them |
| **Fragment + colon** | "The result:", "The takeaway:", "What's needed:", "The implication:" | Humans write complete sentences in prose, not headline fragments |
| Noun-heavy subjects | "The deployment of...", "The integration of...", "The introduction of..." | Passive, distancing |
| Passive constructions | "has been shown to", "is being developed", "was demonstrated" | Avoids direct statements |
| Balanced sentences | Every paragraph: claim → evidence → implication; semicolon-connected clauses | Mechanical rhythm |
| Framework redundancy (on repeat use) | "The BioDisco framework" after already introduced | Redundant when name is already established |
| Opening formulas | "In the realm of...", "In the domain of...", "A systematic evaluation..." | Pompous, detached |
| Result phrasing | "achieves X% improvement on Y benchmark", "achieving state-of-the-art" | Always same structure |
| Excessive bolding | Every technical term **bolded** | Over-emphasizes everything |

### Step 2: Apply Targeted Edits

Make 10-20 edits across the document. Do NOT rewrite entire sections.

> [!IMPORTANT]
> **Preserve word count.** The goal is to make text sound human, not to shorten it. If the original paragraph is 150 words, your edited version should be ~140-160 words. Avoid compounding conciseness across multiple passes—repeated humanization should NOT shrink the document.
>
> **How to preserve word count while removing patterns:** Don't pad with filler words (like "meaningfully", "smartly", "actively"). Instead: (1) Restructure sentences to use natural alternatives that maintain length, (2) Expand existing explanations rather than condensing them, (3) Rearrange clause order to achieve length naturally. Example: "By analyzing discourse" (4 words) → "When analyzing discourse" (4 words) preserves both pattern change AND length without padding.

### Step 2b: Word Count Verification (MANDATORY)

> [!CRITICAL]
> **ZERO NET CHANGE RULE:** Document word count must remain within ±5% of the *original* (not previous iteration). If you've reduced word count by more than 5%, you are **condensing**, not **restructuring**. Stop and add content back.
>
> **Why?** In multi-pass or multi-iteration contexts, even small reductions compound: -5% per pass = 59% remaining after 5 passes.

**Before submitting your work:**

1. Count original document word count
2. Count edited document word count
3. Calculate percentage change: ((New - Original) / Original) × 100
4. If **> -5%**: STOP. You condensed. Restructure instead—expand explanations, add supporting detail, rephrase to recover length without padding.

**Section-by-section tracking (for longer documents):**
- For each section edited, note: `[Section name] - Original: X words → Edited: Y words (Z% change)`
- Flag any section with >5% reduction for restructuring, not condensing

### Condensing vs. Restructuring: The Critical Distinction

This is the most common failure mode. Understand the difference:

| Condensing (❌ DO NOT DO) | Restructuring (✅ DO THIS) |
|---|---|
| "Long sentence with pattern" → "Short sentence" | "Long sentence with pattern" → "Reworded long sentence without pattern" |
| Removes words to improve flow | Keeps words but changes their arrangement and rhythm |
| Results in net loss of content | Preserves all content, just reorganized |
| Example: "An agentic framework for processor design utilizes LLMs to break down complex hardware descriptions" → "Agents decompose chip designs" | Example: "An agentic framework for processor design breaks down complex hardware descriptions, generates HDL, and verifies it with engineer review" (same length, different pattern) |

**When you're tempted to condense, instead:**
1. Expand the explanation: "X happens" → "X happens because Y, which means Z"
2. Add supporting detail: "The system works" → "The system works by using A and B approaches, both of which..."
3. Rephrase with more words: "Transparency doesn't build trust" → "Transparency alone, without cognitive alignment, doesn't build the kind of trust that humans need"
4. Break into multiple sentences: "Long clause, long clause" → "Long clause. New sentence with second clause."

**Multi-Pass Approach:** For longer documents (2000+ words), use multiple passes with focused attention:
- **Pass 1:** Scan for high-frequency patterns—especially "By [gerund]", formulaic transitions, "This [verb] that"
- **Pass 2:** Fix sentence rhythm and variety—ensure paragraphs don't start the same way, vary sentence lengths
- **Pass 3:** Verify consistency—check that no new patterns were created and that edits feel natural
- **Pass 4 (MANDATORY):** Word count check. If total word count dropped >5% from original, stop and restructure passages back to original length.

**Transition Replacements:**

| AI Pattern | Human Alternatives |
|------------|-------------------|
| "However, ..." (overused) | Keep some! Vary with "That said,", "The catch is that", "The trade-off is" |
| "Furthermore, ..." | "Also,", "And", "Plus,", or just start new sentence |
| "Additionally, ..." | "On top of that,", remove and restructure |
| "This suggests that..." | "which suggests", "The implication is that...", "...suggesting that" |
| "This demonstrates..." | "showing", "...which demonstrates", or just state the conclusion |
| "By [gerund]..." | "Through X,", "Using Y,", "When [verb]", restructure to lead with outcome instead, or change passive to active voice |
| "In the realm of..." | "For...", "In...", or just name the domain directly |
| "Simultaneously, ..." | "Meanwhile,", "At the same time,", "In parallel," |
| "The [X] framework..." (repeat) | Just "X" after first introduction |
| "achieves X% on Y" | "a X% jump on Y", "X% better than", "achieving X%", move metric position |

> [!CAUTION]
> **Avoid colon-fragment replacements.** Patterns like "The result:", "The implication:", "What's needed:" are themselves AI tells. Humans write complete sentences:
> - ❌ "The implication: current methods fail" 
> - ✅ "The implication is that current methods fail"
> - ✅ "...which implies that current methods fail"

**Sentence Structure Fixes:**

- Break long compound sentences into two sentences, or use colons (:) sparingly
- **NEVER use em-dashes (—)**: Humans rarely use them; they're a major AI tell. Use periods, commas, colons, or parentheses instead. This is a hard constraint—every em-dash must be removed or replaced.
- Add occasional questions for **topic transitions only**: "So what changed?" / "Why the structural formalism?" (NOT mid-paragraph rhetorical pauses like "What does this imply?" which are AI tells)
- Use "you" when explaining: "This lets you..."
- Vary sentence length dramatically: 5-word sentences next to 40-word ones
- Use active verbs for researchers: "Researchers found" not "Research uncovers"

**Tone Adjustments:**

- Replace "It is worth noting that" → just state the thing
- Replace "It should be noted" → cut entirely or use "Note:"
- Add conversational asides: "Think of it as...", "The key insight:", "Here's the telling detail:"
- Avoid contractions in academic/formal writing—they sound conversational, not scholarly. Reserve casual tone for blog posts or newsletters only.
- Add occasional first-person: "we see here", "what this tells us"
- Include rare hedging: "appears to", "seems to suggest" (humans hedge differently than AI)
- Use occasional metacommentary: "This is worth understanding, but the core idea is simple:"

### Step 3: Vary Your Edits

> [!CAUTION]
> Don't create new patterns. If you replace every "However" with "But", that's just a different pattern. Mix it up:
> - Some "However" → "But"
> - Some "However" → start sentence differently
> - Some "However" → merge with previous sentence using ", but"
> - Some "However" → leave as-is

### Step 4: Check for Balance

After editing, scan the document:
- [ ] **Word count within ±5% of original** (CRITICAL—check this FIRST)
- [ ] No more than 2 consecutive paragraphs start the same way
- [ ] Mix of sentence lengths (short punchy + longer flowing)
- [ ] At least some contractions or informal touches
- [ ] Technical terms bolded sparingly, not exhaustively
- [ ] All citations and section structure preserved

## Examples

**Example 1: Formulaic Opening**
- Before: "A systematic evaluation of 53 large language models has revealed that longer reasoning chains do not reliably produce better answers."
- After: "A systematic evaluation of 53 large language models revealed something counterintuitive: longer reasoning chains don't reliably produce better answers."

**Example 2: "This suggests" Pattern**
- Before: "This method proves particularly effective in mathematical reasoning, suggesting that the dichotomy between imitation and exploration is artificial."
- After: "Works especially well for mathematical reasoning, which suggests the imitation vs. exploration dichotomy might be artificial."

**Example 3: Passive + Formal**
- Before: "The deployment of Large Reasoning Models has been hampered by their tendency to apply uniform computational resources."
- After: "Large Reasoning Models have a problem: they apply the same computational effort whether you ask them to add two numbers or prove a theorem."

**Example 4: Conclusion Softening**
- Before: "This week's research reflects a shift from unbounded reasoning capability toward calibrated cognitive efficiency."
- After: "The week's theme: unbounded reasoning isn't always better."

**Example 5: "By [gerund]" Pattern**
- Before: "By employing a margin policy gradient loss and rejection sampling, CompassJudger-2 attempts to create a generalist judge that rivals larger models."
- After: "CompassJudger-2 uses margin policy gradient loss and rejection sampling to create a generalist judge rivaling larger models."

**Example 6: Framework Redundancy**
- Before: "The RefCritic framework employs a long-chain-of-thought critic module trained via reinforcement learning."
- After: "RefCritic employs a long-chain-of-thought critic module trained via RL."

**Example 7: Result Phrasing**
- Before: "This approach achieves a 23.2% improvement in success rates on novel software environments compared to static baselines."
- After: "The result: 23.2% better success rates on novel software environments."

**Example 8: Adding Questions**
- Before: "However, applying these techniques to open-ended domains has remained elusive due to the lack of verifiable signals."
- After: "However, applying these to open-ended domains has remained elusive. Why? No verifiable signals to anchor the training."

**Example 9: Preserving Word Count While Removing "By [gerund]"**
- Before (32 words): "By analyzing synchronous discourse in human-AI triads, researchers found that the educational value of these agents lies not in their ability to generate content, but in their capacity to alter the structure of reasoning."
- After (32 words): "When analyzing synchronous discourse in human-AI triads, researchers found that the educational value of these agents lies not in their ability to generate content, but in their capacity to alter the structure of reasoning."
- Note: Pattern change achieved by substituting "By" → "When" without restructuring, padding, or cutting. Same word count, improved tone.

## Quality Guidelines

- **Preserve meaning**: Edits should change tone, not content
- **Stay subtle**: 10-20 targeted edits, not a full rewrite
- **Maintain expertise**: The text should still sound knowledgeable, just not robotic
- **Match context**: Different domains require different humanization intensity. Humanization removes AI patterns but shouldn't change the register of the original text.
- **Don't over-correct**: Formal language is fine—"However" is normal in written prose, "But" is too casual. The problem is *overuse* and *uniformity*, not formality itself
- **Respect register**: Written communication isn't WhatsApp. Keep appropriate formality while adding variety
- **First-reference rule**: Keep context on first mention ("A new framework called X", "The Y architecture"). Only drop descriptive nouns on subsequent references after the term is established
- **Preserve introductions**: When something is NEW to the reader, "A new method called X demonstrates..." is human; stripping to just "X demonstrates..." loses necessary context

### Domain-Specific Calibration

The intensity of humanization varies by context. The goal is always the same—remove AI patterns—but not to change the inherent formality of the domain:

| Domain | Edit Count | Focus Areas | Don't Do |
|--------|-----------|------------|----------|
| Academic/Research papers | 8-12 edits | "By [gerund]" → "When/Through", transition variety, sentence rhythm | Add asides or colloquialisms; use contractions |
| Technical documentation | 6-10 edits | Remove "By [gerund]", fix passive voice, clarify with active verbs | Use conversational tone; lose precision |
| Blog posts | 15-20 edits | All patterns, add personality, can include conversational asides | Sacrifice clarity for style |
| Newsletters | 12-18 edits | Pattern removal plus selective personality additions | Sound unprofessional or lose authority |

**Key principle:** Humanization means removing AI *patterns*, not reducing *formality*. An academic paper should remain academic after humanization.

**Critical reminder (applies to ALL domains):** Word count preservation is NOT negotiable. Whether the document is academic, technical, or narrative, maintain ±5% word count. Humanization that compresses content is not humanization—it's summarization. This rule has no exceptions.

### Academic/Research-Specific Warnings

When humanizing technical or academic writing, watch for these pitfalls:

- **Avoid padding to maintain word count.** Don't add hollow adverbs like "meaningfully", "smartly", "actively", or "consistently" just to preserve length. Instead, restructure sentences or expand genuine explanations.
- **Don't sacrifice technical precision for flow.** Keep technical terminology, proper capitalization of systems/frameworks, and specific notation intact. Humanization should not simplify content.
- **Maintain section structure.** Don't alter headings, subheadings, or the hierarchical organization of the paper. Humanization applies to prose only.
- **Watch for pattern substitution.** Removing "By [gerund]" is good; replacing it consistently with "Through X" or "When [verb]" creates a new pattern. Vary your replacements.
- **Keep citations intact.** Do not simplify or paraphrase citations; they must remain exact references to the original work.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Word count dropped >5%** | **STOP. You condensed, not restructured.** Revert changes and instead: expand explanations, add supporting detail, break long sentences into multiple sentences (don't remove words). Aim for same word count, different pattern. |
| Text now sounds too casual | Scale back conversational asides and colloquialisms; keep more original phrasing |
| Created new repetitive pattern | Vary your replacements; use different fixes for same issue |
| Lost technical precision | Restore specific terms; only simplify explanatory phrases |
| Edits feel disconnected | Read surrounding sentences; match the local rhythm |
| All paragraphs still start same way | Vary openers: some with results, some with questions, some with fragments |
| Too many short punchy sentences | Add a few longer, flowing sentences back for rhythm variety—this also helps recover word count |
| Metrics feel buried | Sometimes lead with the number: "23% fewer tokens—that's what ASAP achieves" |
| Compounding word loss across iterations | Always measure against ORIGINAL document, not previous iteration. Each pass must stay within ±5% of original baseline. |

## Cross-Article Consistency Check

When editing multiple related articles, watch for:
- Using the same replacement for a pattern across all articles (creates new uniformity)
- Overusing any single conversational touch ("The key insight:" in every article)
- Same sentence rhythm across articles (all conclusions as fragments, etc.)
- Missing domain-appropriate variation (security articles can be more urgent than methodology papers)
