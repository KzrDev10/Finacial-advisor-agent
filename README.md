# Finacial-advisor-agent
# AI Financial Advisor API

An intelligent backend system that calculates highly accurate financial projections using live market data and uses a Large Language Model (LLM) to explain those strategies to users in conversational plain English.

Unlike standard LLM wrappers that hallucinate math, this system relies on a rigid, vectorized data engine (NumPy/Pandas) for all calculations. The AI acts only as a translation layer to interpret the hard numbers.

## Tech Stack
* **Backend Framework:** Flask, Python
* **Database:** MySQL, SQLAlchemy
* **Data Engine:** NumPy, Pandas, yfinance
* **AI Orchestration:** LangChain, Google Gemini (3.5 Flash)

## Project Architecture
The system is built using a feature-based architecture to separate the mathematical logic from the AI routing:

* `/core_math` - The calculation engines. Handles live data fetching, variance calculation, and vectorized compound interest arrays.
* `/database` - SQLAlchemy models defining user profiles, risk tolerances, and savings goals.
* `/agent` - The LangChain tool wrappers that connect the math engines to the Gemini LLM.
* `/api` - The Flask routes that handle JSON payloads from the frontend.

## Roadmap / Current Status
- [x] Phase 1: Initialize architecture and vector math fundamentals.
- [ ] Phase 2: Build the Market Engine (yfinance + NumPy projections).
- [ ] Phase 3: Setup MySQL database and User models.
- [ ] Phase 4: Wrap engines in LangChain tools and connect Gemini.
- [ ] Phase 5: Build Flask API endpoints for the frontend.