#!/usr/bin/env python3
"""
WCG Stats Fetcher - MVP VERSION
Just fetches the data and shows it raw in README
"""

import requests
import json
import os
from datetime import datetime


def fetch_wcg_data(member_name: str, verification_code: str):
    """Fetch raw WCG data from API"""

    url = f"https://www.worldcommunitygrid.org/api/members/{member_name}/results"

    params = {
        'code': verification_code,
        'format': 'json',
        'limit': 10  # Get 10 results to see structure
    }

    try:
        print(f"🔄 Fetching WCG data for: {member_name}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        print(f" Successfully fetched data!")

        return data

    except requests.exceptions.RequestException as e:
        print(f" Error: {e}")
        return None


def update_readme(data, member_name: str):
    """Update README with raw JSON data"""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

    # Convert data to pretty JSON
    json_str = json.dumps(data, indent=2)

    readme_content = f"""## 🧬 WCG API Response (Raw Data)

**Member:** `{member_name}`  
**Last Updated:** `{timestamp}`

### 📊 Raw API Response:

```json
{json_str}
```

---

**Status:** This is the raw API response. Will be formatted nicely soon!

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

    print(f" Updated {readme_file}")


def main():
    """Main function"""

    # Get credentials from environment
    member_name = os.environ.get('WCG_MEMBER_NAME')
    verification_code = os.environ.get('WCG_VERIFICATION_CODE')

    if not member_name or not verification_code:
        print(" ERROR: Set WCG_MEMBER_NAME and WCG_VERIFICATION_CODE environment variables")
        exit(1)

    print("🚀 WCG Stats Fetcher - MVP Version")

    # Fetch data
    data = fetch_wcg_data(member_name, verification_code)

    if data:
        # Update README with raw data
        update_readme(data, member_name)
        print(" Done! Check your README.md to see the raw API response!")
    else:
        print(" Failed to fetch data")
        exit(1)


if __name__ == "__main__":
    main()
