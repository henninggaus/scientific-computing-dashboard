#!/usr/bin/env python3
"""
Multi-Platform Scientific Computing Stats - MVP VERSION
Fetches data from both WCG and Folding@home and shows raw JSON
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
        'limit': 10
    }
    
    try:
        print(f"🧬 Fetching WCG data for: {member_name}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ WCG: Successfully fetched data!")
        return data
    except Exception as e:
        print(f"❌ WCG Error: {e}")
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
        
        # Fetch detailed stats
        stats_response = requests.get(f"{base_url}/user/{username}/stats", timeout=30)
        stats_data = stats_response.json() if stats_response.status_code == 200 else None
        
        print(f"✅ F@H: Successfully fetched data!")
        
        return {
            "user": user_data,
            "stats": stats_data
        }
    except Exception as e:
        print(f"❌ F@H Error: {e}")
        return None


def update_readme(wcg_data, fah_data, wcg_username: str, fah_username: str):
    """Update README with raw data from both platforms"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    
    readme_content = f"""## 🧬 Scientific Computing Contributions

I contribute computing power to multiple research platforms for medical breakthroughs.

**Last Updated:** `{timestamp}`

---

"""
    
    # WCG Section
    if wcg_data:
        wcg_json = json.dumps(wcg_data, indent=2)
        readme_content += f"""### 🌍 World Community Grid

**Username:** `{wcg_username}`  
**Status:** ✅ Connected

<details>
<summary>📊 Raw API Response (click to expand)</summary>

```json
{wcg_json}
```

</details>

---

"""
    else:
        readme_content += f"""### 🌍 World Community Grid

**Username:** `{wcg_username}`  
**Status:** ⏳ Waiting for data...

---

"""
    
    # F@H Section
    if fah_data:
        fah_json = json.dumps(fah_data, indent=2)
        readme_content += f"""### 💻 Folding@home

**Username:** `{fah_username}`  
**Status:** ✅ Connected

<details>
<summary>📊 Raw API Response (click to expand)</summary>

```json
{fah_json}
```

</details>

---

"""
    else:
        readme_content += f"""### 💻 Folding@home

**Username:** `{fah_username}`  
**Status:** ⏳ Waiting for data...

---

"""
    
    readme_content += """
### 📝 Status

This is showing raw API responses. Will be formatted with nice stats and badges soon! 🚀

**What's next:**
- ✅ APIs connected
- ⏳ Nice formatting and badges coming
- ⏳ Combined statistics
- ⏳ Impact metrics

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
        new_readme = f"""# Scientific Computing Dashboard

{start_marker}
{readme_content}
{end_marker}
"""
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme)
    
    print(f"✅ Updated {readme_file}")


def main():
    """Main function"""
    
    # Get credentials from environment
    wcg_member = os.environ.get('WCG_MEMBER_NAME')
    wcg_code = os.environ.get('WCG_VERIFICATION_CODE')
    fah_username = os.environ.get('FAH_USERNAME')
    
    print("🚀 Multi-Platform Scientific Computing Stats - MVP\n")
    
    # Fetch WCG data (if credentials available)
    wcg_data = None
    if wcg_member and wcg_code:
        wcg_data = fetch_wcg_data(wcg_member, wcg_code)
    else:
        print("⚠️  WCG credentials not set (WCG_MEMBER_NAME, WCG_VERIFICATION_CODE)")
    
    # Fetch F@H data (if username available)
    fah_data = None
    if fah_username:
        fah_data = fetch_fah_data(fah_username)
    else:
        print("⚠️  F@H username not set (FAH_USERNAME)")
    
    # Update README with whatever data we have
    if wcg_data or fah_data:
        update_readme(
            wcg_data, 
            fah_data, 
            wcg_member or "not_set",
            fah_username or "not_set"
        )
        print("\n✅ Done! Check your README.md")
    else:
        print("\n❌ No data fetched. Set at least one platform's credentials.")
        exit(1)


if __name__ == "__main__":
    main()
