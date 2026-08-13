import requests

# Function to convert height to feet
def convert_height_to_feet(feet, inches):
    return feet + (inches / 12)

# Function to calculate BMI
def calculate_bmi(weight_kg, height_feet):
    try:
        if weight_kg <= 0 or height_feet <= 0:
            return "Error: Weight and height must be positive numbers."
        
        height_m = height_feet * 0.3048
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    except Exception as e:
        return f"Error in calculation: {str(e)}"

# Function to determine BMI category
def get_bmi_category(bmi):
    if isinstance(bmi, str):
        return bmi
    
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif 30 <= bmi < 34.9:
        return "Obese (Class 1)"
    elif 35 <= bmi < 39.9:
        return "Obese (Class 2)"
    else:
        return "Obese (Class 3)"

# Function to suggest caloric intake and workout
def suggest_caloric_intake(bmi, weight_kg, height_feet, age, gender, activity_level, days):
    height_cm = height_feet * 30.48
    
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        return "Invalid gender. Please specify 'male' or 'female'."
    
    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    activity_factor = activity_factors.get(activity_level.lower(), 1.2)
    daily_calories = bmr * activity_factor
    
    if bmi < 18.5:
        suggestion = "Increase caloric intake to gain weight."
        target_calories = daily_calories + (500 / days)
        calories_to_burn = 0
        workout_hours = 0
    elif 18.5 <= bmi < 24.9:
        suggestion = "Maintain your current caloric intake and activity level."
        target_calories = daily_calories
        calories_to_burn = 0
        workout_hours = 0
    elif bmi >= 25:
        suggestion = "Reduce caloric intake and increase activity to normalize BMI."
        total_calories_to_burn = 3500 * (bmi - 24.9)
        calories_to_burn_per_day = total_calories_to_burn / days
        target_calories = daily_calories - calories_to_burn_per_day
        workout_hours = round(calories_to_burn_per_day / 500, 1)
    
    return {
        "suggestion": suggestion,
        "target_calories": round(target_calories, 2),
        "calories_to_burn_per_day": round(calories_to_burn_per_day, 2) if bmi >= 25 else 0,
        "workout_hours": workout_hours
    }

# USDA API: Get nutritional information
def get_basic_nutritional_info(food_item):
    api_key = "zcZYjZkFEaaie5uWgcIxLkGbZHNwP5IqJcyRIVvR"   # Replace with your USDA API key
    base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    params = {
        "query": food_item,
        "api_key": api_key,
        "pageSize": 1,
        "dataType": ["SR Legacy", "Foundation", "Survey (FNDDS)"]
    }
    
    try:
        search_response = requests.get(base_url, params=params)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if not search_data.get('foods'):
            return f"No nutritional information found for '{food_item}'."
        
        food = search_data['foods'][0]
        nutrients = food.get('foodNutrients', [])
        
        nutrient_info = {
            "Food Item": food.get('description', food_item).capitalize(),
            "Calories (kcal)": 0,
            "Carbohydrates (g)": 0,
            "Protein (g)": 0,
            "Fat (g)": 0
        }
        
        nutrient_map = {
            1008: "Calories (kcal)",
            1003: "Protein (g)",
            1004: "Fat (g)",
            1005: "Carbohydrates (g)"
        }
        
        for nutrient in nutrients:
            nutrient_id = nutrient.get('nutrientId')
            if nutrient_id in nutrient_map:
                nutrient_info[nutrient_map[nutrient_id]] = round(nutrient.get('value', 0), 2)
        
        return nutrient_info
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the API: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# USDA API: Get calorie information
def get_calories_usda(food_item):
    api_key = "zcZYjZkFEaaie5uWgcIxLkGbZHNwP5IqJcyRIVvR"  # Replace with your USDA API key
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_item}&api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        calories = data['foods'][0]['foodNutrients'][3]['value']
        return f"{food_item.capitalize()} has {calories} calories."
    except (IndexError, KeyError):
        return "Calorie information not found for this item."

# Input helper functions
def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

# Main menu
def main():
    while True:
        print("\nMain Menu")
        print("1. BMI Calculator with Suggestions")
        print("2. Nutritional Information")
        print("3. Calorie Information")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\nBMI (Body Mass Index) Calculator")
            print("-" * 30)
            weight = get_float_input("Enter your weight in kg: ")
            feet = get_integer_input("Enter your height (feet): ")
            inches = get_integer_input("Enter your height (inches): ")
            age = get_integer_input("Enter your age (years): ")
            gender = input("Enter your gender (male/female): ").strip()
            activity_level = input("Enter your activity level (sedentary/lightly active/moderately active/very active/extra active): ").strip()
            days = get_integer_input("In how many days do you want to normalize/maintain your BMI? ")
            
            height = convert_height_to_feet(feet, inches)
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            suggestions = suggest_caloric_intake(bmi, weight, height, age, gender, activity_level, days)
            
            print("\nBMI Results:")
            print("-" * 30)
            print(f"Your height: {feet}'{inches}\" ({height:.2f} feet)")
            print(f"Your BMI is: {bmi}")
            print(f"Category: {category}")
            print("\nSuggestions:")
            print("-" * 30)
            print(f"Suggestion: {suggestions['suggestion']}")
            print(f"Target Daily Calorie Intake: {suggestions['target_calories']} kcal")
            if bmi >= 25:
                print(f"Calories to Burn Per Day: {suggestions['calories_to_burn_per_day']} kcal")
                print(f"Workout Time Needed Per Day: {suggestions['workout_hours']} hours")
        
        elif choice == '2':
            food_item = input("Enter the food item to get nutritional information: ").strip()
            nutrition_info = get_basic_nutritional_info(food_item)
            if isinstance(nutrition_info, dict):
                print("\nNutritional Information:")
                for key, value in nutrition_info.items():
                    print(f"{key}: {value}")
            else:
                print(nutrition_info)
        
        elif choice == '3':
            food_item = input("Enter the food item to get calorie information: ").strip()
            print(get_calories_usda(food_item))
        
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
