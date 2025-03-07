# Backend 
## Donation Platform - Background Check API

📡 API Usage
➡️ Endpoint: /api/background-check
Method: POST
Content-Type: application/json


Use dropdowns for employment status & housing.
Use checkboxes for investment options with a field to enter amounts dynamically.

Sample input 

``` 
{
  "firstname": "Mark",
  "lastname": "Taylor",
  "address": "789 Maple Ave",
  "contact": "+1987654321",
  "employment_status": "employed",
  "income_range": "60k-80k",
  "housing_type": "own",
  "investment_accounts": {
    "stocks": 12000,
    "crypto": 5000
  },
  "gross_income_last_year": 75000,
  "reference": "Sarah Lee"
}

```

The API will return **"eligible": false,** to be used as eligibility cretiria  