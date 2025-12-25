#!/usr/bin/env python3
"""
Gemini Dashboard Generator

Reads aggregated history data and generates a full HTML dashboard.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Constants
HISTORY_FILE = Path(__file__).parent.parent / "data" / "gemini_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "gemini_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "gemini_dashboard.html"
ACCOUNTS_FILE = Path.home() / ".gemini" / "google_accounts.json"

def load_history():
    """Load aggregated history data"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {HISTORY_FILE} not found. Run aggregate_gemini_history.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {HISTORY_FILE}: {e}")
        sys.exit(1)

def get_user_email():
    """Get active user email from config"""
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('active', 'Unknown User')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 'Unknown User'

def format_duration(seconds):
    """Format seconds to human readable duration"""
    if not seconds:
        return '0s'
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {int(seconds % 60)}s"
    else:
        return f"{int(seconds)}s"

def generate_dashboard():
    sessions = load_history()
    user_email = get_user_email()
    
    # Calculate totals
    total_sessions = len(sessions)
    total_messages = sum(s.get('totalMessages', 0) for s in sessions)
    user_messages = sum(s.get('userMessages', 0) for s in sessions)
    total_duration_seconds = sum(s.get('durationSeconds', 0) for s in sessions)
    total_input_tokens = sum(s.get('totalInputTokens', 0) for s in sessions)
    total_output_tokens = sum(s.get('totalOutputTokens', 0) for s in sessions)
    total_tokens = total_input_tokens + total_output_tokens
    
    # Prepare chart data (daily aggregation)
    daily_stats = defaultdict(lambda: {'sessions': 0, 'messages': 0, 'input_tokens': 0, 'output_tokens': 0, 'durations': []})
    
    for s in sessions:
        start_time = s.get('startTime')
        if start_time:
            date_str = start_time.split('T')[0]
            daily_stats[date_str]['sessions'] += 1
            daily_stats[date_str]['messages'] += s.get('totalMessages', 0)
            daily_stats[date_str]['input_tokens'] += s.get('totalInputTokens', 0)
            daily_stats[date_str]['output_tokens'] += s.get('totalOutputTokens', 0)
            # Convert to minutes
            daily_stats[date_str]['durations'].append(s.get('durationSeconds', 0) / 60)
            
    sorted_dates = sorted(daily_stats.keys())
    chart_sessions = [daily_stats[d]['sessions'] for d in sorted_dates]
    chart_messages = [daily_stats[d]['messages'] for d in sorted_dates]
    chart_input_tokens = [daily_stats[d]['input_tokens'] for d in sorted_dates]
    chart_output_tokens = [daily_stats[d]['output_tokens'] for d in sorted_dates]
    chart_durations = [daily_stats[d]['durations'] for d in sorted_dates]
    
    # Calculate Y-Axis Max for Boxplot (90th percentile to exclude extreme outliers)
    all_durations = []
    for d_list in chart_durations:
        all_durations.extend(d_list)
    
    if all_durations:
        all_durations.sort()
        idx = int(len(all_durations) * 0.90)
        y_axis_max = all_durations[idx]
        y_axis_max = int(y_axis_max * 1.1) # 10% padding
        y_axis_max = max(y_axis_max, 10)
    else:
        y_axis_max = 60

    # Generate Recent Sessions Rows
    recent_rows = ""
    for s in sessions[:20]:  # Top 20 recent
        date_str = s.get('startTime', '').split('T')[0]
        duration = format_duration(s.get('durationSeconds', 0))
        msgs = s.get('totalMessages', 0)
        stype = s.get('type', 'CLI')
        summary = s.get('summary')
        if not summary:
             summary = s.get('projectHash', 'N/A')[:8] + "..."
        
        # Truncate long summaries
        if len(summary) > 80:
            summary = summary[:77] + "..."
            
        type_badge = "badge-blue" if stype == "CLI" else "badge-purple"
        
        input_tokens = s.get('totalInputTokens', 0)
        output_tokens = s.get('totalOutputTokens', 0)
        if input_tokens or output_tokens:
            tokens_str = f"{input_tokens:,} / {output_tokens:,}"
        else:
            tokens_str = "-"
        
        recent_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3"><span class="badge {type_badge}">{stype}</span></td>
            <td class="p-3 text-gray-300">{date_str}</td>
            <td class="p-3 text-gray-400">{duration}</td>
            <td class="p-3 text-blue-400 font-mono">{msgs}</td>
            <td class="p-3 text-gray-400 text-xs">{tokens_str}</td>
            <td class="p-3 text-gray-400 text-sm">{summary}</td>
        </tr>
        """

    # Read Template
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: {TEMPLATE_FILE} not found")
        sys.exit(1)

    # Replace Placeholders
    html = template.replace('{{USER_EMAIL}}', user_email)
    html = html.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    html = html.replace('{{TOTAL_SESSIONS}}', str(total_sessions))
    html = html.replace('{{TOTAL_MESSAGES}}', str(total_messages))
    html = html.replace('{{USER_MESSAGES}}', str(user_messages))
    html = html.replace('{{TOTAL_DURATION}}', format_duration(total_duration_seconds))
    html = html.replace('{{TOTAL_TOKENS}}', f"{total_tokens:,}")
    html = html.replace('{{CHART_DATES}}', json.dumps(sorted_dates))
    html = html.replace('{{CHART_SESSIONS}}', json.dumps(chart_sessions))
    html = html.replace('{{CHART_MESSAGES}}', json.dumps(chart_messages))
    html = html.replace('{{CHART_INPUT_TOKENS}}', json.dumps(chart_input_tokens))
    html = html.replace('{{CHART_OUTPUT_TOKENS}}', json.dumps(chart_output_tokens))
    html = html.replace('{{CHART_DURATIONS}}', json.dumps(chart_durations))
    html = html.replace('{{Y_AXIS_MAX}}', str(y_axis_max))
    html = html.replace('{{RECENT_SESSIONS_ROWS}}', recent_rows)

    # Write Output
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html)
        
    print(f"Dashboard generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dashboard()
