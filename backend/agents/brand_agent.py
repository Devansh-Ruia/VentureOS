import os
from groq import Groq
from models import VentureBrief
from tools.domain_tools import generate_domain_candidates, check_domain_availability


def run_brand_task(brief: VentureBrief) -> VentureBrief:
    """
    Generate brand name and check domain availability.
    Returns updated VentureBrief with brand and domain info.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Generate 5 brand name candidates for this business idea:

Idea: {brief.idea}
Differentiation: {brief.differentiation}

Constraints:
- Max 2 words
- No hyphens
- Pronounceable
- Relevant to the idea

Return ONLY a JSON array of 5 strings: ["Name1", "Name2", ...]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    candidates = json.loads(raw)
    
    for candidate in candidates:
        domains = generate_domain_candidates(candidate)
        for domain in domains:
            result = check_domain_availability(domain)
            if result.get("available") and (domain.endswith(".com") or domain.endswith(".io")):
                brief.brand_name = candidate
                brief.domain = domain
                brief.domain_available = True
                return brief
    
    brief.brand_name = candidates[0]
    brief.domain = generate_domain_candidates(candidates[0])[0]
    brief.domain_available = False
    
    return brief
