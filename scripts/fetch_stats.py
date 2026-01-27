#!/usr/bin/env python3
"""
Scientific Computing Stats Fetcher
Fetches live statistics from multiple BOINC projects and Folding@home
Generates complete README from config.json - no hardcoded values.
"""

import asyncio
import aiohttp
import json
import os
import re
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

# Configuration
HISTORY_MAX_DAYS = 365
HISTORY_FILE = Path('data/stats.json')


def load_config() -> dict:
    """Load configuration from config.json"""
    config_paths = ['config.json', 'scripts/config.json', '../config.json']
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    raise FileNotFoundError("config.json not found")


def load_existing_stats() -> dict:
    """Load existing stats.json to preserve history"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"  ⚠ Could not load existing stats: {e}")
    return {}


def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date (YYYY-MM-DD)"""
    start = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - start).days


def calculate_years_since(date_str: str) -> float:
    """Calculate years since a given date"""
    days = calculate_days_since(date_str)
    return round(days / 365.25, 1)


async def fetch_boinc_project(
        session: aiohttp.ClientSession,
        project_key: str,
        project_config: dict
) -> tuple[str, Optional[dict]]:
    """Fetch stats from a standard BOINC project using XML API"""

    name = project_config['name']
    base_url = project_config['url']
    user_id = project_config.get('user_id')

    if not user_id:
        return project_key, None

    try:
        url = f"{base_url}/show_user.php?userid={user_id}&format=xml"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                text = await response.text()
                if '<user>' in text:
                    def extract(pattern, default=0):
                        match = re.search(pattern, text)
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
                    print(f"  ✓ {name}: {data['credits']:,} credits")
                    return project_key, data

        print(f"  ✗ {name}: API error")
        return project_key, None

    except Exception as e:
        print(f"  ✗ {name}: {e}")
        return project_key, None


async def fetch_fah_data(session: aiohttp.ClientSession, username: str) -> Optional[dict]:
    """Fetch Folding@home statistics via official API"""
    try:
        url = f"https://api.foldingathome.org/user/{username}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                data = await response.json()
                print(f"  ✓ Folding@home: {data.get('score', 0):,} points | {data.get('wus', 0)} WUs")
                return data
        print("  ✗ Folding@home: API error")
        return None
    except Exception as e:
        print(f"  ✗ Folding@home: {e}")
        return None


async def fetch_all_projects(config: dict) -> tuple[Optional[dict], dict[str, Optional[dict]]]:
    """Fetch all projects concurrently"""

    print("Fetching data from APIs (parallel)...")
    print()

    async with aiohttp.ClientSession() as session:
        fah_username = config['profiles']['folding_at_home']['username']
        fah_task = fetch_fah_data(session, fah_username)

        projects_config = config['profiles']['projects']
        boinc_tasks = [
            fetch_boinc_project(session, key, proj_config)
            for key, proj_config in projects_config.items()
        ]

        fah_result = await fah_task
        boinc_results = await asyncio.gather(*boinc_tasks)
        boinc_data = {key: data for key, data in boinc_results}

        return fah_result, boinc_data


def build_current_stats(config: dict, fah_data: Optional[dict], boinc_data: dict[str, Optional[dict]]) -> dict:
    """Build the current stats snapshot"""

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

    # Folding@home
    fah_username = config['profiles']['folding_at_home']['username']
    if fah_data:
        stats['folding_at_home'] = {
            'score': fah_data.get('score', 0),
            'work_units': fah_data.get('wus', 0),
            'rank': fah_data.get('rank', 0),
            'total_users': fah_data.get('users', 0),
            'username': fah_username,
            'profile_url': f"https://stats.foldingathome.org/donor/{fah_username}"
        }

    # Process BOINC projects
    projects_config = config['profiles']['projects']

    for key, proj_config in projects_config.items():
        live_data = boinc_data.get(key)
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
        else:
            project_stats['credits'] = 0
            project_stats['live'] = False

        # Nobel connection for Rosetta
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

    # Category aggregation
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

    # BOINC combined profile
    boinc_user_id = config['profiles']['boinc_combined']['user_id']
    stats['boinc_combined'] = {
        'user_id': boinc_user_id,
        'profile_url': f"https://boincstats.com/en/stats/-1/user/detail/{boinc_user_id}",
        'signature_url': f"https://boincstats.com/signature/-1/user/{boinc_user_id}/sig.png"
    }

    if stats['totals']['earliest_join']:
        stats['totals']['total_days'] = calculate_days_since(stats['totals']['earliest_join'])
        stats['totals']['total_years'] = calculate_years_since(stats['totals']['earliest_join'])

    return stats


def create_history_entry(current_stats: dict) -> dict:
    """Create a compact history entry from current stats"""

    today = date.today().isoformat()

    entry = {
        'date': today,
        'boinc_credits': current_stats['totals']['boinc_credits'],
        'fah_score': current_stats.get('folding_at_home', {}).get('score', 0),
        'fah_wus': current_stats.get('folding_at_home', {}).get('work_units', 0),
        'projects': {}
    }

    for key, proj in current_stats['projects'].items():
        if proj.get('credits', 0) > 0:
            entry['projects'][key] = proj['credits']

    return entry


def update_history(existing_stats: dict, new_entry: dict) -> list[dict]:
    """Update history array with new entry, maintaining max days limit"""

    history = existing_stats.get('history', [])
    today = new_entry['date']

    history = [h for h in history if h['date'] != today]
    history.append(new_entry)
    history.sort(key=lambda x: x['date'])

    cutoff_date = (date.today() - timedelta(days=HISTORY_MAX_DAYS)).isoformat()
    history = [h for h in history if h['date'] >= cutoff_date]

    return history


def calculate_trends(history: list[dict], current_stats: dict) -> dict:
    """Calculate trends from historical data"""

    trends = {
        'data_points': len(history),
        'history_start': history[0]['date'] if history else None,
        'history_end': history[-1]['date'] if history else None,
    }

    if len(history) < 2:
        trends['status'] = 'insufficient_data'
        trends['message'] = 'Need at least 2 days of data for trends'
        return trends

    current_boinc = current_stats['totals']['boinc_credits']
    current_fah = current_stats.get('folding_at_home', {}).get('score', 0)

    def get_value_days_ago(days: int, key: str) -> Optional[int]:
        target_date = (date.today() - timedelta(days=days)).isoformat()
        candidates = [h for h in history if h['date'] <= target_date]
        if candidates:
            return candidates[-1].get(key, 0)
        return None

    # BOINC Trends
    boinc_trends = {}

    boinc_7d_ago = get_value_days_ago(7, 'boinc_credits')
    if boinc_7d_ago is not None:
        boinc_trends['last_7_days'] = current_boinc - boinc_7d_ago
        boinc_trends['avg_per_day_7d'] = round(boinc_trends['last_7_days'] / 7)

    boinc_30d_ago = get_value_days_ago(30, 'boinc_credits')
    if boinc_30d_ago is not None:
        boinc_trends['last_30_days'] = current_boinc - boinc_30d_ago
        boinc_trends['avg_per_day_30d'] = round(boinc_trends['last_30_days'] / 30)

    boinc_90d_ago = get_value_days_ago(90, 'boinc_credits')
    if boinc_90d_ago is not None:
        boinc_trends['last_90_days'] = current_boinc - boinc_90d_ago
        boinc_trends['avg_per_day_90d'] = round(boinc_trends['last_90_days'] / 90)

    if len(history) >= 2:
        first_entry = history[0]
        days_tracked = (date.today() - date.fromisoformat(first_entry['date'])).days
        if days_tracked > 0:
            total_gain = current_boinc - first_entry.get('boinc_credits', current_boinc)
            boinc_trends['avg_per_day_alltime'] = round(total_gain / days_tracked)

    trends['boinc'] = boinc_trends

    # Milestones
    milestones = []
    milestone_targets = [40_000_000, 50_000_000, 75_000_000, 100_000_000]

    daily_avg = (
            boinc_trends.get('avg_per_day_30d') or
            boinc_trends.get('avg_per_day_7d') or
            boinc_trends.get('avg_per_day_alltime') or
            0
    )

    if daily_avg > 0:
        for target in milestone_targets:
            if current_boinc < target:
                remaining = target - current_boinc
                days_to_target = remaining // daily_avg
                target_date = (date.today() + timedelta(days=days_to_target)).isoformat()
                milestones.append({
                    'target': target,
                    'target_formatted': f"{target:,}",
                    'remaining': remaining,
                    'days_to_reach': days_to_target,
                    'estimated_date': target_date
                })

    trends['milestones'] = milestones

    # Folding@home trends
    fah_trends = {}

    fah_7d_ago = get_value_days_ago(7, 'fah_score')
    if fah_7d_ago is not None and fah_7d_ago > 0:
        fah_trends['last_7_days'] = current_fah - fah_7d_ago
        fah_trends['avg_per_day_7d'] = round(fah_trends['last_7_days'] / 7)

    fah_30d_ago = get_value_days_ago(30, 'fah_score')
    if fah_30d_ago is not None and fah_30d_ago > 0:
        fah_trends['last_30_days'] = current_fah - fah_30d_ago
        fah_trends['avg_per_day_30d'] = round(fah_trends['last_30_days'] / 30)

    trends['fah'] = fah_trends

    # Most active projects
    project_activity = []
    for key, proj in current_stats['projects'].items():
        current_credits = proj.get('credits', 0)
        if current_credits == 0:
            continue

        credits_30d_ago = None
        target_date = (date.today() - timedelta(days=30)).isoformat()
        candidates = [h for h in history if h['date'] <= target_date]
        if candidates:
            credits_30d_ago = candidates[-1].get('projects', {}).get(key)

        if credits_30d_ago is not None:
            gain = current_credits - credits_30d_ago
            if gain > 0:
                project_activity.append({
                    'key': key,
                    'name': proj['name'],
                    'gain_30d': gain,
                    'avg_per_day': round(gain / 30)
                })

    project_activity.sort(key=lambda x: x['gain_30d'], reverse=True)
    trends['most_active_projects'] = project_activity[:5]

    return trends


def generate_readme(config: dict, current_stats: dict) -> str:
    """Generate complete README from config and live stats"""

    fah_username = config['profiles']['folding_at_home']['username']
    fah_profile = f"https://stats.foldingathome.org/donor/{fah_username}"
    boinc_user_id = config['profiles']['boinc_combined']['user_id']
    boinc_profile = f"https://boincstats.com/en/stats/-1/user/detail/{boinc_user_id}"
    boinc_sig = f"https://boincstats.com/signature/-1/user/{boinc_user_id}/sig.png"

    fah = current_stats.get('folding_at_home', {})
    projects = current_stats['projects']
    totals = current_stats['totals']

    # Find Nobel project (Rosetta)
    nobel_project = None
    for key, proj in projects.items():
        if proj.get('nobel_connection'):
            nobel_project = proj
            break

    # Sort projects by credits
    sorted_projects = sorted(
        projects.items(),
        key=lambda x: x[1].get('credits', 0),
        reverse=True
    )

    # Build project table
    project_rows = []
    for key, proj in sorted_projects:
        name = proj['name']
        url = proj.get('profile_url', proj['url'])
        credits = proj.get('credits', 0)
        credits_str = f"{credits:,}" if credits > 0 else "—"
        since = proj['member_since'][:7]  # YYYY-MM format
        project_rows.append(f"| [{name}]({url}) | {credits_str} | {since} |")

    project_table = "\n".join(project_rows)

    # Nobel section
    nobel_section = ""
    if nobel_project:
        nobel_section = f"""
### Nobel Prize Connection

I joined [{nobel_project['name']}]({nobel_project.get('profile_url', nobel_project['url'])}) in {nobel_project['member_since'][:7]} — about {nobel_project.get('years_before_nobel', 6)} years before David Baker received the 2024 Nobel Prize in Chemistry for computational protein design.

- **{nobel_project.get('credits', 0):,}** credits
- **{nobel_project.get('days_active', 0):,}** days contributing

---
"""

    readme = f"""# Scientific Computing Portfolio

I contribute idle computing power to distributed research projects — protein folding, number theory, astronomy, and more. This repo tracks my contributions automatically.

---

## Statistics

*Updated: {current_stats['generated_at']}*

- **{totals['boinc_projects']}** active BOINC projects
- **{totals['boinc_credits']:,}** total BOINC credits
- **{totals.get('total_years', 0)}** years contributing

---
{nobel_section}
### Folding@home

- {fah.get('score', 0):,} points
- {fah.get('work_units', 0)} work units

[Profile]({fah_profile})

---

### BOINC Projects

| Project | Credits | Since |
|---------|--------:|-------|
{project_table}

![BOINC Stats]({boinc_sig})

[Combined Profile]({boinc_profile})

---

## How it works

A GitHub Action runs daily, fetches live data from the Folding@home and BOINC APIs, and updates this README. No hardcoded numbers — everything comes from `config.json` and live API calls.

```
GitHub Actions (daily)
       │
       ▼
  fetch_stats.py ──► APIs (F@H, BOINC projects)
       │
       ├──► README.md (this file)
       └──► data/stats.json
```

---

## Join in

- [Folding@home](https://foldingathome.org/) — protein folding for disease research
- [BOINC](https://boinc.berkeley.edu/) — dozens of research projects to choose from

---

MIT License
"""
    return readme


def save_stats(stats: dict):
    """Save stats to JSON file"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    print(f"✓ Saved {HISTORY_FILE}")


def save_readme(content: str):
    """Save generated README"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Saved README.md")


async def main():
    print("=" * 60)
    print("Scientific Computing Stats Fetcher")
    print("=" * 60)
    print()

    config = load_config()

    if os.environ.get('FAH_USERNAME'):
        config['profiles']['folding_at_home']['username'] = os.environ['FAH_USERNAME']

    existing_stats = load_existing_stats()
    fah_data, boinc_data = await fetch_all_projects(config)

    print()

    current_stats = build_current_stats(config, fah_data, boinc_data)
    history_entry = create_history_entry(current_stats)
    history = update_history(existing_stats, history_entry)
    trends = calculate_trends(history, current_stats)

    final_stats = {
        'current': current_stats,
        'history': history,
        'trends': trends
    }

    save_stats(final_stats)

    readme_content = generate_readme(config, current_stats)
    save_readme(readme_content)

    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Total BOINC Credits: {current_stats['totals']['boinc_credits']:,}")
    print(f"  Active Projects: {current_stats['totals']['boinc_projects']}")
    print(f"  Contributing since: {current_stats['totals']['earliest_join']}")

    if current_stats.get('folding_at_home'):
        print(f"  Folding@home: {current_stats['folding_at_home']['score']:,} points")


if __name__ == "__main__":
    asyncio.run(main())