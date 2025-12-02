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
        prompt = f"""
        Analyze this prediction and provide a brief insight:

        Prediction: {prediction_data.get('description')}
        Predicted Probability: {prediction_data.get('probability') * 100:.1f}%
        Status: {'Resolved' if prediction_data.get('resolved') else 'Pending'}
        """

        if prediction_data.get('resolved'):
            outcome = 'Happened' if prediction_data.get('outcome') else 'Did not happen'
            prompt += f"\nActual Outcome: {outcome}"

        prompt += """

        Provide a 2-3 sentence insight about this prediction, focusing on:
        - The calibration (was the probability appropriate?)
        - What this tells us about the predictor's judgment
        - Any interesting observations
        """

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
        bins = stats_data.get('calibration_bins', [])

        prompt = f"""
        Analyze this prediction calibration data and provide insights:

        Overall Brier Score: {brier_score:.4f}

        Calibration by confidence level:
        """

        for bin_data in bins:
            prompt += f"""
        - {bin_data['range']}: Predicted {bin_data['avg_predicted']:.1f}%, Actually {bin_data['actual_frequency']:.1f}% ({bin_data['count']} predictions)
        """

        prompt += """

        Provide a 3-4 sentence summary:
        - Overall calibration quality (Brier score interpretation)
        - Which confidence ranges are well-calibrated vs over/under-confident
        - Specific recommendations for improvement
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def suggest_prediction_refinement(self, description):
        """
        Suggest how to make a prediction more specific and measurable.

        Args:
            description (str): The prediction description

        Returns:
            str: Suggestions for improvement
        """
        prompt = f"""
        This is a prediction someone wants to make:

        "{description}"

        Provide 2-3 SHORT, CONCISE suggestions (1-2 sentences each) to make this prediction:
        1. More specific and measurable
        2. Time-bound
        3. Objectively verifiable

        Format: Use simple bullet points (•) without markdown formatting.
        Keep it brief and actionable.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating suggestions: {str(e)}"


# Singleton instance
_gemini_service = None

def get_gemini_service():
    """Get or create the Gemini service singleton."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
