#!/usr/bin/env python3
"""
World Community Grid Stats Fetcher
Fetches live statistics from WCG API and generates markdown reports
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
        print(f"✅ Successfully fetched {len(data.get('results', []))} results")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching WCG data: {e}")
        return {}


def calculate_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate statistics from WCG data"""
    
    results = data.get('results', [])
    
    if not results:
        return {
            'total_results': 0,
            'total_points': 0,
            'total_runtime_hours': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    # Calculate totals
    total_results = len(results)
    total_points = sum(r.get('points', 0) for r in results)
    total_runtime = sum(r.get('runTime', 0) for r in results)
    
    # Convert runtime to hours
    total_runtime_hours = total_runtime / 3600
    
    # Get latest result timestamp
    latest_result = max(results, key=lambda r: r.get('sentTime', 0))
    
    stats = {
        'total_results': total_results,
        'total_points': total_points,
        'total_runtime_hours': round(total_runtime_hours, 2),
        'total_runtime_days': round(total_runtime_hours / 24, 2),
        'latest_result_date': latest_result.get('sentTime', 'N/A'),
        'last_updated': datetime.now().isoformat(),
        'api_limit_note': f"Showing last {total_results} results (API limit: 250)"
    }
    
    return stats


def generate_readme_badge_section(stats: Dict[str, Any], member_name: str) -> str:
    """Generate README section with badges and stats"""
    
    last_updated = datetime.fromisoformat(stats['last_updated']).strftime('%Y-%m-%d %H:%M UTC')
    
    readme = f"""## 🧬 Scientific Computing Contributions

I contribute idle computing power to [World Community Grid](https://www.worldcommunitygrid.org/) for medical research projects (cancer, COVID-19, microbiome research).

### 📊 Live Statistics

![WCG Results](https://img.shields.io/badge/Results_Returned-{stats['total_results']:,}-blue?style=for-the-badge&logo=gridsome)
![WCG Points](https://img.shields.io/badge/Points-{stats['total_points']:,}-green?style=for-the-badge&logo=ethereum)
![Runtime](https://img.shields.io/badge/Runtime-{stats['total_runtime_days']:.0f}_days-orange?style=for-the-badge&logo=clockify)

**🔄 Last Updated:** `{last_updated}`  
**👤 Member Profile:** [View on WCG](https://www.worldcommunitygrid.org/stat/viewMemberInfo.do?userName={member_name})

---

### 💡 What is World Community Grid?

World Community Grid enables anyone to donate their device's computing power to help scientists solve humanity's biggest problems in health and sustainability.

**Active Research Projects:**
- 🧬 **Microbiome Immunity Project** - Understanding immune system interactions
- 🦠 **OpenPandemics COVID-19** - Drug discovery for coronaviruses  
- ⚕️ **Mapping Cancer Markers** - Cancer treatment research

---

"""
    
    return readme


def save_data(stats: Dict[str, Any], output_file: str = 'data/wcg-stats.json'):
    """Save statistics to JSON file"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"✅ Saved statistics to {output_file}")


def update_readme(readme_content: str, readme_file: str = 'README.md'):
    """Update README.md with new statistics"""
    
    # Marker für Auto-Update Section
    start_marker = "<!-- WCG_STATS_START -->"
    end_marker = "<!-- WCG_STATS_END -->"
    
    # Read existing README or create new
    if os.path.exists(readme_file):
        with open(readme_file, 'r') as f:
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
        new_readme = f"""# Scientific Computing Dashboard

{start_marker}
{readme_content}
{end_marker}

## 🔧 Technical Implementation

This dashboard is automatically updated daily via GitHub Actions. It fetches live statistics from the World Community Grid API and updates this README.

**Tech Stack:**
- Python 3.x for API calls
- GitHub Actions for automation
- WCG JSON API for data retrieval

---

**🤝 Want to contribute too?** Join World Community Grid: https://www.worldcommunitygrid.org/
"""
    
    with open(readme_file, 'w') as f:
        f.write(new_readme)
    
    print(f"✅ Updated {readme_file}")


def main():
    """Main execution function"""
    
    # Get credentials from environment variables (GitHub Secrets)
    member_name = os.environ.get('WCG_MEMBER_NAME')
    verification_code = os.environ.get('WCG_VERIFICATION_CODE')
    
    if not member_name or not verification_code:
        print("❌ ERROR: WCG_MEMBER_NAME and WCG_VERIFICATION_CODE must be set as environment variables")
        exit(1)
    
    print("🚀 Starting WCG Stats Update...")
    
    # Fetch data from API
    data = fetch_wcg_stats(member_name, verification_code)
    
    if not data:
        print("❌ No data received from API")
        exit(1)
    
    # Calculate statistics
    stats = calculate_statistics(data)
    
    # Save to JSON
    save_data(stats)
    
    # Generate README content
    readme_content = generate_readme_badge_section(stats, member_name)
    
    # Update README
    update_readme(readme_content)
    
    print("✅ WCG Stats update completed successfully!")
    print(f"📊 Results: {stats['total_results']}")
    print(f"🎯 Points: {stats['total_points']:,}")
    print(f"⏱️  Runtime: {stats['total_runtime_days']:.2f} days")


if __name__ == "__main__":
    main()
