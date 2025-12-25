from typing import Dict, Any, List
from .models import ContentContext, PageOutput

class Template:
    """Base Template class."""
    def render(self, context: ContentContext) -> PageOutput:
        raise NotImplementedError

class FAQTemplate(Template):
    def render(self, context: ContentContext) -> PageOutput:
        # Structure the FAQ page
        faq_list = [{"q": item.question, "a": item.answer, "category": item.category} for item in context.generated_faqs]
        
        return PageOutput(
            page_type="FAQ Page",
            title=f"Frequently Asked Questions - {context.product.product_name}",
            content={
                "faqs": faq_list,
                "total_count": len(faq_list)
            },
            meta_metadata={
                "description": f"Common questions about {context.product.product_name} including usage and benefits."
            }
        )

class ProductPageTemplate(Template):
    def render(self, context: ContentContext) -> PageOutput:
        p = context.product
        return PageOutput(
            page_type="Product Page",
            title=p.product_name,
            content={
                "name": p.product_name,
                "price": p.price,
                "summary": f"{p.product_name} is a {p.concentration} serum designed for {', '.join(p.skin_type)} skin.",
                "details": {
                    "ingredients": p.key_ingredients,
                    "benefits": p.benefits,
                    "usage_instructions": p.how_to_use
                },
                "safety_info": p.side_effects
            },
            meta_metadata={
                "keywords": ", ".join(p.key_ingredients + p.benefits)
            }
        )

class ComparisonPageTemplate(Template):
    def render(self, context: ContentContext) -> PageOutput:
        if not context.competitor:
            raise ValueError("Competitor data missing for comparison template")
            
        rows = [{"feature": row.feature, "us": row.our_product, "them": row.competitor_product} for row in context.comparison_table]
        
        return PageOutput(
            page_type="Comparison Page",
            title=f"{context.product.product_name} vs {context.competitor.product_name}",
            content={
                "primary_product": context.product.product_name,
                "competitor_product": context.competitor.product_name,
                "comparison_table": rows,
                "verdict": f"{context.product.product_name} offers a higher concentration ({context.product.concentration}) compared to {context.competitor.product_name}."
            }
        )
