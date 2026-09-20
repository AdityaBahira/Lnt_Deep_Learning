# Task 5 API Testing - Screenshots Folder

Place your captured Postman and terminal screenshots in this folder before uploading to GitHub:

1. 01_flask_server_startup.png      - Terminal screenshot of Flask server starting on port 5000
2. 02_root_endpoint_tc01.png          - Postman GET / (200 OK) root info response
3. 03_health_probe_tc02.png           - Postman GET /health (200 OK) model readiness probe
4. 04_single_prediction_tc03.png      - Postman POST /predict single sample 14-feature vector (200 OK)
5. 05_batch_prediction_tc04.png       - Postman POST /predict batch sample matrix (200 OK)
6. 06_dict_prediction_tc05.png        - Postman POST /predict key-value dict payload (200 OK)
7. 07_unsupported_media_tc06.png      - Postman POST /predict header text/plain (415 Unsupported Media Type)
8. 08_missing_payload_tc07_tc08.png   - Postman POST /predict empty body {} (400 Bad Request)
9. 09_dimension_mismatch_tc09.png     - Postman POST /predict 4 features vs 14 (422 Unprocessable Entity)
10. 10_non_numeric_tc10.png           - Postman POST /predict string feature value (422 Unprocessable Entity)
11. 11_method_not_allowed_tc11.png     - Postman GET /predict (405 Method Not Allowed)
12. 12_not_found_tc12.png              - Postman GET /api/v2/unknown (404 Not Found)
13. 13_postman_runner_summary.png     - Postman Collection Runner summary screen (100% Passed green screen)
