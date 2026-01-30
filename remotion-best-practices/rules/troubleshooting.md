# Remotion Troubleshooting

Common issues and solutions learned from real projects.

## Video Components: @remotion/media vs Core Remotion

### Problem
When cropping videos with CSS (margins, transforms) to show only part of a video frame:
- `@remotion/media`'s `Video` component handles CSS styling correctly
- Core Remotion's `Video` and `OffthreadVideo` break the layout

### Problem
`@remotion/media`'s Video component does NOT support `startFrom` prop for skipping into a video.

### Solution
Pre-trim videos with ffmpeg instead of trying to skip in Remotion:
```bash
ffmpeg -y -i "source.mp4" -ss 00:00:28.20 -c copy output.mp4
ffmpeg -y -i "source.m4a" -ss 00:00:28.20 -c copy output.m4a
```

This is cleaner than fighting the framework.

---

## Audio/Video Sync Issues

### Problem
Trimming video but forgetting to trim audio causes desync.

### Solution
Always trim both video AND audio files with the same timestamps:
```bash
# Trim video
ffmpeg -y -i "video.mp4" -ss 00:00:10 -to 00:01:30 -c copy trimmed_video.mp4

# Trim audio with SAME timestamps
ffmpeg -y -i "audio.m4a" -ss 00:00:10 -to 00:01:30 -c copy trimmed_audio.m4a
```

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
