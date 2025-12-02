from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Prediction, UserProfile
from .serializers import PredictionSerializer, UserProfileSerializer
from .gemini_service import get_gemini_service


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        prediction = self.get_object()
        outcome = request.data.get('outcome')

        if outcome is None:
            return Response({'error': 'outcome is required'}, status=status.HTTP_400_BAD_REQUEST)

        prediction.resolved = True
        prediction.outcome = bool(outcome)
        prediction.save()

        serializer = self.get_serializer(prediction)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        all_predictions = Prediction.objects.all()
        predictions = all_predictions.filter(resolved=True, outcome__isnull=False)

        total_predictions = all_predictions.count()
        resolved_predictions = predictions.count()

        if not predictions.exists():
            return Response({
                'total_predictions': total_predictions,
                'resolved_predictions': 0,
                'brier_score': None,
                'calibration_bins': []
            })

        # Calculate Brier score
        brier_sum = sum((p.probability - (1.0 if p.outcome else 0.0)) ** 2 for p in predictions)
        brier_score = brier_sum / predictions.count()

        # Calculate calibration bins
        bins = []
        bin_size = 0.1
        min_count = 3

        for i in range(10):
            lower = i * bin_size
            upper = (i + 1) * bin_size

            bin_predictions = [p for p in predictions if lower <= p.probability < upper]

            if len(bin_predictions) >= min_count:
                avg_predicted = sum(p.probability for p in bin_predictions) / len(bin_predictions)
                actual_frequency = sum(1 if p.outcome else 0 for p in bin_predictions) / len(bin_predictions)

                bins.append({
                    'range': f"{int(lower * 100)}-{int(upper * 100)}%",
                    'count': len(bin_predictions),
                    'avg_predicted': round(avg_predicted * 100, 1),
                    'actual_frequency': round(actual_frequency * 100, 1)
                })

        stats_data = {
            'total_predictions': total_predictions,
            'resolved_predictions': resolved_predictions,
            'brier_score': round(brier_score, 4),
            'calibration_bins': bins
        }

        # Generate AI summary if requested
        if request.query_params.get('ai_summary') == 'true' and resolved_predictions > 0:
            try:
                gemini = get_gemini_service()
                ai_summary = gemini.generate_calibration_summary(stats_data)
                stats_data['ai_summary'] = ai_summary
            except Exception as e:
                stats_data['ai_summary'] = f"AI summary unavailable: {str(e)}"

        return Response(stats_data)

    @action(detail=False, methods=['post'])
    def ai_suggest(self, request):
        """Get AI suggestions for improving a prediction description"""
        description = request.data.get('description')

        if not description:
            return Response(
                {'error': 'description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gemini = get_gemini_service()
            suggestions = gemini.suggest_prediction_refinement(description)
            return Response({'suggestions': suggestions})
        except Exception as e:
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def ai_insight(self, request, pk=None):
        """Get AI insight for a specific prediction"""
        prediction = self.get_object()

        prediction_data = {
            'description': prediction.description,
            'probability': prediction.probability,
            'resolved': prediction.resolved,
            'outcome': prediction.outcome,
            'created_at': prediction.created_at,
            'resolve_by': prediction.resolve_by
        }

        try:
            gemini = get_gemini_service()
            insight = gemini.generate_prediction_insight(prediction_data)
            return Response({'insight': insight})
        except Exception as e:
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request):
        # Get or create single profile
        profile, created = UserProfile.objects.get_or_create(pk=1)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None, partial=False):
        profile, created = UserProfile.objects.get_or_create(pk=1)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
