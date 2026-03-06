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
        print("Vercel status:", response.status_code)
        print("Vercel response:", response.json())
        response.raise_for_status()
        
        deployment_id = response.json()["id"]
        url = response.json()["url"]
        
        # Poll until READY
        for _ in range(15):  # max 30 seconds
            time.sleep(2)
            status_res = requests.get(
                f"https://api.vercel.com/v13/deployments/{deployment_id}",
                headers={"Authorization": f"Bearer {os.getenv('VERCEL_TOKEN')}"},
            )
            state = status_res.json().get("readyState", "")
            print(f"Vercel state: {state}")
            if state == "READY":
                return {"url": f"https://{url}", "deployment_id": deployment_id}
            elif state == "ERROR":
                return {"url": None, "deployment_id": deployment_id, "error": "Deploy failed"}
        
        # Timeout — return URL anyway, it'll likely be ready soon
        return {"url": f"https://{url}", "deployment_id": deployment_id}
    
    except Exception as e:
        return {"error": str(e)}
