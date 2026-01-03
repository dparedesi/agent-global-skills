---
name: transcribe
description: Transcribe audio files with speaker diarization using VoxScriber. Use when the user wants to transcribe a meeting, podcast, interview, or any audio file, or when they mention "transcribe", "diarization", "who said what", "meeting transcript", or "audio to text".
---

# Transcribe Audio

Transcribe audio files with automatic speaker identification using VoxScriber.

**Why?** Quickly generate speaker-attributed transcripts from meeting recordings, interviews, or podcasts without manual setup each time.

## Quick Start

```bash
voxscriber <audio_file> --speakers <num>
```

## Prerequisites

> [!WARNING]
> All three prerequisites must be met before running.

1. **VoxScriber installed:** `pip install voxscriber` or `pipx install voxscriber`
2. **HuggingFace token:** Export `HF_TOKEN` environment variable
3. **Pyannote terms accepted:** Visit https://huggingface.co/pyannote/speaker-diarization-3.1

## How It Works

### Step 1: Validate Environment

Before running, verify prerequisites are met:

```bash
# Check voxscriber is installed
which voxscriber || echo "Not installed - run: pip install voxscriber"

# Check HF_TOKEN is set
[ -n "$HF_TOKEN" ] && echo "HF_TOKEN is set" || echo "Missing - run: export HF_TOKEN=your_token"
```

> [!TIP]
> If prerequisites fail, provide the user with the specific fix command.

### Step 2: Identify Audio File and Speaker Count

Extract from user's request:
- **Audio file path** (required)
- **Speaker count** (optional) - use `--speakers N` only if user explicitly provides it

> [!IMPORTANT]
> Do NOT ask the user for speaker count. If not provided, let VoxScriber auto-detect.

### Step 3: Run VoxScriber

```bash
# Basic usage (auto-detect speakers)
voxscriber /path/to/audio.m4a

# With known speaker count (only if user specified)
voxscriber /path/to/audio.m4a --speakers 2

# With custom output directory
voxscriber /path/to/audio.m4a --speakers 3 --output /path/to/output

# All formats
voxscriber /path/to/audio.m4a --formats md,txt,json,srt,vtt
```

### Step 4: Report Results

Tell the user where the transcript files were saved. Default location is same directory as the audio file.

## Examples

**Example 1: Two-person meeting**
- Input: `transcribe ~/Downloads/meeting-2024-01-15.m4a with 2 speakers`
- Command: `voxscriber ~/Downloads/meeting-2024-01-15.m4a --speakers 2`
- Output: `meeting-2024-01-15.md` and `meeting-2024-01-15.txt` in Downloads

**Example 2: Podcast with unknown speakers**
- Input: `transcribe this podcast recording podcast.mp3`
- Command: `voxscriber podcast.mp3` (no --speakers flag, auto-detect)
- Output: `podcast.md` and `podcast.txt` with auto-detected speakers

**Example 3: Interview with subtitles needed**
- Input: `transcribe interview.wav and generate subtitles`
- Command: `voxscriber interview.wav --formats md,txt,srt,vtt`
- Output: Markdown, text, and subtitle files

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--speakers`, `-s` | Number of speakers (if known) | Auto-detect |
| `--output`, `-o` | Output directory | Same as input |
| `--formats`, `-f` | Output formats (md,txt,json,srt,vtt) | md,txt |
| `--model`, `-m` | Whisper model size | large-v3-turbo |
| `--language`, `-l` | Force language (e.g., 'en', 'es') | Auto-detect |
| `--print` | Print transcript to console | Off |
| `--quiet`, `-q` | Suppress progress output | Off |

## Quality Rules

### Naming Conventions
- Output files use the input filename with new extension (e.g., `meeting.m4a` → `meeting.md`)
- Do not rename output files unless user explicitly requests

### Validation Requirements
- Verify audio file exists before running
- Check file extension is supported (m4a, wav, mp3, flac, ogg)
- Confirm `voxscriber` command is available

### Anti-Patterns
- Do NOT guess speaker count - if user doesn't specify, omit `--speakers` flag
- Do NOT use `--language` unless user explicitly requests a specific language
- Do NOT run with `--quiet` unless user asks for silent operation
- Do NOT create output directories without user confirmation

## Testing

### Scenario 1: Basic Transcription
**Query:** "transcribe meeting.m4a"
**Expected:**
- Run `voxscriber meeting.m4a` (no --speakers flag)
- Report output file locations

### Scenario 2: Known Speaker Count
**Query:** "transcribe interview.mp3 with 2 speakers"
**Expected:**
- Run `voxscriber interview.mp3 --speakers 2`
- Use --speakers flag because user specified count

### Scenario 3: Missing Prerequisites
**Query:** "transcribe podcast.wav" (but HF_TOKEN not set)
**Expected:**
- Detect missing token before running
- Provide fix: `export HF_TOKEN=your_token`
- Do NOT run voxscriber until fixed

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "HF_TOKEN required" | Run `export HF_TOKEN=your_token` or add to ~/.zshrc |
| "Access denied" to model | Accept terms at huggingface.co/pyannote/speaker-diarization-3.1 |
| Slow processing | Normal for long files; large-v3-turbo is fastest accurate model |
| Wrong speaker count | Use `--speakers N` if you know the exact count |
| "command not found: voxscriber" | Run `pip install voxscriber` or `pipx install voxscriber` |
