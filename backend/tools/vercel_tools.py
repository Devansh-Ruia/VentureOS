import os
import time
import requests


def deploy_landing_page(html: str, project_name: str) -> dict:
    """
    Deploy a landing page to Vercel via REST API.
    Creates deployment with single index.html file.
    Polls status until READY or ERROR (max 30s).
    Returns deployment URL and ID.
    """
    try:
        token = os.getenv("VERCEL_TOKEN")
        team_id = os.getenv("VERCEL_TEAM_ID")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        url = "https://api.vercel.com/v13/deployments"
        if team_id:
            url += f"?teamId={team_id}"
        
        payload = {
            "name": project_name.lower().replace(" ", "-"),
            "files": [
                {
                    "file": "index.html",
                    "data": html,
                }
            ],
            "projectSettings": {
                "framework": None,
            },
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        deployment_id = data.get("id")
        deployment_url = data.get("url")
        
        # Poll deployment status
        status_url = f"https://api.vercel.com/v13/deployments/{deployment_id}"
        if team_id:
            status_url += f"?teamId={team_id}"
        
        max_wait = 30
        start = time.time()
        
        while time.time() - start < max_wait:
            status_response = requests.get(status_url, headers=headers, timeout=10)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            ready_state = status_data.get("readyState")
            if ready_state == "READY":
                return {
                    "url": f"https://{deployment_url}",
                    "deployment_id": deployment_id,
                }
            elif ready_state == "ERROR":
                return {"error": "Deployment failed", "deployment_id": deployment_id}
            
            time.sleep(2)
        
        return {
            "url": f"https://{deployment_url}",
            "deployment_id": deployment_id,
        }
    
    except Exception as e:
        return {"error": str(e)}
