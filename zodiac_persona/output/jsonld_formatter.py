"""
JSON-LD formatting for zodiac_persona.

Provides structured JSON-LD output based on custom vocabulary.
The models handle the to_dict conversion, this module is for extensions.
"""

from typing import Dict, Any
try:
    from ..core.models import VedicBirthChart
except ImportError:
    from zodiac_persona.core.models import VedicBirthChart

def format_chart(chart: VedicBirthChart) -> Dict[str, Any]:
    """Format birth chart as JSON-LD."""
    return chart.to_dict()

# For future use, e.g., custom contexts or validations
