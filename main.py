#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 - Unified Solution
Automatically detects and runs either Round 1A or Round 1B based on input patterns
"""

import os
import json
import sys
from pathlib import Path
import argparse

# Import both round solutions
from src.process_pdfs import process_pdf_to_outline
from src.persona_intelligence import analyze_persona_intelligence

def detect_input_type(input_dir):
    """
    Detect whether to run Round 1A or Round 1B based on input patterns
    
    Round 1A: Individual PDF files or simple PDF collections
    Round 1B: Collections with persona description files or known collection patterns
    """
    input_path = Path(input_dir)
    
    # Get all files in input directory
    all_files = list(input_path.glob("*"))
    pdf_files = list(input_path.glob("*.pdf"))
    
    # Check for persona directory (as specified in test.md)
    persona_dir = Path("/app/persona")
    has_persona_dir = persona_dir.exists() and any(persona_dir.glob("*.json"))
    
    # Check for persona description files in input directory (Round 1B indicators)
    persona_indicators = [
        "persona.json", "persona.txt", "job_description.json", 
        "job_description.txt", "requirements.json", "requirements.txt"
    ]
    
    has_persona_file = any(
        any(input_path.glob(f"*{indicator}*")) for indicator in persona_indicators
    )
    
    # Check for known Round 1B collection patterns
    collection_patterns = [
        "Collection 1", "Collection 2", "Collection 3",
        "South of France", "Learn Acrobat", "Dinner Ideas", "Breakfast Ideas", "Lunch Ideas"
    ]
    
    # Check if directory name or files suggest Round 1B collections
    dir_name = input_path.name
    is_known_collection = any(pattern in dir_name for pattern in collection_patterns)
    
    # Check file names for collection patterns
    file_collection_match = any(
        any(pattern in file.name for pattern in collection_patterns)
        for file in all_files
    )
    
    print(f"Analysis: {len(pdf_files)} PDFs found")
    print(f"Has persona directory: {has_persona_dir}")
    print(f"Has persona file: {has_persona_file}")
    print(f"Known collection: {is_known_collection}")
    print(f"File collection match: {file_collection_match}")
    
    # Decision logic
    if has_persona_dir or has_persona_file or is_known_collection or file_collection_match:
        print("🧠 Detected Round 1B: Persona-driven document intelligence")
        return "round1b"
    else:
        print("📋 Detected Round 1A: PDF outline extraction")
        return "round1a"

def run_round1a(input_dir, output_dir):
    """Run Round 1A: PDF outline extraction for each PDF"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found for Round 1A processing")
        return False
    
    print(f"🔄 Processing {len(pdf_files)} PDF files for Round 1A...")
    
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            
            # Generate outline
            outline = process_pdf_to_outline(str(pdf_file))
            
            # Save output with same name as PDF but .json extension
            output_file = output_path / f"{pdf_file.stem}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved: {output_file.name}")
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    
    print("🎉 Round 1A processing completed!")
    return True

def run_round1b(input_dir, output_dir):
    """Run Round 1B: Persona-driven document intelligence"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    try:
        print("🧠 Running Round 1B: Persona-driven document intelligence...")
        
        # Run persona intelligence analysis
        result = analyze_persona_intelligence(input_dir, output_dir)
        
        if result:
            print("🎉 Round 1B processing completed!")
            return True
        else:
            print("❌ Round 1B processing failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in Round 1B processing: {e}")
        return False

def main():
    """Main entry point for unified solution"""
    parser = argparse.ArgumentParser(description='Adobe Hackathon Unified Solution')
    parser.add_argument('--input', default='/app/input', help='Input directory path')
    parser.add_argument('--output', default='/app/output', help='Output directory path')
    parser.add_argument('--force-round', choices=['1a', '1b'], help='Force specific round')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    # Validate input directory
    if not os.path.exists(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        sys.exit(1)
    
    print("🚀 Adobe India Hackathon - Unified Solution")
    print(f"📁 Input: {input_dir}")
    print(f"📁 Output: {output_dir}")
    print("-" * 50)
    
    # Detect which round to run (unless forced)
    if args.force_round:
        round_type = f"round{args.force_round}"
        print(f"🔧 Forced to run {round_type.upper()}")
    else:
        round_type = detect_input_type(input_dir)
    
    print("-" * 50)
    
    # Run appropriate solution
    if round_type == "round1a":
        success = run_round1a(input_dir, output_dir)
    elif round_type == "round1b":
        success = run_round1b(input_dir, output_dir)
    else:
        print("❌ Unknown round type detected")
        sys.exit(1)
    
    if success:
        print("\n🏆 Processing completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Processing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
