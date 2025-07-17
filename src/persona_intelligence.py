#!/usr/bin/env python3
"""
Round 1B: Persona-Driven Document Intelligence
Adobe India Hackathon 2025

This module implements intelligent document analysis that extracts and prioritizes
the most relevant sections based on a specific persona and their job-to-be-done.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import PyPDF2
import fitz  # PyMuPDF
from collections import defaultdict, Counter

# Persona definitions with keywords and priorities
PERSONA_DEFINITIONS = {
    "travel_planner": {
        "keywords": [
            "travel", "trip", "tourism", "vacation", "holiday", "destination", "visit", "tour",
            "restaurant", "hotel", "accommodation", "booking", "reservation", "flight", "transport",
            "attractions", "sightseeing", "culture", "tradition", "food", "cuisine", "dining",
            "things to do", "activities", "guide", "tips", "recommendations", "must-see", "itinerary",
            "france", "french", "south", "cities", "history", "places", "location", "region"
        ],
        "priority_sections": [
            "destinations", "attractions", "restaurants", "hotels", "things to do", 
            "activities", "culture", "food", "dining", "travel tips", "recommendations"
        ]
    },
    "hr_professional": {
        "keywords": [
            "hr", "human resources", "employee", "staff", "personnel", "workforce", "hiring",
            "recruitment", "training", "development", "skills", "performance", "management",
            "leadership", "team", "organization", "company", "business", "professional",
            "career", "job", "work", "workplace", "productivity", "efficiency", "process",
            "adobe", "acrobat", "pdf", "software", "tools", "digital", "technology", "workflow",
            "collaboration", "document", "sharing", "signature", "form", "automation"
        ],
        "priority_sections": [
            "training", "skills", "development", "management", "workflow", "productivity",
            "collaboration", "tools", "software", "process", "efficiency", "business"
        ]
    },
    "home_cook": {
        "keywords": [
            "food", "recipe", "cooking", "kitchen", "meal", "dish", "ingredient", "preparation",
            "breakfast", "lunch", "dinner", "appetizer", "main", "side", "dessert", "snack",
            "cuisine", "culinary", "chef", "taste", "flavor", "seasoning", "spice", "herb",
            "baking", "roasting", "grilling", "frying", "healthy", "nutrition", "diet",
            "vegetarian", "vegan", "protein", "carbs", "vegetables", "meat", "seafood"
        ],
        "priority_sections": [
            "recipes", "ingredients", "preparation", "cooking", "meals", "breakfast", 
            "lunch", "dinner", "food", "kitchen", "culinary", "nutrition", "healthy"
        ]
    }
}

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with page information"""
    pages_text = []
    
    try:
        # Use PyMuPDF for better text extraction
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            pages_text.append({
                "page_number": page_num + 1,  # 1-based for user reference
                "text": text.strip(),
                "file": os.path.basename(pdf_path)
            })
        
        doc.close()
        
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        # Fallback to PyPDF2
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    pages_text.append({
                        "page_number": page_num + 1,
                        "text": text.strip(),
                        "file": os.path.basename(pdf_path)
                    })
        except Exception as e2:
            print(f"Both extraction methods failed for {pdf_path}: {e2}")
    
    return pages_text

def detect_persona(documents_text):
    """Detect the most likely persona based on document content"""
    all_text = " ".join([
        page["text"].lower() 
        for doc in documents_text 
        for page in doc
    ])
    
    persona_scores = {}
    
    for persona_name, persona_data in PERSONA_DEFINITIONS.items():
        score = 0
        keyword_matches = 0
        
        for keyword in persona_data["keywords"]:
            # Count keyword occurrences
            matches = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', all_text))
            if matches > 0:
                keyword_matches += 1
                score += matches
        
        # Boost score based on keyword diversity
        if keyword_matches > 0:
            diversity_bonus = (keyword_matches / len(persona_data["keywords"])) * 100
            score += diversity_bonus
        
        persona_scores[persona_name] = {
            "score": score,
            "keyword_matches": keyword_matches,
            "coverage": keyword_matches / len(persona_data["keywords"])
        }
    
    # Find best matching persona
    best_persona = max(persona_scores.items(), key=lambda x: x[1]["score"])
    
    print(f"Persona Detection Results:")
    for name, data in persona_scores.items():
        print(f"  {name}: score={data['score']:.1f}, matches={data['keyword_matches']}, coverage={data['coverage']:.2%}")
    
    return best_persona[0], persona_scores

def score_section_relevance(page_text, persona_name):
    """Score how relevant a section is to the detected persona"""
    if persona_name not in PERSONA_DEFINITIONS:
        return 0, []
    
    persona_data = PERSONA_DEFINITIONS[persona_name]
    text_lower = page_text.lower()
    
    score = 0
    matched_keywords = []
    
    # Score based on keyword matches
    for keyword in persona_data["keywords"]:
        matches = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
        if matches > 0:
            score += matches * 2  # Base score per match
            matched_keywords.append(keyword)
    
    # Bonus for priority sections
    for priority in persona_data["priority_sections"]:
        if priority.lower() in text_lower:
            score += 10  # High bonus for priority sections
            if priority not in matched_keywords:
                matched_keywords.append(priority)
    
    # Bonus for longer, more substantial content
    word_count = len(text_lower.split())
    if word_count > 50:
        score += min(word_count / 10, 20)  # Cap at 20 bonus points
    
    return score, matched_keywords

def extract_sections_and_analyze(documents_text, persona_name):
    """Extract and analyze sections for persona relevance"""
    extracted_sections = []
    subsection_analysis = []
    
    all_sections = []
    
    # Process each document
    for doc_pages in documents_text:
        for page in doc_pages:
            if not page["text"].strip():
                continue
            
            # Score this page/section
            relevance_score, keywords = score_section_relevance(page["text"], persona_name)
            
            if relevance_score > 5:  # Minimum relevance threshold
                # Extract section title (first meaningful line)
                lines = page["text"].split('\n')
                section_title = "Content Section"
                
                for line in lines[:5]:  # Check first 5 lines
                    clean_line = line.strip()
                    if len(clean_line) > 10 and len(clean_line) < 100:
                        # Likely a title or heading
                        section_title = clean_line
                        break
                
                section_data = {
                    "document": page["file"],
                    "page_number": page["page_number"],
                    "section_title": section_title,
                    "relevance_score": relevance_score,
                    "matched_keywords": keywords
                }
                
                all_sections.append(section_data)
                
                # Create refined text for subsection analysis
                refined_text = page["text"][:500] + "..." if len(page["text"]) > 500 else page["text"]
                
                subsection_analysis.append({
                    "document": page["file"],
                    "page_number": page["page_number"],
                    "refined_text": refined_text.strip(),
                    "relevance_score": relevance_score,
                    "matched_keywords": keywords
                })
    
    # Sort by relevance score and assign importance ranks
    all_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    for i, section in enumerate(all_sections):
        section["importance_rank"] = i + 1
        extracted_sections.append({
            "document": section["document"],
            "page_number": section["page_number"],
            "section_title": section["section_title"],
            "importance_rank": section["importance_rank"]
        })
    
    return extracted_sections, subsection_analysis

def generate_job_to_be_done(persona_name, documents):
    """Generate a job-to-be-done based on persona and document content"""
    job_descriptions = {
        "travel_planner": f"Plan comprehensive travel itinerary using information from {len(documents)} documents",
        "hr_professional": f"Analyze training and development resources across {len(documents)} documents for workforce planning",
        "home_cook": f"Discover and organize recipes and cooking ideas from {len(documents)} culinary documents"
    }
    
    return job_descriptions.get(persona_name, f"Analyze and extract insights from {len(documents)} documents")

def analyze_persona_intelligence(input_dir, output_dir):
    """Main function for Round 1B persona-driven document intelligence"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found for persona intelligence analysis")
        return False
    
    print(f"🔄 Analyzing {len(pdf_files)} documents for persona intelligence...")
    
    # Extract text from all documents
    documents_text = []
    document_names = []
    
    for pdf_file in pdf_files:
        print(f"  📄 Processing: {pdf_file.name}")
        pages_text = extract_text_from_pdf(pdf_file)
        documents_text.append(pages_text)
        document_names.append(pdf_file.name)
    
    # Detect persona
    print("\n🧠 Detecting persona...")
    persona_name, persona_scores = detect_persona(documents_text)
    
    # Map internal names to user-friendly names
    persona_display_names = {
        "travel_planner": "Travel Planner",
        "hr_professional": "HR Professional", 
        "home_cook": "Home Cook"
    }
    
    display_persona = persona_display_names.get(persona_name, persona_name.replace("_", " ").title())
    print(f"🎯 Detected persona: {display_persona}")
    
    # Generate job-to-be-done
    job_to_be_done = generate_job_to_be_done(persona_name, documents_text)
    
    # Extract and analyze sections
    print(f"\n📊 Analyzing content relevance for {display_persona}...")
    extracted_sections, subsection_analysis = extract_sections_and_analyze(documents_text, persona_name)
    
    # Prepare output data
    output_data = {
        "metadata": {
            "documents": document_names,
            "persona": display_persona,
            "job_to_be_done": job_to_be_done,
            "timestamp": datetime.now().isoformat() + "Z",
            "detected_persona_confidence": persona_scores[persona_name]["score"],
            "total_sections_analyzed": len(extracted_sections)
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
    
    # Save output
    output_file = output_path / "persona_intelligence_output.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Analysis complete!")
    print(f"📈 Found {len(extracted_sections)} relevant sections")
    print(f"💾 Output saved to: {output_file.name}")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python persona_intelligence.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    success = analyze_persona_intelligence(input_dir, output_dir)
    sys.exit(0 if success else 1)
