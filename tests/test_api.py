"""
Basic smoke tests for the Calibr8 API
"""
import requests
import os

# Use environment variable or default to localhost
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')


def test_api_root():
    """Test that API root is accessible"""
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200
    print("✓ API root accessible")


def test_predictions_list():
    """Test that predictions list endpoint works"""
    response = requests.get(f"{API_BASE_URL}/predictions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(f"✓ Predictions list works ({len(response.json())} predictions)")


def test_create_prediction():
    """Test creating a new prediction"""
    data = {
        "description": "Test prediction - It will rain tomorrow",
        "probability": 0.75,
    }
    response = requests.post(f"{API_BASE_URL}/predictions/", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result['description'] == data['description']
    assert result['probability'] == data['probability']
    assert result['resolved'] is False
    print(f"✓ Created prediction: {result['id']}")
    return result['id']


def test_get_prediction(prediction_id):
    """Test retrieving a specific prediction"""
    response = requests.get(f"{API_BASE_URL}/predictions/{prediction_id}/")
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == prediction_id
    print(f"✓ Retrieved prediction: {prediction_id}")


def test_resolve_prediction(prediction_id):
    """Test resolving a prediction"""
    data = {"outcome": True}
    response = requests.post(
        f"{API_BASE_URL}/predictions/{prediction_id}/resolve/",
        json=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result['resolved'] is True
    assert result['outcome'] is True
    print(f"✓ Resolved prediction: {prediction_id}")


def test_stats():
    """Test stats endpoint"""
    response = requests.get(f"{API_BASE_URL}/predictions/stats/")
    assert response.status_code == 200
    result = response.json()
    assert 'total_predictions' in result
    assert 'resolved_predictions' in result
    assert 'brier_score' in result
    assert 'calibration_bins' in result
    print(f"✓ Stats: {result['total_predictions']} total, {result['resolved_predictions']} resolved")


def test_profile():
    """Test profile endpoint"""
    response = requests.get(f"{API_BASE_URL}/profile/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✓ Profile endpoint works")


def test_delete_prediction(prediction_id):
    """Test deleting a prediction"""
    response = requests.delete(f"{API_BASE_URL}/predictions/{prediction_id}/")
    assert response.status_code == 204
    print(f"✓ Deleted prediction: {prediction_id}")


def run_all_tests():
    """Run all tests in sequence"""
    print("\n🧪 Running Calibr8 API Tests\n")
    print(f"Testing API at: {API_BASE_URL}\n")

    try:
        test_api_root()
        test_predictions_list()

        # Create, retrieve, resolve, and delete a test prediction
        pred_id = test_create_prediction()
        test_get_prediction(pred_id)
        test_resolve_prediction(pred_id)
        test_delete_prediction(pred_id)

        # Test other endpoints
        test_stats()
        test_profile()

        print("\n✅ All tests passed!\n")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to API at {API_BASE_URL}")
        print("Make sure the server is running!\n")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
