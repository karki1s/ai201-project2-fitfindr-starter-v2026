# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
User asked for 'vintage graphic tee under $30' using `python app.py ask 'vintage graphic tee under $30'`
It return following:
The planning loop isn't built yet — see the TODO in agent.py.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
It serches the local catalogue by description keywords, with optional size and price celing filters; 
size matching uses whole tokens and the price limit is inclusive. 
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
`description` (str)
`size` (str) optional field
`max_price` (float) optional field
- **Returns:**
 A list of matching listing dictionaries, ranked by keyword match and then lower price; each includes fields such as title, price, size, and platform.
- **When it has nothing:**
When there is no matches it returns empty list []

### `suggest_outfit`

- **What it does:**
It suggests two outfits built around a selected listing, using items from the user’s wardrobe when available.
- **Inputs:**
`new_item` (dict)
`wardrobe` (dict)
- **Returns:**
A non-empty str with two outfit suggestions; when the wardrobe has items, it names those pieces as written.
- **When it has nothing:**
It returns general outfit ideas and says they are general because no wardrobe is saved.

### `create_fit_card`

- **What it does:**
It writes a short social-media-style caption about the selected second-hand find and how it could be worn.
- **Inputs:**
`outfit` (str)
`new_item` (dict)
- **Returns:**
A str of two to four sentences that includes the price written with digits and the selling platform.
- **When it has nothing:**
If outfit is empty or whitespace, returns a helpful fallback message instead of calling the model or raising an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

If search_listings returns an empty list, set session["error"]
to a message telling the user what to change (e.g. "No listings matched 'graphic
tee' in size M under $30 — try a higher max price, a different size, or fewer
keywords"), then return the session without calling suggest_outfit or
create_fit_card. Otherwise, store the first result in session["selected_item"],
pass it and the wardrobe to suggest_outfit, then pass that outfit and the item
to create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

Ran before run_agent was implemented in agent.py file
```
$ python app.py ask 'graphic tee under $30'

The planning loop isn't built yet — see the TODO in agent.py.

0 model calls this session

```
Ran afterrun_agent was implemented agent.py file as part of milestone-5
```
$ python app.py ask 'graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Early 2000s Brat**
Layer the Y2K baby tee under the vintage black denim jacket, paired with the baggy straight-leg jeans (cinched with the brown leather belt). Finish it off with the chunky white sneakers and the black crossbody bag for a high-contrast, nostalgic street look.

**Outfit 2: Soft Contrast**
Tuck the Y2K baby tee into the wide-leg khaki trousers, worn with the brown leather belt to define the waist. Throw the black cropped zip hoodie loosely over your shoulders and ground the pastels with the black combat boots.

  Fit card: Finally caved and snagged this butterfly baby tee for just $18 on depop, and honestly I'm obsessed. I've been living in it layered under my black denim jacket with baggy jeans for that ultimate early 2000s brat energy. Such a good little staple for the rotation.

2 model calls this session, 487 prompt + 191 output tokens

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

**Outfit 1: Casual Streetwear**
Pair the vintage Levi's 501s with the white ribbed tank top tucked in, layered under the oversized grey crewneck sweatshirt. Cinch the waist with the brown leather belt and finish the look with chunky white sneakers and the black crossbody bag.

**Outfit 2: Edge & Denim**
Style the Levi's 501s with the black cropped zip hoodie and the vintage black denim jacket layered on top for a double-denim moment. Ground the outfit with the black combat boots and accessorize with the black crossbody bag.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi's 501s on Depop for just $38 and I am never taking them off. They have that perfect broken-in feel and look so good with crisp white sneakers. Total effortless Sunday morning coffee run energy.
```
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
I asked to explain me overall structure of the code base and also ask me to outline and check what I have implemented
- *What came back:*
It explain overall code base, suggest certain thing for me to change for the run_agent
- *What I changed:*
Applied some suggestion and verify the codebase and run the tests

**Moment 2**

- *What I asked for:*
I used AI to verify my score for the Scenarios run result conditions. 
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS |PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item carries through | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card has item, price, vibe | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. empty wardrobe | 4 of 5 | PASS | PASS | PASS | PASS |PASS  | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: 10 found, selected 'Y2K Baby Tee — Butterfly Print'
[3] suggest_outfit
      in:  item='Y2K Baby Tee — Butterfly Print', wardrobe=10 items
      out: **Outfit 1: Off-Duty Y2K** Pair the baby tee with your *Baggy straight-leg jeans, dark wash* using the *Brown …
[4] create_fit_card
      in:  item='Y2K Baby Tee — Butterfly Print', outfit='**Outfit 1: Off-Duty Y2K**\nPair the baby tee with your *Bagg'…
      out: Found this cute butterfly baby tee on Depop for just $18 and I'm obsessed. I've been living in it layered unde…
  try 1: completed — fit card 255 chars

impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: no results, stopping before suggest_outfit
  try 1: stopped early — Nothing in the listings matched description 'designer ballgo

empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
[2] search_listings
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: 7 found, selected 'Denim Jacket — Light Wash, Cropped'
[3] suggest_outfit
      in:  item='Denim Jacket — Light Wash, Cropped', wardrobe=0 items
      out: **Off-Duty Streetwear:** Layer it over an oversized black graphic hoodie, high-waisted olive green cargo pants…
[4] create_fit_card
      in:  item='Denim Jacket — Light Wash, Cropped', outfit='**Off-Duty Streetwear:** Layer it over an oversized black g…
      out: Scored this light wash cropped denim jacket on Poshmark for $42 and I’m obsessed. It’s giving major off-duty s…
  try 1: completed — fit card 218 chars

selected item carries through  (example wardrobe)
  query: band tee size L
[1] parse_query
      in:  band tee size L
      out: {'description': 'band tee', 'size': 'L', 'max_price': None}
[2] search_listings
      in:  {'description': 'band tee', 'size': 'L', 'max_price': None}
      out: 2 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey
      →    branch: 2 found, selected 'Graphic Tee — 2003 Tour Bootleg Style'
[3] suggest_outfit
      in:  item='Graphic Tee — 2003 Tour Bootleg Style', wardrobe=10 items
      out: **Outfit 1: 2000s Streetwear Grunge** Tuck the graphic tee into the baggy straight-leg jeans, cinched with the…
[4] create_fit_card
      in:  item='Graphic Tee — 2003 Tour Bootleg Style', outfit='**Outfit 1: 2000s Streetwear Grunge**\nTuck the graphic …
      out: Scored this 2003 tour bootleg graphic tee on Depop for just $24 and it’s already doing all the heavy lifting i…
  try 1: completed — fit card 283 chars

fit card has item, price, vibe  (example wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
[2] search_listings
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: 7 found, selected 'Denim Jacket — Light Wash, Cropped'
  [rate limit] 15 requests used this minute. Waiting 43s. This is normal.
[3] suggest_outfit
      in:  item='Denim Jacket — Light Wash, Cropped', wardrobe=10 items
      out: **Outfit 1: The Double Denim Contrast** Layer the new light wash cropped jacket over the white ribbed tank top…
[4] create_fit_card
      in:  item='Denim Jacket — Light Wash, Cropped', outfit='**Outfit 1: The Double Denim Contrast**\nLayer the new ligh…
      out: Scored this cropped light wash denim jacket on Poshmark for $42 and I’m obsessed. Just threw it on over a whit…
  try 1: completed — fit card 246 chars

empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
[2] search_listings
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: 7 found, selected 'Denim Jacket — Light Wash, Cropped'
[3] suggest_outfit
      in:  item='Denim Jacket — Light Wash, Cropped', wardrobe=0 items
      out: **Outfit 1: Elevated Streetwear** Layer the cropped light-wash jacket over an oversized graphic black band tee…
[4] create_fit_card
      in:  item='Denim Jacket — Light Wash, Cropped', outfit='**Outfit 1: Elevated Streetwear**\nLayer the cropped light-…
      out: Scored this cropped light-wash denim jacket on Poshmark for $42 and I'm obsessed. Currently living for throwin…
  try 1: completed — fit card 240 chars
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | Each try counted as PASS if the run didn't stop early and the session held an outfit suggestion and a fit card. All 5 did. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | PASS if the trace ended at `search_listings` with `[] (empty)`, there was no `suggest_outfit` step, and the message named something to change. All 5 named broader words, a different size than XXS, and a price above $5. |
| 3 | The selected item is the same item passed to the next tool | 4 of 5 | MET (5/5) | PASS if the first search result was the `selected_item`, the trace showed that same title going into `suggest_outfit` and `create_fit_card`, and the fit card described that item. It did in all 5. I counted shortened names like "bootleg tour tee" as the same item, because the price ($24) and platform (Depop) also matched. |
| 4 | The fit card includes the key identifying details | 4 of 5 | MET (5/5) | PASS if the card named the denim jacket, gave a price, and described a specific outfit. All 5 said "$42 on Poshmark" and described a look such as double denim or 90s streetwear. |
| 5 | An empty wardrobe still produces a fit card | 4 of 5 | MET (5/5) | PASS if the trace showed `wardrobe=0 items`, the outfit was non-empty general advice about the jacket, and a fit card came back. All 5 did. |


**Diagnoses**
No criterion missed. The log still showed two problems that my criteria were too loose to catch.

1. Wrong item ranked first — in the tool (`search_listings`).
For "vintage graphic tee", all 5 tries chose "Y2K Baby Tee — Butterfly Print" over
"Graphic Tee — 2003 Tour Bootleg Style". All three tee listings matched all three
query words (`vintage`, `graphic`, `tee`) somewhere in their text, so they tied at a
score of 3. Python's sort is stable, so the tie kept file order, and the Baby Tee is
listing 1 while the Graphic Tee is listing 5. The score counts a word found in the
description the same as a word in the title. Criterion 1 passed because it only
checks that all three tools ran, not that the best item was chosen.

2. The fit card invents ownership — in the model's output (`create_fit_card` prompt).
With an empty wardrobe, the cards say things like "I've been living in it over a satin
slip dress and Sambas", which are clothes the user never said they own. `suggest_outfit`
correctly gives general advice, but `create_fit_card` gets that advice as "how it's
being styled" and the prompt asks for a first-person post, so the model writes the
suggestions as things the user already did. The tool and the branch work; the prompt
doesn't tell the model the pieces are suggestions.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'black combat boots under $60' --trace
[1] parse_query
      in:  black combat boots under $60
      out: {'description': 'black combat boots', 'size': None, 'max_price': 60.0}
[2] search_listings
      in:  {'description': 'black combat boots', 'size': None, 'max_price': 60.0}
      out: 9 items: Oversized Flannel Shirt — Plaid Red/Black, Graphic Tee — 2003 Tour Bootleg Style, Platform Mary Janes — Black Patent … +6 more
      →    branch: 9 found, selected 'Oversized Flannel Shirt — Plaid Red/Black'
[3] suggest_outfit
      in:  item='Oversized Flannel Shirt — Plaid Red/Black', wardrobe=10 items
      out: **Outfit 1 (90s Grunge Layering):** Wear the white ribbed tank top tucked into the baggy straight-leg jeans, s…
[4] create_fit_card
      in:  item='Oversized Flannel Shirt — Plaid Red/Black', outfit='**Outfit 1 (90s Grunge Layering):** Wear the white r…
      out: Scored this red and black flannel on thredUp for just $22 and I’m so obsessed. Totally leaning into that 90s g…

  Found:    Oversized Flannel Shirt — Plaid Red/Black — $22.0 on thredUp

  Outfit:   **Outfit 1 (90s Grunge Layering):** Wear the white ribbed tank top tucked into the baggy straight-leg jeans, secured with the brown leather belt. Layer the oversized red/black flannel shirt unbuttoned over top, and finish with the black combat boots and black crossbody bag.

**Outfit 2 (Streetwear Contrast):** Pair the wide-leg khaki trousers with the black cropped zip hoodie. Throw the oversized red/black flannel shirt over the hoodie as an unbuttoned outer layer, and ground the look with the chunky white sneakers and black crossbody bag.

  Fit card: Scored this red and black flannel on thredUp for just $22 and I’m so obsessed. Totally leaning into that 90s grunge vibe by throwing it unbuttoned over a white tank and baggy jeans, laced up with some chunky combat boots. It's giving effortless cool without even trying.

2 model calls this session, 483 prompt + 184 output tokens
```

**Empty search**

```
$ python app.py ask 'Red sari under $10' --trace
[1] parse_query
      in:  Red sari under $10
      out: {'description': 'Red sari', 'size': None, 'max_price': 10.0}
[2] search_listings
      in:  {'description': 'Red sari', 'size': None, 'max_price': 10.0}
      out: [] (empty)
      →    branch: no results, stopping before suggest_outfit

  Nothing in the listings matched description 'Red sari', max price $10.
Things you can change and try: try broader words: 'jacket' finds more than 'leather jacket'; raise the price ceiling above the $10.

0 model calls this session

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

```
I first register the search_listing tool to the mcp_server. After it I verify the tool is available or not using below command: 

```
$python mcp_client.py 
Asking mcp_server.py what it offers…

  search_listings
    
Search a fixed catalogue of secondhand clothing listings.

Args:
    description: keywords for the item, e.g. "vintage graphic tee".
    size: size to filter by, case-insensitive, matched as whole words:
          "M" matches "M", "S/M" and "M/L" but not "XL"; "US 9" for shoes,
          "W30" for jeans. Omit to allow any size.
    max_price: highest price in US dollars, inclusive (30 allows a $30.00
               item). Omit for no price limit.

Returns a list of listing dicts, best keyword match first. Each
has: id, title, description, category, style_tags (list of str), size,
condition, price (float, USD), colors (list of str), brand (str or null —
usually null), platform.

Returns an empty list [] when nothing matches. That is a normal result,
not an error.

    - description: string
    - size: string  (optional)
    - max_price: number  (optional)
```
Then I switched the direct tool call to MCP call_tool from mcp_client and verify it works using bellow command. Rewrite worked for me verified that the search_listings tool was called via tool_call.
```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Brat**
Pair the baby tee with your *Baggy straight-leg jeans, dark wash*. Cinch the waist with the *Brown leather belt*, throw the *Black cropped zip hoodie* over your shoulders, and finish with *Chunky white sneakers* and the *Black crossbody bag*.

**Outfit 2: Soft Contrast**
Tuck the baby tee into the *Wide-leg khaki trousers* paired with the *Brown leather belt*. Layer the *Vintage black denim jacket* on top and ground the look with *Black combat boots* and the *Black crossbody bag*.

  Fit card: scored this little butterfly baby tee on depop for just $18 and I'm obsessed. honestly living out my ultimate y2k brat era pairing it with baggy dark-wash jeans and throwing that cropped zip hoodie over my shoulders. such an easy 2000s mood.

2 model calls this session, 486 prompt + 185 output tokens
```


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
Nothing. All five criteria were MET at 5/5 in the before-run, so no criterion had a
miss to fix. I re-ran the same code with `python run_eval.py --label after` as a
second measurement, to see whether the results were stable or the first run got
lucky.

**Which failure it was meant to fix:**
None of the five criteria failed. My diagnoses found two real problems (the
search ranks the wrong tee first, and the fit card invents clothes the user owns),
but no criterion catches either one, so a fix for them wouldn't show up in this
table. That is a weakness in my criteria and scenarios, explained below.


### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item carries through | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card has item, price, vibe | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. empty wardrobe | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |


**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

There was no change, so there was nothing to help. The after-run matches the
before-run: 25 of 25 tries passed, the same items were selected in every try, and
the fit cards varied in wording but always named the item, its price, and the
platform. What the second run does show is that my scenarios are too easy to tell
me anything:

- **One query per criterion.** Each criterion runs one fixed query 5 times.
  `search_listings` is deterministic, so criteria 2 and 3 get the same search result
  on all 5 tries. They can only ever score 0/5 or 5/5, and once the code works they
  will always be 5/5.
- **I chose queries I knew would match.** "denim jacket under $50" and "band tee
  size L" were checked against the data before I wrote them in, so criteria 1, 3
  and 4 never test a phrasing the keyword search might miss — which is the exact
  weakness I named in criterion 1's "why this target".
- **The criteria check that steps ran, not that they were right.** Criterion 1
  passed while the agent picked "Y2K Baby Tee" for "vintage graphic tee" instead of
  "Graphic Tee — 2003 Tour Bootleg Style". Criterion 5 passed while the fit cards
  said "I've been living in it with…" about clothes the user doesn't own.


---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

No criterion is missed, but three things are still wrong:

1. Ranking ties go to file order (`tools.py::search_listings`). The three tee
   listings all score 3 for "vintage graphic tee", so whichever comes first in the
   file wins. Fix: weight title matches higher than description matches. I didn't
   make this change because no criterion was failing, so I had no target to
   measure it against. In hindsight, I should have written a criterion for it.
2. Fit cards invent ownership with an empty wardrobe
   (`tools.py::create_fit_card`). The prompt asks for a first-person post and passes
   general advice as "how it's being styled". Fix: tell the model these are
   suggestions, not pieces the user owns.
3. My scenarios can't detect either problem. Each criterion runs one easy,
   pre checked query. The next step would be adding the tougher scenarios listed
   above and rerunning before changing any code, so a fix would have a failing
   baseline to improve on.


<!-- 
═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
