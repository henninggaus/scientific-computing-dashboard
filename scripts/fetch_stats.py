#!/usr/bin/env python3
"""
Multi-Platform Scientific Computing Stats
Fetches data from WCG and Folding@home with nice formatting
"""

import requests
import json
import os
from datetime import datetime


def fetch_wcg_data(member_name: str, verification_code: str):
    """Fetch World Community Grid data"""

    url = f"https://www.worldcommunitygrid.org/api/members/{member_name}/results"

    params = {
        'code': verification_code,
        'format': 'json',
        'limit': 250
    }

    try:
        print(f"🧬 Fetching WCG data for: {member_name}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"WCG: Successfully fetched {len(data.get('results', []))} results!")
        return data
    except Exception as e:
        print(f"WCG Error: {e}")
        return None


def fetch_fah_data(username: str):
    """Fetch Folding@home data"""

    base_url = "https://api.foldingathome.org"

    try:
        print(f"💻 Fetching F@H data for: {username}")

        # Fetch main user stats
        response = requests.get(f"{base_url}/user/{username}", timeout=30)
        response.raise_for_status()
        user_data = response.json()

        print(f"F@H: Successfully fetched data!")
        print(f"   Score: {user_data.get('score', 0):,}")
        print(f"   Work Units: {user_data.get('wus', 0)}")
        print(f"   Rank: #{user_data.get('rank', 0):,}")

        return user_data

    except Exception as e:
        print(f"F@H Error: {e}")
        return None


def calculate_wcg_stats(data):
    """Calculate WCG statistics"""

    results = data.get('results', [])

    if not results:
        return None

    total_results = len(results)
    total_points = sum(r.get('points', 0) for r in results)
    total_runtime = sum(r.get('CpuTime', 0) for r in results)

    total_runtime_hours = total_runtime / 3600
    total_runtime_days = total_runtime_hours / 24
    cpu_years = total_runtime_hours / 8760

    return {
        'total_results': total_results,
        'total_points': total_points,
        'total_runtime_hours': round(total_runtime_hours, 2),
        'total_runtime_days': round(total_runtime_days, 2),
        'cpu_years': round(cpu_years, 3)
    }


def update_readme(wcg_stats, fah_data, wcg_username: str, fah_username: str):
    """Update README with impressive formatted stats"""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

    readme_content = f"""## 🧬 Scientific Computing Contributions

I contribute computing power to multiple research platforms for medical breakthroughs.

**🔄 Last Updated:** `{timestamp}`

---

"""

    # === FOLDING@HOME SECTION ===
    if fah_data:
        score = fah_data.get('score', 0)
        wus = fah_data.get('wus', 0)
        rank = fah_data.get('rank', 0)
        total_users = fah_data.get('users', 0)

        # Calculate percentile
        percentile = 100 - (rank / total_users * 100) if total_users > 0 else 0

        readme_content += f"""### 💻 Folding@home

![F@H Score](https://img.shields.io/badge/Score-{score:,}-blue?style=for-the-badge&logo=bitcoin)
![F@H Work Units](https://img.shields.io/badge/Work_Units-{wus}-green?style=for-the-badge&logo=checkmarx)
![F@H Rank](https://img.shields.io/badge/Rank-%23{rank:,}-purple?style=for-the-badge&logo=rancher)

**My Folding@home Contribution:**
- 🎯 **{score:,} Points** earned through protein folding calculations
- ⚡ **{wus} Work Units** completed for disease research
- 🏆 **Rank #{rank:,}** out of {total_users:,} active contributors worldwide
- 📊 **Top {percentile:.1f}%** of all Folding@home volunteers

**What I'm helping research:**
- 🧬 Protein folding for Alzheimer's and Parkinson's disease
- 🦠 COVID-19 and infectious disease treatments
- ⚕️ Cancer research and drug discovery
- 💊 Understanding protein misfolding diseases

**Username:** `{fah_username}`  
**Profile:** [View on F@H Stats](https://stats.foldingathome.org/donor/{fah_username})

---

"""
    else:
        readme_content += f"""### 💻 Folding@home

**Username:** `{fah_username}`  
**Status:** ⏳ Connecting to API...

---

"""

    # === WORLD COMMUNITY GRID SECTION ===
    if wcg_stats:
        cpu_years_str = f"{wcg_stats['cpu_years']:.2f}" if wcg_stats[
                                                               'cpu_years'] < 1 else f"{wcg_stats['cpu_years']:.1f}"

        readme_content += f"""### 🌍 World Community Grid

![CPU Years](https://img.shields.io/badge/CPU_Years-{cpu_years_str}-purple?style=for-the-badge&logo=cpanel)
![WCG Tasks](https://img.shields.io/badge/Tasks-{wcg_stats['total_results']:,}-red?style=for-the-badge&logo=dna)
![WCG Points](https://img.shields.io/badge/Points-{wcg_stats['total_points']:,}-green?style=for-the-badge&logo=ethereum)

**My World Community Grid Contribution:**
- ⚡ **{cpu_years_str} CPU-Years** dedicated to medical research
- 🧬 **{wcg_stats['total_results']:,} research calculations** completed
- ⏱️ **{wcg_stats['total_runtime_hours']:,.0f}+ hours** of processing power donated
- 📅 **{wcg_stats['total_runtime_days']:.0f} days** of continuous computing

**What I'm helping research:**
- 🦠 COVID-19 drug discovery (OpenPandemics)
- ⚕️ Cancer marker identification (Mapping Cancer Markers)
- 🧬 Immune system research (Microbiome Immunity Project)

**Username:** `{wcg_username}`  
**Profile:** [View on WCG](https://www.worldcommunitygrid.org/stat/viewMemberInfo.do?userName={wcg_username})

---

"""
    else:
        readme_content += f"""### 🌍 World Community Grid

**Username:** `{wcg_username}`  
**Status:** ⏳ Waiting for BOINC data...

---

"""

    # === COMBINED IMPACT ===
    if fah_data or wcg_stats:
        readme_content += """### 🌟 Combined Impact

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

"""

    readme_content += """### 🔧 About This Dashboard

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

"""

    # Update README
    start_marker = "<!-- WCG_STATS_START -->"
    end_marker = "<!-- WCG_STATS_END -->"

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
        new_readme = f"""# 🧬 Scientific Computing Dashboard

{start_marker}
{readme_content}
{end_marker}
"""

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme)

    print(f"Updated {readme_file}")


def main():
    """Main function"""

    # Get credentials from environment
    wcg_member = os.environ.get('WCG_MEMBER_NAME')
    wcg_code = os.environ.get('WCG_VERIFICATION_CODE')
    fah_username = os.environ.get('FAH_USERNAME')

    print("🚀 Multi-Platform Scientific Computing Stats - VERSION B\n")

    # Fetch F@H data (if username available)
    fah_data = None
    if fah_username:
        fah_data = fetch_fah_data(fah_username)
    else:
        print("⚠️  F@H username not set (FAH_USERNAME)")

    # Fetch WCG data (if credentials available)
    wcg_data = None
    wcg_stats = None
    if wcg_member and wcg_code:
        wcg_data = fetch_wcg_data(wcg_member, wcg_code)
        if wcg_data:
            wcg_stats = calculate_wcg_stats(wcg_data)
    else:
        print("⚠️  WCG credentials not set (WCG_MEMBER_NAME, WCG_VERIFICATION_CODE)")

    # Update README with whatever data we have
    if fah_data or wcg_stats:
        update_readme(
            wcg_stats,
            fah_data,
            wcg_member or "not_set",
            fah_username or "not_set"
        )
        print("\nDone! Check your README.md")

        # Print summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY:")
        print("=" * 60)
        if fah_data:
            print(
                f"💻 F@H: {fah_data.get('score', 0):,} points, {fah_data.get('wus', 0)} WUs, Rank #{fah_data.get('rank', 0):,}")
        if wcg_stats:
            print(f"🌍 WCG: {wcg_stats['cpu_years']:.3f} CPU-years, {wcg_stats['total_results']} tasks")
        print("=" * 60)
    else:
        print("\nNo data fetched. Set at least one platform's credentials.")
        exit(1)


if __name__ == "__main__":
    main()