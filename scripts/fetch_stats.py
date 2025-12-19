#!/usr/bin/env python3
"""
Scientific Computing Stats Fetcher
Fetches live statistics from multiple BOINC projects and Folding@home
"""

import json
import os
import re
import requests
from datetime import datetime, date
from pathlib import Path


def load_config() -> dict:
    """Load configuration from config.json"""
    config_paths = ['config.json', 'scripts/config.json', '../config.json']
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    raise FileNotFoundError("config.json not found")


def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date (YYYY-MM-DD)"""
    start = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - start).days


def calculate_years_since(date_str: str) -> float:
    """Calculate years since a given date"""
    days = calculate_days_since(date_str)
    return round(days / 365.25, 1)


def fetch_boinc_project(project_key: str, project_config: dict) -> dict | None:
    """Fetch stats from a standard BOINC project using XML API"""

    name = project_config['name']
    base_url = project_config['url']
    user_id = project_config.get('user_id')

    if not user_id:
        return None

    try:
        print(f"Fetching {name} data for user: {user_id}")

        url = f"{base_url}/show_user.php?userid={user_id}&format=xml"
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
                'credits': int(extract(r'<total_credit>([^<]+)</total_credit>')),
                'avg_credit': round(extract(r'<expavg_credit>([^<]+)</expavg_credit>'), 2),
            }

            print(f"  ✓ Credits: {data['credits']:,}")
            return data
        else:
            print(f"  ✗ API returned non-XML response")
            return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def fetch_fah_data(username: str) -> dict | None:
    """Fetch Folding@home statistics via official API"""
    try:
        print(f"Fetching Folding@home data for: {username}")
        response = requests.get(f"https://api.foldingathome.org/user/{username}", timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"  ✓ Score: {data.get('score', 0):,} | WUs: {data.get('wus', 0)}")
        return data
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def build_stats(config: dict) -> dict:
    """Build complete stats object from all sources"""

    print("=" * 60)
    print("Scientific Computing Stats Fetcher")
    print("=" * 60)
    print()

    stats = {
        'last_updated': datetime.now().isoformat(),
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M UTC'),
        'projects': {},
        'categories': {},
        'totals': {
            'boinc_credits': 0,
            'boinc_projects': 0,
            'earliest_join': None
        }
    }

    # Fetch Folding@home
    fah_data = fetch_fah_data(config['profiles']['folding_at_home']['username'])
    if fah_data:
        stats['folding_at_home'] = {
            'score': fah_data.get('score', 0),
            'work_units': fah_data.get('wus', 0),
            'rank': fah_data.get('rank', 0),
            'total_users': fah_data.get('users', 0),
            'username': config['profiles']['folding_at_home']['username'],
            'profile_url': f"https://stats.foldingathome.org/donor/{config['profiles']['folding_at_home']['username']}"
        }

    print()

    # Fetch each BOINC project
    projects_config = config['profiles']['projects']

    for key, proj_config in projects_config.items():
        print()

        live_data = fetch_boinc_project(key, proj_config)
        member_since = proj_config.get('member_since', '2020-01-01')

        project_stats = {
            'name': proj_config['name'],
            'category': proj_config['category'],
            'description': proj_config['description'],
            'url': proj_config['url'],
            'member_since': member_since,
            'days_active': calculate_days_since(member_since),
            'years_active': calculate_years_since(member_since),
        }

        if proj_config.get('user_id'):
            project_stats['user_id'] = proj_config['user_id']
            project_stats['profile_url'] = f"{proj_config['url']}/show_user.php?userid={proj_config['user_id']}"

        if live_data:
            project_stats['credits'] = live_data['credits']
            project_stats['avg_credit'] = live_data['avg_credit']
            project_stats['live'] = True
        elif proj_config.get('fallback_credits'):
            project_stats['credits'] = proj_config['fallback_credits']
            project_stats['live'] = False
            print(f"  Using fallback credits for {proj_config['name']}")
        else:
            project_stats['credits'] = 0
            project_stats['live'] = False

        if proj_config.get('uses_image'):
            project_stats['image_url'] = (
                f"https://www.worldcommunitygrid.org/getDynamicImage.do?"
                f"memberName={proj_config['username']}&mnOn=true&stat=1&"
                f"imageNum=1&rankOn=true&projectsOn=true&special=true"
            )
            project_stats['member_id'] = proj_config.get('member_id')

        if proj_config.get('nobel_connection'):
            nobel_date = datetime.strptime('2024-10-09', '%Y-%m-%d').date()
            join_date = datetime.strptime(member_since, '%Y-%m-%d').date()
            project_stats['days_before_nobel'] = (nobel_date - join_date).days
            project_stats['years_before_nobel'] = round((nobel_date - join_date).days / 365.25, 1)
            project_stats['nobel_connection'] = True

        stats['projects'][key] = project_stats

        if project_stats.get('credits', 0) > 0:
            stats['totals']['boinc_credits'] += project_stats['credits']
            stats['totals']['boinc_projects'] += 1

        if stats['totals']['earliest_join'] is None or member_since < stats['totals']['earliest_join']:
            stats['totals']['earliest_join'] = member_since

    categories = config.get('categories', {})
    for cat_key, cat_config in categories.items():
        cat_credits = sum(
            p.get('credits', 0)
            for p in stats['projects'].values()
            if p.get('category') == cat_key
        )
        cat_projects = sum(
            1 for p in stats['projects'].values()
            if p.get('category') == cat_key
        )
        stats['categories'][cat_key] = {
            'name': cat_config['name'],
            'icon': cat_config['icon'],
            'color': cat_config['color'],
            'total_credits': cat_credits,
            'project_count': cat_projects
        }

    stats['boinc_combined'] = {
        'user_id': config['profiles']['boinc_combined']['user_id'],
        'profile_url': f"https://boincstats.com/en/stats/-1/user/detail/{config['profiles']['boinc_combined']['user_id']}",
        'signature_url': f"https://boincstats.com/signature/-1/user/{config['profiles']['boinc_combined']['user_id']}/sig.png"
    }

    if stats['totals']['earliest_join']:
        stats['totals']['total_days'] = calculate_days_since(stats['totals']['earliest_join'])
        stats['totals']['total_years'] = calculate_years_since(stats['totals']['earliest_join'])

    return stats


def save_stats(stats: dict):
    """Save stats to JSON file"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    print()
    print(f"✓ Saved stats.json")


def update_readme(stats: dict):
    """Update README with live statistics"""

    projects = stats['projects']
    fah = stats.get('folding_at_home', {})
    rosetta = projects.get('rosetta', {})

    # Sort projects by credits (excluding rosetta, shown separately)
    sorted_projects = sorted(
        [(k, v) for k, v in projects.items() if k != 'rosetta'],
        key=lambda x: x[1].get('credits', 0),
        reverse=True
    )

    # Nobel section
    nobel_section = ""
    if rosetta.get('nobel_connection'):
        nobel_section = f"""
### 🏆 Nobel Prize Connection

> **Rosetta@home** — Contributing to David Baker's Nobel Prize-winning research

I joined Rosetta@home on **{rosetta['member_since']}** — **{rosetta.get('years_before_nobel', 6.4)} years before** David Baker received the **2024 Nobel Prize in Chemistry** for computational protein design.

- **{rosetta.get('credits', 0):,}** credits earned
- **{rosetta.get('days_active', 0):,}** days contributing ({rosetta.get('years_active', 0)} years)

[View Rosetta Profile]({rosetta.get('profile_url', '#')})

---

"""

    content = f"""## Live Statistics

Updated: {stats['generated_at']}

### Overview

- **{stats['totals']['boinc_projects']}** active BOINC projects
- **{stats['totals']['boinc_credits']:,}** total BOINC credits
- **{stats['totals']['total_years']}** years contributing

---
{nobel_section}
### Folding@home

- {fah.get('score', 0):,} points
- {fah.get('work_units', 0)} work units

[View Profile]({fah.get('profile_url', '#')})

---

### Other BOINC Projects

| Project | Credits | Member Since |
|---------|--------:|--------------|
"""

    for key, proj in sorted_projects:
        credits_str = f"{proj.get('credits', 0):,}" if proj.get('credits', 0) > 0 else "—"
        content += f"| [{proj['name']}]({proj.get('profile_url', proj['url'])}) | {credits_str} | {proj['member_since']} |\n"

    content += f"""
---

### BOINC Combined

![BOINC Stats]({stats['boinc_combined']['signature_url']})

[View Full Profile]({stats['boinc_combined']['profile_url']})

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
            new_content = before + start_marker + "\n" + content + end_marker + after

            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✓ Updated README.md")
        else:
            print("  README markers not found, skipping update")
    else:
        print("  README.md not found, skipping update")


def main():
    config = load_config()

    if os.environ.get('FAH_USERNAME'):
        config['profiles']['folding_at_home']['username'] = os.environ['FAH_USERNAME']

    stats = build_stats(config)
    save_stats(stats)
    update_readme(stats)

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Total BOINC Credits: {stats['totals']['boinc_credits']:,}")
    print(f"  Active Projects: {stats['totals']['boinc_projects']}")
    print(f"  Contributing since: {stats['totals']['earliest_join']}")
    if stats.get('folding_at_home'):
        print(f"  Folding@home: {stats['folding_at_home']['score']:,} points")


if __name__ == "__main__":
    main()