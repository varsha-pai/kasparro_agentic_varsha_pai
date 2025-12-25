# Project Documentation: Kasparro Content System

## 👋 Introduction
We built a system that acts like a mini-marketing team. It takes raw product data (like price, ingredients) and automatically writes website content.

## 🎯 Sample Problem
**Input**: A messy list of facts about "GlowBoost Vitamin C Serum".
**Output**: Properly formatted:
1.  **FAQ Page** (with 15+ questions).
2.  **Product Page** (clean summary).
3.  **Comparison Page** (vs a competitor).

## 🏗️ How It Works (The "Team")
We didn't just write one big script. We built "Agents" to handle specific jobs:

### 1. The Parser Agent (Data Reader)
*   **Job**: Reads the file given by the user.
*   **Why**: Data is often messy. This agent fixes numbers and cleans up text.
*   **Code**: `src/agents.py -> ParserAgent`

### 2. The Strategist Agent (The Brain)
*   **Job**: Thinks of ideas.
*   **Why**: We need to generate questions like "Is it safe?" based on the ingredients.
*   **Code**: `src/agents.py -> ContentStrategistAgent`

### 3. The Writer Agent (The Publisher)
*   **Job**: Selects the right template (FAQ vs Product Page) and fills in the blanks.
*   **Why**: We want the output to always look consistent.
*   **Code**: `src/agents.py -> WriterAgent`

## 🧩 Key Concepts
*   **Logic Blocks**: Small helper functions in `src/logic_blocks.py`. For example, `extract_price` grabs the number `699` from `₹699`.
*   **Templates**: Blueprints for our pages in `src/templates.py`.

## 📊 Flow Chart
Input (JSON) -> [Parser] -> Clean Data -> [Strategist] -> Ideas -> [Writer] -> Final Output (JSON)
