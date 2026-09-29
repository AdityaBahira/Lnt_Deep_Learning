"""
test_integration.py
-------------------
Automated Integration Test Suite for Task 8: Streamlit + Flask API Integration.
Verifies HTTP endpoints, payload formats, error codes, and frontend connector integration.
"""

import sys
import os
import time
import requests
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from flask_api import app, get_model_engine
from utils import ModelConnector, load_dataset, FEATURE_NAMES

class Task8IntegrationTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Flask test client and ModelConnector."""
        app.testing = True
        cls.client = app.test_client()
        cls.connector = ModelConnector(default_api_url="http://127.0.0.1:5000")
        cls.sample_vec = [45.0, 170.0, 75.0, 25.95, 6500.0, 2400.0, 6.8, 78.0, 128.0, 82.0, 2.5, 4.0, 0.0, 0.0]

    def test_01_root_endpoint(self):
        """Test GET / landing endpoint."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Health Risk Deep Learning REST API", data["service_name"])
        print("[PASS] TC-01: Root endpoint GET / returned 200 OK.")

    def test_02_health_endpoint(self):
        """Test GET /health probe endpoint."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])
        self.assertEqual(data["feature_count"], 14)
        print("[PASS] TC-02: Health probe GET /health returned 200 OK & healthy state.")

    def test_03_single_feature_prediction(self):
        """Test POST /predict with payload format {"features": [...]}."""
        payload = {"features": self.sample_vec}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["predictions_count"], 1)
        pred = data["predictions"][0]
        self.assertIn("predicted_label", pred)
        self.assertIn("confidence_score", pred)
        self.assertIn("class_probabilities", pred)
        print(f"[PASS] TC-03: Single prediction returned label '{pred['predicted_label']}' ({pred['confidence_score'] * 100:.1f}% confidence).")

    def test_04_batch_instances_prediction(self):
        """Test POST /predict with payload format {"instances": [[...], [...]]}."""
        payload = {"instances": [self.sample_vec, self.sample_vec, self.sample_vec]}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["predictions_count"], 3)
        print("[PASS] TC-04: Batch prediction returned 3 successful results.")

    def test_05_dictionary_data_prediction(self):
        """Test POST /predict with dictionary format {"data": {"age": 45, ...}}."""
        feat_dict = {name: val for name, val in zip(FEATURE_NAMES, self.sample_vec)}
        payload = {"data": feat_dict}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["predictions_count"], 1)
        print("[PASS] TC-05: Dictionary format prediction returned 200 OK.")

    def test_06_unsupported_media_type(self):
        """Test POST /predict with invalid Content-Type (expect 415)."""
        res = self.client.post("/predict", data="hello", content_type="text/plain")
        self.assertEqual(res.status_code, 415)
        data = res.get_json()
        self.assertEqual(data["error_code"], "UNSUPPORTED_MEDIA_TYPE")
        print("[PASS] TC-06: Non-JSON content type correctly rejected with HTTP 415.")

    def test_07_invalid_payload_structure(self):
        """Test POST /predict with missing required keys (expect 400)."""
        payload = {"invalid_key": [1, 2, 3]}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data["error_code"], "MISSING_REQUIRED_KEY")
        print("[PASS] TC-07: Missing required keys correctly rejected with HTTP 400.")

    def test_08_dimension_mismatch(self):
        """Test POST /predict with wrong feature count (expect 422)."""
        payload = {"features": [45.0, 170.0, 75.0]}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 422)
        data = res.get_json()
        self.assertEqual(data["error_code"], "MODEL_VALIDATION_ERROR")
        print("[PASS] TC-08: Feature dimension mismatch correctly caught with HTTP 422.")

    def test_09_non_numeric_feature(self):
        """Test POST /predict with non-numeric value (expect 422)."""
        invalid_vec = list(self.sample_vec)
        invalid_vec[0] = "invalid_age_str"
        payload = {"features": invalid_vec}
        res = self.client.post("/predict", json=payload)
        self.assertEqual(res.status_code, 422)
        data = res.get_json()
        self.assertEqual(data["error_code"], "NON_NUMERIC_FEATURE")
        print("[PASS] TC-09: Non-numeric feature value correctly rejected with HTTP 422.")

    def test_10_not_found_endpoint(self):
        """Test non-existent URL path (expect 404)."""
        res = self.client.get("/non_existent_route")
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertEqual(data["error_code"], "NOT_FOUND")
        print("[PASS] TC-10: Invalid route correctly returns HTTP 404.")

    def test_11_direct_engine_connector_fallback(self):
        """Test ModelConnector Direct PyTorch Engine fallback mode."""
        res = self.connector.predict_single(self.sample_vec, mode="DIRECT")
        self.assertIn("predicted_label", res)
        self.assertIn("Direct PyTorch Engine", res["mode"])
        print("[PASS] TC-11: ModelConnector Direct PyTorch fallback mode verified.")

if __name__ == "__main__":
    print("======================================================================")
    print("    TASK 8 AUTOMATED INTEGRATION TEST SUITE (FLASK API + STREAMLIT)")
    print("======================================================================")
    unittest.main()
