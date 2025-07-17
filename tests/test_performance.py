#!/usr/bin/env python3
"""
Performance test for Adobe India Hackathon Round 1A
Tests processing speed and validates 10-second requirement
"""

import os
import sys
import time
import json
from pathlib import Path

def setup_test_environment():
    """Set up the test environment"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Add src directory to path
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    return project_root

def main():
    """Main performance test function"""
    print("⏱️  Performance Test: PDF Outline Extractor")
    print("==================================================")
    
    # Set up environment
    project_root = setup_test_environment()
    
    # Import the solution
    try:
        import process_pdfs
    except ImportError as e:
        print(f"❌ Cannot import process_pdfs: {e}")
        sys.exit(1)
    
    # Find test PDF files
    input_dir = project_root / "input"
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in input/ directory")
        sys.exit(1)
    
    print(f"📄 Testing with {len(pdf_files)} PDF files...")
    
    # Test each file
    results = []
    total_time = 0
    
    for pdf_file in pdf_files:
        print(f"🔍 Testing: {pdf_file.name}")
        
        # Time the processing
        start_time = time.time()
        
        try:
            # Load and process the PDF
            doc = process_pdfs.load_pdf(str(pdf_file))
            title = process_pdfs.extract_title(doc)
            headings = process_pdfs.extract_headings(doc)
            
            processing_time = time.time() - start_time
            total_time += processing_time
            
            # Collect results
            result = {
                "file": pdf_file.name,
                "pages": len(doc),
                "time": processing_time,
                "title": title,
                "headings": len(headings)
            }
            results.append(result)
            
            print(f"  📊 Pages: {len(doc)}")
            print(f"  ⏱️  Time: {processing_time:.2f}s")
            print(f"  📝 Title: {title}")
            print(f"  🔤 Headings: {len(headings)}")
            
            # Check time requirement
            if processing_time <= 10:
                print(f"  ✅ Processing time OK ({processing_time:.2f}s < 10s)")
            else:
                print(f"  ❌ Processing time too long ({processing_time:.2f}s > 10s)")
                
        except Exception as e:
            print(f"  ❌ Error processing {pdf_file.name}: {e}")
            continue
    
    # Summary
    print(f"\n📈 Performance Summary:")
    print("------------------------------")
    print(f"Total files processed: {len(results)}")
    print(f"Total processing time: {total_time:.2f}s")
    print(f"Average time per file: {total_time/len(results):.2f}s")
    
    # Find longest processing time
    if results:
        longest = max(results, key=lambda x: x['time'])
        print(f"Longest processing time: {longest['time']:.2f}s ({longest['file']})")
    
    # Check overall requirement
    if total_time <= 10:
        print("✅ All files processed within 10-second limit!")
    else:
        print("❌ Total processing time exceeds 10 seconds")
    
    # Save detailed results
    results_file = project_root / "performance_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()
