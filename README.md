# aliceyt.net

Source for the website at **[aliceyt.net](https://aliceyt.net)**.

Editing a file here and committing it automatically rebuilds and publishes the
site.
It usually goes live **within a minute or two**.

---

## After you commit, check the mark

Next to your commit you'll see a small symbol -- it tells you whether your change actually reached the website:

| Symbol | Meaning |
| --- | --- |
| 🟡 Yellow dot | Building. Wait about a minute. |
| ✅ Green check | Published. Your change is live at aliceyt.net. |
| ❌ Red X | **Something's wrong. The site did not update.** |

If you see a red X, click it, then click **Details** to see what went wrong. The message will name the file and the line number.

---

## Editing the text pages

These are the ordinary text pages, and they're safe to edit freely:

| File | What it is |
| --- | --- |
| [`content/biography.md`](content/biography.md) | The About page |
| [`content/_index.md`](content/_index.md) | The home page |
| [`content/select-research-reports.md`](content/select-research-reports.md) | Research reports page |

Don't edit lines between the two `---` markers at the very top of the file.

---

## Editing the lists (publications, teaching, education)

These three live in the `data/` folder and are in a stricter format called JSON:

| File | What it is |
| --- | --- |
| [`data/publications.json`](data/publications.json) | Publications list |
| [`data/teaching.json`](data/teaching.json) | Teaching list |
| [`data/education.json`](data/education.json) | Education list |

JSON is fussy about punctuation.
One missing bracket stops the **entire site** from updating, so it's worth a 20-second check before committing.

### The shape to follow

Each entry is wrapped in `{ }`, and entries are separated by commas:

```json
[
    {
        "role": "Affiliate Faculty",
        "company": "University of Denver"
    },
    {
        "summary": "Social Inequalities (2026)"
    }
]
```

The things that break it, in order of how often they happen:

- A missing `}` at the end of an entry
- A missing `,` between two entries
- A comma after the **last** entry (the last one must not have one)
- A missing `"` at either end of a piece of text

### Check it before you commit

1. Open the file here on GitHub and click the pencil ✏️
2. Select all the text (`Ctrl+A` / `Cmd+A`) and copy it
3. Go to **[jsonlint.com](https://jsonlint.com)**, paste, click **Validate JSON**
4. Green "Valid JSON" means you're safe to commit. Red names the line that's wrong.
5. Fix it back on the GitHub tab, then commit

To save: click the branch icon in the left sidebar, type a short description of your change, then click **Commit**.

---

## If the site stops updating

1. Go to the **Actions** tab at the top of this repository
2. The top entry is the most recent attempt — click it
3. A red X shows which step failed; click it to read the message

Common causes:

- **A typo in one of the `data/*.json` files** — the message names the file and line.
- **`Invalid username or token`** — the deploy token has expired and needs to be replaced.

---

## How it's put together

[Hugo](https://gohugo.io) static site, using the [hugo-resume](https://github.com/eddiewebb/hugo-resume) theme.
On every push to `main`, [`.github/workflows/gh-pages.yml`](.github/workflows/gh-pages.yml) validates the data files, builds the site, and pushes the result to the `gh-pages` branch of `aliceyt24/aliceyt24.github.io`, which serves `aliceyt.net`.
