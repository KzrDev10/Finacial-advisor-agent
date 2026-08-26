"""
FinanceAI Agent — powered by Gemini + LangChain tools.

Tools exposed to the agent:
  1. assess_risk          — runs the risk profiler (age, timeline, volatility comfort)
  2. project_savings      — compound growth projection (fixed savings/contributions)
  3. project_stock    s    — live stock projection via yfinance
  4. answer_finance_question — general financial Q&A (no tool, just LLM knowledge)
"""

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from core_math.risk_profiler import assess_risk_profile
from core_math.compounding_engine import project_fixed_savings
from core_math.market_engine import project_stock_growth

load_dotenv()

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.4,
)

# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def assess_risk(age: int, timeline_years: int, volatility_comfort: int) -> str:
    """
    Assess a user's investment risk profile.

    Args:
        age: User's age in years (e.g. 28).
        timeline_years: Investment horizon in years (e.g. 10).
        volatility_comfort: Comfort with market swings on a scale of 1–10
                            (1 = very uncomfortable, 10 = very comfortable).

    Returns:
        A string: 'Conservative', 'Moderate', or 'Aggressive'.
    """
    result = assess_risk_profile(age, timeline_years, volatility_comfort)
    return (
        f"Based on your age ({age}), investment timeline ({timeline_years} years), "
        f"and volatility comfort ({volatility_comfort}/10), your risk profile is: **{result}**.\n\n"
        f"{'This means you should focus on stable, low-risk assets like bonds and dividend stocks.' if result == 'Conservative' else ''}"
        f"{'This means a balanced mix of growth stocks and bonds suits you well.' if result == 'Moderate' else ''}"
        f"{'This means you can handle higher-risk, higher-reward investments like growth stocks and crypto.' if result == 'Aggressive' else ''}"
    )


@tool
def project_savings(
    current_savings: float,
    monthly_contribution: float,
    annual_interest_rate: float,
    months: int,
) -> str:
    """
    Project how savings will grow with fixed monthly contributions and compound interest.

    Args:
        current_savings: Current lump-sum savings in GBP/USD (e.g. 5000).
        monthly_contribution: Amount added every month (e.g. 500).
        annual_interest_rate: Expected annual interest rate as a decimal (e.g. 0.07 for 7%).
        months: Number of months to project (e.g. 60 for 5 years).

    Returns:
        A readable summary of projected values at 25%, 50%, 75%, and 100% of the timeline.
    """
    balances = project_fixed_savings(
        current_savings, monthly_contribution, annual_interest_rate, months
    )
    checkpoints = [
        int(months * 0.25) - 1,
        int(months * 0.50) - 1,
        int(months * 0.75) - 1,
        months - 1,
    ]
    lines = []
    for idx in checkpoints:
        if 0 <= idx < len(balances):
            month_num = idx + 1
            years = month_num / 12
            lines.append(f"  • Month {month_num} ({years:.1f} yrs): **£{balances[idx]:,.2f}**")

    return (
        f"Projected savings growth for £{current_savings:,.0f} starting balance "
        f"+ £{monthly_contribution:,.0f}/month at {annual_interest_rate*100:.1f}% annual rate:\n"
        + "\n".join(lines)
        + f"\n\nFinal balance after {months} months: **£{balances[-1]:,.2f}**"
    )


@tool
def project_stock(ticker: str, investment_amount: float, months: int = 12) -> str:
    """
    Project the future value of an investment in a specific stock using real historical data.

    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'TSLA', 'MSFT', 'BTC-USD').
        investment_amount: Amount to invest in GBP/USD (e.g. 1000).
        months: Number of months to project (default: 12).

    Returns:
        A readable projection based on the stock's 1-year historical performance.
    """
    try:
        balances = project_stock_growth(ticker, investment_amount, months)
        checkpoints = [
            int(months * 0.25) - 1,
            int(months * 0.50) - 1,
            int(months * 0.75) - 1,
            months - 1,
        ]
        lines = []
        for idx in checkpoints:
            if 0 <= idx < len(balances):
                month_num = idx + 1
                lines.append(f"  • Month {month_num}: **£{balances[idx]:,.2f}**")

        return (
            f"📈 {ticker.upper()} projection for £{investment_amount:,.0f} over {months} months "
            f"(based on 1-year historical performance):\n"
            + "\n".join(lines)
            + f"\n\nProjected value at end: **£{balances[-1]:,.2f}**\n"
            + "_Note: Past performance does not guarantee future results._"
        )
    except Exception as e:
        return f"Could not fetch data for '{ticker}'. Please check the ticker symbol. Error: {str(e)}"


# ── Prompt ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are FinanceAI, an intelligent financial advisor assistant built into the FinanceAI platform.

You help users with:
- Understanding their risk profile and investment style
- Projecting savings growth with compound interest
- Analysing stock performance and projections using real market data
- Answering general financial questions clearly and concisely

Guidelines:
- Be clear, friendly, and professional
- Always include a disclaimer that this is not formal financial advice
- Use the tools available to give data-backed answers
- Format numbers with commas and currency symbols (£ or $ depending on context)
- If the user hasn't given enough information to use a tool, ask for it politely
- Keep responses concise but complete — use bullet points and bold for key numbers
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# ── Agent ─────────────────────────────────────────────────────────────────────
tools = [assess_risk, project_savings, project_stock]

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)


def run_agent(user_message: str, chat_history: list = None) -> str:
    """
    Run the agent with a user message and optional chat history.

    Args:
        user_message: The user's latest message string.
        chat_history: A list of LangChain message objects (HumanMessage / AIMessage).

    Returns:
        The agent's response string.
    """
    if chat_history is None:
        chat_history = []
    try:
        result = agent_executor.invoke({
            "input": user_message,
            "chat_history": chat_history,
        })
        return result["output"]
    except Exception as e:
        return f"I encountered an error while processing your request: {str(e)}"
