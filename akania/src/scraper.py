"""
Web scraping logic for extracting company data.
"""
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader

def extract_urls_from_tavily(tavily_response):
    """Extract all URLs from Tavily search results"""
    results = tavily_response.get('results', [])
    urls = [result.get('url') for result in results if result.get('url')]
    return urls

def scrape_urls(urls):
    """Scrape content from URLs"""
    scraped_docs = []
    for url in urls:
        try:
            loader = WebBaseLoader([url])
            docs = loader.load()
            scraped_docs.extend(docs)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            continue
    return scraped_docs
