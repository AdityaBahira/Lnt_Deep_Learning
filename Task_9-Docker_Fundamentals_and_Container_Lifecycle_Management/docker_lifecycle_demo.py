"""
Task 9: Docker Fundamentals and Container Lifecycle Management
Automated Python Script using Lightweight Docker Hub Image (< 150 MB)
"""

import subprocess
import time
import os

LOG_FILE = "docker_command_logs.txt"
DL_IMAGE = "python:3.10-slim"  # Official Lightweight Image (~125 MB, < 1GB)
LOCAL_TAG = "my_dl_runtime:v1"
CONTAINER_NAME = "dl_runtime_container"
VOLUME_NAME = "dl_storage_vol"
NETWORK_NAME = "dl_bridge_net"

def run_cmd(cmd, desc=""):
    print(f"\n==================================================")
    print(f"[ACTION] {desc}")
    print(f"[COMMAND] {cmd}")
    print(f"==================================================")
    try:
        res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        output = res.stdout if res.returncode == 0 else res.stderr
        print(output)
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- {desc} ---\nCommand: {cmd}\nExit Code: {res.returncode}\nOutput:\n{output}\n")
            
        return res.returncode == 0, output
    except Exception as e:
        err = f"Execution error: {str(e)}"
        print(err)
        return False, err

def main():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    print(f"Starting Task 9 Docker Operations using Lightweight Image ({DL_IMAGE} ~125MB)...")
    
    # 1. Architecture Verification
    run_cmd("docker --version", "1. Check Docker Version")
    run_cmd("docker info", "2. View Docker Engine Info")
    
    # 2. Docker Images & Registry Exploration
    run_cmd(f"docker pull {DL_IMAGE}", f"3. Pull Lightweight Image from Docker Hub ({DL_IMAGE})")
    run_cmd("docker images", "4. List Local Docker Images")
    run_cmd(f"docker inspect {DL_IMAGE}", f"5. Inspect Image Layers & Metadata ({DL_IMAGE})")
    run_cmd(f"docker tag {DL_IMAGE} {LOCAL_TAG}", f"6. Tag Image for Local Use ({LOCAL_TAG})")
    run_cmd("docker images", "7. Verify Tagged Image Listing")
    
    # 3. Storage & Networking Concepts
    run_cmd(f"docker volume create {VOLUME_NAME}", "8. Create Named Volume for Persistent Storage")
    run_cmd("docker volume ls", "9. List Docker Volumes")
    run_cmd(f"docker network create {NETWORK_NAME}", "10. Create Custom Docker Bridge Network")
    run_cmd("docker network ls", "11. List Docker Networks")
    
    # 4. Container Lifecycle Operations
    run_cmd(f"docker run -d --name {CONTAINER_NAME} -v {VOLUME_NAME}:/workspace --network {NETWORK_NAME} {DL_IMAGE} python -c \"import time, sys; print('Lightweight Deep Learning Runtime Initialized!'); sys.stdout.flush(); time.sleep(3600)\"", 
            "12. Run Container in Detached Mode using Lightweight Image")
    
    time.sleep(2)
    run_cmd("docker ps", "13. List Active Running Containers")
    run_cmd(f"docker exec {CONTAINER_NAME} python -c \"import sys, platform; print('Python Version:', sys.version.split()[0]); print('Platform:', platform.platform())\"", 
            "14. Execute In-Container System Check (exec)")
    
    run_cmd(f"docker logs {CONTAINER_NAME}", "15. View Container Logs")
    
    # Pause & Unpause
    run_cmd(f"docker pause {CONTAINER_NAME}", "16. Pause Container Processes")
    run_cmd("docker ps", "17. Verify Container Paused Status")
    run_cmd(f"docker unpause {CONTAINER_NAME}", "18. Unpause Container Processes")
    
    # Stats
    run_cmd(f"docker stats {CONTAINER_NAME} --no-stream", "19. Monitor Container Resource Stats")
    
    # Stop, Start & Restart
    run_cmd(f"docker stop {CONTAINER_NAME}", "20. Stop Container Gracefully")
    run_cmd("docker ps -a", "21. List Stopped Containers")
    run_cmd(f"docker start {CONTAINER_NAME}", "22. Start Stopped Container")
    run_cmd(f"docker restart {CONTAINER_NAME}", "23. Restart Container")
    
    # Cleanup
    run_cmd(f"docker stop {CONTAINER_NAME}", "24. Stop Container before Cleanup")
    run_cmd(f"docker rm {CONTAINER_NAME}", "25. Remove Container")
    run_cmd(f"docker volume rm {VOLUME_NAME}", "26. Remove Volume")
    run_cmd(f"docker network rm {NETWORK_NAME}", "27. Remove Custom Network")
    run_cmd(f"docker rmi {LOCAL_TAG}", "28. Remove Local Image Tag")
    
    print("\nTask 9 Docker Automation Completed Successfully!")
    print(f"Log file generated: {LOG_FILE}")

if __name__ == "__main__":
    main()
