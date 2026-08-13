from flask import Flask, request, jsonify, render_template
from project import calculate_bmi, suggest_caloric_intake, get_basic_nutritional_info, get_calories_usda, convert_height_to_feet

app = Flask(__name__)

# Function to categorize BMI
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# BMI Calculation route
@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi_endpoint():
    data = request.json
    weight = float(data['weight'])
    feet = int(data['feet'])
    inches = int(data['inches'])
    age = int(data['age'])
    gender = data['gender']
    activity_level = data['activityLevel']
    days = int(data['days'])

    height = convert_height_to_feet(feet, inches)
    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)
    suggestions = suggest_caloric_intake(bmi, weight, height, age, gender, activity_level, days)

    return jsonify({
        "bmi": bmi,
        "category": category,
        "suggestions": suggestions
    })

# Nutritional Information route
@app.route('/nutrition_info', methods=['POST'])
def nutrition_info_endpoint():
    data = request.json
    food_item = data['foodItem']
    nutrition_info = get_basic_nutritional_info(food_item)
    return jsonify(nutrition_info)

# Calorie Information route
@app.route('/calorie_info', methods=['POST'])
def calorie_info_endpoint():
    data = request.json
    food_item = data['foodItem']
    calorie_info = get_calories_usda(food_item)
    return jsonify({"calorie_info": calorie_info})

# Result page route
@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
