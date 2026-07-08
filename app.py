from flask import Flask, request, jsonify
from flask_cors import CORS
import razorpay

app = Flask(__name__)
CORS(app)

RAZORPAY_KEY_ID = "rzp_test_TB4hm6OBFwMJAA"
RAZORPAY_KEY_SECRET = "djbd7P7YQxI9xpTSI8fCzcSN"

try:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception as e:
    client = None

@app.route('/')
def home():
    return jsonify({"status": "Server running successfully", "project": "UPI Self Verifier Live"})

@app.route('/api/verify-upi', methods=['POST'])
def verify_upi():
    try:
        data = request.get_json()
        if not data or "upiId" not in data:
            return jsonify({"success": False, "message": "UPI ID missing in payload"}), 400
            
        upi_id = str(data.get("upiId")).strip()
        
        if "@" not in upi_id:
            return jsonify({"success": False, "message": "Invalid UPI ID format (@ missing)"})

        # 👑 REAL HIT ONLY:
        # Agar tumhare pass Live Key (rzp_live_...) hogi tabhi Razorpay real name nikaal ke dega
        if client and "live" in RAZORPAY_KEY_ID:
            try:
                response = client.vpa.validate({"vpa": upi_id})
                if response.get("success"):
                    return jsonify({
                        "success": True,
                        "realBankingName": response.get("customer_name")
                    })
            except Exception as e:
                return jsonify({"success": False, "message": f"Razorpay API Error: {str(e)}"})
        
        # Test Mode standard behavior (No Fake Names List!)
        # Agar Test Key hai, to ye simply bata dega ki ID format sahi hai par Live Key chahiye.
        return jsonify({
            "success": True,
            "realBankingName": f"{upi_id.split('@')[0].upper()} [Test Mode Active - Need Razorpay Live Key for Bank Name]"
        })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
