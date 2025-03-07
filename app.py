from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_eligibility(data):
    """Function to evaluate if the user is eligible for donations."""
    score = 0

    # Employment status
    if data["employment_status"] == "employed":
        score += 30  
        if "income_range" in data and data["income_range"] == "60k-80k":
            score += 10
    elif data["employment_status"] == "unemployed":
        score -= 30  
    else:
        score -= 10 

    # Housing situation
    if data["housing_type"] == "own":
        score += 20  
    elif data["housing_type"] == "rent":
        score -= 10  
    else:  
        score -= 5  

    # Gross income
    if data["gross_income_last_year"] > 40000:
        score += 15
    else:
        score -= 20

    # Investments - Check if the user has significant investments
    if "investment_accounts" in data and isinstance(data["investment_accounts"], dict):
        total_investments = sum(data["investment_accounts"].values())
        if total_investments > 10000:
            score += 20  
        elif total_investments > 5000:
            score += 10  
        

    # Determine eligibility (low score = high financial need)
    eligible = score <= 20  

    return {"eligible": eligible, "score": score}

@app.route("/api/background-check", methods=["POST"])
def background_check():
    """API endpoint for checking user eligibility"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["firstname", "lastname", "address", "contact", 
                           "employment_status", "housing_type", "gross_income_last_year", "reference"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Validate investment accounts
        if "investment_accounts" in data and not isinstance(data["investment_accounts"], dict):
            return jsonify({"error": "investment_accounts must be a dictionary with investment types and amounts"}), 400

        # Compute eligibility
        result = calculate_eligibility(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
