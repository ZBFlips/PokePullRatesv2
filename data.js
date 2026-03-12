// ============================================================
//  PullRates.gg — Set Data
//  Source: ThePriceDex / TCGPlayer / community pull data
//  Prices: TCGPlayer NM ungraded market average
//  Resale: TCGPlayer / StockX / eBay single-pack market avg
// ============================================================

const RARITY_COLORS = {
  // ── Scarlet & Violet era ────────────────────────────────
  MHR: '#dc2626', HR:  '#f59e0b', SIR: '#ec4899', MAR: '#f97316',
  UR:  '#8b5cf6', IR:  '#3b82f6', ACE: '#14b8a6', DR:  '#22c55e',
  R:   '#84cc16', U:   '#94a3b8', C:   '#64748b',
  // ── Paldean Fates shinies ───────────────────────────────
  SHR: '#67e8f9', SHU: '#c084fc',
  // ── Sword & Shield era (Trainer Gallery / regular) ──────
  TGS: '#dc2626', RBOW:'#f0abfc', TGU: '#ec4899',
  TGVM:'#f59e0b', TGV: '#8b5cf6', TGH: '#3b82f6',
  GGS: '#dc2626', GGU: '#a78bfa', GGVS:'#67e8f9',
  SR:  '#f97316', VSTAR:'#22c55e',VMAX:'#84cc16',
  V:   '#06b6d4', RAD: '#2dd4bf', RH:  '#6b7280',
};

const RARITY_LABELS = {
  // ── Scarlet & Violet era ────────────────────────────────
  MHR: 'Mega Hyper Rare',       HR:   'Hyper Rare',
  SIR: 'Special Illus. Rare',   MAR:  'Mega Attack Rare',
  UR:  'Ultra Rare',             IR:   'Illus. Rare',
  ACE: 'ACE SPEC Rare',          DR:   'Double Rare',
  R:   'Rare Holo',              U:    'Uncommon',
  C:   'Common',
  // ── Paldean Fates shinies ───────────────────────────────
  SHR: 'Shiny Rare',             SHU:  'Shiny Ultra Rare',
  // ── Sword & Shield era ──────────────────────────────────
  TGS: 'TG Secret Rare',         RBOW: 'Rainbow Rare',
  TGU: 'TG Ultra Rare',          TGVM: 'TG Rare Holo VMAX',
  TGV: 'TG Rare Holo V',         TGH:  'TG Rare Holo',
  GGS: 'GG Secret Rare',         GGU:  'GG Ultra Rare',
  GGVS:'GG Rare Holo VSTAR',     SR:   'Secret Rare',
  VSTAR:'Rare Holo VSTAR',       VMAX: 'Rare Holo VMAX',
  V:   'Rare Holo V',             RAD:  'Radiant Rare',
  RH:  'Rare Holo',
};

const SETS = [

  {
    id: 'me2pt5',
    name: 'Ascended Heroes',
    series: 'Mega Evolution',
    released: '2026-01-30',
    cardCount: 295,
    packEV: 7.21,
    packResalePrice: 9.50,
    pricesUpdated: 'March 9, 2026',
    accentColor: '#7c3aed',
    topCard: { name: 'Mega Gengar ex SIR', price: 993 },
    rarities: [
      { key:'MHR', pullPct:0.0500,  avgPrice:417,   ev:0.42, count:2  },
      { key:'SIR', pullPct:0.0499,  avgPrice:189,   ev:2.08, count:22 },
      { key:'MAR', pullPct:0.4329,  avgPrice:22,    ev:0.68, count:7  },
      { key:'UR',  pullPct:0.4202,  avgPrice:5.17,  ev:0.30, count:14 },
      { key:'IR',  pullPct:0.3788,  avgPrice:11.86, ev:1.48, count:33 },
      { key:'DR',  pullPct:0.5128,  avgPrice:1.91,  ev:0.38, count:39 },
      { key:'R',   pullPct:2.841,   avgPrice:0.17,  ev:0.12, count:25 },
      { key:'U',   pullPct:4.348,   avgPrice:0.14,  ev:0.43, count:69 },
      { key:'C',   pullPct:4.762,   avgPrice:0.14,  ev:0.54, count:84 },
    ],
    notable: [
      { name:'Mega Gengar ex',          rarity:'MHR', price:993, pullPct:0.0500 },
      { name:'Mega Charizard Y ex',     rarity:'MHR', price:666, pullPct:0.0500 },
      { name:'Mega Dragonite ex',       rarity:'SIR', price:611, pullPct:0.0499 },
      { name:'Pikachu ex',              rarity:'SIR', price:505, pullPct:0.0499 },
      { name:"Team Rocket's Mewtwo ex", rarity:'SIR', price:250, pullPct:0.0499 },
      { name:'Mega Dragonite ex',       rarity:'MAR', price:60,  pullPct:0.4329 },
      { name:'Canari ex',               rarity:'UR',  price:30,  pullPct:0.4202 },
      { name:'Psyduck',                 rarity:'IR',  price:100, pullPct:0.3788 },
    ],
  },

  {
    id: 'sv9',
    name: 'Journey Together',
    series: 'Scarlet & Violet',
    released: '2025-03-28',
    cardCount: 190,
    packEV: 3.07,
    packResalePrice: 6.75,
    pricesUpdated: 'March 8, 2026',
    accentColor: '#22d3ee',
    topCard: { name: "Lillie's Clefairy ex SIR", price: 122 },
    rarities: [
      { key:'HR',  pullPct:0.2433, avgPrice:10.33, ev:0.08, count:3  },
      { key:'SIR', pullPct:0.1934, avgPrice:54.16, ev:0.63, count:6  },
      { key:'UR',  pullPct:0.5952, avgPrice:2.22,  ev:0.15, count:11 },
      { key:'IR',  pullPct:0.7752, avgPrice:6.61,  ev:0.56, count:11 },
      { key:'DR',  pullPct:1.267,  avgPrice:0.84,  ev:0.17, count:16 },
      { key:'R',   pullPct:4.566,  avgPrice:0.16,  ev:0.12, count:16 },
      { key:'U',   pullPct:7.143,  avgPrice:0.12,  ev:0.35, count:42 },
      { key:'C',   pullPct:4.695,  avgPrice:0.13,  ev:0.53, count:85 },
    ],
    notable: [
      { name:"Lillie's Clefairy ex", rarity:'SIR', price:122, pullPct:0.1934 },
      { name:'Salamence ex',         rarity:'SIR', price:54,  pullPct:0.1934 },
      { name:"N's Zoroark ex",       rarity:'SIR', price:51,  pullPct:0.1934 },
    ],
  },

  {
    id: 'sv8pt5',
    name: 'Prismatic Evolutions',
    series: 'Scarlet & Violet',
    released: '2025-01-17',
    cardCount: 180,
    packEV: 4.56,
    packResalePrice: 24.00,
    pricesUpdated: 'March 9, 2026',
    accentColor: '#a78bfa',
    topCard: { name: 'Umbreon ex SIR', price: 1121 },
    rarities: [
      { key:'HR',  pullPct:0.1120, avgPrice:14.87,  ev:0.08, count:5  },
      { key:'SIR', pullPct:0.0694, avgPrice:113.52, ev:2.52, count:32 },
      { key:'UR',  pullPct:0.6211, avgPrice:0.72,   ev:0.05, count:12 },
      { key:'ACE', pullPct:0.7813, avgPrice:0.48,   ev:0.02, count:6  },
      { key:'DR',  pullPct:0.6614, avgPrice:1.72,   ev:0.28, count:25 },
      { key:'R',   pullPct:3.623,  avgPrice:0.19,   ev:0.14, count:21 },
      { key:'U',   pullPct:9.091,  avgPrice:0.11,   ev:0.32, count:33 },
      { key:'C',   pullPct:8.696,  avgPrice:0.09,   ev:0.38, count:46 },
    ],
    notable: [
      { name:'Umbreon ex', rarity:'SIR', price:1121, pullPct:0.0694 },
      { name:'Sylveon ex', rarity:'SIR', price:301,  pullPct:0.0694 },
      { name:'Leafeon ex', rarity:'SIR', price:245,  pullPct:0.0694 },
    ],
  },

  {
    id: 'sv8',
    name: 'Surging Sparks',
    series: 'Scarlet & Violet',
    released: '2024-11-08',
    cardCount: 252,
    packEV: 3.08,
    packResalePrice: 7.00,
    pricesUpdated: 'March 9, 2026',
    accentColor: '#f59e0b',
    topCard: { name: 'Pikachu ex SIR', price: 256 },
    rarities: [
      { key:'HR',  pullPct:0.0883, avgPrice:17.52, ev:0.09, count:6  },
      { key:'SIR', pullPct:0.1046, avgPrice:62.82, ev:0.72, count:11 },
      { key:'UR',  pullPct:0.3210, avgPrice:3.15,  ev:0.21, count:21 },
      { key:'IR',  pullPct:0.3334, avgPrice:6.32,  ev:0.48, count:23 },
      { key:'ACE', pullPct:0.6289, avgPrice:1.27,  ev:0.06, count:8  },
      { key:'DR',  pullPct:0.9416, avgPrice:1.17,  ev:0.20, count:18 },
      { key:'R',   pullPct:4.762,  avgPrice:0.14,  ev:0.11, count:16 },
      { key:'U',   pullPct:4.918,  avgPrice:0.12,  ev:0.36, count:61 },
      { key:'C',   pullPct:4.545,  avgPrice:0.11,  ev:0.43, count:88 },
    ],
    notable: [
      { name:'Pikachu ex', rarity:'SIR', price:256, pullPct:0.1046 },
      { name:'Latias ex',  rarity:'SIR', price:170, pullPct:0.1046 },
      { name:'Milotic ex', rarity:'SIR', price:95,  pullPct:0.1046 },
    ],
  },

  {
    id: 'sv7',
    name: 'Stellar Crown',
    series: 'Scarlet & Violet',
    released: '2024-09-13',
    cardCount: 175,
    packEV: 3.19,
    packResalePrice: 5.50,
    pricesUpdated: 'March 9, 2026',
    accentColor: '#3b82f6',
    topCard: { name: 'Squirtle IR', price: 90 },
    rarities: [
      { key:'HR',  pullPct:0.2433, avgPrice:8.73,  ev:0.06, count:3  },
      { key:'SIR', pullPct:0.1848, avgPrice:22.60, ev:0.25, count:6  },
      { key:'UR',  pullPct:0.6135, avgPrice:2.80,  ev:0.19, count:11 },
      { key:'IR',  pullPct:0.5988, avgPrice:17.73, ev:1.38, count:13 },
      { key:'ACE', pullPct:1.647,  avgPrice:0.38,  ev:0.02, count:3  },
      { key:'DR',  pullPct:1.208,  avgPrice:0.88,  ev:0.15, count:14 },
      { key:'R',   pullPct:5.102,  avgPrice:0.13,  ev:0.10, count:15 },
      { key:'U',   pullPct:7.692,  avgPrice:0.10,  ev:0.29, count:39 },
      { key:'C',   pullPct:5.618,  avgPrice:0.10,  ev:0.40, count:71 },
    ],
    notable: [
      { name:'Squirtle',    rarity:'IR',  price:90, pullPct:0.5988 },
      { name:'Bulbasaur',   rarity:'IR',  price:78, pullPct:0.5988 },
      { name:'Dachsbun ex', rarity:'SIR', price:37, pullPct:0.1848 },
    ],
  },

  {
    id: 'sv6pt5',
    name: 'Shrouded Fable',
    series: 'Scarlet & Violet',
    released: '2024-08-02',
    cardCount: 99,
    packEV: 4.09,
    packResalePrice: 7.50,
    pricesUpdated: 'February 26, 2026',
    accentColor: '#10b981',
    topCard: { name: 'Fezandipiti ex SIR', price: 46 },
    rarities: [
      { key:'HR',  pullPct:0.1558, avgPrice:28.01, ev:0.22, count:5  },
      { key:'SIR', pullPct:0.2292, avgPrice:28.07, ev:0.32, count:5  },
      { key:'UR',  pullPct:0.6993, avgPrice:4.77,  ev:0.33, count:10 },
      { key:'IR',  pullPct:0.5136, avgPrice:21.81, ev:1.68, count:15 },
      { key:'ACE', pullPct:1.667,  avgPrice:0.59,  ev:0.03, count:3  },
      { key:'DR',  pullPct:2.778,  avgPrice:1.95,  ev:0.32, count:6  },
      { key:'R',   pullPct:10.87,  avgPrice:0.14,  ev:0.11, count:7  },
      { key:'U',   pullPct:14.93,  avgPrice:0.12,  ev:0.36, count:20 },
      { key:'C',   pullPct:14.29,  avgPrice:0.09,  ev:0.36, count:28 },
    ],
    notable: [
      { name:'Fezandipiti ex',    rarity:'SIR', price:46, pullPct:0.2292 },
      { name:'Duskull',           rarity:'IR',  price:45, pullPct:0.5136 },
      { name:'Basic Dark Energy', rarity:'HR',  price:44, pullPct:0.1558 },
    ],
  },

  {
    id: 'sv6',
    name: 'Twilight Masquerade',
    series: 'Scarlet & Violet',
    released: '2024-05-24',
    cardCount: 226,
    packEV: 3.01,
    packResalePrice: 5.75,
    pricesUpdated: 'February 7, 2026',
    accentColor: '#ec4899',
    topCard: { name: 'Greninja ex SIR', price: 280 },
    rarities: [
      { key:'HR',  pullPct:0.1134, avgPrice:7.16,  ev:0.05, count:6  },
      { key:'SIR', pullPct:0.1064, avgPrice:53.86, ev:0.63, count:11 },
      { key:'UR',  pullPct:0.3145, avgPrice:3.04,  ev:0.20, count:21 },
      { key:'IR',  pullPct:0.3679, avgPrice:10.19, ev:0.79, count:21 },
      { key:'ACE', pullPct:0.8403, avgPrice:2.64,  ev:0.13, count:6  },
      { key:'DR',  pullPct:1.209,  avgPrice:0.89,  ev:0.15, count:14 },
      { key:'R',   pullPct:4.785,  avgPrice:0.15,  ev:0.11, count:16 },
      { key:'U',   pullPct:5.464,  avgPrice:0.09,  ev:0.26, count:55 },
      { key:'C',   pullPct:5.263,  avgPrice:0.09,  ev:0.34, count:76 },
    ],
    notable: [
      { name:'Greninja ex', rarity:'SIR', price:280, pullPct:0.1064 },
      { name:'Perrin',      rarity:'SIR', price:96,  pullPct:0.1064 },
      { name:'Eevee',       rarity:'IR',  price:59,  pullPct:0.3679 },
    ],
  },

  {
    id: 'sv4',
    name: 'Paradox Rift',
    series: 'Scarlet & Violet',
    released: '2023-11-03',
    cardCount: 266,
    packEV: 2.90,
    packResalePrice: 5.25,
    pricesUpdated: 'February 11, 2026',
    accentColor: '#f97316',
    topCard: { name: 'Groudon IR', price: 73 },
    rarities: [
      { key:'HR',  pullPct:0.1742, avgPrice:4.99,  ev:0.06, count:7  },
      { key:'SIR', pullPct:0.1406, avgPrice:15.91, ev:0.34, count:15 },
      { key:'UR',  pullPct:0.2370, avgPrice:2.70,  ev:0.18, count:28 },
      { key:'IR',  pullPct:0.2263, avgPrice:12.58, ev:0.97, count:34 },
      { key:'DR',  pullPct:0.7752, avgPrice:0.92,  ev:0.14, count:20 },
      { key:'R',   pullPct:2.882,  avgPrice:0.15,  ev:0.12, count:27 },
      { key:'U',   pullPct:5.556,  avgPrice:0.12,  ev:0.37, count:54 },
      { key:'C',   pullPct:4.926,  avgPrice:0.09,  ev:0.36, count:81 },
    ],
    notable: [
      { name:'Groudon',    rarity:'IR',  price:73, pullPct:0.2263 },
      { name:'Altaria ex', rarity:'SIR', price:40, pullPct:0.1406 },
      { name:'Minun',      rarity:'IR',  price:33, pullPct:0.2263 },
    ],
  },

  {
    id: 'sv3pt5',
    name: 'Pokémon 151',
    series: 'Scarlet & Violet',
    released: '2023-09-22',
    cardCount: 207,
    packEV: 4.50,
    packResalePrice: 24.17,
    pricesUpdated: 'December 2025',
    accentColor: '#84cc16',
    topCard: { name: 'Charizard ex SIR', price: 239 },
    rarities: [
      { key:'HR',  pullPct:0.6173, avgPrice:13.00, ev:0.24, count:3  },
      { key:'SIR', pullPct:0.4464, avgPrice:72.00, ev:2.13, count:7  },
      { key:'UR',  pullPct:0.4132, avgPrice:3.50,  ev:0.22, count:16 },
      { key:'IR',  pullPct:0.4739, avgPrice:9.50,  ev:0.72, count:16 },
      { key:'DR',  pullPct:1.142,  avgPrice:1.20,  ev:0.18, count:12 },
      { key:'R',   pullPct:3.077,  avgPrice:0.12,  ev:0.09, count:25 },
      { key:'U',   pullPct:4.839,  avgPrice:0.10,  ev:0.30, count:62 },
      { key:'C',   pullPct:6.061,  avgPrice:0.09,  ev:0.37, count:66 },
    ],
    notable: [
      { name:'Charizard ex', rarity:'SIR', price:239, pullPct:0.4464 },
      { name:'Venusaur ex',  rarity:'SIR', price:78,  pullPct:0.4464 },
      { name:'Blastoise ex', rarity:'SIR', price:73,  pullPct:0.4464 },
    ],
  },

  {
    id: 'sv3',
    name: 'Obsidian Flames',
    series: 'Scarlet & Violet',
    released: '2023-08-11',
    cardCount: 230,
    packEV: 2.98,
    packResalePrice: 5.00,
    pricesUpdated: 'February 9, 2026',
    accentColor: '#ef4444',
    topCard: { name: 'Charizard ex SIR', price: 73 },
    rarities: [
      { key:'HR',  pullPct:0.6410, avgPrice:13.92, ev:0.27, count:3  },
      { key:'SIR', pullPct:0.5215, avgPrice:16.68, ev:0.52, count:6  },
      { key:'UR',  pullPct:0.5525, avgPrice:2.98,  ev:0.20, count:12 },
      { key:'IR',  pullPct:0.6329, avgPrice:8.98,  ev:0.68, count:12 },
      { key:'DR',  pullPct:0.6494, avgPrice:1.25,  ev:0.17, count:21 },
      { key:'R',   pullPct:8.000,  avgPrice:0.09,  ev:0.07, count:10 },
      { key:'U',   pullPct:4.054,  avgPrice:0.10,  ev:0.30, count:74 },
      { key:'C',   pullPct:4.348,  avgPrice:0.09,  ev:0.37, count:92 },
    ],
    notable: [
      { name:'Charizard ex (SIR)',  rarity:'SIR', price:73, pullPct:0.5215 },
      { name:'Charizard ex (Gold)', rarity:'HR',  price:35, pullPct:0.6410 },
      { name:'Ninetales',           rarity:'IR',  price:24, pullPct:0.6329 },
    ],
  },
  
  {
    id: 'swsh10', name: 'Astral Radiance', series: 'Sword & Shield',
    released: 'May 27, 2022', cardCount: 246, packEV: 0, packResalePrice: 4.15,
    pricesUpdated: 'Pending...', accentColor: '#60a5fa',
    topCard: { name: 'Machamp V (Alternate Full Art)', price: 0 },
    rarities: [
      { key: 'SR', pullPct: 1.2, avgPrice: 0, ev: 0, count: 15 },
      { key: 'RBOW', pullPct: 1.5, avgPrice: 0, ev: 0, count: 18 },
      { key: 'UR', pullPct: 4.0, avgPrice: 0, ev: 0, count: 24 },
      { key: 'VMAX', pullPct: 5.5, avgPrice: 0, ev: 0, count: 12 },
      { key: 'V', pullPct: 12.0, avgPrice: 0, ev: 0, count: 21 },
      { key: 'RH', pullPct: 18.0, avgPrice: 0, ev: 0, count: 20 },
      { key: 'R', pullPct: 58.0, avgPrice: 0, ev: 0, count: 20 }
    ],
    notable: [
      { name: 'Machamp V (Alternate Full Art)', rarity: 'UR', price: 0, pullPct: 0.15 }
    ]
  },
  
  {
    id: 'swsh9', name: 'Brilliant Stars', series: 'Sword & Shield',
    released: 'February 25, 2022', cardCount: 216, packEV: 0, packResalePrice: 4.50,
    pricesUpdated: 'Pending...', accentColor: '#facc15',
    topCard: { name: 'Charizard V (Alternate Full Art)', price: 0 },
    rarities: [
      { key: 'SR', pullPct: 1.1, avgPrice: 0, ev: 0, count: 14 },
      { key: 'RBOW', pullPct: 1.4, avgPrice: 0, ev: 0, count: 16 },
      { key: 'UR', pullPct: 3.8, avgPrice: 0, ev: 0, count: 22 },
      { key: 'VMAX', pullPct: 5.0, avgPrice: 0, ev: 0, count: 14 },
      { key: 'V', pullPct: 11.5, avgPrice: 0, ev: 0, count: 20 },
      { key: 'RH', pullPct: 18.0, avgPrice: 0, ev: 0, count: 20 },
      { key: 'R', pullPct: 58.0, avgPrice: 0, ev: 0, count: 20 }
    ],
    notable: [
      { name: 'Charizard V (Alternate Full Art)', rarity: 'UR', price: 0, pullPct: 0.12 }
    ]
  },
  
  {
    id: 'swsh8', name: 'Fusion Strike', series: 'Sword & Shield',
    released: 'November 12, 2021', cardCount: 284, packEV: 0, packResalePrice: 4.25,
    pricesUpdated: 'Pending...', accentColor: '#d946ef',
    topCard: { name: 'Gengar VMAX (Alternate Art Secret)', price: 0 },
    rarities: [
      { key: 'SR', pullPct: 1.0, avgPrice: 0, ev: 0, count: 18 },
      { key: 'RBOW', pullPct: 1.2, avgPrice: 0, ev: 0, count: 20 },
      { key: 'UR', pullPct: 3.5, avgPrice: 0, ev: 0, count: 28 },
      { key: 'VMAX', pullPct: 4.5, avgPrice: 0, ev: 0, count: 16 },
      { key: 'V', pullPct: 10.0, avgPrice: 0, ev: 0, count: 24 },
      { key: 'RH', pullPct: 18.0, avgPrice: 0, ev: 0, count: 20 },
      { key: 'R', pullPct: 58.0, avgPrice: 0, ev: 0, count: 20 }
    ],
    notable: [
      { name: 'Gengar VMAX (Alternate Art Secret)', rarity: 'UR', price: 0, pullPct: 0.10 }
    ]
  }


  // ── BATCH 2 ─────────────────────────────────────────────────

  { id:'sv4pt5', name:'Paldean Fates', series:'Scarlet & Violet', released:'2024-01-26', cardCount:245, packEV:4.85, packResalePrice:14.00, pricesUpdated:'March 2026', accentColor:'#67e8f9', topCard:{name:'Mew ex SIR',price:537}, rarities:[{key:'SIR',pullPct:1.724,avgPrice:121,ev:2.09,count:8},{key:'SHR',pullPct:25.65,avgPrice:2.50,ev:0.64,count:121},{key:'SHU',pullPct:7.08,avgPrice:8.00,ev:0.57,count:11},{key:'HR',pullPct:1.613,avgPrice:13.0,ev:0.21,count:1},{key:'IR',pullPct:7.143,avgPrice:5.00,ev:0.36,count:22},{key:'UR',pullPct:6.667,avgPrice:2.50,ev:0.17,count:18},{key:'DR',pullPct:12.50,avgPrice:0.90,ev:0.11,count:17},{key:'R',pullPct:76.92,avgPrice:0.13,ev:0.10,count:25},{key:'U',pullPct:300,avgPrice:0.10,ev:0.30,count:70},{key:'C',pullPct:400,avgPrice:0.09,ev:0.36,count:69}], notable:[{name:'Mew ex',rarity:'SIR',price:537,pullPct:1.724},{name:'Charizard ex',rarity:'SIR',price:217,pullPct:1.724},{name:'Gardevoir ex',rarity:'SIR',price:117,pullPct:1.724},{name:'Pikachu',rarity:'SHR',price:38,pullPct:25.65},{name:'Iono',rarity:'SIR',price:28,pullPct:1.724},{name:'Mew ex',rarity:'SHU',price:26,pullPct:7.08},{name:'Snorlax',rarity:'SHR',price:24,pullPct:25.65}]},

  { id:'sv5', name:'Temporal Forces', series:'Scarlet & Violet', released:'2024-03-22', cardCount:218, packEV:2.86, packResalePrice:5.50, pricesUpdated:'December 16, 2025', accentColor:'#06b6d4', topCard:{name:'Raging Bolt ex SIR',price:63}, rarities:[{key:'HR',pullPct:0.720,avgPrice:9.18,ev:0.07,count:6},{key:'SIR',pullPct:1.170,avgPrice:30.07,ev:0.35,count:10},{key:'UR',pullPct:6.667,avgPrice:4.01,ev:0.27,count:18},{key:'IR',pullPct:7.692,avgPrice:12.97,ev:1.00,count:22},{key:'ACE',pullPct:5.000,avgPrice:3.97,ev:0.20,count:7},{key:'DR',pullPct:16.95,avgPrice:0.95,ev:0.16,count:15},{key:'R',pullPct:76.92,avgPrice:0.11,ev:0.08,count:14},{key:'U',pullPct:300,avgPrice:0.07,ev:0.21,count:55},{key:'C',pullPct:400,avgPrice:0.06,ev:0.25,count:71}], notable:[{name:'Raging Bolt ex',rarity:'SIR',price:63,pullPct:1.170},{name:'Gastly',rarity:'IR',price:53,pullPct:7.692},{name:'Iron Crown ex',rarity:'SIR',price:45,pullPct:1.170},{name:"Morty's Conviction",rarity:'SIR',price:41,pullPct:1.170},{name:'Milotic ex',rarity:'UR',price:28,pullPct:6.667}]},

  { id:'sv2', name:'Paldea Evolved', series:'Scarlet & Violet', released:'2023-06-09', cardCount:279, packEV:3.89, packResalePrice:5.25, pricesUpdated:'January 25, 2026', accentColor:'#22d3ee', topCard:{name:'Magikarp IR',price:273}, rarities:[{key:'HR',pullPct:1.761,avgPrice:5.57,ev:0.10,count:9},{key:'SIR',pullPct:3.175,avgPrice:17.91,ev:0.57,count:15},{key:'UR',pullPct:6.623,avgPrice:2.97,ev:0.20,count:26},{key:'IR',pullPct:7.692,avgPrice:22.91,ev:1.76,count:36},{key:'DR',pullPct:13.70,avgPrice:0.86,ev:0.12,count:17},{key:'R',pullPct:76.92,avgPrice:0.14,ev:0.11,count:25},{key:'U',pullPct:300,avgPrice:0.13,ev:0.38,count:70},{key:'C',pullPct:400,avgPrice:0.08,ev:0.31,count:81}], notable:[{name:'Magikarp',rarity:'IR',price:273,pullPct:7.692},{name:'Tyranitar',rarity:'IR',price:59,pullPct:7.692},{name:'Raichu',rarity:'IR',price:58,pullPct:7.692},{name:'Espeon',rarity:'SIR',price:42,pullPct:3.175},{name:'Gardevoir ex',rarity:'UR',price:28,pullPct:6.623}]},

  { id:'sv1', name:'Scarlet & Violet', series:'Scarlet & Violet', released:'2023-03-31', cardCount:258, packEV:2.65, packResalePrice:4.75, pricesUpdated:'March 2026', accentColor:'#f43f5e', topCard:{name:'Miraidon ex SIR',price:85}, rarities:[{key:'HR',pullPct:0.990,avgPrice:6.50,ev:0.06,count:10},{key:'SIR',pullPct:1.160,avgPrice:24.00,ev:0.28,count:10},{key:'UR',pullPct:3.788,avgPrice:3.20,ev:0.21,count:22},{key:'IR',pullPct:5.464,avgPrice:7.80,ev:0.57,count:27},{key:'DR',pullPct:10.99,avgPrice:0.95,ev:0.21,count:18},{key:'R',pullPct:71.43,avgPrice:0.14,ev:0.12,count:21},{key:'U',pullPct:300,avgPrice:0.11,ev:0.34,count:64},{key:'C',pullPct:400,avgPrice:0.08,ev:0.31,count:86}], notable:[{name:'Miraidon ex',rarity:'SIR',price:85,pullPct:1.160},{name:'Koraidon ex',rarity:'SIR',price:65,pullPct:1.160},{name:'Arcanine ex',rarity:'SIR',price:42,pullPct:1.160},{name:'Meowscarada ex',rarity:'UR',price:22,pullPct:3.788},{name:'Garganacl',rarity:'IR',price:18,pullPct:5.464}]},

  { id:'swsh12pt5', name:'Crown Zenith', series:'Sword & Shield', released:'2023-01-20', cardCount:230, packEV:6.70, packResalePrice:22.00, pricesUpdated:'March 2026', accentColor:'#fbbf24', topCard:{name:'Giratina VSTAR GG Secret',price:201}, rarities:[{key:'GGS',pullPct:0.800,avgPrice:118.45,ev:0.95,count:4},{key:'GGU',pullPct:3.745,avgPrice:5.65,ev:0.21,count:10},{key:'GGVS',pullPct:3.745,avgPrice:43.30,ev:1.62,count:10},{key:'TGVM',pullPct:1.124,avgPrice:22.68,ev:0.26,count:3},{key:'TGV',pullPct:3.378,avgPrice:19.89,ev:0.67,count:9},{key:'TGH',pullPct:22.22,avgPrice:5.79,ev:1.30,count:34},{key:'SR',pullPct:0.750,avgPrice:31.49,ev:0.24,count:1},{key:'UR',pullPct:2.849,avgPrice:4.05,ev:0.12,count:13},{key:'VSTAR',pullPct:3.257,avgPrice:2.26,ev:0.07,count:8},{key:'V',pullPct:12.35,avgPrice:1.29,ev:0.16,count:17},{key:'RAD',pullPct:4.545,avgPrice:2.95,ev:0.13,count:3},{key:'RH',pullPct:17.86,avgPrice:0.34,ev:0.06,count:20},{key:'R',pullPct:62.50,avgPrice:0.13,ev:0.08,count:22},{key:'U',pullPct:300,avgPrice:0.07,ev:0.20,count:29},{key:'C',pullPct:500,avgPrice:0.08,ev:0.38,count:42}], notable:[{name:'Giratina VSTAR',rarity:'GGS',price:201,pullPct:0.800},{name:'Arceus VSTAR',rarity:'GGS',price:117,pullPct:0.800},{name:'Mewtwo VSTAR',rarity:'GGVS',price:173,pullPct:3.745},{name:'Pikachu VMAX',rarity:'GGVS',price:58,pullPct:3.745},{name:'Deoxys VMAX',rarity:'TGVM',price:48,pullPct:1.124}]},

  { id:'swsh11', name:'Lost Origin', series:'Sword & Shield', released:'2022-09-09', cardCount:247, packEV:3.86, packResalePrice:15.00, pricesUpdated:'March 2026', accentColor:'#9333ea', topCard:{name:'Giratina V Ultra Rare',price:577}, rarities:[{key:'TGS',pullPct:0.916,avgPrice:16.87,ev:0.15,count:2},{key:'TGU',pullPct:1.039,avgPrice:4.05,ev:0.04,count:6},{key:'TGVM',pullPct:0.693,avgPrice:24.19,ev:0.17,count:4},{key:'TGV',pullPct:1.212,avgPrice:13.51,ev:0.16,count:7},{key:'TGH',pullPct:8.547,avgPrice:8.78,ev:0.75,count:11},{key:'SR',pullPct:0.760,avgPrice:4.45,ev:0.03,count:6},{key:'RBOW',pullPct:1.280,avgPrice:6.45,ev:0.08,count:15},{key:'UR',pullPct:3.906,avgPrice:32.92,ev:1.28,count:25},{key:'VSTAR',pullPct:3.788,avgPrice:1.18,ev:0.04,count:6},{key:'V',pullPct:11.63,avgPrice:0.70,ev:0.08,count:12},{key:'RAD',pullPct:5.000,avgPrice:0.64,ev:0.03,count:3},{key:'RH',pullPct:17.86,avgPrice:0.37,ev:0.07,count:22},{key:'R',pullPct:58.82,avgPrice:0.14,ev:0.08,count:28},{key:'U',pullPct:300,avgPrice:0.09,ev:0.27,count:50},{key:'C',pullPct:500,avgPrice:0.07,ev:0.35,count:49}], notable:[{name:'Giratina V',rarity:'UR',price:577,pullPct:3.906},{name:'Aerodactyl V',rarity:'UR',price:148,pullPct:3.906},{name:'Pikachu VMAX',rarity:'TGVM',price:73,pullPct:0.693},{name:'Giratina VSTAR',rarity:'VSTAR',price:32,pullPct:3.788},{name:'Comfey',rarity:'RH',price:24,pullPct:17.86}]},

  { id:'swsh12', name:'Silver Tempest', series:'Sword & Shield', released:'2022-11-11', cardCount:245, packEV:2.97, packResalePrice:8.00, pricesUpdated:'March 2026', accentColor:'#94a3b8', topCard:{name:'Lugia V Ultra Rare',price:354}, rarities:[{key:'TGS',pullPct:0.916,avgPrice:10.89,ev:0.10,count:2},{key:'TGU',pullPct:1.157,avgPrice:4.63,ev:0.05,count:6},{key:'TGVM',pullPct:0.771,avgPrice:35.81,ev:0.28,count:4},{key:'TGV',pullPct:1.350,avgPrice:11.91,ev:0.16,count:7},{key:'TGH',pullPct:8.333,avgPrice:3.08,ev:0.26,count:11},{key:'SR',pullPct:0.940,avgPrice:6.03,ev:0.06,count:6},{key:'RBOW',pullPct:1.259,avgPrice:9.26,ev:0.12,count:14},{key:'UR',pullPct:3.704,avgPrice:18.79,ev:0.70,count:26},{key:'VSTAR',pullPct:3.185,avgPrice:1.57,ev:0.05,count:6},{key:'V',pullPct:11.49,avgPrice:1.25,ev:0.14,count:15},{key:'RAD',pullPct:5.102,avgPrice:0.84,ev:0.04,count:3},{key:'RH',pullPct:17.86,avgPrice:0.29,ev:0.05,count:14},{key:'R',pullPct:62.50,avgPrice:0.14,ev:0.09,count:21},{key:'U',pullPct:300,avgPrice:0.09,ev:0.27,count:56},{key:'C',pullPct:500,avgPrice:0.08,ev:0.42,count:53}], notable:[{name:'Lugia V',rarity:'UR',price:354,pullPct:3.704},{name:'Rayquaza VMAX',rarity:'TGVM',price:99,pullPct:0.771},{name:'Lugia VSTAR',rarity:'RBOW',price:34,pullPct:1.259},{name:'Alolan Vulpix V',rarity:'TGV',price:22,pullPct:1.350},{name:'Regieleki VMAX',rarity:'UR',price:19,pullPct:3.704}]},

  { id:'swsh7', name:'Evolving Skies', series:'Sword & Shield', released:'2021-08-27', cardCount:237, packEV:5.50, packResalePrice:55.00, pricesUpdated:'February 17, 2026', accentColor:'#0ea5e9', topCard:{name:'Umbreon VMAX Rainbow Rare',price:1678}, rarities:[{key:'SR',pullPct:0.910,avgPrice:6.96,ev:0.06,count:12},{key:'RBOW',pullPct:1.141,avgPrice:163.82,ev:1.87,count:22},{key:'UR',pullPct:3.876,avgPrice:50.54,ev:1.96,count:38},{key:'VMAX',pullPct:5.587,avgPrice:7.33,ev:0.41,count:15},{key:'V',pullPct:10.53,avgPrice:1.51,ev:0.16,count:18},{key:'RH',pullPct:18.18,avgPrice:0.29,ev:0.05,count:20},{key:'R',pullPct:58.82,avgPrice:0.14,ev:0.09,count:19},{key:'U',pullPct:300,avgPrice:0.08,ev:0.25,count:51},{key:'C',pullPct:500,avgPrice:0.09,ev:0.46,count:42}], notable:[{name:'Umbreon VMAX',rarity:'RBOW',price:1678,pullPct:1.141},{name:'Rayquaza VMAX',rarity:'RBOW',price:657,pullPct:1.141},{name:'Dragonite V',rarity:'UR',price:382,pullPct:3.876},{name:'Umbreon V',rarity:'UR',price:234,pullPct:3.876},{name:'Glaceon VMAX',rarity:'RBOW',price:170,pullPct:1.141}]},

];

function buildSearchIndex() {
  const idx = [];
  SETS.forEach(set => {
    set.notable.forEach(card => {
      idx.push({ ...card, setId: set.id, setName: set.name });
    });
  });
  return idx;
}

const CARD_INDEX = buildSearchIndex();

function priceFmt(p) {
  if (p >= 1000) return '$' + Math.round(p).toLocaleString();
  if (p >= 100)  return '$' + Math.round(p);
  if (p >= 1)    return '$' + p.toFixed(p < 10 ? 2 : 0);
  return '$' + p.toFixed(2);
}

function pullFmt(pct) {
  if (pct < 0.1) return '1 in ' + Math.round(100/pct).toLocaleString() + ' packs';
  return '~' + pct.toFixed(2) + '% / pack';
}
