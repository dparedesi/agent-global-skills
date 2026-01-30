---
name: assets
description: Importing images, videos, audio, and fonts into Remotion
metadata:
  tags: assets, staticFile, images, fonts, public
---

# Importing assets in Remotion

## The public folder

Place assets in the `public/` folder at your project root.

## Using staticFile()

You MUST use `staticFile()` to reference files from the `public/` folder:

```tsx
import {Img, staticFile} from 'remotion';

export const MyComposition = () => {
  return <Img src={staticFile('logo.png')} />;
};
```

The function returns an encoded URL that works correctly when deploying to subdirectories.

## Using with components

**Images:**

```tsx
import {Img, staticFile} from 'remotion';

<Img src={staticFile('photo.png')} />;
```

**Videos:**

```tsx
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';

<Video src={staticFile('clip.mp4')} />;
```

**Audio:**

```tsx
import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';

<Audio src={staticFile('music.mp3')} />;
```

**Fonts:**

```tsx
import {staticFile} from 'remotion';

const fontFamily = new FontFace('MyFont', `url(${staticFile('font.woff2')})`);
await fontFamily.load();
document.fonts.add(fontFamily);
```

## Remote URLs

Remote URLs can be used directly without `staticFile()`:

```tsx
<Img src="https://example.com/image.png" />
<Video src="https://remotion.media/video.mp4" />
```

## Important notes

- Remotion components (`<Img>`, `<Video>`, `<Audio>`) ensure assets are fully loaded before rendering
- Special characters in filenames (`#`, `?`, `&`) are automatically encoded

## Troubleshooting: Videos not loading

### ⚠️ CRITICAL: Always use `staticFile()`

**WRONG:**
```tsx
// This will NOT work in dev server!
<Video src="/assets/video.mp4" />
// Dev server treats this as a client-side route → returns HTML
```

**CORRECT:**
```tsx
// This works!
import { staticFile } from "remotion";
<Video src={staticFile("assets/video.mp4")} />
```

**What happens without `staticFile()`:**
- Dev server returns `content-type: text/html` instead of `video/mp4`
- Browser gets HTML page, not the video file
- Error: `DEMUXER_ERROR_COULD_NOT_OPEN: FFmpegDemuxer: open context failed`

### Debugging checklist

1. **Check server response:**
   ```bash
   curl -I http://localhost:3000/assets/video.mp4
   # Should see: content-type: video/mp4
   # If you see: content-type: text/html → you're NOT using staticFile()
   ```

2. **Test with known-good files:**
   - Download any sample MP4 from the internet
   - Place in `public/` folder
   - Test with `staticFile("assets/sample.mp4")`
   - If this works, your original files are the issue

3. **Verify file paths:**
   - Files must be in `public/` folder at project root
   - Path is relative to `public/`: `staticFile("assets/video.mp4")` → `public/assets/video.mp4`
   - No leading slash in the path

4. **Video format (only convert if having issues):**
   - .mov files work fine with `staticFile()` in modern browsers (Chrome/Safari)
   - Don't convert just because of extension - `staticFile()` is the fix 90% of the time
   - Only convert if you get codec-specific errors AFTER using `staticFile()`
   - If needed: `ffmpeg -i input.mov -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags faststart output.mp4`

5. **Browser testing:**
   - Test in actual Chrome/Safari, NOT headless browsers (Playwright, Puppeteer)
   - Headless browsers have limited codec support
   - `readyState: 4` in browser console means video loaded successfully
