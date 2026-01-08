# 🧬 Scientific Computing Portfolio

> **Contributing to Global Scientific Research Through Distributed Computing**

[![Folding@home](https://img.shields.io/badge/Folding@home-Active-green?style=for-the-badge&logo=moleculer)](https://stats.foldingathome.org/donor/HenningSarrus)
[![BOINC](https://img.shields.io/badge/BOINC-Active-blue?style=for-the-badge&logo=atom)](https://boincstats.com/stats/-1/user/detail/38537905500)

I contribute idle computing power across multiple platforms to accelerate scientific research in medicine, astronomy, mathematics, and physics.

---

## 🏆 Portfolio Overview

**Research Impact Areas:**
🧬 Drug Discovery • ⚕️ Cancer Research • 🧠 Neurological Disorders • 🦠 Infectious Diseases • 🔭 Astronomy • 🔢 Mathematics • 💊 Protein Folding

---

<!-- LIVE_STATS_START -->
## Live Statistics

Updated: 2026-01-08 00:25 UTC

### Overview

- **13** active BOINC projects
- **36,606,594** total BOINC credits
- **7.6** years contributing

---

### 🏆 Nobel Prize Connection

> **Rosetta@home** — Contributing to David Baker's Nobel Prize-winning research

I joined Rosetta@home on **2018-06-03** — **6.4 years before** David Baker received the **2024 Nobel Prize in Chemistry** for computational protein design.

- **1,064,227** credits earned
- **2,776** days contributing (7.6 years)

[View Rosetta Profile](https://boinc.bakerlab.org/rosetta/show_user.php?userid=2003572)

---


### Folding@home

- 7,908,286 points
- 149 work units

[View Profile](https://stats.foldingathome.org/donor/HenningSarrus)

---

### Other BOINC Projects

| Project | Credits | Member Since |
|---------|--------:|--------------|
| [Collatz Conjecture](https://boinc.thesonntags.com/collatz) | 23,165,561 | 2019-08-05 |
| [GPUGRID](https://www.gpugrid.net/gpugrid/show_user.php?userid=543812) | 6,450,000 | 2019-04-20 |
| [Amicable Numbers](https://sech.me/boinc/Amicable/show_user.php?userid=22852) | 2,351,650 | 2019-10-05 |
| [SiDock@home](https://www.sidock.si/sidock/show_user.php?userid=13871) | 2,112,815 | 2025-04-10 |
| [Climateprediction.net](https://www.cpdn.org) | 898,928 | 2019-08-05 |
| [PrimeGrid](https://www.primegrid.com/show_user.php?userid=1188549) | 224,437 | 2019-09-12 |
| [MilkyWay@home](https://milkyway.cs.rpi.edu/milkyway/show_user.php?userid=1365700) | 124,111 | 2019-10-05 |
| [yoyo@home](https://www.rechenkraft.net/yoyo/show_user.php?userid=319246) | 101,050 | 2018-08-11 |
| [Asteroids@home](https://asteroidsathome.net/boinc/show_user.php?userid=403666) | 75,840 | 2018-08-11 |
| [SETI@home](https://setiathome.berkeley.edu) | 21,928 | 2018-08-11 |
| [Ramanujan Machine](https://rnma.xyz/boinc/show_user.php?userid=2554988) | 16,011 | 2025-03-29 |
| [Cosmology@Home](https://www.cosmologyathome.org) | 36 | 2019-08-05 |

---

### BOINC Combined

![BOINC Stats](https://boincstats.com/signature/-1/user/38537905500/sig.png)

[View Full Profile](https://boincstats.com/en/stats/-1/user/detail/38537905500)

---

Data fetched automatically via GitHub Actions.

<!-- LIVE_STATS_END -->

---

## 🌟 Why This Matters

### The Power of Distributed Computing

> "Research that would take centuries on a single computer can be completed in months through volunteer computing networks."

**Real-World Impact:**
- Drug candidates discovered for COVID-19, cancer, and Alzheimer's
- Protein structures solved enabling disease research
- Mathematical conjectures tested (Collatz, prime numbers)
- Astronomical phenomena modeled (Milky Way structure, asteroids)
- Computational problems solved across multiple scientific disciplines

---

## 🔧 Technical Implementation

This repository demonstrates DevOps and automation skills with **zero hardcoded statistics**:

### Architecture

```
┌─────────────────────────────────────────────┐
│   GitHub Actions (Cron: Daily 00:00 UTC)    │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Python Script  │
              │  F@H + BOINC    │
              │  API Fetch      │
              └────────┬────────┘
                       │
               ┌───────┴───────┐
               │               │
               ▼               ▼
        ┌─────────────┐ ┌─────────────┐
        │ README.md   │ │ stats.json  │
        │ Auto-update │ │ Dashboard   │
        └─────────────┘ └─────────────┘
```

### Key Features

✅ **Dynamic Statistics** - All numbers from live APIs, not hardcoded  
✅ **Multi-Platform Aggregation** - Folding@home + BOINC data  
✅ **Centralized Configuration** - config.json for all settings  
✅ **Production Error Handling** - Graceful API failure recovery  
✅ **Zero Manual Intervention** - Fully automated daily updates  
✅ **Years Active Calculation** - Auto-calculated from start year  

### Tech Stack

- **Python 3.11** - REST API integration with type hints
- **GitHub Actions** - Scheduled automation (cron job)
- **Folding@home API** - Real-time F@H statistics
- **BOINCStats API** - BOINC credit tracking
- **JSON Configuration** - Centralized settings management

---

## 📁 Repository Structure

```
scientific-computing-dashboard/
├── .github/workflows/
│   └── update_scientific_stats.yml    # Daily automation
├── config.json                         # Centralized configuration
├── data/
│   └── stats.json                      # Generated stats for dashboard
├── docs/
│   └── index.html                      # Web dashboard
├── scripts/
│   └── fetch_stats.py                  # API fetcher
├── README.md                           # This file (auto-updated)
└── requirements.txt                    # Python dependencies
```

---

## 🚀 Getting Started

Want to contribute to scientific research too?

### Join These Platforms:

**💻 Folding@home (Protein Folding):**
1. Visit [foldingathome.org](https://foldingathome.org/)
2. Download the client
3. Start folding proteins for disease research

**🔬 BOINC (Multiple Projects):**
1. Download [BOINC Client](https://boinc.berkeley.edu/download.php)
2. Choose research projects that interest you
3. Let your computer solve problems while idle

---

## 🤝 Connect

**My Profiles:**
- 💻 **Folding@home:** [HenningSarrus](https://stats.foldingathome.org/donor/HenningSarrus)
- 🔬 **BOINC Combined:** [View on BOINCStats](https://boincstats.com/stats/-1/user/detail/38537905500)

---

## 📜 License

This automation implementation is open source. MIT License.

---

**🔄 Last Update:** Automated via GitHub Actions  
**🤖 Update Frequency:** Daily at 00:00 UTC  
**📊 Data Sources:** Live APIs from Folding@home + BOINCStats

---

*Contributing to science, one computation at a time.* 🧬
