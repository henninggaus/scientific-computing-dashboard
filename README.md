# 🧬 Scientific Computing Dashboard

> **Automated tracking of my contributions to scientific research through distributed computing**

This repository showcases my ongoing contributions to **World Community Grid** - a humanitarian initiative that uses donated computing power from devices worldwide to advance cutting-edge scientific research in health and sustainability.

---

<!-- WCG_STATS_START -->
## 📊 Statistics Loading...

*Statistics will be automatically updated daily via GitHub Actions*

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

