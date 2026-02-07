# Remotion Troubleshooting

Common issues and solutions learned from real projects.

---

## Zoom Recording Assets

For Zoom recordings, you will find multiple assets. This pattern helps map which asset to use:

| File Pattern | Content |
|--------------|---------|
| `Date-time-Recording_avo_...mp4` | Host camera |
| `Date-time-Recording_as_...mp4` | Only screen sharing video |
| `Date-time-Recording_gvo_...mp4` | Cameras of participants when they unmute themselves |
| `Date-time-Recording_gallery_...mp4` | Gallery view with all participants |
| `Date-time-Recording.m4a` | Full Audio |

### Best Practice
When importing the `.mp4` files, import only the video (muted) and use the `.m4a` for the audio separately. This gives you better control over audio levels and sync.

```tsx
import { Video, Audio } from "@remotion/media";
import { staticFile } from "remotion";

// Import video muted, use separate audio track
<Video src={staticFile("Recording_gallery_1920x1170.mp4")} muted />
<Audio src={staticFile("Recording.m4a")} />
```

---

## Trimming Videos - The Script Approach

### Mental Model
**NEVER trim files manually with one-off ffmpeg commands.** Trimming requirements will change, and you need a repeatable process.

### The Right Way
1. **Create a trimming script** in your project that trims ALL source files
2. **Output to a subfolder** under `public/` (e.g., `public/trimmed/`)
3. **Use simplified output names** (screen_share.mp4, speakers.mp4, audio.m4a) - easier to reference
4. **Keep original files untouched** - only reference trimmed files in your composition
5. **Re-run the script** when timestamps change

### Trimming Script Template

Create `scripts/trim-videos.sh` in your project:

```bash
#!/bin/bash
# Trim videos based on configured timestamps
# Usage: ./scripts/trim-videos.sh

set -e

# ====== CONFIGURATION - EDIT THESE VALUES ======
START_TIME=""              # Leave empty to start from beginning
END_TIME="00:21:38.12"     # End of clip

# Source directory and file prefix (from Zoom recording)
SOURCE_DIR="public"
PREFIX="GMT20260129-091335_Recording"

# Output directory (subfolder under public)
OUTPUT_DIR="public/trimmed"
# ====== END CONFIGURATION ======

echo "Creating output directory..."
mkdir -p "$OUTPUT_DIR"

# Build ffmpeg time arguments
TIME_ARGS=""
[ -n "$START_TIME" ] && TIME_ARGS="$TIME_ARGS -ss $START_TIME"
[ -n "$END_TIME" ] && TIME_ARGS="$TIME_ARGS -to $END_TIME"

echo "Trimming with: $TIME_ARGS"
echo "Output to: $OUTPUT_DIR"
echo ""

# Trim screen share video (_as_) -> screen_share.mp4
echo "Processing screen share video..."
ffmpeg -y -i "$SOURCE_DIR/${PREFIX}_as_"*.mp4 $TIME_ARGS -c copy "$OUTPUT_DIR/screen_share.mp4" 2>/dev/null

# Trim host camera video (_avo_) -> speakers.mp4
echo "Processing host camera video..."
ffmpeg -y -i "$SOURCE_DIR/${PREFIX}_avo_"*.mp4 $TIME_ARGS -c copy "$OUTPUT_DIR/speakers.mp4" 2>/dev/null

# Trim gallery video if exists -> gallery.mp4
if ls "$SOURCE_DIR/${PREFIX}_gallery_"*.mp4 1>/dev/null 2>&1; then
    echo "Processing gallery video..."
    ffmpeg -y -i "$SOURCE_DIR/${PREFIX}_gallery_"*.mp4 $TIME_ARGS -c copy "$OUTPUT_DIR/gallery.mp4" 2>/dev/null
fi

# Trim participants camera video (_gvo_) if exists -> participants.mp4
if ls "$SOURCE_DIR/${PREFIX}_gvo_"*.mp4 1>/dev/null 2>&1; then
    echo "Processing participants camera video..."
    ffmpeg -y -i "$SOURCE_DIR/${PREFIX}_gvo_"*.mp4 $TIME_ARGS -c copy "$OUTPUT_DIR/participants.mp4" 2>/dev/null
fi

# Trim audio file -> audio.m4a
echo "Processing audio..."
ffmpeg -y -i "$SOURCE_DIR/${PREFIX}.m4a" $TIME_ARGS -c copy "$OUTPUT_DIR/audio.m4a" 2>/dev/null

# Get duration and save to metadata.json for auto-updating Root.tsx
echo ""
echo "=== DONE ==="
echo "Trimmed files created in $OUTPUT_DIR:"
ls -la "$OUTPUT_DIR"
echo ""
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_DIR/speakers.mp4" 2>/dev/null)
echo "Duration: $DURATION seconds"
echo "{ \"durationInSeconds\": $DURATION }" > "$OUTPUT_DIR/metadata.json"
echo "Metadata saved to $OUTPUT_DIR/metadata.json"
```

### Output File Structure
```
public/
├── GMT20260129-...mp4       # Original files (untouched)
├── GMT20260129-....m4a
└── trimmed/                 # Trimmed files (simplified names)
    ├── screen_share.mp4     # From _as_ (screen share)
    ├── speakers.mp4         # From _avo_ (host camera)
    ├── gallery.mp4          # From _gallery_ (if exists)
    ├── participants.mp4     # From _gvo_ (if exists)
    ├── audio.m4a            # From .m4a
    └── metadata.json        # Duration info for Root.tsx
```

### Usage

```bash
chmod +x scripts/trim-videos.sh
./scripts/trim-videos.sh
```

Then update your composition to use files from `public/trimmed/`:

```tsx
defaultProps={{
  screenShareSrc: "trimmed/screen_share.mp4",
  speakerSrc: "trimmed/speakers.mp4",
  audioSrc: "trimmed/audio.m4a",
}}
```

### When Timestamps Change
Just edit the `START_TIME` and `END_TIME` in the script and re-run. No manual ffmpeg commands needed.

### Auto-Updating Duration with metadata.json (Recommended)

Instead of manually updating `VIDEO_DURATION_SECONDS` after each trim, have the script output a `metadata.json` file that Root.tsx imports.

**Step 1:** The trim script already outputs `metadata.json`:
```bash
# At the end of trim-videos.sh
echo "{ \"durationInSeconds\": $DURATION }" > "$OUTPUT_DIR/metadata.json"
```

**Step 2:** Enable JSON imports in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

**Step 3:** Import and use in `Root.tsx`:
```tsx
import "./index.css";
import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import metadata from "../public/trimmed/metadata.json";

const FPS = 30;
const DURATION_IN_FRAMES = Math.ceil(metadata.durationInSeconds * FPS);

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyComp"
      component={MyComposition}
      durationInFrames={DURATION_IN_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{
        screenShareSrc: "trimmed/screen_share.mp4",
        speakerSrc: "trimmed/speakers.mp4",
        audioSrc: "trimmed/audio.m4a",
      }}
    />
  );
};
```

Now when you re-run `./scripts/trim-videos.sh`, the duration automatically updates when you restart the studio - no manual step needed!

---

## Video Components: @remotion/media vs Core Remotion

### Problem
When cropping videos with CSS (margins, transforms) to show only part of a video frame:
- `@remotion/media`'s `Video` component handles CSS styling correctly
- Core Remotion's `Video` and `OffthreadVideo` break the layout

### Problem
`@remotion/media`'s Video component does NOT support `startFrom` prop for skipping into a video.

### Solution
Use the trimming script approach above instead of trying to skip in Remotion.

---

## Audio/Video Sync Issues

### Problem
Trimming video but forgetting to trim audio causes desync.

### Solution
Use the trimming script approach - it automatically trims ALL files (video AND audio) with the same timestamps

---

## Sequence Duration Placeholders

### Problem
Using placeholder durations for Sequences causes incorrect timeline display (long blue bars).

### Solution
Check actual duration with ffprobe and update configs:
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "video.mp4"
```

Then use the actual value:
```tsx
const PART2_DURATION = Math.round(23.06 * 30); // actual seconds * fps
```

---

## Timestamp Conversion for Trimmed Videos

### Problem
When making multiple cuts, you lose track of how trimmed timestamps map to source timestamps.

### Solution
Create a cuts tracking file (e.g., `cuts.json`):
```json
{
  "segments": [
    { "start": "00:00:00", "end": "00:01:13.29" },
    { "start": "00:01:28.21", "end": "00:02:34.11" }
  ],
  "trimmedToSource": {
    "offsets": [
      { "afterTrimmed": "00:00:00", "addSeconds": 0 },
      { "afterTrimmed": "00:01:13.29", "addSeconds": 14.92 }
    ]
  }
}
```

User always provides trimmed timestamps. Add cumulative offset to get source timestamp.

---

## Audio Crossfades Between Compositions

### Solution
Use the `volume` prop with `interpolate`:
```tsx
// Fade out at end of Part 1
const audioVolume = interpolate(
  frame,
  [totalFrames - fadeDuration, totalFrames],
  [1, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

<Audio src={audioSrc} volume={audioVolume} />
```

```tsx
// Fade in at start of Part 2
const audioVolume = interpolate(
  frame,
  [0, fadeDuration],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

<Audio src={audioSrc} volume={audioVolume} />
```

---

## Rendering Tips

### File Size Control
Use CRF (Constant Rate Factor) to control output size:
```bash
npx remotion render FullVideo --codec=h264 --crf=28
```
- CRF 18-20: High quality, large file
- CRF 23-25: Good balance
- CRF 28-30: Smaller file, still decent for screen recordings

### Speed Up Rendering
Add concurrency based on CPU cores:
```bash
npx remotion render FullVideo --codec=h264 --crf=28 --concurrency=8
```

Note: Remotion uses CPU, not GPU. The concurrency flag controls parallel frame rendering.
