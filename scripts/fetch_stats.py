#!/usr/bin/env python3
"""
Scientific Computing Stats Fetcher
Automated daily updates for distributed computing portfolio
Fetches live data from Folding@home API + embeds BOINC graphics
"""

import requests
import os
from datetime import datetime


def fetch_fah_data(username: str):
    """Fetch Folding@home statistics via official API"""

    base_url = "https://api.foldingathome.org"

    try:
        print(f"💻 Fetching Folding@home data for: {username}")

        response = requests.get(f"{base_url}/user/{username}", timeout=30)
        response.raise_for_status()
        user_data = response.json()

        print(f"✅ F@H API Success!")
        print(f"   Score: {user_data.get('score', 0):,}")
        print(f"   Work Units: {user_data.get('wus', 0)}")
        print(f"   Rank: #{user_data.get('rank', 0):,}")

        return user_data

    except Exception as e:
        print(f"❌ F@H API Error: {e}")
        return None


def update_readme(fah_data, fah_username: str):
    """Update README with live Folding@home stats"""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

    # Build dynamic content section
    readme_content = f"""## 📊 Live Platform Statistics

**🔄 Last Updated:** `{timestamp}`

This section updates automatically daily via GitHub Actions.

---

"""

    # === FOLDING@HOME SECTION ===
    if fah_data:
        score = fah_data.get('score', 0)
        wus = fah_data.get('wus', 0)
        rank = fah_data.get('rank', 0)
        total_users = fah_data.get('users', 0)

        # Calculate percentile (higher is better - top X%)
        percentile = 100 - (rank / total_users * 100) if total_users > 0 else 0

        readme_content += f"""### 💻 Folding@home

![F@H Score](https://img.shields.io/badge/Score-{score:,}-blue?style=for-the-badge&logo=bitcoin)
![F@H Work Units](https://img.shields.io/badge/Work_Units-{wus}-green?style=for-the-badge&logo=checkmarx)
![F@H Rank](https://img.shields.io/badge/Rank-%23{rank:,}-purple?style=for-the-badge&logo=rancher)

**Current Stats:**
- 🎯 **{score:,} Points** earned through protein folding calculations
- ⚡ **{wus} Work Units** completed for disease research
- 🏆 **Rank #{rank:,}** out of {total_users:,} active contributors worldwide
- 📊 **Top {percentile:.1f}%** of all Folding@home volunteers

**Research Areas:**
- 🧬 Protein folding for Alzheimer's and Parkinson's disease
- 🦠 COVID-19 and infectious disease treatments
- ⚕️ Cancer research and drug discovery
- 💊 Understanding protein misfolding diseases

**Profile:** [View on F@H Stats](https://stats.foldingathome.org/donor/{fah_username})

---

"""
    else:
        readme_content += f"""### 💻 Folding@home

**Status:** ⏳ Connecting to API...

---

"""

    # === COMBINED IMPACT ===
    readme_content += """### 🌟 Combined Impact

**7+ Years of Continuous Scientific Contribution:**

**Platforms:**
- 🔬 **BOINC Network** - 33M+ Credits across 12+ projects (see live graphics above)
- 💻 **Folding@home** - Real-time stats via API (see above)

**Research Areas:**
- 🧬 Protein folding & structural biology
- 🦠 Infectious disease treatment
- ⚕️ Cancer research & drug discovery
- 🧠 Neurological disorders (Alzheimer's, Parkinson's)
- 💊 Pharmaceutical development
- 🔢 Pure mathematics (Collatz, prime numbers)
- 🔭 Astronomy & astrophysics

**Why This Matters:**
> Distributed computing allows researchers to run calculations that would take decades on single computers. By donating spare computing power, volunteers accelerate scientific breakthroughs that save lives.

---

"""

    # === TECHNICAL IMPLEMENTATION ===
    readme_content += """### 🔧 Technical Implementation

**Full Production Automation:**
- 🤖 **GitHub Actions** - Scheduled daily cron job (00:00 UTC)
- 🐍 **Python 3.11** - REST API integration with error handling
- 📡 **Folding@home API** - Live statistics retrieval
- 🎨 **BOINCStats Graphics** - Embedded live images from 12+ projects
- 📊 **Markdown Badges** - Professional visual metrics
- 🚀 **Zero Manual Intervention** - Fully automated deployment

**Architecture:**
```
GitHub Actions (Daily Cron)
    ↓
Python Script fetches F@H API
    ↓
Updates README.md with live data
    ↓
Auto-commits via git
    ↓
Live on GitHub repo
```

**Tech Stack:** Python • REST APIs • GitHub Actions • Git Automation • Markdown

---

**Want to contribute to science?**
- 🔬 [Join BOINC](https://boinc.berkeley.edu/)
- 💻 [Join Folding@home](https://foldingathome.org/)

"""

    # Update README between markers
    start_marker = "<!-- LIVE_STATS_START -->"
    end_marker = "<!-- LIVE_STATS_END -->"

    readme_file = 'README.md'

    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            existing_readme = f.read()

        if start_marker in existing_readme and end_marker in existing_readme:
            before = existing_readme.split(start_marker)[0]
            after = existing_readme.split(end_marker)[1]
            new_readme = f"{before}{start_marker}\n{readme_content}\n{end_marker}{after}"
        else:
            new_readme = f"{existing_readme}\n\n{start_marker}\n{readme_content}\n{end_marker}\n"
    else:
        new_readme = f"""# 🧬 Scientific Computing Portfolio

{start_marker}
{readme_content}
{end_marker}
"""

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme)

    print(f"✅ Updated {readme_file}")


def main():
    """Main execution function"""

    # Get credentials from GitHub Secrets
    fah_username = os.environ.get('FAH_USERNAME')

    print("🚀 Scientific Computing Stats Fetcher - Production Version\n")
    print("=" * 70)

    if not fah_username:
        print("❌ Error: FAH_USERNAME environment variable not set")
        exit(1)

    # Fetch Folding@home data
    fah_data = fetch_fah_data(fah_username)

    if fah_data:
        # Update README with live stats
        update_readme(fah_data, fah_username)

        # Print summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY - DEPLOYMENT SUCCESSFUL")
        print("=" * 70)
        print(f"💻 Folding@home:")
        print(f"   Score: {fah_data.get('score', 0):,} points")
        print(f"   Work Units: {fah_data.get('wus', 0)}")
        print(f"   Rank: #{fah_data.get('rank', 0):,} / {fah_data.get('users', 0):,}")
        print("=" * 70)
        print("✅ README.md updated successfully")
        print("🔬 BOINC graphics embedded (auto-updating)")
        print("=" * 70)
    else:
        print("\n❌ Failed to fetch Folding@home data")
        print("⚠️  Proceeding with partial update...")
        update_readme(None, fah_username or "HenningSarrus")


if __name__ == "__main__":
    main()