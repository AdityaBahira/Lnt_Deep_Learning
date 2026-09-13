"""
test_client.py
--------------
Automated test suite and sample output generator for the Flask Deep Learning API.
Executes test requests across all valid and error scenarios and exports detailed
results to sample_outputs.json.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def run_api_tests():
    print("=" * 70)
    print("STARTING FLASK DEEP LEARNING API AUTOMATED TEST SUITE")
    print("=" * 70)

    client = app.test_client()
    test_results = []

    # Utility to log test step
    def execute_test(test_id, description, method, path, headers=None, data=None, expected_status=200):
        print(f"\n[Test #{test_id}] {description}")
        print(f"--> {method} {path}")
        
        start_time = datetime.now(timezone.utc)
        if method == "GET":
            response = client.get(path, headers=headers)
        elif method == "POST":
            response = client.post(path, headers=headers, data=data)
        elif method == "PUT":
            response = client.put(path, headers=headers, data=data)

        status_code = response.status_code
        try:
            body = response.get_json()
        except Exception:
            body = response.get_data(as_text=True)

        passed = (status_code == expected_status)
        symbol = "[PASSED]" if passed else "[FAILED]"
        print(f"<-- Status Code: {status_code} (Expected: {expected_status}) | {symbol}")

        test_record = {
            "test_id": test_id,
            "description": description,
            "request": {
                "method": method,
                "path": path,
                "headers": headers or {},
                "body": json.loads(data) if data and isinstance(data, str) and data.startswith("{") else data
            },
            "response": {
                "status_code": status_code,
                "expected_status": expected_status,
                "body": body
            },
            "passed": passed
        }
        test_results.append(test_record)
        return response

    # 1. Test Root Endpoint
    execute_test(1, "Root Info Endpoint Check", "GET", "/", expected_status=200)

    # 2. Test Health Check Endpoint
    execute_test(2, "Health Readiness & Model Check", "GET", "/health", expected_status=200)

    # 3. Test Valid Single Sample Prediction
    single_payload = json.dumps({
        "features": [45.0, 26.5, 125.0, 110.0, 210.0, 75.0, 5.0, 7.0]
    })
    execute_test(
        3, "Valid Single Sample Prediction", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=single_payload, expected_status=200
    )

    # 4. Test Valid Batch Predictions (2 Samples)
    batch_payload = json.dumps({
        "instances": [
            [25.0, 21.0, 110.0, 85.0, 160.0, 65.0, 10.0, 8.0],
            [72.0, 34.5, 160.0, 195.0, 290.0, 92.0, 1.0, 5.0]
        ]
    })
    execute_test(
        4, "Valid Batch Predictions (Multiple Patients)", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=batch_payload, expected_status=200
    )

    # 5. Test Valid Dict Key-Value Feature Payload Pattern
    dict_payload = json.dumps({
        "data": {
            "age": 60, "bmi": 31.2, "blood_pressure": 145, "glucose_level": 165,
            "cholesterol": 250, "heart_rate": 84, "physical_activity_hours": 2, "sleep_hours": 6
        }
    })
    execute_test(
        5, "Valid Dict Feature Mapping Payload", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=dict_payload, expected_status=200
    )

    # 6. Test Error: HTTP 415 Unsupported Media Type (Missing Content-Type Header)
    execute_test(
        6, "Error Handling: Unsupported Media Type (HTTP 415)", "POST", "/predict",
        headers={"Content-Type": "text/plain"}, data="age=45", expected_status=415
    )

    # 7. Test Error: HTTP 400 Bad Request (Missing JSON payload body)
    execute_test(
        7, "Error Handling: Missing JSON Payload Body (HTTP 400)", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data="", expected_status=400
    )

    # 8. Test Error: HTTP 400 Bad Request (Missing 'features'/'instances' key)
    invalid_key_payload = json.dumps({"incorrect_key": [1, 2, 3]})
    execute_test(
        8, "Error Handling: Missing Required Key (HTTP 400)", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=invalid_key_payload, expected_status=400
    )

    # 9. Test Error: HTTP 422 Unprocessable Entity (Invalid Dimension - 5 features instead of 8)
    wrong_dim_payload = json.dumps({"features": [45.0, 26.5, 125.0, 110.0, 210.0]})
    execute_test(
        9, "Error Handling: Wrong Feature Array Dimension (HTTP 422)", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=wrong_dim_payload, expected_status=422
    )

    # 10. Test Error: HTTP 422 Unprocessable Entity (Non-numeric values in array)
    string_feat_payload = json.dumps({"features": [45.0, "high_bmi", 125.0, 110.0, 210.0, 75.0, 5.0, 7.0]})
    execute_test(
        10, "Error Handling: Non-numeric Feature Values (HTTP 422)", "POST", "/predict",
        headers={"Content-Type": "application/json"}, data=string_feat_payload, expected_status=422
    )

    # 11. Test Error: HTTP 405 Method Not Allowed (GET method on /predict)
    execute_test(
        11, "Error Handling: Method Not Allowed GET on /predict (HTTP 405)", "GET", "/predict", expected_status=405
    )

    # 12. Test Error: HTTP 404 Not Found (Non-existent Endpoint)
    execute_test(
        12, "Error Handling: Non-existent URL Path (HTTP 404)", "GET", "/api/v2/unknown", expected_status=404
    )

    # 13. Test Interactive HTML Docs Page
    execute_test(
        13, "Interactive HTML Documentation Page", "GET", "/docs", expected_status=200
    )

    # Summary
    passed_count = sum(1 for t in test_results if t["passed"])
    total_count = len(test_results)

    print("\n" + "=" * 70)
    print(f"TEST SUITE COMPLETE: {passed_count}/{total_count} TESTS PASSED")
    print("=" * 70)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_outputs.json")
    with open(output_path, "w") as f:
        json.dump({
            "test_summary": {
                "total_tests": total_count,
                "passed_tests": passed_count,
                "failed_tests": total_count - passed_count,
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "test_results": test_results
        }, f, indent=4)

    print(f"Sample test prediction outputs saved to: {output_path}")

if __name__ == "__main__":
    run_api_tests()
