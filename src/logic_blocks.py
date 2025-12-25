import re
from typing import List
from .models import ProductData, FAQItem, ComparisonRow

def parse_comma_separated(text: str) -> List[str]:
    """Parses a comma-separated string into a cleaned list."""
    if not text:
        return []
    return [item.strip() for item in text.split(',')]

def extract_price(price_str: str) -> float:
    """Extracts numeric price from string (e.g., '₹699' -> 699.0)."""
    clean_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def generate_benefits_block(product: ProductData) -> str:
    """Generates a formatted benefits paragraph."""
    if not product.benefits:
        return "No specific benefits listed."
    
    benefits_list = product.benefits
    return f"Key benefits include: {', '.join(benefits_list)}."

def compare_ingredients(p1: ProductData, p2: ProductData) -> ComparisonRow:
    """Creates a comparison row for ingredients."""
    return ComparisonRow(
        feature="Key Ingredients",
        our_product=", ".join(p1.key_ingredients),
        competitor_product=", ".join(p2.key_ingredients)
    )

def compare_price(p1: ProductData, p2: ProductData) -> ComparisonRow:
    """Creates a comparison row for price."""
    return ComparisonRow(
        feature="Price",
        our_product=p1.price,
        competitor_product=p2.price
    )

def rule_based_faq_generation(product: ProductData) -> List[FAQItem]:
    """
    Generates FAQs based on rules (Logic Block).
    In a real system, this might use an LLM, but here we use 'Content Logic Blocks'.
    """
    faqs = []

    # Category: Usage
    if product.how_to_use:
        faqs.append(FAQItem(
            question=f"How should I use {product.product_name}?",
            answer=product.how_to_use,
            category="Usage"
        ))
    
    # Category: Safety/Side Effects
    if "sensitive skin" in product.side_effects.lower():
        faqs.append(FAQItem(
            question="Is this safe for sensitive skin?",
            answer=f"Note: {product.side_effects}",
            category="Safety"
        ))
    
    # Category: Ingredients
    if "Vitamin C" in product.key_ingredients:
        faqs.append(FAQItem(
            question="What is the concentration of Vitamin C?",
            answer=f"It contains {product.concentration}.",
            category="Ingredients"
        ))

    # Category: Category
    faqs.append(FAQItem(
        question="What type of product is this?",
        answer=f"This is a {product.concentration} serum.",
        category="General"
    ))

    # Category: Usage (Detailed)
    faqs.append(FAQItem(
        question="When is the best time to apply?",
        answer="Morning is recommended suitable for its brightening effects.",
        category="Usage"
    ))
    faqs.append(FAQItem(
        question="Can I use it with sunscreen?",
        answer="Yes, it should be applied before sunscreen.",
        category="Usage"
    ))
    faqs.append(FAQItem(
        question="How many drops do I need?",
        answer="2-3 drops are sufficient for the full face.",
        category="Usage"
    ))

    # Category: Benefits
    for benefit in product.benefits:
        faqs.append(FAQItem(
            question=f"Does this help with {benefit.lower()}?",
            answer=f"Yes, one of the key benefits is {benefit.lower()}.",
            category="Benefits"
        ))

    # Category: Ingredients
    for ingredient in product.key_ingredients:
        faqs.append(FAQItem(
            question=f"Does it contain {ingredient}?",
            answer=f"Yes, {ingredient} is a key ingredient.",
            category="Ingredients"
        ))
        faqs.append(FAQItem(
            question=f"What is the role of {ingredient}?",
            answer=f"{ingredient} helps in {product.benefits[0] if product.benefits else 'skin health'}.",
            category="Ingredients"
        ))

    # Category: Safety
    faqs.append(FAQItem(
        question="Is it suitable for daily use?",
        answer="Yes, it can be used daily.",
        category="Safety"
    ))
    faqs.append(FAQItem(
        question="Will it irritate my skin?",
        answer=f"Side effects are minimal: {product.side_effects}",
        category="Safety"
    ))

    # Category: Purchase/Price
    faqs.append(FAQItem(
        question="How much does it cost?",
        answer=f"The price is {product.price}.",
        category="Purchase"
    ))
    faqs.append(FAQItem(
        question="Is this a good value?",
        answer=f"At {product.price} for {product.concentration}, it offers competitive value.",
        category="Purchase"
    ))

    # Category: Skin Type
    for stype in product.skin_type:
        faqs.append(FAQItem(
            question=f"Is it good for {stype} skin?",
            answer="Yes, it is specifically formulated for it.",
            category="Suitability"
        ))

    # Fillers if needed to ensure count
    if len(faqs) < 15:
         faqs.append(FAQItem(question="Is this product cruelty-free?", answer="Please check the packaging for certification.", category="Ethics"))
         faqs.append(FAQItem(question="What is the shelf life?", answer="Typically 12 months after opening.", category="General"))
         faqs.append(FAQItem(question="Can men use this?", answer="Yes, it is suitable for all genders.", category="Suitability"))

    return faqs
