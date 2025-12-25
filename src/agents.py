from typing import Dict, Any, List
import json
from .models import ProductData, CompetitorData, ContentContext, PageOutput, ComparisonRow
from .logic_blocks import (
    parse_comma_separated, 
    rule_based_faq_generation, 
    compare_ingredients, 
    compare_price,
    extract_price
)
from .templates import FAQTemplate, ProductPageTemplate, ComparisonPageTemplate

class ParserAgent:
    """
    Title: Parser Agent
    Role: The 'Reader'
    Responsibility: 
        - Reads the raw, messy JSON data from the file.
        - Fixes small issues (like turning "Price: 100" into just the number 100).
        - Returns a clean, structured object we can trust.
    """
    def parse(self, raw_data: Dict[str, Any], is_competitor=False) -> ProductData:
        # Pre-processing logic could go here (e.g., lowercase keys)
        
        # Convert comma separated strings to lists for model
        if isinstance(raw_data.get('skin_type'), str):
            raw_data['skin_type'] = parse_comma_separated(raw_data['skin_type'])
        if isinstance(raw_data.get('key_ingredients'), str):
            raw_data['key_ingredients'] = parse_comma_separated(raw_data['key_ingredients'])
        if isinstance(raw_data.get('benefits'), str):
            raw_data['benefits'] = parse_comma_separated(raw_data['benefits'])
            
        # Extract numeric price for value
        raw_data['price_value'] = extract_price(raw_data.get('price', '0'))
        
        if is_competitor:
            return CompetitorData(**raw_data)
        return ProductData(**raw_data)

class ContentStrategistAgent:
    """
    Title: Strategist Agent
    Role: The 'Brain'
    Responsibility:
        - Takes the clean product data.
        - Generates new ideas (questions, insights).
        - Compares it with competitors.
        - Decides *what* should go on the page.
    """
    def generate_context(self, product: ProductData, competitor: CompetitorData = None) -> ContentContext:
        context = ContentContext(product=product, competitor=competitor)
        
        # 1. Generate FAQs
        context.generated_faqs = rule_based_faq_generation(product)
        
        # 2. Generate Comparisons if competitor exists
        if competitor:
            context.comparison_table.append(compare_ingredients(product, competitor))
            context.comparison_table.append(compare_price(product, competitor))
            
            # Derived comparison
            conc_diff = "Higher" if "10%" in product.concentration and "5%" in competitor.concentration else "Different"
            context.comparison_table.append(ComparisonRow(
                feature="Concentration", 
                our_product=product.concentration, 
                competitor_product=competitor.concentration
            ))
            
        return context

class WriterAgent:
    """
    Title: Writer Agent
    Role: The 'Publisher'
    Responsibility:
        - Takes the ideas from the Strategist.
        - Puts them into a specific format (Template).
        - Produces the final JSON that the website uses.
    """
    def __init__(self):
        self.templates = {
            "faq": FAQTemplate(),
            "product": ProductPageTemplate(),
            "comparison": ComparisonPageTemplate()
        }
    
    def write_page(self, page_type: str, context: ContentContext) -> Dict[str, Any]:
        template = self.templates.get(page_type)
        if not template:
            raise ValueError(f"Unknown template: {page_type}")
        
        page_output = template.render(context)
        return page_output.model_dump()

class Orchestrator:
    """
    - Coordinates the whole team.
    - Passes work from Parser -> Strategist -> Writer.
    """
    def __init__(self):
        self.parser = ParserAgent()
        self.strategist = ContentStrategistAgent()
        self.writer = WriterAgent()
        
    def run(self, input_file: str, competitor_file: str = None):
        # Step 1: Parse
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_product = json.load(f)
        product = self.parser.parse(raw_product)
        
        competitor = None
        if competitor_file:
            with open(competitor_file, 'r', encoding='utf-8') as f:
                raw_comp = json.load(f)
            competitor = self.parser.parse(raw_comp, is_competitor=True)
            
        # Step 2: Strategize
        context = self.strategist.generate_context(product, competitor)
        
        # Step 3: Write
        faq_page = self.writer.write_page("faq", context)
        prod_page = self.writer.write_page("product", context)
        comp_page = self.writer.write_page("comparison", context)
        
        return faq_page, prod_page, comp_page
