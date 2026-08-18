# Forward-Logic Paper Standard

Use this reference for paper planning, drafting, figures, and polishing. It supplements evidence rules; it never permits a claim that the research artifacts do not support.

## Separate global payoff from local explanation

The title, abstract, and introduction may state the final contribution and strongest supported result early. That global promise helps the reader decide what the paper is about. The technical exposition must still reconstruct necessity in forward order. Before a design choice appears, the reader must already know the concrete problem it addresses, why the obvious or inherited approach is insufficient, and the requirement the new choice must satisfy.

Do not hide the final method as a mystery. Do not reveal a component first and add its rationale later. The correct order is payoff early, necessity before each local choice.

## Track reader state

For every major section or method step, record:

| Reader-state field | Required answer |
|---|---|
| established prior | What the reader already learned in this paper |
| missing or wrong prior | What a competent reader is unlikely to know, or is likely to assume incorrectly |
| exposed problem | The concrete limitation visible at this point |
| insufficient default | Why the obvious baseline response does not solve it |
| derived requirement | What any adequate next step must accomplish |
| design response | The smallest choice that meets that requirement |
| predicted observable | What evidence would show that the response works for the stated reason |

No design response may enter the main argument before the exposed problem, insufficient default, and derived requirement are established. If a choice has no such chain, remove it from the main story or identify the missing evidence.

## Make paragraphs inferential units

A paragraph should perform one reasoning move: establish a claim, give the evidence or mechanism needed to accept it, and state the consequence for the next move. A paragraph is not a container for everything about one topic. Merge short fragments when none carries an argument alone; split only when the inference changes.

Spend words on missing priors, wrong priors, non-obvious distinctions, and transitions that the argument depends on. State field consensus in one sentence unless the paper challenges it. Prefer familiar words, direct syntax, and nearby subjects and verbs. Remove terms that sound technical but do not identify a mechanism, quantity, assumption, or obligation.

Use lists only for genuinely parallel items, procedures, or compact reference material. The main scientific argument should read as connected prose.

## Design figures from one takeaway

Write one complete sentence that a figure must communicate before drawing it. The figure passes only if a reader can extract that sentence in about three seconds.

Keep an element only when removing it would weaken the takeaway. Use visual hierarchy to show the comparison, mechanism, or causal step that carries the claim. Do not translate every textual module into a box, every mention into an arrow, or every available result into a panel. A caption states what is compared, what the reader should notice, and the scope of the supported conclusion.

## Audit forward order

Before finalizing a section or figure, ask:

1. Does any design choice appear before its problem and requirement?
2. Does any sentence rely on knowledge the paper has not yet established?
3. Does a paragraph merely collect a topic instead of advancing an inference?
4. Is space spent restating consensus while a non-obvious transition is compressed?
5. Does any term lack a concrete referent or testable meaning?
6. Can each figure's takeaway be stated in one sentence and read in three seconds?
7. Can any box, arrow, panel, label, or sentence be removed without weakening the argument?
