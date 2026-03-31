from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# ===============================================
# API KEYS DATABASE
# ===============================================
API_KEYS = {
    "AKASH_PARMA": {
        "user": "@Akash_Exploits_bot",
        "expires": "2050-12-31",
        "requests": 0,
        "limit": 100000000000
    }
}

# SubhxCosmo Mobile Search API
SUBHX_MOBILE_API = "https://api.subhxcosmo.in/api?key=CYBERXZEXX&type=mobile&term="

@app.route('/', methods=['GET'])
def get_mobile_info():
    api_key = request.args.get('key')
    mobile_num = request.args.get('num') # Mobile number mate 'num' parameter

    # 1. Key Validation
    if not api_key or api_key not in API_KEYS:
        return jsonify({"success": False, "error": "Invalid or Missing API Key"}), 403
    
    if not mobile_num:
        return jsonify({"success": False, "error": "Mobile number (num) missing"}), 400

    key_info = API_KEYS[api_key]
    key_info["requests"] += 1

    try:
        # 2. Fetch data from SubhxCosmo
        response = requests.get(f"{SUBHX_MOBILE_API}{mobile_num}", timeout=25)
        if response.status_code != 200:
            return jsonify({"success": False, "error": "Upstream API Offline"}), 503
        
        raw_data = response.json()
        
        if not raw_data.get("success"):
            return jsonify({"success": False, "error": "No records found"}), 404

        result_data = raw_data.get("result", {})
        
        # 3. Construct Final Big Response
        big_response = {
            "api_key_info": {
                "expires": key_info["expires"],
                "key_used": f"{api_key[:4]}***{api_key[-2:]}",
                "remaining_requests": key_info["limit"] - key_info["requests"],
                "user": key_info["user"]
            },
            "owner": "https://t.me/cyber_apis",
            "developer": "@Akash_Exploits_bot",
            "status": "success",
            "search_count": result_data.get("count", 0),
            "search_results": result_data.get("results", []),
            "timestamp": datetime.now().isoformat(),
            "scan_time": result_data.get("search_time", "N/A")
        }

        return jsonify(big_response)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
