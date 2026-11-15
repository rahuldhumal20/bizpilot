
INDUSTRY_PROFILES = {
    "retail": {
        "name": "Retail and E-commerce",
        "focus": """
Focus on inventory management, stock forecasting, point-of-sale systems,
customer experience, order management, returns, supplier management,
and sales analytics.
"""
    },
    "beauty": {
        "name": "Beauty and Wellness",
        "focus": """
Focus on appointment scheduling, customer records, staff calendars,
service management, repeat bookings, customer retention and marketing.
Do not make medical or treatment claims.
"""
    },
    "food": {
        "name": "Food and Restaurants",
        "focus": """
Focus on food inventory, procurement, wastage, order management,
staff scheduling, delivery operations and food hygiene.
Flag applicable food safety and licensing requirements for verification.
"""
    },
    "healthcare": {
        "name": "Healthcare",
        "focus": """
Focus on administrative workflows, appointment management, operations,
patient privacy, secure records and authorized professional oversight.
Do not diagnose, prescribe treatment or replace qualified medical advice.
Flag applicable healthcare regulations for professional verification.
"""
    },
    "education": {
        "name": "Education",
        "focus": """
Focus on student management, attendance, learning platforms,
admissions, assessments, scheduling and educational outcomes.
Protect student and minor data.
"""
    },
    "manufacturing": {
        "name": "Manufacturing",
        "focus": """
Focus on production planning, equipment, quality control, raw materials,
inventory, worker safety, maintenance and supply-chain efficiency.
Flag safety-critical engineering decisions for qualified review.
"""
    },
    "water": {
        "name": "Water and Sanitation",
        "focus": """
Focus on source-water testing, contaminant identification, treatment
selection, water capacity, operating costs, maintenance and treated-water
verification.

Never claim water is safe based only on TDS, pH, turbidity or basic sensors.
Do not prescribe a final treatment system without suitable laboratory
water-quality results and qualified technical assessment.
Distinguish microbiological contamination from chemical contamination.
Flag applicable drinking-water standards and regulatory requirements
for verification.
"""
    },
    "agriculture": {
        "name": "Agriculture",
        "focus": """
Focus on crop planning, irrigation, soil testing, input costs,
equipment, storage, weather risks and market access.
Avoid unsupported pesticide or chemical recommendations.
"""
    },
    "hospitality": {
        "name": "Hospitality and Tourism",
        "focus": """
Focus on reservations, guest experience, occupancy, pricing,
housekeeping, staff scheduling, reviews and service operations.
"""
    },
    "logistics": {
        "name": "Logistics and Transportation",
        "focus": """
Focus on route planning, fleet management, fuel, delivery tracking,
warehouse operations, scheduling and vehicle maintenance.
Flag transport safety and regulatory requirements for verification.
"""
    },
    "professional": {
        "name": "Professional Services",
        "focus": """
Focus on client acquisition, project management, service delivery,
billing, workflow automation, customer relationship management
and resource utilization.
"""
    },
    "other": {
        "name": "General Business",
        "focus": """
Understand the business model before proposing a solution.
Focus on customer needs, operations, revenue, costs, resources,
risks and measurable business outcomes.
Ask for missing information rather than inventing facts.
"""
    }
}


def build_domain_context(industry_domain: str) -> str:
    profile = INDUSTRY_PROFILES.get(
        industry_domain,
        INDUSTRY_PROFILES["other"]
    )

    return f"""
INDUSTRY INTELLIGENCE PROFILE

Industry: {profile["name"]}

DOMAIN-SPECIFIC GUIDANCE:
{profile["focus"]}

GENERAL RULES:
1. Recommendations must address the actual business problem.
2. Do not assume missing business information.
3. Clearly distinguish facts, assumptions and estimates.
4. Consider the business size and available budget.
5. Flag safety, legal and regulatory matters requiring expert verification.
6. Do not present estimated prices as confirmed vendor quotations.
7. If essential information is missing, identify it explicitly.
"""
