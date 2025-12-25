import os
import json
import glob
from datetime import datetime, timezone

GEMINI_TMP_DIR = os.path.expanduser("~/.gemini/tmp")
GEMINI_BRAIN_DIR = os.path.expanduser("~/.gemini/antigravity/brain")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "gemini_history.json")

def parse_session_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        session_id = data.get('sessionId')
        start_time_str = data.get('startTime')
        last_updated_str = data.get('lastUpdated')
        project_hash = data.get('projectHash')
        messages = data.get('messages', [])
        
        if not start_time_str:
            return None

        # Calculate counts
        user_messages = sum(1 for m in messages if m.get('type') == 'user')
        model_messages = sum(1 for m in messages if m.get('type') == 'gemini' or m.get('type') == 'model')
        
        # Calculate tokens (Incremental estimation)
        total_input_tokens = 0
        total_output_tokens = 0
        last_input_tokens = 0
        
        # Sort messages by timestamp to ensure correct order
        sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''))
        
        for m in sorted_messages:
            tokens = m.get('tokens')
            if tokens:
                current_input = tokens.get('input', 0)
                current_output = tokens.get('output', 0)
                
                # Output is always new
                total_output_tokens += current_output
                
                # Input is cumulative context. Estimate new input.
                # If current < last, context was likely reset or branched. Treat as new.
                if current_input >= last_input_tokens:
                    diff = current_input - last_input_tokens
                    # Heuristic: If diff is very small (e.g. < 10), it might just be the user prompt.
                    # If diff is 0, no new input?
                    total_input_tokens += diff
                else:
                    # Context reset
                    total_input_tokens += current_input
                
                last_input_tokens = current_input + current_output # Output becomes part of next input context
        
        # Calculate duration
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        if last_updated_str:
            last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
            duration_seconds = (last_updated - start_time).total_seconds()
        else:
            duration_seconds = 0
            
        return {
            "type": "CLI",
            "sessionId": session_id,
            "startTime": start_time_str,
            "projectHash": project_hash,
            "userMessages": user_messages,
            "modelMessages": model_messages,
            "totalMessages": len(messages),
            "totalInputTokens": total_input_tokens,
            "totalOutputTokens": total_output_tokens,
            "durationSeconds": duration_seconds,
            "filePath": file_path,
            "summary": None
        }
        
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def parse_brain_folder(folder_path):
    try:
        session_id = os.path.basename(folder_path)
        
        # Find all files in the folder to estimate duration
        all_files = glob.glob(os.path.join(folder_path, "*"))
        if not all_files:
            return None
            
        timestamps = []
        summaries = set()
        
        # Scan metadata files for specific info
        meta_files = glob.glob(os.path.join(folder_path, "*.metadata.json"))
        for meta_file in meta_files:
            try:
                with open(meta_file, 'r') as f:
                    data = json.load(f)
                    if data.get('updatedAt'):
                        timestamps.append(datetime.fromisoformat(data['updatedAt'].replace('Z', '+00:00')))
                    if data.get('summary'):
                        # Summary can be a string or list
                        s = data['summary']
                        if isinstance(s, list):
                            for item in s:
                                summaries.add(item)
                        elif isinstance(s, str):
                            summaries.add(s)
            except (KeyError, TypeError, ValueError):
                pass
                
        # Also check file modification times for all files
        for f in all_files:
            mtime = os.path.getmtime(f)
            timestamps.append(datetime.fromtimestamp(mtime, tz=timezone.utc))
            
        if not timestamps:
            return None
            
        timestamps.sort()
        start_time = timestamps[0]
        end_time = timestamps[-1]
        duration_seconds = (end_time - start_time).total_seconds()
        
        # If duration is 0 (single file/timestamp), assume a default small duration
        if duration_seconds < 1:
            duration_seconds = 60
            
        # Estimate messages based on file count (rough proxy)
        # Each 'resolved' file or 'task' file likely represents a turn or action
        total_messages = len(all_files)
        
        return {
            "type": "Antigravity",
            "sessionId": session_id,
            "startTime": start_time.isoformat(),
            "projectHash": "antigravity-brain",
            "userMessages": 0, # Unknown
            "modelMessages": 0, # Unknown
            "totalMessages": total_messages, # Estimated
            "totalInputTokens": 0, # Not available in logs
            "totalOutputTokens": 0, # Not available in logs
            "durationSeconds": duration_seconds,
            "filePath": folder_path,
            "summary": list(summaries)[0] if summaries else "Antigravity Session"
        }
        
    except Exception as e:
        print(f"Error parsing brain folder {folder_path}: {e}")
        return None

def main():
    sessions = []
    
    # 1. Scan CLI Sessions
    print(f"Scanning {GEMINI_TMP_DIR} for Gemini CLI sessions...")
    search_pattern = os.path.join(GEMINI_TMP_DIR, "**", "chats", "session-*.json")
    session_files = glob.glob(search_pattern, recursive=True)
    print(f"Found {len(session_files)} CLI session files.")
    
    for file_path in session_files:
        session_data = parse_session_file(file_path)
        if session_data:
            sessions.append(session_data)
            
    # 2. Scan Antigravity Brain Sessions
    print(f"Scanning {GEMINI_BRAIN_DIR} for Antigravity sessions...")
    if os.path.exists(GEMINI_BRAIN_DIR):
        brain_folders = [f.path for f in os.scandir(GEMINI_BRAIN_DIR) if f.is_dir()]
        print(f"Found {len(brain_folders)} Brain folders.")
        
        for folder in brain_folders:
            brain_data = parse_brain_folder(folder)
            if brain_data:
                sessions.append(brain_data)
    else:
        print(f"Brain directory not found: {GEMINI_BRAIN_DIR}")
            
    # Sort by start time
    sessions.sort(key=lambda x: x['startTime'], reverse=True)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)
        
    print(f"Successfully aggregated {len(sessions)} sessions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
