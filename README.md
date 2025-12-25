# Kasparro Content Generation System

Welcome! This project is an automated system that takes raw product data (like a vitamin serum) and turns it into ready-to-use website content (FAQs, Product Pages, and Comparisons).

It uses **Agents** to split the work, just like a real team would:
1.  **Parser Agent**: Reads the messy input data and cleans it up.
2.  **Strategist Agent**: Thinks of questions and compares products.
3.  **Writer Agent**: Takes all that info and formats it into final pages.

## 📂 Project Structure
- `data/`: Contains the input files (`glowboost.json`).
- `output/`: Where the final files will appear.
- `src/`: The code for our agents and logic.
- `main.py`: The control center that runs everything.

## System Architecture
<img width="672" height="788" alt="image" src="https://github.com/user-attachments/assets/dad4f735-2e46-4aee-b239-3aca6ecb96a1" />


## 🚀 How to Run

### Prerequisite
Make sure you have Python installed.

### Step 1: Open Terminal
Open your terminal or command prompt in this folder.

### Step 2: Run the Main Script
Type the following command and hit Enter:
```bash
python main.py
```

### Step 3: Check Results
Open the `output` folder. You will see three new files:
- `faq.json`
- `product_page.json`
- `comparison_page.json`

## 🛠️ How It Works (For Developers)
- **Modularity**: We kept logic separate from agents. See `src/logic_blocks.py`.
- **Templates**: We use simple Python classes to define how a page looks. See `src/templates.py`.
- **Agents**: Each agent has one job. Check `src/agents.py` to see them in action.


