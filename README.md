# PullRates.gg — Pokémon TCG Pull Rate Visualizer

A static website showing pull rates and market prices for Pokémon TCG booster packs.
No backend required — open `index.html` in any browser, or host on GitHub Pages for free.

---

## 🚀 Deploy to GitHub Pages (Step by Step)

### 1. Create a GitHub account
Go to https://github.com and sign up if you don't have an account.

### 2. Create a new repository
- Click the **+** button in the top-right → **New repository**
- Name it `pokepullrates` (or anything you like)
- Set it to **Public**
- Do NOT initialize with README
- Click **Create repository**

### 3. Upload your files
- On the new repo page, click **uploading an existing file**
- Drag and drop ALL files from this folder:
  - `index.html`
  - `set.html`
  - `data.js`
- Click **Commit changes**

### 4. Enable GitHub Pages
- Go to your repo → **Settings** → **Pages** (left sidebar)
- Under **Source**, select **Deploy from a branch**
- Branch: `main`, folder: `/ (root)`
- Click **Save**

### 5. Your site is live!
After 1–2 minutes, your site will be live at:
`https://YOUR-USERNAME.github.io/pokepullrates/`

---

## 📁 File Structure

```
pokepullrates/
├── index.html   Homepage — set browser + card search
├── set.html     Individual set page — scatter chart + EV breakdown
├── data.js      All set data, pull rates, and prices
└── README.md    This file
```

---

## ➕ Adding a New Set

All data lives in `data.js`. To add a new set:

1. Open `data.js`
2. Copy an existing set block inside the `SETS` array
3. Fill in:
   - `id` — a short unique identifier (e.g. `sv10`)
   - `name` — full set name
   - `released` — release date `YYYY-MM-DD`
   - `packEV` — expected value per pack in USD
   - `pricesUpdated` — when you last updated prices
   - `accentColor` — hex color for the set card UI
   - `topCard` — the set's most valuable card + price
   - `rarities[]` — one entry per rarity tier with:
     - `key` — rarity code (HR, SIR, UR, IR, ACE, DR, R, U, C, etc.)
     - `pullPct` — specific card pull chance as a percentage
     - `avgPrice` — average market price for that rarity in USD
     - `ev` — expected value contribution per pack for that rarity
     - `count` — number of cards in that rarity
   - `notable[]` — 3–5 named chase cards with actual prices
4. Save and push to GitHub — the new set appears automatically

### Finding Pull Rate Data
- **ThePriceDex**: https://www.thepricedex.com/sets (best source — has pull rates + EV)
- **TCGPlayer**: https://www.tcgplayer.com (primary price source)
- **CardChill**: https://cardchill.com (community pull rate research)

### Rarity Key Reference
| Key | Label |
|-----|-------|
| MHR | Mega Hyper Rare |
| HR  | Hyper Rare |
| SIR | Special Illus. Rare |
| MAR | Mega Attack Rare |
| UR  | Ultra Rare |
| IR  | Illus. Rare |
| ACE | ACE SPEC Rare |
| DR  | Double Rare |
| R   | Rare Holo |
| U   | Uncommon |
| C   | Common |

---

## 🔄 Updating Prices

Prices change over time. To update:
1. Check current prices on TCGPlayer NM ungraded
2. Update `avgPrice` in each rarity's entry in `data.js`
3. Update `pricesUpdated` to today's date
4. Update `notable[].price` for named chase cards
5. Commit and push — the update tag on each set page shows the date

---

## 🌐 Custom Domain (Optional)

To use a custom domain like `pullrates.gg`:
1. Buy a domain from Namecheap, Cloudflare, etc.
2. In GitHub Pages settings, enter your domain under **Custom domain**
3. Add a CNAME DNS record pointing to `YOUR-USERNAME.github.io`
4. GitHub will handle HTTPS automatically

---

*Data sourced from ThePriceDex, TCGPlayer, and community pack opening research.
Not affiliated with Nintendo, Game Freak, or Creatures Inc.*
