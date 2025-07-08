"""
Console assistant for answering questions about African companies.
Based on your notebook implementation.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from company_profiles import CompanyInfo, save_company_profile
from scraper import extract_urls_from_tavily, scrape_urls

# Load environment
load_dotenv('../../.env')

def extract_company_data(company_query: str):
    """Extract company data - from your notebook with retry mechanism"""
    try:
        # Setup
        search = TavilySearch(max_results=5, topic="general")
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a data extraction expert. Extract company information from the provided web content.

            **Instructions:**
            - Extract only factual information that is explicitly mentioned in the content
            - If information is not found, leave the field empty/null
            - Focus on the main company being discussed
            - Use exact names and terms from the source

            **Extract the following information:**
            - Company name
            - Countries where it operates (focus on African countries if mentioned)
            - Industry/sector
            - Business description (About 100 words)
            - Key people (names and titles)
            - transactions involving the company
            - Any other notable business activities

            Provide the information in a structured format.

            web contents: {content}
            urls: {urls}
            """),
        ])
        
        llm_with_structured_output = llm.with_structured_output(CompanyInfo)
        chain = prompt | llm_with_structured_output

        def try_extraction(search_query: str):
            """Helper function to try extraction with a specific query"""
            # Search with Tavily
            tavily_response = search.invoke({"query": search_query})

            if not tavily_response or not tavily_response.get('results'):
                return None

            # Extract URLs (limit to 3)
            urls = extract_urls_from_tavily(tavily_response)[:3]

            if not urls:
                return None

            # Scrape all URLs
            scraped_docs = scrape_urls(urls)

            if not scraped_docs:
                return None

            # Extract structured data
            result = chain.invoke({
                "content": scraped_docs,
                "urls": urls
            })

            return result

        def is_result_incomplete(result):
            """Check if result has empty/missing key fields"""
            if not result:
                return True
            
            # Check for empty key fields
            empty_fields = (
                not result.company_name or
                not result.countries or
                not result.sector or
                not result.business_description
            )
            return empty_fields

        # First attempt with original query
        print(f"🔍 First search: I need only website urls for {company_query}")
        result = try_extraction(f"I need only website urls for {company_query}")
        
        # If result is incomplete, try alternate query
        if is_result_incomplete(result):
            company_name = company_query.split('(')[0].strip()  # Extract company name without country
            alternate_query = f"{company_name} company about business information profile"
            print(f"🔄 Retry search: {alternate_query}")
            
            retry_result = try_extraction(alternate_query)
            
            # Use retry result if it's more complete
            if retry_result and not is_result_incomplete(retry_result):
                result = retry_result
                print("✅ Retry successful - using improved data")
            elif retry_result:
                # Merge results if both have some data
                if result and retry_result:
                    # Use non-empty fields from retry result
                    if not result.company_name and retry_result.company_name:
                        result.company_name = retry_result.company_name
                    if not result.countries and retry_result.countries:
                        result.countries = retry_result.countries
                    if not result.sector and retry_result.sector:
                        result.sector = retry_result.sector
                    if not result.business_description and retry_result.business_description:
                        result.business_description = retry_result.business_description
                    if not result.key_people and retry_result.key_people:
                        result.key_people = retry_result.key_people
                    print("🔄 Merged data from both searches")

        # Save to JSON
        if result:
            save_company_profile(result)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None

def quick_test(company_name: str):
    """Quick test function from your notebook"""
    result = extract_company_data(company_name)

    if result:
        print(f"✅ SUCCESS!")
        print(f"Company: {result.company_name}")
        print(f"Countries: {result.countries}")
        print(f"Sector: {result.sector}")
        print(f"Key People: {len(result.key_people)}")
        print(f"URLs scraped: {len(result.source_urls)}")
    else:
        print("❌ FAILED")

    return result

def main():
    """Test the 5 companies"""
    print("🌍 Starting African Companies Data Extraction...")
    print("=" * 50)
    
    companies = [
        "Sylndr (Egypt)",
        "Lapaire Glasses (Kenya)", 
        "Merec Industries (Mozambique)",
        "SanLei (Lesotho)",
        "Moni-Shop (DRC)"
    ]
    
    print("🌍 African Companies Data Extraction")
    print("=" * 40)
    
    # Check API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set OPENAI_API_KEY in .env file")
        return
    
    if not os.getenv('TAVILY_API_KEY'):
        print("❌ Please set TAVILY_API_KEY in .env file")
        return
    
    print("✅ API keys configured")
    
    # Test each company
    for i, company in enumerate(companies, 1):
        print(f"\n--- Testing {i}/5: {company} ---")
        quick_test(company)

if __name__ == "__main__":
    main()
