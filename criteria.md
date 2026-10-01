# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

If search_listings returns at least one listing, the loop always goes on to
suggest_outfit and create_fit_card. An empty wardrobe doesn't break this path,
because suggest_outfit returns general styling advice instead of failing. I didn't
set 5 of 5 because search_listings is a plain keyword match. A query can describe
something the catalogue has in words the listings don't use, so a query that should match can still come back empty and stop early.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

The stop is a plain check in run_agent. if search_listings returns an empty list,
we will set session["error"] and return before suggest_outfit or create_fit_card runs.
That check involves no keyword guessing and no model output, so the same empty result
takes the same path every time. The weakness behind criterion 1 doesn't apply here:
a query built to match nothing can't be missed by a loose keyword match. Anything
less than 5 of 5 would mean the branch itself is broken. 

---

## 3. The selected item is the same item passed to the next tool

Given a query that matches at least one listing, the item chosen from search results is the same item that reaches suggest_outfit and appears in the final response — 4 of 5 tries.

**Why this target:**
This catches a state bug that would otherwise look like a broken tool call. The search can succeed, the model can still answer, and the agent can still appear functional while quietly passing a different item than the one the user selected. I think a4 of 5 target is realistic because state mismatches are likely to happen when results are re ordered or a previous session value is reused.

---

## 4. The fit card includes the key identifying details

For each fit card produced from a valid item, the card names the item, includes a price or price range, and gives a short caption describing the outfit — in at least 4 of 5 tries.

**Why this target:**
The model is allowed to vary in wording, so the criterion should not require identical phrasing. What matters is that the card is usable and specific: the user can tell what item is being recommended, whether it is affordable, and what the outfit is meant to be. This is a realistic target because the model sometimes skips details or produces generic text, but it should still include the core facts most of the time.

---

## 5. An empty wardrobe still produces a fit card

Given a matching query and get_empty_wardrobe(), suggest_outfit returns general
styling advice (not "" and not an exception) and the agent still returns a fit card
— in at least 4 of 5 tries.

**Why this target:**
The switch to general advice happens in code, but the advice itself comes from the
model. With no wardrobe pieces to name, it may return a one-line generic tip that
never mentions the selected item, and the fit card built from it won't describe a
real outfit. I picked 4 of 5 which allows for that without letting a real bug slide.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
