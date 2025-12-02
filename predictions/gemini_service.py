"""
Gemini AI Service for generating personalized insights about predictions.
"""
import google.generativeai as genai
from django.conf import settings


class GeminiService:
    """Service class for interacting with Google's Gemini API."""

    def __init__(self):
        """Initialize the Gemini service with API key from settings."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured in settings")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use Gemini 2.5 Flash Lite preview model
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')

    def generate_prediction_insight(self, prediction_data):
        """
        Generate personalized insights for a prediction.

        Args:
            prediction_data (dict): Dictionary containing prediction information
                - description: The prediction description
                - probability: The predicted probability (0.0-1.0)
                - resolved: Whether the prediction is resolved
                - outcome: The actual outcome (if resolved)
                - created_at: When the prediction was created
                - resolve_by: When it should be resolved

        Returns:
            str: Generated insight text
        """
        prob = prediction_data.get('probability') * 100
        resolved = prediction_data.get('resolved')

        if resolved:
            outcome = 'happened' if prediction_data.get('outcome') else 'did not happen'
            prompt = f"""Quick analysis of this prediction:

Prediction: "{prediction_data.get('description')}"
Your confidence: {prob:.0f}%
What actually happened: It {outcome}

Write 2-3 short sentences in plain text (no markdown) analyzing:
1. Was your {prob:.0f}% confidence appropriate?
2. One specific insight about this prediction

Be conversational and helpful."""
        else:
            prompt = f"""This prediction is still pending:

"{prediction_data.get('description')}"
Predicted at {prob:.0f}% confidence

Write 1-2 short sentences in plain text (no markdown) about:
- Whether the confidence level seems reasonable
- What to watch for when it resolves

Be brief and conversational."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insight: {str(e)}"

    def generate_calibration_summary(self, stats_data):
        """
        Generate a summary of overall calibration performance.

        Args:
            stats_data (dict): Dictionary containing calibration statistics
                - brier_score: Overall Brier score
                - calibration_bins: List of calibration bins with predictions

        Returns:
            str: Generated calibration summary
        """
        brier_score = stats_data.get('brier_score', 0)
        total = stats_data.get('total_predictions', 0)
        resolved = stats_data.get('resolved_predictions', 0)
        bins = stats_data.get('calibration_bins', [])

        # Build calibration data
        calibration_data = ""
        for bin_data in bins:
            calibration_data += f"{bin_data['range']}: Predicted {bin_data['avg_predicted']:.1f}%, Actually {bin_data['actual_frequency']:.1f}% ({bin_data['count']} predictions)\n"

        prompt = f"""You are analyzing prediction calibration for someone tracking their forecasting accuracy.

DATA:
- Total predictions: {total}
- Resolved predictions: {resolved}
- Brier Score: {brier_score:.4f} (lower is better, 0 = perfect, 0.25 = random)

CALIBRATION BY CONFIDENCE LEVEL:
{calibration_data if calibration_data else "Not enough data yet (need at least 3 predictions per bin)"}

TASK: Write a brief, friendly 3-4 sentence analysis in plain text (no markdown, no asterisks, no formatting).

Focus on:
1. What the Brier score means for their accuracy
2. Which confidence ranges show good/poor calibration
3. One specific actionable tip to improve

Keep it conversational and encouraging. Use simple percentages and comparisons."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def generate_prediction_suggestions(self, past_predictions=None):
        """
        Generate 3 relevant prediction suggestions for the user.

        Args:
            past_predictions (list): Optional list of past prediction descriptions

        Returns:
            list: Three prediction suggestions as dictionaries with 'description' and 'confidence' keys
        """
        past_context = ""
        if past_predictions and len(past_predictions) > 0:
            past_list = "\n".join([f"- {p}" for p in past_predictions[:10]])
            past_context = f"\n\nUser's past predictions:\n{past_list}\n\nAvoid repeating these topics and try to match their style."

        prompt = f"""You are helping someone track predictions to improve their calibration. Generate 3 interesting, specific predictions they should make.

Requirements for good predictions:
- Specific and measurable (clear yes/no outcome)
- Appropriate difficulty level (not too obvious, not impossible to know)
- Time-bound (resolvable within days/weeks/months)
- Relevant to a person's daily life, current events, or personal goals
- Diverse topics (don't repeat similar themes){past_context}

Generate exactly 3 predictions. For each, provide:
1. The prediction statement (1-2 sentences, specific and measurable)
2. A suggested starting confidence level (as a percentage between 30-80%)

Format your response as a JSON array like this:
[
  {{"description": "prediction text here", "confidence": 65}},
  {{"description": "another prediction", "confidence": 50}},
  {{"description": "third prediction", "confidence": 70}}
]

IMPORTANT: Return ONLY the JSON array, no other text or formatting."""

        try:
            response = self.model.generate_content(prompt)
            import json
            # Try to parse JSON response
            text = response.text.strip()
            # Remove markdown code blocks if present
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
                text = text.strip()

            suggestions = json.loads(text)
            return suggestions[:3]  # Ensure we only return 3
        except Exception as e:
            # Fallback suggestions if API fails
            return [
                {"description": "It will rain in my city this week", "confidence": 50},
                {"description": "I will complete my main work project by the end of this month", "confidence": 70},
                {"description": "A major tech company will announce a new product in the next 30 days", "confidence": 60}
            ]


# Singleton instance
_gemini_service = None

def get_gemini_service():
    """Get or create the Gemini service singleton."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
