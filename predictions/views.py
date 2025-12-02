from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Prediction, UserProfile
from .serializers import PredictionSerializer, UserProfileSerializer


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
        predictions = Prediction.objects.filter(resolved=True, outcome__isnull=False)

        if not predictions.exists():
            return Response({
                'count': 0,
                'brier_score': None,
                'bins': []
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
                    'avg_predicted': round(avg_predicted, 3),
                    'actual_frequency': round(actual_frequency, 3)
                })

        return Response({
            'count': predictions.count(),
            'brier_score': round(brier_score, 3),
            'bins': bins
        })


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
