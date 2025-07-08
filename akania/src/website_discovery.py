"""
Website discovery module for finding company websites.
Based on Tavily search and SerpAPI implementations.
"""
import os
from typing import List, Dict, Optional
from langchain_tavily import TavilySearch
from langchain_community.utilities import SerpAPIWrapper


class WebsiteDiscoveryService:
    """Service for discovering company websites using multiple search engines"""
    
    def __init__(self):
        self.tavily_search = None
        self.serp_search = None
        self._initialize_search_engines()
    
    def _initialize_search_engines(self):
        """Initialize available search engines based on API keys"""
        try:
            if os.getenv('TAVILY_API_KEY'):
                self.tavily_search = TavilySearch(
                    max_results=5,
                    topic="general"
                )
        except Exception as e:
            print(f"Tavily initialization failed: {e}")
        
        try:
            if os.getenv('SERPAPI_API_KEY'):
                self.serp_search = SerpAPIWrapper()
        except Exception as e:
            print(f"SerpAPI initialization failed: {e}")
    
    def extract_urls_from_tavily(self, tavily_response: Dict) -> List[str]:
        """Extract all URLs from Tavily search results"""
        if not tavily_response or 'results' not in tavily_response:
            return []
        
        results = tavily_response.get('results', [])
        urls = [result.get('url') for result in results if result.get('url')]
        return urls
    
    def search_with_tavily(self, company_query: str, max_results: int = 5) -> List[str]:
        """Search for company URLs using Tavily"""
        if not self.tavily_search:
            return []
        
        try:
            query = f"I need only website urls for {company_query}"
            response = self.tavily_search.invoke({"query": query})
            urls = self.extract_urls_from_tavily(response)
            return urls[:max_results]
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    def search_with_serpapi(self, company_query: str) -> List[str]:
        """Search for company URLs using SerpAPI"""
        if not self.serp_search:
            return []
        
        try:
            query = f"I need website urls for {company_query}"
            response = self.serp_search.run(query)
            # Parse response and extract URLs
            # Note: SerpAPI response parsing would need to be implemented
            # based on actual response format
            return []
        except Exception as e:
            print(f"SerpAPI search error: {e}")
            return []
    
    def discover_company_websites(self, company_query: str, max_urls: int = 3) -> List[str]:
        """
        Discover company websites using available search engines
        
        Args:
            company_query: Company name and optionally country/region
            max_urls: Maximum number of URLs to return
        
        Returns:
            List of discovered website URLs
        """
        all_urls = []
        
        # Try Tavily first
        tavily_urls = self.search_with_tavily(company_query, max_urls)
        all_urls.extend(tavily_urls)
        
        # If we don't have enough URLs, try SerpAPI
        if len(all_urls) < max_urls and self.serp_search:
            serp_urls = self.search_with_serpapi(company_query)
            all_urls.extend(serp_urls)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in all_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls[:max_urls]
    
    def validate_website_url(self, url: str) -> bool:
        """Basic validation of website URL"""
        if not url:
            return False
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Add more validation logic as needed
        return True
    
    def filter_relevant_urls(self, urls: List[str], company_name: str) -> List[str]:
        """Filter URLs to keep only those likely to be company websites"""
        if not urls:
            return []
        
        # Simple filtering - prioritize domains that contain company name
        company_words = company_name.lower().split()
        
        relevant_urls = []
        other_urls = []
        
        for url in urls:
            if any(word in url.lower() for word in company_words):
                relevant_urls.append(url)
            else:
                other_urls.append(url)
        
        # Return relevant URLs first, then others
        return relevant_urls + other_urls


# Convenience function for quick usage
def discover_websites(company_query: str, max_urls: int = 3) -> List[str]:
    """
    Quick function to discover company websites
    
    Args:
        company_query: Company name and optionally country/region
        max_urls: Maximum number of URLs to return
    
    Returns:
        List of discovered website URLs
    """
    service = WebsiteDiscoveryService()
    return service.discover_company_websites(company_query, max_urls)
