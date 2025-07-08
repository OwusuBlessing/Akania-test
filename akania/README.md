# African Companies Data Extraction Pipeline

A comprehensive multi-stage data collection system that gathers company information through web scraping, search optimization, and intelligent data extraction using AI.

## 🌟 Features

- **Multi-stage Pipeline**: 7-stage data collection process for comprehensive company information
- **Intelligent Search**: Uses Tavily and SerpAPI for discovering company websites
- **Web Scraping**: Automated content extraction from company websites
- **AI-Powered Extraction**: Uses GPT-4 to convert raw web content into structured data
- **Interactive Assistant**: Command-line interface for easy data extraction and querying
- **Batch Processing**: Extract data for multiple companies at once
- **Data Storage**: Persistent storage for company profiles

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the environment template and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` file with your API keys:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional but recommended
TAVILY_API_KEY=your_tavily_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

### 3. Quick Test

Run a quick test to verify everything works:

```bash
python test_extraction.py
```

### 4. Interactive Mode

Start the interactive assistant:

```bash
python run.py
```

## 📁 Project Structure

```
akania/
├── src/
│   ├── assistant.py              # Interactive command-line assistant
│   ├── company_profiles.py       # Data models and storage management
│   ├── content_extractor.py      # AI-powered data extraction
│   ├── pipeline_orchestrator.py  # Main pipeline coordination
│   ├── scraper.py                # Web scraping functionality
│   └── website_discovery.py      # Company website discovery
├── tests/
│   └── test_assistant.py         # Unit tests
└── README.md
```

## 🔄 Pipeline Stages

### Stage 1: Website Discovery
- **Objective**: Locate the primary company website
- **Tools**: Tavily Search, SerpAPI
- **Output**: Verified company website URLs

### Stage 2: Website Scraping
- **Objective**: Extract content from company websites
- **Tools**: LangChain WebBaseLoader, BeautifulSoup
- **Output**: Raw website content

### Stage 3: Data Extraction
- **Objective**: Convert raw content to structured information
- **Tools**: OpenAI GPT-4, Pydantic models
- **Output**: Structured company data

### Stage 4: Gap Analysis
- **Objective**: Identify missing information
- **Process**: Automated field validation
- **Output**: List of missing data fields

### Stage 5: Targeted Search
- **Objective**: Fill information gaps
- **Process**: Field-specific search queries
- **Output**: Additional relevant information

### Stage 6: News Analysis
- **Objective**: Gather recent developments
- **Process**: News article analysis
- **Output**: Current company status and insights

## 💻 Usage Examples

### Command Line Interface

```bash
# Extract single company
python template.py --company "Flutterwave Nigeria"

# Batch processing
python template.py --batch companies.txt

# Setup validation
python template.py --setup

# Interactive mode
python template.py
```

### Interactive Assistant Commands

```
extract <company name>     - Extract data for a new company
search <query>            - Search stored companies
show <company name>       - Show detailed company information
list                      - List all stored companies
setup                     - Check system configuration
help                      - Show help message
exit                      - Exit the assistant
```

### Programmatic Usage

```python
from akania.src.pipeline_orchestrator import test_company

# Extract company data
result = test_company("Jumia Kenya")

if result:
    print(f"Company: {result.company_name}")
    print(f"Countries: {result.countries}")
    print(f"Sector: {result.sector}")
```

## 📊 Data Structure

The system extracts the following information for each company:

```python
class CompanyInfo:
    company_name: str                    # Company name
    countries: List[str]                 # Operating countries
    sector: List[str]                    # Business sectors
    business_description: str            # Company description
    key_people: List[KeyPeople]         # Leadership team
    transactions: str                    # Recent transactions/funding
    source_urls: List[str]              # Source websites
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (Required): OpenAI API key for LLM processing
- `TAVILY_API_KEY` (Optional): Tavily search API key
- `SERPAPI_API_KEY` (Optional): SerpAPI key for web search
- `GOOGLE_API_KEY` (Optional): Google Search API key
- `GOOGLE_CSE_ID` (Optional): Google Custom Search Engine ID

### Pipeline Settings

You can customize pipeline behavior by modifying:
- Maximum URLs to scrape per company
- LLM model selection
- Search result limits
- Data quality thresholds

## 🧪 Testing

```bash
# Run unit tests
python -m pytest akania/tests/

# Quick functionality test
python test_extraction.py

# Validate setup
python template.py --setup
```

## 📈 Performance Tips

1. **API Keys**: Having both Tavily and SerpAPI keys improves search reliability
2. **Rate Limiting**: The system includes built-in rate limiting for web requests
3. **Caching**: Scraped content is cached to avoid re-scraping
4. **Batch Processing**: Use batch mode for processing multiple companies efficiently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

Apache License 2.0 - See LICENSE file for details

## 🆘 Support

If you encounter issues:

1. Check that all required environment variables are set
2. Verify your API keys are valid
3. Run the setup validation: `python template.py --setup`
4. Check the logs for specific error messages

## 🔮 Future Enhancements

- LinkedIn integration for professional network data
- Industry-specific data extraction templates
- Real-time data monitoring and alerts
- Enhanced data validation and quality scoring
- API endpoint for external integrations
