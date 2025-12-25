from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ProductData(BaseModel):
    """Internal model for the product."""
    product_name: str
    concentration: Optional[str] = None
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: str
    currency: str = "INR"
    price_value: float = 0.0

class CompetitorData(ProductData):
    """Model for competitor product (same structure for now)."""
    pass

class FAQItem(BaseModel):
    question: str
    answer: str
    category: str

class ComparisonRow(BaseModel):
    feature: str
    our_product: str
    competitor_product: str

class ContentContext(BaseModel):
    """Context object passed between agents."""
    product: ProductData
    competitor: Optional[CompetitorData] = None
    generated_faqs: List[FAQItem] = []
    comparison_table: List[ComparisonRow] = []

class PageOutput(BaseModel):
    """Generic structure for a specific page output."""
    page_type: str
    title: str
    content: Dict[str, Any]
    meta_metadata: Dict[str, str] = {}
