#!/usr/bin/env python
from pathlib import Path
import os

esmvaltool_output_dir = Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "cycle" / "1"

pages_to_link = []
images = []
for subdir in esmvaltool_output_dir.iterdir():
    index_page = subdir / "index.html"
    pages_to_link.append(str(index_page))

    for image_dir in subdir.glob("plots/*/*/png"):
        for file in Path(image_dir).iterdir():
            if file.suffix == ".png":
                rel_path = file.relative_to(esmvaltool_output_dir)
                images.append(str(rel_path))

lines_to_type = []
for page_link in pages_to_link:
    name_parts = page_link.split("/")[-2].split("_")[1:-2]
    name = "_".join(name_parts)
    line = f'<a href="{page_link}">{name}</a>\n'
    lines_to_type.append(line)
for image in images:
    line = f'<img src="{image}"/>\n'
    lines_to_type.append(line)

with open(esmvaltool_output_dir / "index.html", "w") as f:
    f.writelines(lines_to_type)
