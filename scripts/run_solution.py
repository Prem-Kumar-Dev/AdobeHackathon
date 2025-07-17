#!/usr/bin/env python3
"""
Main solution runner for Adobe India Hackathon Round 1A
This script sets up the proper input/output paths and runs the PDF outline extractor
"""

import os
import sys
import shutil
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def setup_docker_simulation():
    """Set up directories to simulate Docker environment"""
    base_dir = Path(__file__).parent.parent  # Go up to project root
    
    # Create input and output directories
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"
    
    # Clean existing directories
    if input_dir.exists():
        shutil.rmtree(input_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # Create fresh directories
    input_dir.mkdir()
    output_dir.mkdir()
    
    # Copy sample PDFs from dataset
    dataset_pdfs = base_dir / "Dataset" / "Challenge _1(a)" / "Datasets" / "Pdfs"
    if dataset_pdfs.exists():
        for pdf_file in dataset_pdfs.glob("*.pdf"):
            shutil.copy2(pdf_file, input_dir)
            print(f"📄 Added {pdf_file.name} to input/")
    else:
        print(f"⚠️  Dataset not found at: {dataset_pdfs}")
        print("Please ensure the Dataset folder contains Challenge _1(a) data")
    
    return input_dir, output_dir

def patch_paths_for_local_run(input_dir, output_dir):
    """Patch the paths in process_pdfs for local execution"""
    import process_pdfs
    
    # Monkey patch the Path function
    original_path = process_pdfs.Path
    
    def patched_path(path_str):
        if path_str == "/app/input":
            return input_dir
        elif path_str == "/app/output":
            return output_dir
        else:
            return original_path(path_str)
    
    process_pdfs.Path = patched_path
    return original_path

def main():
    """Main function to run the solution"""
    print("🚀 Adobe India Hackathon - Round 1A: PDF Outline Extractor")
    print("=" * 60)
    print("Running solution locally (simulating Docker environment)")
    print("=" * 60)
    
    try:
        # Setup directories
        input_dir, output_dir = setup_docker_simulation()
        
        # Import and patch the processor
        import process_pdfs
        original_path = patch_paths_for_local_run(input_dir, output_dir)
        
        # Run the main processing function
        process_pdfs.process_pdfs()
        
        # Show results
        print("\n📊 Results Summary:")
        print("-" * 30)
        
        output_files = list(output_dir.glob("*.json"))
        if output_files:
            print(f"✅ Successfully processed {len(output_files)} files:")
            for json_file in output_files:
                print(f"  📄 {json_file.name}")
        else:
            print("❌ No output files generated")
        
        print(f"\n📁 Results available in: {output_dir}")
        print("=" * 60)
        print("🎉 Solution completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running solution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
