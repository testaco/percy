#!/usr/bin/env python3
import os
import glob
import subprocess
from pathlib import Path

def ensure_output_dirs():
    """Ensure handbook directories exist"""
    Path("handbook/md").mkdir(parents=True, exist_ok=True)
    Path("handbook/pdf/chapters").mkdir(parents=True, exist_ok=True)
    Path("handbook/temp").mkdir(parents=True, exist_ok=True)

def generate_chapter_pdf(chapter_num: int, patterns: list[str]) -> str:
    """Generate PDF for a specific chapter from markdown files"""
    output_file = f"handbook/pdf/chapters/chapter{chapter_num}.pdf"
    
    # Collect all markdown files matching the patterns for this chapter
    md_files = []
    for pattern in patterns:
        md_files.extend(sorted(glob.glob(f"handbook/md/{pattern}*.md")))
    
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
    
    # Define chapter patterns
    chapters = [
        (1, "T1A T1B G1A E1A T1C T1D G1B E1B E1F T1E G1E E1C T1F G1C G1D E1E E1D".split()),
        (2, "T2A T2B T2C G2A G2B G2C G2D G2E E2A E2B E2C E2D E2E".split()),
        (3, "T3A T3B T3C G3A G3B G3C E3A E3B E3C".split()),
        (4, "T4A T4B G4A G4B G4C G4D G4E E4A E4B E4C E4D E4E".split()),
        (5, "T5A T5B T5C T5D G5A G5B G5C E5A E5B E5C E5D".split()),
        (6, "T6A T6B T6C T6D G6A G6B E6A E6B E6C E6D E6E E6F".split()),
        (7, "T7A T7B T7C T7D G7A G7B G7C E7A E7B E7C E7D E7E E7F E7G E7H".split()),
        (8, "T8A T8B T8C T8D G8A G8B G8C E8A E8B E8C E8D".split()),
        (9, "T9A T9B G9A G9B G9C G9D E9A E9B E9C E9D E9E E9F E9G E9H".split()),
        (10, "T0A T0B T0C G0A G0B E0A".split()),  # Handle T0, G0, E0 as chapter 10
    ]
    
    # Generate chapter PDFs
    chapter_pdfs = []
    for chapter_num, patterns in chapters:
        pdf = generate_chapter_pdf(chapter_num, patterns)
        if pdf:
            chapter_pdfs.append(pdf)
    
    # Combine all chapters into final handbook
    if chapter_pdfs:
        combine_pdfs(chapter_pdfs, "handbook/pdf/handbook.pdf")

if __name__ == "__main__":
    main()
