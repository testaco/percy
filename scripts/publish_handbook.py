#!/usr/bin/env python3
import json
import os
import glob
import subprocess
from pathlib import Path

def ensure_output_dirs():
    """Ensure handbook directories exist"""
    Path("data/handbook/md").mkdir(parents=True, exist_ok=True)
    Path("data/handbook/pdf/chapters").mkdir(parents=True, exist_ok=True)
    Path("data/handbook/temp").mkdir(parents=True, exist_ok=True)

def generate_chapter_pdf(chapter_num: int, patterns: list[str]) -> str:
    """Generate PDF for a specific chapter from markdown files"""
    output_file = f"data/handbook/pdf/chapters/chapter{chapter_num}.pdf"
    
    # Collect all markdown files matching the patterns for this chapter
    md_files = []
    for pattern in patterns:
        md_files.extend(sorted(glob.glob(f"data/handbook/md/{pattern}*.md")))
    
    if not md_files:
        print(f"No markdown files found for chapter {chapter_num}")
        return None
    
    # Build pandoc command
    cmd = [
        "pandoc",
        "--pdf-engine=xelatex",
        "-V", "geometry:top=2cm, bottom=1.5cm, left=2cm, right=2cm",
        *md_files,
        "-o", output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Generated {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error generating chapter {chapter_num}: {e}")
        return None

def combine_pdfs(chapter_pdfs: list[str], output_file: str):
    """Combine multiple PDFs into a single file using pdftk"""
    if not chapter_pdfs:
        print("No chapter PDFs to combine")
        return
    
    cmd = ["pdftk", *chapter_pdfs, "cat", "output", output_file]
    try:
        subprocess.run(cmd, check=True)
        print(f"Generated {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining PDFs: {e}")

def main():
    ensure_output_dirs()
    
    with open("data/handbook/toc.json", "r") as f:
      chapters = json.load(f)

    # Generate chapter PDFs
    chapter_pdfs = []
    for chapter_num, chapter_name, patterns in chapters:
        pdf = generate_chapter_pdf(chapter_num, patterns)
        if pdf:
            chapter_pdfs.append(pdf)
    
    # Combine all chapters into final handbook
    if chapter_pdfs:
        combine_pdfs(chapter_pdfs, "data/handbook/pdf/handbook.pdf")

if __name__ == "__main__":
    main()
