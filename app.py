from flask import Flask, request, jsonify
from flask_cors import CORS
import razorpay

app = Flask(__name__)
# CORS enable karne se tumhari HTML website bina kisi error ke is server se connect ho payegi
CORS(app)

# Tumhari Razorpay Test Keys jo tumne di hain
RAZORPAY_KEY_ID = "rzp_test_TB4hm6OBFwMJAA"
RAZORPAY_KEY_SECRET = "djbd7P7YQxI9xpTSI8fCzcSN"

# Razorpay client initialize kiya
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/')
def home():
    return jsonify({"status": "Server running successfully", "project": "UPI Self Verifier"})

@app.route('/api/verify-upi', methods=['POST'])
def verify_upi():
    data = request.get_json()
    if not data or "upiId" not in data:
        return jsonify({"success": False, "message": "UPI ID missing in request payload"}), 400
        
    upi_id = data.get("upiId").trim()
    
    try:
        # Razorpay backend validation endpoint code
        response = client.vpa.validate({"vpa": upi_id})
        
        if response.get("success"):
            return jsonify({
                "success": True,
                "realBankingName": response.get("customer_name")
            })
        else:
            return jsonify({"success": False, "message": "Invalid UPI ID ya bank se response nahi mila"})
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
  
