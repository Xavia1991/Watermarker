import gradio as gr
from modules import scripts_postprocessing, ui_components, script_callbacks
from modules.processing import Processed
from PIL import Image
import modules.shared as shared
import os
import math

class WatermarkScript(scripts_postprocessing.ScriptPostprocessing):
    name = "Add Watermark"
    order = 42000

    def ui(self):
        with ui_components.InputAccordion(False, label="Add Watermark") as enable:
            watermark_file = gr.File(label="Watermark Image", file_types=[".png", ".jpg", ".jpeg", ".gif"])
            watermark_scale = gr.Slider(label="Watermark Scale", minimum=0.1, maximum=2.0, step=0.1, value=1.0)
            watermark_alpha = gr.Slider(label="Watermark Alpha", minimum=0.0, maximum=1.0, step=0.05, value=1.0)
            watermark_anchor = gr.Radio(
                label="Watermark Anchor",
                choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                value="bottom-right"
            )

        return {
            "enable": enable,
            "watermark_file": watermark_file,
            "watermark_scale": watermark_scale,
            "watermark_alpha": watermark_alpha,
            "watermark_anchor": watermark_anchor
        }

    def process(self, pp, enable, watermark_file, watermark_scale, watermark_alpha, watermark_anchor):
        if not enable:
            return

        if watermark_file:
            try:
                watermark_image = Image.open(watermark_file.name).convert("RGBA")
            except Exception as e:
                print(f"Error loading selected watermark image: {e}")
                return
        else:
            default_image_path = shared.opts.extras_watermark_default_image
            if default_image_path and os.path.exists(default_image_path):
                try:
                    watermark_image = Image.open(default_image_path).convert("RGBA")
                except Exception as e:
                    print(f"Error loading default watermark image: {e}")
                    return
            else:
                print("No watermark image selected or default image not set.")
                return

        original_image = pp.image.convert("RGBA")
        
        # Calculate reference size from image area
        image_area = original_image.width * original_image.height
        reference_size = math.sqrt(image_area)
        
        # Define target size with increased base factor
        BASE_SCALE_FACTOR = 0.5  # Increased from 0.1 to allow full size at max scale
        target_size = reference_size * BASE_SCALE_FACTOR * watermark_scale
        
        # Preserve watermark aspect ratio and cap by image dimensions
        watermark_aspect = watermark_image.width / watermark_image.height
        max_width = original_image.width
        max_height = original_image.height
        
        if original_image.width / original_image.height > watermark_aspect:
            # Image is wider; scale by height
            new_height = int(min(target_size, max_height))
            new_width = int(min(new_height * watermark_aspect, max_width))
        else:
            # Image is taller or equal; scale by width
            new_width = int(min(target_size, max_width))
            new_height = int(min(new_width / watermark_aspect, max_height))

        # Resize watermark
        resized_watermark = watermark_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Apply alpha transparency
        if watermark_alpha < 1.0:
            r, g, b, a = resized_watermark.split()
            a = a.point(lambda i: i * watermark_alpha)
            resized_watermark = Image.merge("RGBA", (r, g, b, a))

        # Calculate position based on anchor
        if watermark_anchor == "top-left":
            position = (0, 0)
        elif watermark_anchor == "top-right":
            position = (original_image.width - new_width, 0)
        elif watermark_anchor == "bottom-left":
            position = (0, original_image.height - new_height)
        elif watermark_anchor == "bottom-right":
            position = (original_image.width - new_width, original_image.height - new_height)
        elif watermark_anchor == "center":
            position = (
                (original_image.width - new_width) // 2,
                (original_image.height - new_height) // 2
            )

        new_image = original_image.copy()
        new_image.paste(resized_watermark, position, mask=resized_watermark if resized_watermark.mode == 'RGBA' else None)
        pp.image = new_image

def on_ui_settings():
    section = "extras_watermark", "Watermarks"
    shared.opts.add_option(
        key="extras_watermark_default_image",
        info=shared.OptionInfo(
            default="",
            label="Default Watermark Image",
            component=gr.Textbox,
            component_args={"placeholder": "Enter path to default watermark image (e.g., C:\\Images\\default.png)"},
            section=section,
        ),
    )

script_callbacks.on_ui_settings(on_ui_settings)