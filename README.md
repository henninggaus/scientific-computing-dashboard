# 🧬 Scientific Computing Dashboard

> **Automated tracking of my contributions to scientific research through distributed computing**

This repository showcases my ongoing contributions to **World Community Grid** - a humanitarian initiative that uses donated computing power from devices worldwide to advance cutting-edge scientific research in health and sustainability.

---

<!-- WCG_STATS_START -->
## 🧬 Scientific Computing Contributions

I contribute computing power to multiple research platforms for medical breakthroughs.

**🔄 Last Updated:** `2025-11-16 00:25 UTC`

---

### 💻 Folding@home

![F@H Score](https://img.shields.io/badge/Score-3,833,867-blue?style=for-the-badge&logo=bitcoin)
![F@H Work Units](https://img.shields.io/badge/Work_Units-27-green?style=for-the-badge&logo=checkmarx)
![F@H Rank](https://img.shields.io/badge/Rank-%23216,493-purple?style=for-the-badge&logo=rancher)

**My Folding@home Contribution:**
- 🎯 **3,833,867 Points** earned through protein folding calculations
- ⚡ **27 Work Units** completed for disease research
- 🏆 **Rank #216,493** out of 3,021,483 active contributors worldwide
- 📊 **Top 92.8%** of all Folding@home volunteers

**What I'm helping research:**
- 🧬 Protein folding for Alzheimer's and Parkinson's disease
- 🦠 COVID-19 and infectious disease treatments
- ⚕️ Cancer research and drug discovery
- 💊 Understanding protein misfolding diseases

**Username:** `HenningSarrus`  
**Profile:** [View on F@H Stats](https://stats.foldingathome.org/donor/HenningSarrus)

---

### 🌍 World Community Grid

**Username:** `not_set`  
**Status:** ⏳ Waiting for BOINC data...

---

### 🌟 Combined Impact

By contributing to both platforms, I'm supporting a diverse range of critical medical research:

**Research Areas:**
- 🧬 Protein folding & structural biology
- 🦠 Infectious disease treatment
- ⚕️ Cancer research & drug discovery  
- 🧠 Neurological disorders (Alzheimer's, Parkinson's)
- 💊 Pharmaceutical development
- 🔬 Computational biology

**Why This Matters:**
> Distributed computing allows researchers to run calculations that would take decades on single computers. By donating spare computing power, volunteers like me help accelerate scientific breakthroughs that save lives.

---

### 🔧 About This Dashboard

This dashboard is fully automated:
- 🤖 **GitHub Actions** fetch fresh data daily at 00:00 UTC
- 🐍 **Python scripts** process APIs from both platforms
- 📊 **Live statistics** update automatically
- 🚀 **Zero manual intervention** required

**Tech Stack:** Python 3.11, GitHub Actions, REST APIs, Markdown

---

**Want to contribute to science too?**
- 💻 [Join Folding@home](https://foldingathome.org/)
- 🌍 [Join World Community Grid](https://www.worldcommunitygrid.org/)


<!-- WCG_STATS_END -->

---

## 🎯 About This Project

### What is World Community Grid?

World Community Grid (WCG) is IBM's philanthropic initiative that creates the world's largest public computing grid to tackle humanity's biggest challenges in health and sustainability.

**How it works:**
1. 💻 Volunteers donate idle computing power
2. 🧬 Scientists use this power for complex calculations
3. 🔬 Research that would take decades on single computers completes in months
4. 💊 Results accelerate drug discovery, disease research, and environmental studies

### My Contribution

I dedicate spare computing cycles to help researchers:
- 🦠 Discover new treatments for COVID-19 and other diseases
- 🧬 Understand the human microbiome and immune system
- ⚕️ Map cancer markers for better treatments
- 🌍 Advance clean energy research

---

## 🔧 Technical Implementation

This dashboard demonstrates practical DevOps and automation skills:

### Architecture
```
┌─────────────────┐
│  WCG Public API │
└────────┬────────┘
         │ JSON
         ▼
┌─────────────────┐
│ Python Script   │ ← Runs daily via GitHub Actions
│ fetch_wcg_stats │
└────────┬────────┘
         │
         ├─► data/wcg-stats.json (Live data)
         └─► README.md (Auto-updated badges)
```

### Tech Stack
- **Python 3.11** - API integration and data processing
- **GitHub Actions** - Scheduled automation (cron: daily at 00:00 UTC)
- **WCG JSON API** - Real-time statistics retrieval
- **Markdown Badges** - Visual statistics display

### Features
✅ Fully automated daily updates  
✅ No manual intervention required  
✅ Live statistics from official WCG API  
✅ Clean, professional presentation  
✅ Production-ready error handling  

---

## 📁 Repository Structure

```
scientific-computing-dashboard/
├── .github/workflows/
│   └── update-wcg-stats.yml       # GitHub Action (scheduled daily)
├── scripts/
│   └── fetch_wcg_stats.py         # API fetching & processing
├── data/
│   └── wcg-stats.json             # Live statistics (auto-updated)
├── README.md                       # This file (auto-updated)
└── .gitignore
```

---

## 🚀 How to Run Locally

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/scientific-computing-dashboard.git
cd scientific-computing-dashboard

# Set environment variables
export WCG_MEMBER_NAME="your_wcg_username"
export WCG_VERIFICATION_CODE="your_verification_code"

# Install dependencies
pip install requests

# Run script
python scripts/fetch_stats.py
```

---

## 🤝 Join the Cause

**Want to contribute to scientific research too?**

1. Visit [World Community Grid](https://www.worldcommunitygrid.org/)
2. Create a free account
3. Download the BOINC client
4. Select research projects you want to support
5. Let your computer help save lives! 💙

---

## 📜 License

This dashboard implementation is open source. Feel free to fork and adapt for your own WCG tracking!

---

**🔄 Last Repository Update:** See commit history  
**🤖 Automated Updates:** Daily at 00:00 UTC via GitHub Actions

