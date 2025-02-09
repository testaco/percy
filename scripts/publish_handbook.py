#!/usr/bin/env python3
import os
import glob
import subprocess
from pathlib import Path

def ensure_output_dirs():
    """Ensure handbook and temp directories exist"""
    Path("handbook/chapters").mkdir(parents=True, exist_ok=True)
    Path("handbook/temp").mkdir(parents=True, exist_ok=True)

def generate_chapter_pdf(chapter_num: int, patterns: list[str]) -> str:
    """Generate PDF for a specific chapter from markdown files"""
    output_file = f"handbook/chapters/chapter{chapter_num}.pdf"
    
    # Collect all markdown files matching the patterns for this chapter
    md_files = []
    for pattern in patterns:
        md_files.extend(glob.glob(f"handbook/{pattern}*.md"))
    
    if not md_files:
        print(f"No markdown files found for chapter {chapter_num}")
        return None
    
    md_files.sort()  # Ensure consistent ordering
    
    # Build pandoc command
    cmd = [
        "pandoc",
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
        (1, ["T1", "G1", "E1"]),
        (2, ["T2", "G2", "E2"]),
        (3, ["T3", "G3", "E3"]),
        (4, ["T4", "G4", "E4"]),
        (5, ["T5", "G5", "E5"]),
        (6, ["T6", "G6", "E6"]),
        (7, ["T7", "G7", "E7"]),
        (8, ["T8", "G8", "E8"]),
        (9, ["T9", "G9", "E9"]),
        (10, ["T0", "G0", "E0"]),  # Handle T0, G0, E0 as chapter 10
    ]
    
    # Generate chapter PDFs
    chapter_pdfs = []
    for chapter_num, patterns in chapters:
        pdf = generate_chapter_pdf(chapter_num, patterns)
        if pdf:
            chapter_pdfs.append(pdf)
    
    # Combine all chapters into final handbook
    if chapter_pdfs:
        combine_pdfs(chapter_pdfs, "handbook/handbook.pdf")

if __name__ == "__main__":
    main()
