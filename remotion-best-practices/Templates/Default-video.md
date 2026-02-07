---
name: default-video
description: Standard video template with screen sharing as main content and floating speaker camera
metadata:
  tags: template, screen-share, speaker, layout, landscape, portrait
---

# Default Video Template

This template creates a video composition with:
- **Main content**: Screen sharing video (`_as_` asset)
- **Floating speaker**: Host camera video (`_avo_` asset) as a small overlay
- **Audio**: Separate audio track (`.m4a` asset)

## Layout Options

### Landscape (Default)
- Dimensions: 1920x1080 (16:9)
- Speaker position: Bottom-right corner
- Speaker size: 320x180

### Portrait
- Dimensions: 1080x1920 (9:16)
- Speaker position: Top-right corner
- Speaker size: 280x158

## Implementation

```tsx
import { AbsoluteFill, staticFile } from "remotion";
import { Video, Audio } from "@remotion/media";

type LayoutStyle = "landscape" | "portrait";

interface DefaultVideoProps {
  screenShareSrc: string;
  speakerSrc: string;
  audioSrc: string;
  style?: LayoutStyle;
}

const LAYOUT_CONFIG = {
  landscape: {
    width: 1920,
    height: 1080,
    speaker: {
      width: 320,
      height: 180,
      position: { bottom: 24, right: 24 },
      borderRadius: 12,
    },
  },
  portrait: {
    width: 1080,
    height: 1920,
    speaker: {
      width: 280,
      height: 158,
      position: { top: 24, right: 24 },
      borderRadius: 12,
    },
  },
};

export const DefaultVideo: React.FC<DefaultVideoProps> = ({
  screenShareSrc,
  speakerSrc,
  audioSrc,
  style = "landscape",
}) => {
  const config = LAYOUT_CONFIG[style];

  return (
    <AbsoluteFill>
      {/* Main screen share video */}
      <Video
        src={staticFile(screenShareSrc)}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* Floating speaker camera */}
      <Video
        src={staticFile(speakerSrc)}
        muted
        style={{
          position: "absolute",
          ...config.speaker.position,
          width: config.speaker.width,
          height: config.speaker.height,
          borderRadius: config.speaker.borderRadius,
          border: "3px solid white",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
          objectFit: "cover",
        }}
      />

      {/* Audio track */}
      <Audio src={staticFile(audioSrc)} />
    </AbsoluteFill>
  );
};
```

## Root.tsx Configuration

```tsx
import { Composition } from "remotion";
import { DefaultVideo } from "./DefaultVideo";

const LAYOUT_STYLE = "landscape"; // or "portrait"
const LAYOUT_CONFIG = {
  landscape: { width: 1920, height: 1080 },
  portrait: { width: 1080, height: 1920 },
};

export const RemotionRoot: React.FC = () => {
  const { width, height } = LAYOUT_CONFIG[LAYOUT_STYLE];

  return (
    <Composition
      id="DefaultVideo"
      component={DefaultVideo}
      durationInFrames={DURATION_IN_FRAMES}
      fps={30}
      width={width}
      height={height}
      defaultProps={{
        screenShareSrc: "Recording_as_1800x1170.mp4",
        speakerSrc: "Recording_avo_1280x720.mp4",
        audioSrc: "Recording.m4a",
        style: LAYOUT_STYLE,
      }}
    />
  );
};
```

## Customization Options

### Speaker Position Variants
- `bottom-right` (default for landscape)
- `top-right` (default for portrait)
- `bottom-left`
- `top-left`

### Speaker Size
Adjust `speaker.width` and `speaker.height` in config to resize the floating camera.

### Border and Shadow
Customize the speaker overlay appearance via style props:
- `border`: Change color/width
- `borderRadius`: Adjust roundness
- `boxShadow`: Modify drop shadow
