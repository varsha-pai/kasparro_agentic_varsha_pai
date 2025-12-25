import json
import os
from src.agents import Orchestrator

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    output_dir = os.path.join(base_dir, 'output')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    input_file = os.path.join(data_dir, 'glowboost.json')
    competitor_file = os.path.join(data_dir, 'competitor_b.json')
    
    print("\n--- Starting Kasparro Content System ---")
    print("1. Initializing Agents (Parser, Strategist, Writer)...")
    orchestrator = Orchestrator()
    
    try:
        print(f"2. Reading input from: {input_file}")
        # The orchestrator handles the full pipeline: Parse -> Strategize -> Write
        faq, product, comparison = orchestrator.run(input_file, competitor_file)
        
        print("3. Generating content...")
        
        # Save key outputs
        # ----------------
        
        # 1. FAQ Page
        faq_path = os.path.join(output_dir, 'faq.json')
        with open(faq_path, 'w', encoding='utf-8') as f:
            json.dump(faq, f, indent=2)
        print(f"   [✓] FAQ Page saved to: output/faq.json")
            
        # 2. Product Page
        prod_path = os.path.join(output_dir, 'product_page.json')
        with open(prod_path, 'w', encoding='utf-8') as f:
            json.dump(product, f, indent=2)
        print(f"   [✓] Product Page saved to: output/product_page.json")
            
        # 3. Comparison Page
        comp_path = os.path.join(output_dir, 'comparison_page.json')
        with open(comp_path, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2)
        print(f"   [✓] Comparison Page saved to: output/comparison_page.json")
            
        print("\n--- Success! All tasks completed. ---\n")
        
    except Exception as e:
        print(f"\n[!] Error during execution: {e}")

if __name__ == "__main__":
    main()
