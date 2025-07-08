#!/usr/bin/env python3
"""
African Companies Data Extraction Pipeline

Main entry point for the multi-stage data collection system that gathers 
comprehensive company information through web scraping, search optimization, 
and intelligent data extraction.

Usage:
    python template.py                          # Interactive mode
    python template.py --company "Flutterwave Nigeria"  # Extract single company
    python template.py --batch companies.txt   # Batch processing
    python template.py --setup                 # Setup validation
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add the akania src directory to Python path
src_path = Path(__file__).parent / "akania" / "src"
sys.path.insert(0, str(src_path))

try:
    from pipeline_orchestrator import CompanyDataPipeline, test_company
    from assistant import AfricanCompaniesAssistant
    from company_profiles import CompanyProfileManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure you're running from the project root directory.")
    sys.exit(1)


def setup_environment():
    """Load environment variables and validate setup"""
    # Load .env file if it exists
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return False
    
    return True


def create_env_template():
    """Create a .env template file if it doesn't exist"""
    env_file = Path(__file__).parent / ".env"
    env_template = Path(__file__).parent / ".env.example"
    
    if not env_file.exists() and not env_template.exists():
        template_content = """# African Companies Assistant - Environment Variables

# Required: OpenAI API Key for LLM processing
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Search APIs (at least one recommended)
TAVILY_API_KEY=your_tavily_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here

# Optional: Google Search API
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_cse_id_here
"""
        
        with open(env_template, 'w') as f:
            f.write(template_content)
        
        print(f"📄 Created {env_template}")
        print("Please copy this to .env and add your API keys.")


def extract_single_company(company_query: str):
    """Extract data for a single company"""
    print(f"🚀 Single Company Extraction Mode")
    print(f"Target: {company_query}")
    
    result = test_company(company_query)
    
    if result:
        print(f"\n✅ Successfully extracted data for {result.company_name}")
        return True
    else:
        print(f"\n❌ Failed to extract data for {company_query}")
        return False


def batch_extract_companies(batch_file: str):
    """Extract data for multiple companies from a file"""
    batch_path = Path(batch_file)
    
    if not batch_path.exists():
        print(f"❌ Batch file not found: {batch_file}")
        return False
    
    # Read company names from file
    try:
        with open(batch_path, 'r', encoding='utf-8') as f:
            companies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"❌ Error reading batch file: {e}")
        return False
    
    if not companies:
        print("❌ No companies found in batch file")
        return False
    
    print(f"🚀 Batch Extraction Mode")
    print(f"Processing {len(companies)} companies from {batch_file}")
    
    # Run batch extraction
    pipeline = CompanyDataPipeline()
    results = pipeline.batch_extract(companies)
    
    # Generate summary
    successful = sum(1 for result in results.values() if result is not None)
    print(f"\n📊 FINAL SUMMARY")
    print(f"Total: {len(companies)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(companies) - successful}")
    
    return successful > 0


def validate_setup():
    """Validate system setup and configuration"""
    print("🔧 SYSTEM VALIDATION")
    print("=" * 40)
    
    # Check environment setup
    env_ok = setup_environment()
    print(f"Environment setup: {'✅' if env_ok else '❌'}")
    
    # Check pipeline components
    try:
        pipeline = CompanyDataPipeline()
        validation = pipeline.validate_setup()
        
        print("\nPipeline Components:")
        for component, status in validation.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component.replace('_', ' ').title()}")
        
        # Overall status
        critical_ok = validation.get('llm_ready', False)
        search_ok = validation.get('website_discovery_ready', False)
        
        if critical_ok and search_ok:
            print(f"\n✅ System is ready for operation!")
            return True
        else:
            print(f"\n❌ System setup incomplete.")
            return False
            
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False


def interactive_mode():
    """Run the interactive assistant"""
    print("🤖 Starting Interactive Assistant Mode")
    assistant = AfricanCompaniesAssistant()
    assistant.run()


def create_sample_batch_file():
    """Create a sample batch file for testing"""
    sample_file = Path(__file__).parent / "sample_companies.txt"
    
    if sample_file.exists():
        return
    
    sample_companies = [
        "# African Companies Sample Batch File",
        "# One company per line, comments start with #",
        "",
        "Flutterwave Nigeria",
        "Jumia Kenya", 
        "Andela Nigeria",
        "Paystack Nigeria",
        "Kuda Bank Nigeria",
        "Sendy Kenya",
        "Kobo360 Nigeria",
        "Cellulant Kenya"
    ]
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_companies))
    
    print(f"📄 Created sample batch file: {sample_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="African Companies Data Extraction Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python template.py                                    # Interactive mode
  python template.py --company "Flutterwave Nigeria"   # Single extraction
  python template.py --batch companies.txt             # Batch processing
  python template.py --setup                           # Validate setup
  python template.py --create-sample                   # Create sample files
        """
    )
    
    parser.add_argument('--company', '-c', 
                       help='Extract data for a single company')
    parser.add_argument('--batch', '-b', 
                       help='Batch extract from file (one company per line)')
    parser.add_argument('--setup', '-s', action='store_true',
                       help='Validate system setup and configuration')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample batch file and .env template')
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.create_sample:
        create_env_template()
        create_sample_batch_file()
        return
    
    if args.setup:
        success = validate_setup()
        sys.exit(0 if success else 1)
    
    # Ensure environment is set up
    if not setup_environment():
        print("\n💡 Tip: Run 'python template.py --create-sample' to create template files")
        sys.exit(1)
    
    if args.company:
        success = extract_single_company(args.company)
        sys.exit(0 if success else 1)
    
    elif args.batch:
        success = batch_extract_companies(args.batch)
        sys.exit(0 if success else 1)
    
    else:
        # Default to interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()