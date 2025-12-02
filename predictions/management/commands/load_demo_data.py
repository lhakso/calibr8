from django.core.management.base import BaseCommand
from predictions.models import Prediction
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Load demo predictions for testing'

    def handle(self, *args, **options):
        # Clear existing predictions
        Prediction.objects.all().delete()

        demo_predictions = [
            # Unresolved predictions (for you to test resolving)
            {
                'description': 'I will finish reading my current book this week',
                'probability': 0.75,
            },
            {
                'description': 'It will rain tomorrow',
                'probability': 0.30,
            },
            {
                'description': 'I will exercise at least 3 times this week',
                'probability': 0.65,
            },
            {
                'description': 'My favorite team will win their next game',
                'probability': 0.55,
            },
            {
                'description': 'I will complete my iOS project by the deadline',
                'probability': 0.85,
            },
            {
                'description': 'I will learn a new programming language this month',
                'probability': 0.40,
            },

            # Some already resolved (to show stats)
            {
                'description': 'I thought it would be sunny yesterday',
                'probability': 0.70,
                'resolved': True,
                'outcome': True,
            },
            {
                'description': 'I predicted I would wake up before 8am',
                'probability': 0.50,
                'resolved': True,
                'outcome': False,
            },
            {
                'description': 'I thought my package would arrive on time',
                'probability': 0.80,
                'resolved': True,
                'outcome': True,
            },
            {
                'description': 'I predicted I would go to the gym',
                'probability': 0.60,
                'resolved': True,
                'outcome': False,
            },
            {
                'description': 'I thought the meeting would be cancelled',
                'probability': 0.20,
                'resolved': True,
                'outcome': False,
            },
            {
                'description': 'I predicted my friend would call me back',
                'probability': 0.90,
                'resolved': True,
                'outcome': True,
            },
            {
                'description': 'I thought I would finish my homework early',
                'probability': 0.45,
                'resolved': True,
                'outcome': True,
            },
            {
                'description': 'I predicted the restaurant would be crowded',
                'probability': 0.70,
                'resolved': True,
                'outcome': True,
            },
        ]

        created_count = 0
        for pred_data in demo_predictions:
            Prediction.objects.create(**pred_data)
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created_count} demo predictions!')
        )
        self.stdout.write(
            self.style.WARNING('Note: All previous predictions were deleted.')
        )
