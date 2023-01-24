# Stable Diffusion Booru Tag Getter Extension

Creates a UI element within the [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), for obtaining tags from a specific xbooru post.
Currently supports: `Danbooru`, `Safebooru`, `e621`.

## Preview

![image](https://i.imgur.com/VRiWR23.png)

### Options

#### "Using LoRA?"

Aims to only output character descriptor tags (e.g. `blue hair`, `orange eyes`, `ahoge`, `bangs`, etc.) and not tags that describe the image (e.g. `white gloves`, `cowboy shot`, and other miscellaneous tags not relevant to the character).

#### "Using NovelAI?"

Prepends "(masterpiece: 1.2), (best quality:1.2)" to the outputted tags.

## Installation

1. Install [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. Clone this repository into the `stable-diffusion-webui/extensions` directory
3. Run `python3 -m pip install -r requirements.txt` in the `stable-diffusion-webui/extensions/stable-diffusion-danbooru-tag-getter` directory
4. Launch the webui and navigate to the "Booru Tags" dropdown at the bottom of `txt2img` and `img2img` pages.

##### Where did the commits go?

I removed all prior commits for privacy reasons.
