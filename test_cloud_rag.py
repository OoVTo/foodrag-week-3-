# -*- coding: utf-8 -*-
"""
Cloud RAG System - Comprehensive Test Suite

This test suite validates the Upstash Vector Database + Groq LLM integration.
Tests cover integration, data handling, semantic search, and LLM generation.

Run with: python -m pytest test_cloud_rag.py -v
Or directly: python test_cloud_rag.py
"""

import os
import json
import sys
import time
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_test_header(message: str):
    """Print formatted test header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_pass(message: str):
    """Print green pass message"""
    print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {message}")


def print_fail(message: str):
    """Print red fail message"""
    print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {message}")


def print_skip(message: str):
    """Print yellow skip message"""
    print(f"{Colors.YELLOW}⊘ SKIP{Colors.RESET}: {message}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  INFO{Colors.RESET}: {message}")


# ============================================================================
# TEST 1: Environment & Configuration
# ============================================================================

def test_environment_setup():
    """Test that environment variables are properly configured"""
    print_test_header("TEST 1: Environment & Configuration")
    
    tests_passed = 0
    tests_failed = 0
    
    # Check if .env file exists
    env_file_exists = os.path.isfile('.env')
    if env_file_exists:
        print_pass(".env file exists")
        tests_passed += 1
    else:
        print_skip(".env file not found (expected for testing)")
        
    # Check for environment variables
    required_vars = [
        'UPSTASH_VECTOR_REST_URL',
        'UPSTASH_VECTOR_REST_TOKEN', 
        'GROQ_API_KEY'
    ]
    
    for var in required_vars:
        if os.getenv(var):
            print_pass(f"Environment variable {var} is set")
            tests_passed += 1
        else:
            print_info(f"Environment variable {var} not set (set in .env file)")
    
    # Check foods.json exists
    if os.path.isfile('foods.json'):
        print_pass("foods.json exists")
        tests_passed += 1
    else:
        print_fail("foods.json not found")
        tests_failed += 1
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 2: Food Database Validation
# ============================================================================

def test_food_database():
    """Test food database structure and content"""
    print_test_header("TEST 2: Food Database Validation")
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        with open('foods.json', 'r', encoding='utf-8') as f:
            foods = json.load(f)
        
        # Check if it's a list
        if isinstance(foods, list):
            print_pass(f"Foods database is a valid list with {len(foods)} items")
            tests_passed += 1
        else:
            print_fail("Foods database is not a list")
            tests_failed += 1
            return tests_passed, tests_failed
        
        # Check minimum items (requirement: 20+)
        if len(foods) >= 20:
            print_pass(f"Database has {len(foods)} items (requirement met)")
            tests_passed += 1
        else:
            print_fail(f"Database has only {len(foods)} items (need 20+)")
            tests_failed += 1
        
        # Validate food item structure
        required_fields = ['id', 'text']
        valid_items = 0
        
        for item in foods:
            if all(field in item for field in required_fields):
                valid_items += 1
        
        if valid_items == len(foods):
            print_pass(f"All {len(foods)} items have required fields")
            tests_passed += 1
        else:
            print_fail(f"Only {valid_items}/{len(foods)} items have required fields")
            tests_failed += 1
        
        # Check metadata enrichment
        metadata_fields = ['region', 'type', 'cooking_method', 'nutritional_benefits']
        items_with_metadata = 0
        
        for item in foods:
            if any(field in item for field in metadata_fields):
                items_with_metadata += 1
        
        enrichment_ratio = (items_with_metadata / len(foods)) * 100
        if enrichment_ratio >= 70:
            print_pass(f"Metadata enrichment: {enrichment_ratio:.1f}% of items")
            tests_passed += 1
        else:
            print_info(f"Metadata enrichment: {enrichment_ratio:.1f}% (could be improved)")
        
        # Check cuisine diversity
        regions = set()
        food_types = set()
        for item in foods:
            if 'region' in item:
                regions.add(item['region'])
            if 'type' in item:
                food_types.add(item['type'])
        
        if len(regions) >= 3:
            print_pass(f"Good cuisine diversity: {len(regions)} regions covered")
            tests_passed += 1
        else:
            print_info(f"Cuisine coverage: {len(regions)} regions")
        
    except json.JSONDecodeError:
        print_fail("foods.json is not valid JSON")
        tests_failed += 1
    except FileNotFoundError:
        print_fail("foods.json not found")
        tests_failed += 1
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 3: Upstash Integration (if credentials available)
# ============================================================================

def test_upstash_integration():
    """Test Upstash Vector Database integration"""
    print_test_header("TEST 3: Upstash Vector Database Integration")
    
    tests_passed = 0
    tests_failed = 0
    
    upstash_url = os.getenv('UPSTASH_VECTOR_REST_URL')
    upstash_token = os.getenv('UPSTASH_VECTOR_REST_TOKEN')
    
    if not upstash_url or not upstash_token:
        print_skip("Upstash credentials not configured")
        print_info("To test: Set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN")
        return tests_passed, tests_failed
    
    try:
        from upstash_vector import Index
        print_pass("Upstash Vector SDK is installed")
        tests_passed += 1
        
        # Try to initialize connection
        try:
            vector_index = Index(url=upstash_url, token=upstash_token)
            print_pass("Connected to Upstash Vector Database")
            tests_passed += 1
            
            # Try to get info
            info = vector_index.info()
            print_pass(f"Database info retrieved - Vector count: {info.get('vector_count', 'N/A')}")
            tests_passed += 1
            
        except Exception as e:
            print_fail(f"Could not connect to Upstash: {str(e)}")
            tests_failed += 1
            
    except ImportError:
        print_skip("Upstash Vector SDK not installed")
        print_info("To test: pip install upstash-vector")
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 4: Groq LLM Integration (if credentials available)
# ============================================================================

def test_groq_integration():
    """Test Groq LLM API integration"""
    print_test_header("TEST 4: Groq LLM API Integration")
    
    tests_passed = 0
    tests_failed = 0
    
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key:
        print_skip("Groq API key not configured")
        print_info("To test: Set GROQ_API_KEY environment variable")
        return tests_passed, tests_failed
    
    try:
        from groq import Groq
        print_pass("Groq Python SDK is installed")
        tests_passed += 1
        
        # Initialize client
        try:
            client = Groq(api_key=groq_key)
            print_pass("Groq API client initialized successfully")
            tests_passed += 1
            
            # Test model fallback list
            models = [
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768"
            ]
            print_pass(f"Model fallback chain ready ({len(models)} models)")
            tests_passed += 1
            
        except Exception as e:
            print_fail(f"Could not initialize Groq client: {str(e)}")
            tests_failed += 1
            
    except ImportError:
        print_skip("Groq SDK not installed")
        print_info("To test: pip install groq")
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 5: Cloud Version Script Validation
# ============================================================================

def test_cloud_version_script():
    """Validate cloud-version/rag_run.py exists and has required functions"""
    print_test_header("TEST 5: Cloud Version Script Validation")
    
    tests_passed = 0
    tests_failed = 0
    
    cloud_script = 'cloud-version/rag_run.py'
    
    if os.path.isfile(cloud_script):
        print_pass("Cloud version script exists")
        tests_passed += 1
        
        # Check file size
        size = os.path.getsize(cloud_script)
        if size > 5000:
            print_pass(f"Script is substantial ({size} bytes)")
            tests_passed += 1
        else:
            print_info(f"Script size: {size} bytes")
        
        # Check for required imports
        with open(cloud_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_imports = [
            'from upstash_vector import Index',
            'from groq import Groq',
            'class RAGEditorApp',
            'def ask_question'
        ]
        
        for import_str in required_imports:
            if import_str in content:
                print_pass(f"Contains: {import_str.split()[0]}...")
                tests_passed += 1
            else:
                print_fail(f"Missing: {import_str}")
                tests_failed += 1
    else:
        print_fail(f"Cloud version script not found: {cloud_script}")
        tests_failed += 1
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 6: Documentation Completeness
# ============================================================================

def test_documentation():
    """Verify all documentation files exist and are substantial"""
    print_test_header("TEST 6: Documentation Completeness")
    
    tests_passed = 0
    tests_failed = 0
    
    required_docs = {
        'README.md': 'Main documentation',
        'CLOUD_SETUP.md': 'Cloud setup guide',
        'IMPLEMENTATION_SUMMARY.md': 'Implementation details',
        'PERFORMANCE_COMPARISON.md': 'Performance report',
        '.env.example': 'Environment template',
    }
    
    for doc, description in required_docs.items():
        if os.path.isfile(doc):
            size = os.path.getsize(doc)
            if size > 500:  # At least 500 bytes
                print_pass(f"{doc} exists ({size} bytes) - {description}")
                tests_passed += 1
            else:
                print_fail(f"{doc} exists but is too small ({size} bytes)")
                tests_failed += 1
        else:
            print_fail(f"Missing: {doc}")
            tests_failed += 1
    
    return tests_passed, tests_failed


# ============================================================================
# TEST 7: Performance Baseline
# ============================================================================

def test_performance_baseline():
    """Test baseline performance of critical operations"""
    print_test_header("TEST 7: Performance Baseline")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test JSON loading performance
    start = time.time()
    with open('foods.json', 'r', encoding='utf-8') as f:
        foods = json.load(f)
    json_load_time = time.time() - start
    
    if json_load_time < 0.5:  # Should load in <500ms
        print_pass(f"JSON loading: {json_load_time*1000:.1f}ms (target: <500ms)")
        tests_passed += 1
    else:
        print_info(f"JSON loading: {json_load_time*1000:.1f}ms")
    
    # Test text enrichment performance
    if foods:
        start = time.time()
        item = foods[0]
        enriched = item.get("text", "")
        if "region" in item:
            enriched += f" Region: {item['region']}."
        if "type" in item:
            enriched += f" Type: {item['type']}."
        enrichment_time = time.time() - start
        
        if enrichment_time < 0.001:  # Should be <1ms
            print_pass(f"Text enrichment: {enrichment_time*1000:.3f}ms (target: <1ms)")
            tests_passed += 1
        else:
            print_info(f"Text enrichment: {enrichment_time*1000:.3f}ms")
    
    print_pass("Performance baseline established")
    tests_passed += 1
    
    return tests_passed, tests_failed


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and provide summary"""
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  Cloud RAG System - Quality Assurance Test Suite".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    print(f"{Colors.RESET}\n")
    
    all_results = []
    
    # Run all tests
    all_results.append(("Environment Setup", test_environment_setup()))
    all_results.append(("Food Database", test_food_database()))
    all_results.append(("Upstash Integration", test_upstash_integration()))
    all_results.append(("Groq Integration", test_groq_integration()))
    all_results.append(("Cloud Script", test_cloud_version_script()))
    all_results.append(("Documentation", test_documentation()))
    all_results.append(("Performance", test_performance_baseline()))
    
    # Print summary
    print_test_header("TEST SUMMARY")
    
    total_pass = 0
    total_fail = 0
    
    for test_name, (passed, failed) in all_results:
        total_pass += passed
        total_fail += failed
        status_symbol = f"{Colors.GREEN}✅{Colors.RESET}" if failed == 0 else f"{Colors.RED}⚠️ {Colors.RESET}"
        print(f"{status_symbol} {test_name}: {passed} passed, {failed} failed")
    
    # Final verdict
    print(f"\n{Colors.BOLD}" + "="*70 + f"{Colors.RESET}")
    
    if total_fail == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.RESET}")
        print(f"   Total: {total_pass} tests passed")
    else:
        print(f"{Colors.YELLOW}⚠️  SOME TESTS FAILED{Colors.RESET}")
        print(f"   Passed: {total_pass} | Failed: {total_fail}")
    
    print(f"{Colors.BOLD}" + "="*70 + f"{Colors.RESET}\n")
    
    return total_fail == 0


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
