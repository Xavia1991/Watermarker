# Stable Diffusion WebUI Watermarker

A simple extension for Stable Diffusion WebUI that lets you add watermarks to your images in the Extras tab. Customize the size, transparency, and position easily!
Keeps metadata intact. 

## What It Does
- Adds a watermark to your images.
- Lets you pick the watermark image, size, transparency, and where it goes.
- Saves a default watermark path for quick use.

## How to Install
Option A: Go to Extension Tab in WebUI, in Tab install from URL paste https://github.com/Xavia1991/Watermarker
  
Option B: Download this folder and put it in the `extensions/` folder of your Stable Diffusion WebUI.
   
2. Reload UI or Restart the WebUI
3. Look for "Add Watermark" in the Extras tab.

## How to Use
- **Extras Tab**: Upload an image, open "Add Watermark," tweak the options, and hit "Generate."
- **Settings Tab**: Set a default watermark image under "Watermarks" if you want to skip uploading each time.

Recommended:
Set up Extras Tab to your likings, set the default watermark Image and then under settings -> Default click apply.
You won't have to click anything for your watermarks in the future.

## Options in Extras Tab
- **Enable Watermark**: Check this to turn it on (unchecked by default).
- **Watermark Image**: Upload your watermark (PNG, JPG, JPEG, GIF).
- **Watermark Scale**: Slide from 0.1 (tiny) to 2.0 (big) to set the size (starts at 1.0).
- **Watermark Alpha**: Slide from 0.0 (see-through) to 1.0 (solid) for transparency (starts at 1.0).
- **Watermark Anchor**: Pick where it goes:
  - Top-Left
  - Top-Right
  - Bottom-Left
  - Bottom-Right (default)
  - Center

![image](https://github.com/user-attachments/assets/c7ccbf5d-e453-4cbb-b333-c9bde8f9b2c2)
![image](https://github.com/user-attachments/assets/40c7a6f6-4ffe-4b5b-977a-beda2835d98a)
