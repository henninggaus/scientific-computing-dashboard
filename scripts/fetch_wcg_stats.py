#!/usr/bin/env python3
"""
World Community Grid Stats Fetcher - VERSION B (IMPRESSIVE MODE)
Fetches live statistics from WCG API and generates HR-friendly, impact-focused reports
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Any


def fetch_wcg_stats(member_name: str, verification_code: str) -> Dict[str, Any]:
    """Fetch WCG statistics from API"""
    
    # API Endpoints
    member_url = f"https://www.worldcommunitygrid.org/api/members/{member_name}/results"
    
    params = {
        'code': verification_code,
        'format': 'json',
        'limit': 250  # Letzte 250 Results
    }
    
    try:
        print(f"🔄 Fetching data for member: {member_name}")
        response = requests.get(member_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f" Successfully fetched {len(data.get('results', []))} results")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f" Error fetching WCG data: {e}")
        return {}


def calculate_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate statistics from WCG data"""
    
    results = data.get('results', [])
    
    if not results:
        return {
            'total_results': 0,
            'total_points': 0,
            'total_runtime_hours': 0,
            'total_runtime_days': 0,
            'cpu_years': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    # Calculate totals
    total_results = len(results)
    total_points = sum(r.get('points', 0) for r in results)
    total_runtime = sum(r.get('runTime', 0) for r in results)
    
    # Convert runtime to different units
    total_runtime_hours = total_runtime / 3600
    total_runtime_days = total_runtime_hours / 24
    cpu_years = total_runtime_hours / 8760  # 1 year = 8760 hours
    
    # Get latest result timestamp
    latest_result = max(results, key=lambda r: r.get('sentTime', 0))
    
    stats = {
        'total_results': total_results,
        'total_points': total_points,
        'total_runtime_hours': round(total_runtime_hours, 2),
        'total_runtime_days': round(total_runtime_days, 2),
        'cpu_years': round(cpu_years, 3),
        'latest_result_date': latest_result.get('sentTime', 'N/A'),
        'last_updated': datetime.now().isoformat(),
        'api_limit_note': f"Showing last {total_results} results (API limit: 250)"
    }
    
    return stats


def generate_readme_badge_section(stats: Dict[str, Any], member_name: str) -> str:
    """Generate README section with impressive badges and impact metrics"""
    
    last_updated = datetime.fromisoformat(stats['last_updated']).strftime('%Y-%m-%d %H:%M UTC')
    
    # Format CPU years for display
    cpu_years_display = stats['cpu_years']
    if cpu_years_display < 0.01:
        cpu_years_str = f"{cpu_years_display:.4f}"
    elif cpu_years_display < 1:
        cpu_years_str = f"{cpu_years_display:.2f}"
    else:
        cpu_years_str = f"{cpu_years_display:.1f}"
    
    readme = f"""## 🧬 Scientific Computing Contributions

I contribute idle computing power to [World Community Grid](https://www.worldcommunitygrid.org/) for medical research projects tackling humanity's biggest health challenges.

### 📊 Live Impact Metrics

![CPU Years](https://img.shields.io/badge/CPU_Years-{cpu_years_str}-purple?style=for-the-badge&logo=cpanel)
![Medical Tasks](https://img.shields.io/badge/Medical_Tasks-{stats['total_results']:,}-red?style=for-the-badge&logo=dna)
![WCG Points](https://img.shields.io/badge/Points-{stats['total_points']:,}-green?style=for-the-badge&logo=ethereum)
![Computing Hours](https://img.shields.io/badge/Hours-{stats['total_runtime_hours']:,.0f}-orange?style=for-the-badge&logo=clockify)

### 💡 What This Means

**My Computing Contribution:**
- ⚡ **{cpu_years_str} CPU-Years** dedicated to medical research
- 🧬 **{stats['total_results']:,} research calculations** completed for scientific projects
- ⏱️ **{stats['total_runtime_hours']:,.0f}+ hours** of processing power donated
- 📅 **{stats['total_runtime_days']:.0f} days** of continuous 24/7 computing

**Real-World Equivalent:**
> This is equivalent to running a high-performance workstation non-stop, 24/7, for **{stats['total_runtime_days']:.0f} consecutive days** dedicated solely to medical research calculations.

**🔄 Last Updated:** `{last_updated}`  
**👤 Member Profile:** [View on WCG](https://www.worldcommunitygrid.org/stat/viewMemberInfo.do?userName={member_name})

---

### 🎯 Research Impact Areas

My computing contributions directly support breakthrough research in:

#### 🦠 **Disease Treatment & Drug Discovery**
- **OpenPandemics - COVID-19**: Screening billions of chemical compounds to discover potential treatments for COVID-19 and future pandemics
- **Mapping Cancer Markers**: Identifying cancer markers in cells to develop personalized cancer treatments

#### 🧬 **Biological & Medical Research**
- **Microbiome Immunity Project**: Understanding how the human microbiome interacts with the immune system to fight diseases
- Accelerating research that would take decades on single computers into months through distributed computing

#### 💊 **The Bigger Picture**
Every calculation I process helps scientists:
- Test potential drug candidates faster
- Understand disease mechanisms better  
- Develop more effective treatments
- Advance personalized medicine

---

### 🌍 What is World Community Grid?

World Community Grid brings together volunteers from around the world to create the largest non-profit computing grid benefiting humanity. By donating my computer's idle processing power, I help scientists tackle some of the world's most pressing problems in health and sustainability.

**How it works:**
1. 💻 I donate spare CPU cycles when my computer is idle
2. 🔬 Scientists use this power for complex medical calculations
3. 📊 Research that would take years completes in months
4. 💊 Results accelerate drug discovery and disease treatment

---

"""
    
    return readme


def save_data(stats: Dict[str, Any], output_file: str = 'data/wcg-stats.json'):
    """Save statistics to JSON file"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f" Saved statistics to {output_file}")


def update_readme(readme_content: str, readme_file: str = 'README.md'):
    """Update README.md with new statistics"""
    
    # Marker für Auto-Update Section
    start_marker = "<!-- WCG_STATS_START -->"
    end_marker = "<!-- WCG_STATS_END -->"
    
    # Read existing README or create new
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            existing_readme = f.read()
        
        # Check if markers exist
        if start_marker in existing_readme and end_marker in existing_readme:
            # Replace content between markers
            before = existing_readme.split(start_marker)[0]
            after = existing_readme.split(end_marker)[1]
            new_readme = f"{before}{start_marker}\n{readme_content}\n{end_marker}{after}"
        else:
            # Append at the end
            new_readme = f"{existing_readme}\n\n{start_marker}\n{readme_content}\n{end_marker}\n"
    else:
        # Create new README
        new_readme = f"""# 🧬 Scientific Computing Dashboard

> **Automated tracking of my contributions to scientific research through distributed computing**

This repository showcases my ongoing contributions to **World Community Grid** - a humanitarian initiative that uses donated computing power from devices worldwide to advance cutting-edge scientific research in health and sustainability.

---

{start_marker}
{readme_content}
{end_marker}

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
 Fully automated daily updates  
 No manual intervention required  
 Live statistics from official WCG API  
 Clean, professional presentation  
 Production-ready error handling  
 Impact-focused metrics for HR/recruiters

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
python scripts/fetch_wcg_stats.py
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

"""
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme)
    
    print(f" Updated {readme_file}")


def main():
    """Main execution function"""
    
    # Get credentials from environment variables (GitHub Secrets)
    member_name = os.environ.get('WCG_MEMBER_NAME')
    verification_code = os.environ.get('WCG_VERIFICATION_CODE')
    
    if not member_name or not verification_code:
        print(" ERROR: WCG_MEMBER_NAME and WCG_VERIFICATION_CODE must be set as environment variables")
        exit(1)
    
    print("🚀 Starting WCG Stats Update (VERSION B - IMPRESSIVE MODE)...")
    
    # Fetch data from API
    data = fetch_wcg_stats(member_name, verification_code)
    
    if not data:
        print(" No data received from API")
        exit(1)
    
    # Calculate statistics
    stats = calculate_statistics(data)
    
    # Save to JSON
    save_data(stats)
    
    # Generate README content
    readme_content = generate_readme_badge_section(stats, member_name)
    
    # Update README
    update_readme(readme_content)
    
    print(" WCG Stats update completed successfully!")
    print(f"📊 Results: {stats['total_results']}")
    print(f"🎯 Points: {stats['total_points']:,}")
    print(f"⏱️  Runtime: {stats['total_runtime_days']:.2f} days")
    print(f"⚡ CPU-Years: {stats['cpu_years']:.3f}")


if __name__ == "__main__":
    main()
