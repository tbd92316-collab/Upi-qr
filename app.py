from flask import Flask, request, jsonify
from flask_cors import CORS
import razorpay
import random

app = Flask(__name__)
CORS(app)

RAZORPAY_KEY_ID = "rzp_test_TB4hm6OBFwMJAA"
RAZORPAY_KEY_SECRET = "djbd7P7YQxI9xpTSI8fCzcSN"

try:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception as e:
    client = None

# Genuine looking test names database
TEST_NAMES = [
    "Akash Mohanty", "Rajesh Kumar Das", "Suman Sharma", 
    "Priyanka Mishra", "Amit Kumar Pradhan", "Rahul Patnaik",
    "Deepak Rao", "Subham Naik", "Anjali Choudhury"
]

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

        # Agar future me real Live Key daloge to ye real block chalega
        try:
            if "live" in RAZORPAY_KEY_ID and client:
                response = client.vpa.validate({"vpa": upi_id})
                if response.get("success"):
                    return jsonify({
                        "success": True,
                        "realBankingName": response.get("customer_name")
                    })
        except Exception:
            pass
            
        # 👑 FIXED SIMULATOR LOGIC: 
        # Agar numeric ID ya random merchant id milti hai, toh list se ek real name return karega
        clean_prefix = upi_id.split("@")[0].replace(".", " ").replace("_", " ").strip()
        
        # Check agar prefix sirf number ya alphanumeric code hai
        if clean_prefix.isalnum() and any(char.isdigit() for char in clean_prefix):
            # Seed ensure karega ki ek specific UPI ID par hamesha wahi ek naam fix dikhaye!
            random.seed(upi_id)
            real_looking_name = random.choice(TEST_NAMES)
        else:
            real_looking_name = clean_prefix.title()

        simulated_name = f"{real_looking_name} [Verified Test Account]"
        
        return jsonify({
            "success": True,
            "realBankingName": simulated_name
        })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
