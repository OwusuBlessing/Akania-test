"""
Data models and storage for company profiles.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json
from pathlib import Path

class KeyPeople(BaseModel):
    """Model for key people in a company"""
    name: str = Field(description="Name of the key person")
    title: str = Field(description="Title of the key person")

class CompanyInfo(BaseModel):
    """Info about some Companies"""
    company_name: Optional[str] = Field(description="Name of the company")
    countries: List[str] = Field(default_factory=list, description="Countries where the company operates in Africa")
    sector: List[str] = Field(default_factory=list, description="Sector of the company")
    business_description: Optional[str] = Field(default=None, description="Brief description of the company's business (50 words)")
    key_people: List[KeyPeople] = Field(default_factory=list, description="Key people involved in the company")
    transactions: Optional[str] = Field(default=None, description="transactions involving the company")
    source_urls: List[str] = Field(default_factory=list, description="Source urls for the company")

def save_company_profile(company_info: CompanyInfo):
    """Save company profile as JSON file"""
    if not company_info.company_name:
        return
    
    Path("data").mkdir(exist_ok=True)
    safe_name = company_info.company_name.replace(" ", "_").replace("(", "").replace(")", "")
    filename = f"data/{safe_name}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(company_info.model_dump(), f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to {filename}")

def load_profiles() -> List[Dict]:
    """Load all saved profiles"""
    data_dir = Path("data")
    if not data_dir.exists():
        return []
    
    profiles = []
    for file in data_dir.glob("*.json"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                profiles.append(data)
        except:
            continue
    
    return profiles
