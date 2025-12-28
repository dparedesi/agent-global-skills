#!/usr/bin/env python3
"""
Claude History Aggregator

Scans all session files in ~/.claude/projects/ and consolidates them
into a single historical database for analysis.

Output: ~/.claude/skills/llms-dashboard/data/claude_history.json
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Constants
# CLAUDE_PROJECTS_DIR: Where Claude Code stores session transcripts.
# Each subdirectory represents a project, containing .jsonl files (one per session).
# Format: ~/.claude/projects/<project-hash>/<session-id>.jsonl
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

# OUTPUT_DIR: Directory for generated data files.
# Created automatically if it doesn't exist.
OUTPUT_DIR = Path(__file__).parent.parent / "data"

# OUTPUT_FILE: Consolidated historical data for all sessions.
# Contains daily_stats, sessions, project_stats, and model_totals.
# This file can grow large (several MB) for heavy Claude Code users.
OUTPUT_FILE = OUTPUT_DIR / "claude_history.json"

def parse_jsonl_file(filepath):
    """Parse a JSONL file and extract session data"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    messages.append(data)
                except json.JSONDecodeError as e:
                    # Skip malformed lines
                    continue
    except Exception as e:
        print(f"  ⚠️  Error reading {filepath.name}: {e}")
        return []
    return messages

def extract_session_data(messages, project_path, filename):
    """Extract relevant data from session messages"""
    session = {
        'filename': filename,
        'project': project_path,
        'project_name': project_path.split('-')[-1] if project_path else 'unknown',
        'session_id': None,
        'agent_id': None,
        'version': None,
        'git_branch': None,
        'start_time': None,
        'end_time': None,
        'duration_ms': 0,
        'message_count': 0,
        'user_messages': 0,
        'assistant_messages': 0,
        'tool_calls': 0,
        'models_used': defaultdict(lambda: {
            'input_tokens': 0,
            'output_tokens': 0,
            'cache_read': 0,
            'cache_creation': 0,
            'requests': 0
        }),
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_cache_read': 0,
        'total_cache_creation': 0,
    }
    
    timestamps = []
    
    for msg in messages:
        # Extract session metadata
        if not session['session_id'] and msg.get('sessionId'):
            session['session_id'] = msg.get('sessionId')
        if not session['agent_id'] and msg.get('agentId'):
            session['agent_id'] = msg.get('agentId')
        if not session['version'] and msg.get('version'):
            session['version'] = msg.get('version')
        if not session['git_branch'] and msg.get('gitBranch'):
            session['git_branch'] = msg.get('gitBranch')
        
        # Track timestamps
        if msg.get('timestamp'):
            try:
                ts = msg['timestamp']
                if isinstance(ts, str):
                    timestamps.append(ts)
            except (KeyError, TypeError):
                pass
        
        # Count messages
        session['message_count'] += 1
        msg_type = msg.get('type')
        
        if msg_type == 'user':
            session['user_messages'] += 1
        elif msg_type == 'assistant':
            session['assistant_messages'] += 1
            
            # Extract token usage from assistant messages
            message_data = msg.get('message', {})
            model = message_data.get('model', 'unknown')
            usage = message_data.get('usage', {})
            
            if usage:
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
                cache_read = usage.get('cache_read_input_tokens', 0)
                cache_creation = usage.get('cache_creation_input_tokens', 0)
                
                session['models_used'][model]['input_tokens'] += input_tokens
                session['models_used'][model]['output_tokens'] += output_tokens
                session['models_used'][model]['cache_read'] += cache_read
                session['models_used'][model]['cache_creation'] += cache_creation
                session['models_used'][model]['requests'] += 1
                
                session['total_input_tokens'] += input_tokens
                session['total_output_tokens'] += output_tokens
                session['total_cache_read'] += cache_read
                session['total_cache_creation'] += cache_creation
            
            # Count tool calls
            content = message_data.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        session['tool_calls'] += 1
    
    # Calculate time range
    if timestamps:
        timestamps.sort()
        session['start_time'] = timestamps[0]
        session['end_time'] = timestamps[-1]
        try:
            start = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
            end = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
            session['duration_ms'] = int((end - start).total_seconds() * 1000)
        except (ValueError, TypeError, AttributeError):
            pass
    
    # Convert defaultdict to regular dict for JSON serialization
    session['models_used'] = dict(session['models_used'])
    
    return session

def aggregate_all_sessions():
    """Scan all project directories and aggregate session data"""
    
    if not CLAUDE_PROJECTS_DIR.exists():
        print(f"❌ Projects directory not found: {CLAUDE_PROJECTS_DIR}")
        sys.exit(1)
    
    all_sessions = []
    daily_stats = defaultdict(lambda: {
        'date': None,
        'sessions': 0,
        'messages': 0,
        'user_messages': 0,
        'assistant_messages': 0,
        'tool_calls': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'cache_read': 0,
        'cache_creation': 0,
        'models': defaultdict(lambda: {'requests': 0, 'tokens': 0}),
        'projects': set()
    })
    
    model_totals = defaultdict(lambda: {
        'input_tokens': 0,
        'output_tokens': 0,
        'cache_read': 0,
        'cache_creation': 0,
        'requests': 0
    })
    
    project_stats = defaultdict(lambda: {
        'sessions': 0,
        'messages': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'first_session': None,
        'last_session': None
    })
    
    # Scan all project directories
    project_dirs = [d for d in CLAUDE_PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    print(f"📁 Found {len(project_dirs)} project directories")
    
    total_files = 0
    processed_files = 0
    
    for project_dir in project_dirs:
        project_path = project_dir.name
        jsonl_files = list(project_dir.glob("*.jsonl"))
        total_files += len(jsonl_files)
        
        print(f"\n📂 {project_path}")
        print(f"   Found {len(jsonl_files)} session files")
        
        for jsonl_file in jsonl_files:
            messages = parse_jsonl_file(jsonl_file)
            if not messages:
                continue
            
            session = extract_session_data(messages, project_path, jsonl_file.name)
            
            # Skip empty sessions
            if session['message_count'] == 0:
                continue
            
            all_sessions.append(session)
            processed_files += 1
            
            # Aggregate into daily stats
            if session['start_time']:
                try:
                    date = session['start_time'][:10]  # YYYY-MM-DD
                    daily_stats[date]['date'] = date
                    daily_stats[date]['sessions'] += 1
                    daily_stats[date]['messages'] += session['message_count']
                    daily_stats[date]['user_messages'] += session['user_messages']
                    daily_stats[date]['assistant_messages'] += session['assistant_messages']
                    daily_stats[date]['tool_calls'] += session['tool_calls']
                    daily_stats[date]['input_tokens'] += session['total_input_tokens']
                    daily_stats[date]['output_tokens'] += session['total_output_tokens']
                    daily_stats[date]['cache_read'] += session['total_cache_read']
                    daily_stats[date]['cache_creation'] += session['total_cache_creation']
                    daily_stats[date]['projects'].add(project_path)
                    
                    for model, usage in session['models_used'].items():
                        daily_stats[date]['models'][model]['requests'] += usage['requests']
                        daily_stats[date]['models'][model]['tokens'] += usage['input_tokens'] + usage['output_tokens']
                except (KeyError, ValueError, TypeError):
                    pass
            
            # Aggregate model totals
            for model, usage in session['models_used'].items():
                model_totals[model]['input_tokens'] += usage['input_tokens']
                model_totals[model]['output_tokens'] += usage['output_tokens']
                model_totals[model]['cache_read'] += usage['cache_read']
                model_totals[model]['cache_creation'] += usage['cache_creation']
                model_totals[model]['requests'] += usage['requests']
            
            # Aggregate project stats
            project_stats[project_path]['sessions'] += 1
            project_stats[project_path]['messages'] += session['message_count']
            project_stats[project_path]['input_tokens'] += session['total_input_tokens']
            project_stats[project_path]['output_tokens'] += session['total_output_tokens']
            
            if session['start_time']:
                if not project_stats[project_path]['first_session'] or session['start_time'] < project_stats[project_path]['first_session']:
                    project_stats[project_path]['first_session'] = session['start_time']
                if not project_stats[project_path]['last_session'] or session['start_time'] > project_stats[project_path]['last_session']:
                    project_stats[project_path]['last_session'] = session['start_time']
    
    # Convert daily stats for JSON serialization
    daily_list = []
    for date in sorted(daily_stats.keys()):
        day = daily_stats[date]
        day['projects'] = list(day['projects'])
        day['models'] = dict(day['models'])
        daily_list.append(day)
    
    # Build output structure
    output = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_sessions': len(all_sessions),
            'total_files_scanned': total_files,
            'files_with_data': processed_files,
            'total_projects': len(project_stats),
            'date_range': {
                'first': daily_list[0]['date'] if daily_list else None,
                'last': daily_list[-1]['date'] if daily_list else None,
                'days_with_activity': len(daily_list)
            },
            'totals': {
                'messages': sum(s['message_count'] for s in all_sessions),
                'user_messages': sum(s['user_messages'] for s in all_sessions),
                'assistant_messages': sum(s['assistant_messages'] for s in all_sessions),
                'tool_calls': sum(s['tool_calls'] for s in all_sessions),
                'input_tokens': sum(s['total_input_tokens'] for s in all_sessions),
                'output_tokens': sum(s['total_output_tokens'] for s in all_sessions),
                'cache_read': sum(s['total_cache_read'] for s in all_sessions),
                'cache_creation': sum(s['total_cache_creation'] for s in all_sessions),
            }
        },
        'model_totals': dict(model_totals),
        'project_stats': dict(project_stats),
        'daily_stats': daily_list,
        'sessions': all_sessions
    }
    
    return output

def main():
    print("🔍 Claude History Aggregator")
    print("=" * 50)
    print(f"📂 Source: {CLAUDE_PROJECTS_DIR}")
    print(f"💾 Output: {OUTPUT_FILE}")
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Aggregate all sessions
    data = aggregate_all_sessions()
    
    # Write output
    print(f"\n💾 Writing consolidated data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 AGGREGATION SUMMARY")
    print("=" * 50)
    summary = data['summary']
    print(f"\n📁 Projects: {summary['total_projects']}")
    print(f"📄 Session files scanned: {summary['total_files_scanned']}")
    print(f"✅ Sessions with data: {summary['files_with_data']}")
    
    if summary['date_range']['first']:
        print(f"\n📅 Date range: {summary['date_range']['first']} → {summary['date_range']['last']}")
        print(f"   Days with activity: {summary['date_range']['days_with_activity']}")
    
    print(f"\n💬 Total messages: {summary['totals']['messages']:,}")
    print(f"   User messages: {summary['totals']['user_messages']:,}")
    print(f"   Assistant messages: {summary['totals']['assistant_messages']:,}")
    print(f"   Tool calls: {summary['totals']['tool_calls']:,}")
    
    print(f"\n🎯 Token usage:")
    print(f"   Input tokens: {summary['totals']['input_tokens']:,}")
    print(f"   Output tokens: {summary['totals']['output_tokens']:,}")
    print(f"   Cache read: {summary['totals']['cache_read']:,}")
    print(f"   Cache creation: {summary['totals']['cache_creation']:,}")
    
    print(f"\n🤖 Model breakdown:")
    for model, usage in data['model_totals'].items():
        model_short = model.replace('claude-', '').replace('-20251101', '').replace('-20251001', '').replace('-20250929', '')
        print(f"   {model_short}:")
        print(f"      Requests: {usage['requests']:,}")
        print(f"      Tokens: {usage['input_tokens'] + usage['output_tokens']:,}")
    
    print(f"\n✅ Data saved to: {OUTPUT_FILE}")
    print(f"   File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
