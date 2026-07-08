from flask import Flask, request, jsonify
from flask_cors import CORS
import razorpay

app = Flask(__name__)
CORS(app)

# Tumhari Razorpay Keys
RAZORPAY_KEY_ID = "rzp_test_TB4hm6OBFwMJAA"
RAZORPAY_KEY_SECRET = "djbd7P7YQxI9xpTSI8fCzcSN"

try:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception:
    client = None

@app.route('/')
def home():
    return jsonify({"status": "Server running successfully"})

@app.route('/api/verify-upi', methods=['POST'])
def verify_upi():
    try:
        data = request.get_json()
        if not data or "upiId" not in data:
            return jsonify({"success": False, "message": "UPI ID missing"}), 400
            
        upi_id = str(data.get("upiId")).strip()
        
        if not client:
            return jsonify({"success": False, "message": "Razorpay client not initialized"})

        # Razorpay Validation Hit
        response = client.vpa.validate({"vpa": upi_id})
        
        # Exact output parameters request ke mutabik
        if response.get("success"):
            return jsonify({
                "success": True,
                "upiId": upi_id,
                "realBankingName": response.get("customer_name")
            })
        else:
            return jsonify({
                "success": False, 
                "message": "Bank server se response nahi mila ya ID galat hai"
            })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
