from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_eligibility(data):
    """Function to evaluate if the user is eligible for donations."""
    score = 0

    # Employment status
    employment_status = data.get("employment_status", "").lower()
    income_range = data.get("income_range", "")

    employment_scores = {
        "employed": 30,
        "unemployed": -30
    }
    score += employment_scores.get(employment_status, -10)

    if employment_status == "employed" and income_range == "60k-80k":
        score += 10

    # Housing situation
    housing_scores = {"own": 20, "rent": -10}
    score += housing_scores.get(data.get("housing_type", "").lower(), -5)

    # Gross income
    gross_income = data.get("gross_income_last_year", 0)
    score += 15 if gross_income > 40000 else -20

    # Investments
    investment_accounts = data.get("investment_accounts", {})
    if isinstance(investment_accounts, dict):
        total_investments = sum(investment_accounts.values())
        if total_investments > 10000:
            score += 20
        elif total_investments > 5000:
            score += 10

    # Determine eligibility (low score = high financial need)
    eligible = score <= 20
    return {"eligible": eligible, "score": score}

@app.route("/api/background-check", methods=["POST"])
def background_check():
    """API endpoint for checking user eligibility."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = [
            "firstname", "lastname", "address", "contact",
            "employment_status", "housing_type", "gross_income_last_year", "reference"
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Validate investment accounts
        if "investment_accounts" in data and not isinstance(data["investment_accounts"], dict):
            return jsonify({"error": "investment_accounts must be a dictionary with investment types and amounts"}), 400

        # Compute eligibility
        result = calculate_eligibility(data)
        return jsonify(result), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
    except TypeError as e:
        return jsonify({"error": f"Type error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
