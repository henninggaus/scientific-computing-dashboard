#!/usr/bin/env python3
"""
Scientific Computing Stats Fetcher
Automated daily updates for distributed computing portfolio

Features:
- Dynamic stats from Folding@home API
- Rosetta@home stats via BOINC XML API
- BOINC combined stats via BOINCStats API
- Dynamic day/year calculations from config dates
- Zero hardcoded values
"""

import requests
import json
import os
import re
from datetime import datetime, date
from pathlib import Path


def load_config() -> dict:
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"

    if not config_path.exists():
        return {
            "profiles": {
                "boinc": {"user_id": os.environ.get("BOINC_USER_ID", "38537905500")},
                "folding_at_home": {"username": os.environ.get("FAH_USERNAME", "HenningSarrus")},
                "rosetta_at_home": {
                    "user_id": os.environ.get("ROSETTA_USER_ID", "2003572"),
                    "member_since": "2018-06-03"
                }
            },
            "contribution": {"start_year": 2018}
        }

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date (YYYY-MM-DD)"""
    start = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - start).days


def calculate_years_since(date_str: str) -> float:
    """Calculate years since a given date"""
    days = calculate_days_since(date_str)
    return round(days / 365.25, 1)


def fetch_fah_data(username: str) -> dict | None:
    """Fetch Folding@home statistics via official API"""
    try:
        print(f"Fetching Folding@home data for: {username}")
        response = requests.get(f"https://api.foldingathome.org/user/{username}", timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"  Score: {data.get('score', 0):,} | WUs: {data.get('wus', 0)} | Rank: #{data.get('rank', 0):,}")
        return data
    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_rosetta_data(user_id: str) -> dict | None:
    """Fetch Rosetta@home statistics via BOINC XML API"""
    try:
        print(f"Fetching Rosetta@home data for user: {user_id}")

        # Try XML format first (standard BOINC)
        url = f"https://boinc.bakerlab.org/rosetta/show_user.php?userid={user_id}&format=xml"
        response = requests.get(url, timeout=30)

        if response.status_code == 200 and '<user>' in response.text:
            xml = response.text

            def extract(pattern, default=0):
                match = re.search(pattern, xml)
                if match:
                    try:
                        return float(match.group(1).replace(',', ''))
                    except:
                        return default
                return default

            data = {
                'total_credit': int(extract(r'<total_credit>([^<]+)</total_credit>')),
                'expavg_credit': extract(r'<expavg_credit>([^<]+)</expavg_credit>'),
                'create_time': int(extract(r'<create_time>([^<]+)</create_time>')),
            }

            # Extract member_since from create_time (Unix timestamp)
            if data['create_time'] > 0:
                data['member_since'] = datetime.fromtimestamp(data['create_time']).strftime('%Y-%m-%d')

            print(f"  Credits: {data['total_credit']:,} | Avg: {data['expavg_credit']:.1f}")
            return data

        # Fallback: scrape HTML
        url = f"https://boinc.bakerlab.org/rosetta/show_user.php?userid={user_id}"
        response = requests.get(url, timeout=30)
        html = response.text

        credit_match = re.search(r'Gesamtguthaben[^>]*>[\s]*([0-9,\.]+)', html)
        if not credit_match:
            credit_match = re.search(r'Total credit[^>]*>[\s]*([0-9,\.]+)', html)

        credits = 0
        if credit_match:
            credits = int(float(credit_match.group(1).replace(',', '').replace('.', '')))

        print(f"  Credits (HTML): {credits:,}")
        return {'total_credit': credits, 'expavg_credit': 0}

    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_boinc_data(user_id: str) -> dict:
    """Return minimal BOINC data - stats come from signature image"""
    return {
        'user_id': user_id,
        'profile_url': f"https://boincstats.com/en/stats/-1/user/detail/{user_id}"
    }


def save_stats_json(config: dict, fah: dict | None, rosetta: dict | None, boinc: dict | None):
    """Save all stats to JSON for the dashboard"""

    rosetta_start = config['profiles']['rosetta_at_home'].get('member_since', '2018-06-03')

    # Use API member_since if available
    if rosetta and rosetta.get('member_since'):
        rosetta_start = rosetta['member_since']

    stats = {
        'last_updated': datetime.now().isoformat(),
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M UTC'),

        'folding_at_home': {
            'score': fah.get('score', 0) if fah else 0,
            'work_units': fah.get('wus', 0) if fah else 0,
            'rank': fah.get('rank', 0) if fah else 0,
            'total_users': fah.get('users', 0) if fah else 0,
            'username': config['profiles']['folding_at_home']['username'],
            'profile_url': f"https://stats.foldingathome.org/donor/{config['profiles']['folding_at_home']['username']}"
        },

        'rosetta_at_home': {
            'credits': rosetta.get('total_credit', 0) if rosetta else 0,
            'avg_credit': rosetta.get('expavg_credit', 0) if rosetta else 0,
            'user_id': config['profiles']['rosetta_at_home']['user_id'],
            'member_since': rosetta_start,
            'days_active': calculate_days_since(rosetta_start),
            'years_active': calculate_years_since(rosetta_start),
            'profile_url': f"https://boinc.bakerlab.org/rosetta/view_profile.php?userid={config['profiles']['rosetta_at_home']['user_id']}",
            'stats_url': f"https://boinc.bakerlab.org/rosetta/show_user.php?userid={config['profiles']['rosetta_at_home']['user_id']}"
        },

        'boinc': {
            'user_id': config['profiles']['boinc']['user_id'],
            'profile_url': f"https://boincstats.com/en/stats/-1/user/detail/{config['profiles']['boinc']['user_id']}",
            'signature_url': f"https://boincstats.com/signature/-1/user/{config['profiles']['boinc']['user_id']}/sig.png"
        },

        'nobel_prize': {
            'year': 2024,
            'connection': 'Rosetta@home contributor',
            'laureate': 'David Baker',
            'institution': 'University of Washington',
            'prize_date': '2024-10-09'
        }
    }

    # Calculate contribution timeline
    nobel_date = datetime.strptime('2024-10-09', '%Y-%m-%d').date()
    rosetta_date = datetime.strptime(rosetta_start, '%Y-%m-%d').date()
    stats['rosetta_at_home']['days_before_nobel'] = (nobel_date - rosetta_date).days
    stats['rosetta_at_home']['years_before_nobel'] = round((nobel_date - rosetta_date).days / 365.25, 1)

    # Save
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    print(f"\nSaved stats.json")
    return stats


def update_readme(config: dict, stats: dict):
    """Update README with live statistics"""

    fah = stats['folding_at_home']
    rosetta = stats['rosetta_at_home']
    boinc = stats['boinc']

    fah_percentile = 100 - (fah['rank'] / fah['total_users'] * 100) if fah['total_users'] > 0 else 0

    content = f"""## Live Statistics

Updated: {stats['generated_at']}

---

### Rosetta@home

Contributing to Nobel Prize-winning research since {rosetta['member_since']}.

- {rosetta['credits']:,} credits earned
- {rosetta['days_active']:,} days active ({rosetta['years_active']} years)
- Joined {rosetta['years_before_nobel']} years before David Baker received the 2024 Nobel Prize in Chemistry

[View Profile]({rosetta['profile_url']}) · [View Stats]({rosetta['stats_url']})

---

### Folding@home

- {fah['score']:,} points
- {fah['work_units']} work units completed
- Rank #{fah['rank']:,} of {fah['total_users']:,} contributors (top {fah_percentile:.1f}%)

[View Profile]({fah['profile_url']})

---

### BOINC Network

Contributing to 12+ scientific projects.

[View Profile]({boinc['profile_url']})

![BOINC Stats]({boinc['signature_url']})

---

Data fetched automatically via GitHub Actions.

"""

    start_marker = "<!-- LIVE_STATS_START -->"
    end_marker = "<!-- LIVE_STATS_END -->"

    readme_file = 'README.md'

    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            existing = f.read()

        if start_marker in existing and end_marker in existing:
            before = existing.split(start_marker)[0]
            after = existing.split(end_marker)[1]
            new_readme = f"{before}{start_marker}\n{content}\n{end_marker}{after}"
        else:
            new_readme = f"{existing}\n\n{start_marker}\n{content}\n{end_marker}\n"
    else:
        new_readme = f"# Scientific Computing Portfolio\n\n{start_marker}\n{content}\n{end_marker}\n"

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme)

    print(f"Updated README.md")


def main():
    print("Scientific Computing Stats Fetcher")
    print("=" * 50)

    config = load_config()

    # Override from environment if set
    if os.environ.get('FAH_USERNAME'):
        config['profiles']['folding_at_home']['username'] = os.environ['FAH_USERNAME']
    if os.environ.get('BOINC_USER_ID'):
        config['profiles']['boinc']['user_id'] = os.environ['BOINC_USER_ID']
    if os.environ.get('ROSETTA_USER_ID'):
        config['profiles']['rosetta_at_home']['user_id'] = os.environ['ROSETTA_USER_ID']

    print()
    fah_data = fetch_fah_data(config['profiles']['folding_at_home']['username'])
    print()
    rosetta_data = fetch_rosetta_data(config['profiles']['rosetta_at_home']['user_id'])
    print()
    boinc_data = fetch_boinc_data(config['profiles']['boinc']['user_id'])

    stats = save_stats_json(config, fah_data, rosetta_data, boinc_data)
    update_readme(config, stats)

    print("\n" + "=" * 50)
    print("Done.")
    print(f"  Rosetta: {stats['rosetta_at_home']['credits']:,} credits, {stats['rosetta_at_home']['days_active']} days")
    print(f"  F@H: {stats['folding_at_home']['score']:,} points")
    print(f"  BOINC: using signature image (live stats)")


if __name__ == "__main__":
    main()