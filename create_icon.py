"""
Generate Ventry application icons from existing logo
"""

from PIL import Image
import os

SOURCE_LOGO = "ventry_icon.png"        # your existing logo
OUT_DIR = "assets"

SIZES = [16, 32, 64, 128, 256]

os.makedirs(OUT_DIR, exist_ok=True)

# Load original logo
img = Image.open(SOURCE_LOGO).convert("RGBA")

# Ensure square icon
width, height = img.size
if width != height:
    raise ValueError("Logo must be square (e.g. 512x512, 1024x1024)")

icons = []

for size in SIZES:
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    path = f"{OUT_DIR}/ventry_icon_{size}.png"
    resized.save(path, format="PNG")
    icons.append(resized)
    print(f"✓ Created {path}")

# Create Windows ICO (multi-size)
ico_path = f"{OUT_DIR}/ventry_icon.ico"
img.save(
    ico_path,
    format="ICO",
    sizes=[(s, s) for s in SIZES]
)

print(f"✓ Created {ico_path}")
