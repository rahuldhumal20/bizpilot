# BizPilot – AI Business Consultant

An AI-powered business consulting application that helps small businesses understand operational challenges, explore practical solutions, estimate implementation costs, and generate structured implementation roadmaps.

BizPilot uses **five specialized AI agents orchestrated through LangGraph**, with a Python-based financial validation component to review financial estimates.

## Project Overview

Small businesses often struggle to identify the right technology solutions for their operational problems. Professional consulting can be expensive, and business owners may not know where to begin.

BizPilot provides an AI-assisted starting point: users describe their business, explain their challenges, and enter their available budget. The application generates a structured business intelligence report.

## Key Features

- **Business Analysis:** Identifies business challenges, root causes, operational impact, and opportunities.
- **Solution Architecture:** Recommends practical solutions based on business requirements and budget.
- **Cost Analysis:** Estimates initial implementation costs and recurring operating expenses.
- **Financial Validation:** Uses Python to validate financial estimates and identify budget concerns.
- **Project Roadmap:** Generates implementation phases, tasks, dependencies, deliverables, and testing plans.
- **Critic Review:** Evaluates problem understanding, solution suitability, financial feasibility, implementation feasibility, and risks.
- **Business Intelligence Dashboard:** Displays the final report with formatted Markdown and agent execution status.

## AI Agent Workflow

BizPilot uses five specialist AI agents and one supporting financial validation component.

| Component | Responsibility |
|---|---|
| Business Analyst | Understands the business and identifies problems |
| Solution Architect | Designs practical solutions |
| Cost Analyst | Estimates implementation and operating costs |
| Financial Validator | Validates financial data using Python |
| Project Planner | Creates the implementation roadmap |
| Critic Agent | Reviews the complete proposal |

The Financial Validator is a Python utility, not a sixth AI agent.

### Workflow

User Input → FastAPI → Business Analyst → Solution Architect → Cost Analyst → Financial Validator → Project Planner → Critic Agent → Final Report

LangGraph coordinates the sequential workflow and passes information between components.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite |
| Styling | Tailwind CSS |
| Icons | Lucide React |
| Backend | Python, FastAPI |
| Data Validation | Pydantic |
| LLM Integration | LangChain |
| Agent Orchestration | LangGraph |
| LLM Provider | Groq |
| Report Rendering | React Markdown, Remark GFM |
| Configuration | python-dotenv |

## Project Structure

```text
bizpilot/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── agents/
│   │   │   ├── business_analyst.py
│   │   │   ├── solution_architect.py
│   │   │   ├── cost_analyst.py
│   │   │   ├── project_planner.py
│   │   │   ├── critic.py
│   │   │   └── financial_validator_agent.py
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   └── workflow.py
│   │   ├── domain/
│   │   │   └── industry_rules.py
│   │   └── validators/
│   │       └── financial_validator.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- Git
- A Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/rahuldhumal20/bizpilot.git
cd bizpilot
```

### 2. Set up the backend

```powershell
cd backend

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
FRONTEND_URL=http://localhost:5173
MONGODB_URI=
```

Replace the API key with your own key. Never commit `.env` to GitHub.

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Backend development URL:

`http://127.0.0.1:8000`

FastAPI documentation:

`http://127.0.0.1:8000/docs`

### 3. Set up the frontend

Open a second terminal:

```powershell
cd frontend

npm install
npm run dev
```

Open the local Vite URL shown in the terminal, normally:

`http://localhost:5173`

### 4. Run the application

1. Start the backend.
2. Start the frontend.
3. Open the frontend in your browser.
4. Enter business information and the available budget.
5. Submit the business analysis request.
6. Review the generated report and agent execution status.

## API

### Business Analysis

**Method:** `POST`

**Endpoint:** `/api/analyze`

The API accepts business information including:

- Business name
- Industry and industry domain
- Business description
- Business problem
- Budget amount
- Currency
- Budget scope
- Business size

Supported currencies: INR, USD, EUR and GBP.

Budget scopes: `initial_only` and `first_year_total`.

The response contains the analysis status, final report, and agent execution logs.

## Financial Validation

The financial validator checks structured cost estimates before the project roadmap is generated.

It checks financial fields, numeric values, cost ranges, currency consistency, and budget feasibility.

When annual business benefits are unknown, BizPilot does not invent values or calculate unsupported ROI figures. Such estimates are marked for review.

## Current Project Status

**Development stage:** MVP implementation and finalization.

Implemented:
- React frontend and FastAPI backend.
- Five specialist AI agents.
- Sequential LangGraph workflow.
- Python financial validation.
- Final business report generation.
- Markdown report rendering.
- Agent execution logs.
- Local scenario testing.

Remaining:
- Complete final end-to-end regression testing.
- Improve consistency between solution and cost estimates.
- Verify error handling and incomplete LLM responses.
- Confirm production environment configuration.
- Deploy frontend and backend.
- Test the deployed application.

## Scope of the MVP

The current MVP focuses on business analysis, solution recommendations, cost estimates, financial validation, implementation planning, and proposal review.

Features such as authentication, report history, PDF export, payment integration, additional agents, and automated revision loops are outside the current MVP scope.

## Important Notes

BizPilot provides AI-assisted preliminary business recommendations. It is not a substitute for professional financial, legal, tax, engineering, or regulatory advice.

Prices, software features, compliance requirements, and implementation estimates must be independently verified before a business makes purchasing or implementation decisions.

## Author

**Rahul Dhumal**

- GitHub: [@rahuldhumal20](https://github.com/rahuldhumal20)
- LinkedIn: [Rahul Dhumal](https://linkedin.com/in/rahul-dhumal-803421365)

---

Built to demonstrate Generative AI, multi-agent orchestration, backend development, financial validation, and practical business problem-solving.
