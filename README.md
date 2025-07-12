# African Companies Data Extraction & Chat System

A comprehensive system for extracting detailed information about African companies and providing an interactive chat interface to explore the data.

## 🌍 Project Overview

This project extracts detailed company profiles from African businesses using advanced web scraping, search APIs, and LLM-powered data extraction. It provides a professional web-based chat interface to interact with the extracted data.

## 📊 Recent Changes & Improvements

### ✅ **Project Cleanup & Simplification**
- **Removed duplicate data folders**: Consolidated from 2 data directories to 1 clean `/data/` folder
- **Removed redundant chat interfaces**: Simplified from multiple chat apps to one professional backend
- **Cleaned up development files**: Removed test files and development scripts for clarity
- **Streamlined codebase**: Focused on essential functionality only

### ✅ **Enhanced Data Quality**
- **5 Enhanced Company Profiles** with comprehensive information:
  - Lapaire Glasses (Kenya) - Eyewear startup
  - Merec Industries (Mozambique) - Industrial company
  - Moni-Shop (DR Congo) - Supermarket chain
  - SanLei Premium Trout (Lesotho) - Aquaculture
  - Sylndr (Egypt) - Used car marketplace

### ✅ **Multi-Source Data Extraction**
- **Tavily Search API** integration for web content discovery
- **SerpAPI** integration for comprehensive search results
- **LLM-supervised extraction** using GPT-4o-mini for intelligent data processing
- **Quality assessment system** with completeness scoring
- **Intelligent data merging** from multiple sources

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file (copy from `.env.example`):
```bash
# Required
OPENAI_API_KEY="your-openai-key"

# At least one search API recommended
TAVILY_API_KEY="your-tavily-key"
SERPAPI_API_KEY="your-serpapi-key"
```

## 🔧 How to Use

### 1. Run the Enhanced Scraper

Extract data for new companies using the multi-source scraper:

```bash
# Navigate to the scraper directory
cd akania/src

# Run extraction for a single company
python enhanced_scraper.py

# Or run batch extraction for multiple companies
python extraction_orchestrator.py
```

**What the scraper does:**
- 🔍 Searches multiple sources (Tavily, SerpAPI)
- 🌐 Scrapes relevant web content
- 🤖 Uses LLM to extract structured data
- 📊 Assesses data quality and completeness
- 💾 Saves enhanced profiles to `/data/`

### 2. Run the Chat Interface

Start the professional web-based chat system:

```bash
# Navigate to backend
cd backend

# Start the FastAPI server
python main.py
```

**Then open:** `http://localhost:8000`

**Chat Features:**
- 💬 Natural language queries about African companies
- 📋 Detailed company information display
- 👥 Key people and leadership details
- 💰 Investment and transaction history
- 🌍 Geographic and sector information
- 🎨 Professional, responsive web interface

## 📁 Project Structure

```
/
├── data/                          # Enhanced company data (PRODUCTION)
│   ├── Lapaire_Glasses.json
│   ├── Merec_Industries.json
│   ├── Moni-Shop.json
│   ├── SanLei_Premium_Trout.json
│   └── Sylndr.json
│
├── backend/                       # Web chat interface
│   ├── main.py                   # FastAPI server
│   ├── templates/
│   │   └── chat.html            # Professional web interface
│   └── static/
│       ├── css/chat.css         # Styling
│       └── js/chat.js           # Frontend logic
│
├── akania/src/                   # Core extraction logic
│   ├── enhanced_scraper.py      # Multi-source extraction
│   ├── extraction_orchestrator.py # Batch processing
│   ├── company_profiles.py      # Data models
│   ├── scraper.py              # Basic web scraping
│   ├── website_discovery.py    # URL discovery
│   └── assistant.py            # LLM integration
│
├── requirements.txt             # Dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🎯 Example Usage

### Chat Queries You Can Try:
- *"Tell me about Sylndr"*
- *"What companies are in Kenya?"*
- *"Show me companies in the retail sector"*
- *"Who are the key people at Lapaire?"*
- *"What investments has Merec Industries received?"*
- *"List all companies in East Africa"*

### Scraper Usage:
```python
from akania.src.enhanced_scraper import extract_company_enhanced

# Extract data for a new company
result = extract_company_enhanced("New African Company Name")
```

## 📊 Data Quality Features

The system includes advanced quality assessment:

- **Completeness Scoring**: 0-1 score based on filled fields
- **Critical Field Validation**: Company name, location, description
- **Multi-Source Verification**: Cross-referencing multiple data sources
- **LLM Supervision**: Intelligent extraction and validation
- **Quality Reporting**: Detailed assessment of data completeness

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS/JavaScript
- **LLM**: OpenAI GPT-4o-mini
- **Search APIs**: Tavily, SerpAPI
- **Web Scraping**: BeautifulSoup, WebBaseLoader
- **Data Processing**: LangChain, Pydantic

## 📈 Performance

- **5 enhanced company profiles** with comprehensive data
- **Multi-source extraction** for maximum data completeness
- **Quality scores** averaging 0.8+ for all companies
- **Fast chat responses** with detailed company information
- **Professional web interface** with responsive design

## 🔄 Development Workflow

1. **Add new companies**: Use `enhanced_scraper.py` or `extraction_orchestrator.py`
2. **Test data quality**: Check completeness scores and quality assessments
3. **Update chat interface**: Data automatically loads from `/data/`
4. **Deploy**: Simple FastAPI deployment with static files

## 🎉 Key Features

✅ **Professional chat interface** with web UI  
✅ **Multi-source data extraction** (Tavily + SerpAPI + Web scraping)  
✅ **LLM-powered intelligence** for data processing  
✅ **Quality assessment system** with scoring  
✅ **5 comprehensive company profiles** ready to explore  
✅ **Clean, maintainable codebase** optimized for demonstration  
✅ **Easy deployment** with minimal dependencies  

---

**Ready to explore African business data!** 🌍✨
