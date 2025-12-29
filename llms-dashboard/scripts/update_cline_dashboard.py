#!/usr/bin/env python3
"""Cline Dashboard Generator"""
import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path(__file__).parent.parent / "data" / "cline_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "cline_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "cline_dashboard.html"

def main():
    with open(HISTORY_FILE) as f:
        data = json.load(f)
    
    s = data['summary']
    recent_rows = ""
    for t in data['sessions'][:30]:
        ts = datetime.fromtimestamp(t['ts']/1000).strftime('%Y-%m-%d') if t.get('ts') else 'N/A'
        task = t.get('task', '')[:60] + ('...' if len(t.get('task', '')) > 60 else '')
        tokens = f"{t.get('tokensIn',0) + t.get('tokensOut',0):,}"
        cost = f"${t.get('cost',0):.2f}"
        recent_rows += f'<tr class="border-b border-gray-700"><td class="p-2 text-gray-400">{ts}</td><td class="p-2 text-gray-300">{task}</td><td class="p-2 text-blue-400">{tokens}</td><td class="p-2 text-green-400">{cost}</td></tr>'
    
    with open(TEMPLATE_FILE) as f:
        html = f.read()
    
    replacements = {
        '{{TIMESTAMP}}': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '{{TOTAL_TASKS}}': str(s['total_tasks']),
        '{{TOTAL_COST}}': f"{s['total_cost']:.2f}",
        '{{TOKENS_IN}}': f"{s['total_tokens_in']:,}",
        '{{TOKENS_OUT}}': f"{s['total_tokens_out']:,}",
        '{{CACHE_WRITES}}': f"{s['total_cache_writes']:,}",
        '{{WORKSPACES}}': str(s['unique_workspaces']),
        '{{DAILY_DATA}}': json.dumps(data['daily_stats']),
        '{{WORKSPACE_DATA}}': json.dumps(data['workspaces'][:8]),
        '{{RECENT_TASKS}}': recent_rows,
    }
    for k, v in replacements.items():
        html = html.replace(k, v)
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {OUTPUT_FILE}")
    print(f"   Tasks: {s['total_tasks']}, Cost: ${s['total_cost']:.2f}")

if __name__ == "__main__":
    main()
