#!/usr/bin/env python3
"""
Local functionality test for Adobe India Hackathon Round 1A
Tests basic functionality of the PDF outline extractor
"""

import os
import sys
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

def test_basic_functionality():
    """Test basic functionality of the PDF processor"""
    print("🧪 Testing Basic Functionality")
    print("==============================")
    
    # Set up environment
    project_root = setup_test_environment()
    
    # Import the solution
    try:
        import process_pdfs
        print("✅ Successfully imported process_pdfs")
    except ImportError as e:
        print(f"❌ Cannot import process_pdfs: {e}")
        return False
    
    # Test with sample files
    input_dir = project_root / "input"
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in input/ directory")
        return False
    
    print(f"📄 Found {len(pdf_files)} PDF files for testing")
    
    # Test each file
    for pdf_file in pdf_files[:3]:  # Test first 3 files
        print(f"\n🔍 Testing: {pdf_file.name}")
        
        try:
            # Load PDF
            doc = process_pdfs.load_pdf(str(pdf_file))
            print(f"  ✅ Successfully loaded PDF ({len(doc)} pages)")
            
            # Extract title
            title = process_pdfs.extract_title(doc)
            print(f"  ✅ Extracted title: '{title}'")
            
            # Extract headings
            headings = process_pdfs.extract_headings(doc)
            print(f"  ✅ Extracted {len(headings)} headings")
            
            # Validate output format
            if headings:
                sample_heading = headings[0]
                required_keys = {'level', 'text', 'page'}
                if all(key in sample_heading for key in required_keys):
                    print(f"  ✅ Heading format is valid")
                else:
                    print(f"  ❌ Invalid heading format: {sample_heading}")
                    return False
            
        except Exception as e:
            print(f"  ❌ Error processing {pdf_file.name}: {e}")
            return False
    
    return True

def test_output_format():
    """Test that output JSON format is correct"""
    print("\n🧪 Testing Output Format")
    print("=========================")
    
    # Set up environment
    project_root = setup_test_environment()
    
    # Check output directory
    output_dir = project_root / "output"
    json_files = list(output_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No JSON output files found")
        return False
    
    print(f"📄 Found {len(json_files)} JSON output files")
    
    # Test each JSON file
    for json_file in json_files[:2]:  # Test first 2 files
        print(f"\n🔍 Testing: {json_file.name}")
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Check required fields
            if 'title' not in data:
                print(f"  ❌ Missing 'title' field")
                return False
            
            if 'outline' not in data:
                print(f"  ❌ Missing 'outline' field")
                return False
            
            print(f"  ✅ Has required fields (title, outline)")
            
            # Check outline format
            if data['outline']:
                sample_heading = data['outline'][0]
                required_keys = {'level', 'text', 'page'}
                if all(key in sample_heading for key in required_keys):
                    print(f"  ✅ Outline format is valid")
                else:
                    print(f"  ❌ Invalid outline format: {sample_heading}")
                    return False
            
            print(f"  ✅ Title: '{data['title']}'")
            print(f"  ✅ Outline entries: {len(data['outline'])}")
            
        except Exception as e:
            print(f"  ❌ Error reading {json_file.name}: {e}")
            return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Adobe India Hackathon - Round 1A: Local Tests")
    print("==================================================")
    
    success = True
    
    # Run basic functionality test
    if not test_basic_functionality():
        success = False
    
    # Run output format test
    if not test_output_format():
        success = False
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("================")
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
