from flask import Flask, abort, json, redirect, render_template, request
import json
from urllib.request import urlopen

import pyautogui


app = Flask(__name__)

user = {}
meal = {}
day = {}

global calories
global calories_consumed

def newDay():
    global day
    global calories_consumed
    day = {
    "carbs": "0",
    "protein": "0",
    "fats": "0",
    "calories": "0"
    }
    calories_consumed = 0

def createMeal():
    global meal
    meal = {
        "carbs": "",
        "protein": "",
        "fats": "",
        "calories": ""
    }

def addMealToDay():
    day['carbs'] = int(day['carbs']) + int(meal['carbs'])
    day['protein'] = int(day['protein']) + int(meal['protein'])
    day['fats'] = int(day['fats']) + int(meal['fats'])
    day['calories'] = int(day['calories']) + int(meal['calories'])

def updateUser() -> None:
    global user
    infoFile = open('information.json')
    data = json.load(infoFile)
    user = {
        "name": data['name'],
        "height": data['height'],
        "weight": data['weight'],
        "sex": data['sex'],
        "activity_level": data['activity_level'],
        "age": data['age']
    }
    infoFile.close()

# Routes

@app.post('/setup')
def initial():
    global calories

    newDay()
    user['name'] = request.form.get('name')
    user['height'] = request.form.get('height')
    user['weight'] = request.form.get('weight')
    user['age'] = request.form.get('age')

    gen = request.form.get('sex')
    if gen == "1":
        user['sex'] = 'Male'
    elif gen == "2":
        user['sex'] = 'Female'
    else:
        abort(400)

    user['activity_level'] = request.form.get('activity_level')

    # Change json file to reflect new values
    out_file = open('information.json', 'w')
    json.dump(user, out_file)
    out_file.close()

    return redirect('/', 302)

@app.get('/setup')
def setup():
    newDay()
    return render_template('setup.html', heading='Welcome', hidenav='hide')

@app.get('/')
def index():
    # Opens the JSON file and updates the attributes of the user to the latest JSON information
    updateUser()

    if str(user['name']) == '' or str(user['weight']) == '' or str(user['sex']) == '' or str(user['height']) == '' or str(user['activity_level']) == '' or str(user['age']) == '':
        return redirect('/setup', 302)

    calories = determine_calories(user['sex'], user['weight'], user['height'], user['activity_level'], user['age'])

    return render_template('today.html', heading='TODAY', calories=calories, user=user, day=day, calsRemaining=(calories-calories_consumed))

@app.get('/settings')
def settings():
    updateUser()
    if str(user['name']) == '' or str(user['weight']) == '' or str(user['sex']) == '' or str(user['height']) == '' or str(user['activity_level']) == '' or str(user['age']) == '':
        return redirect('/setup', 302)
    return render_template('settings.html', heading='SETTINGS', user=user)

@app.post('/settings')
def update_settings():
    global user

    if request.form.get('btn') == 'CHANGE USER':
        return redirect('/setup', 302)

    out_file = open('information.json', 'w')

    height = request.form.get('changeHeight')
    weight = request.form.get('changeWeight')
    age = request.form.get('changeAge')
    activity = request.form.get('changeActivity')

    if height:
        user['height'] = height
    if weight:
        user['weight'] = weight
    if age:
        user['age'] = age
    if activity:
        user['activity_level'] = activity
    if not height and weight and age and activity:
        # do nothing
        pass
    else:
        newDay()
        json.dump(user, out_file)
    out_file.close()
    return redirect('/settings', 302)

@app.post('/track')
def post_calories():

    global calories_consumed
    global meal
    createMeal()
    carbs = request.form.get('am-of-carbs')
    protein = request.form.get('am-of-pro')
    fats = request.form.get('am-of-fats')
    cals = request.form.get('am-of-cals')

    try:
        validateMeal(carbs, protein, fats, cals)
    except:
        pyautogui.alert('Invalid Caloric Ratio of Macros to Calories')
        return redirect('/track', 302)

    calories_consumed = calories_consumed + int(cals)

    meal['carbs'] = carbs
    meal['protein'] = protein
    meal['fats'] = fats
    meal['calories'] = cals
    addMealToDay()

    return redirect('/track', 302)

@app.get('/track')
def track():
    updateUser()
    if str(user['name']) == '' or str(user['weight']) == '' or str(user['sex']) == '' or str(user['height']) == '' or str(user['activity_level']) == '' or str(user['age']) == '':
        return redirect('/setup', 302)

    calories = determine_calories(user['sex'], user['weight'], user['height'], user['activity_level'], user['age'])

    return render_template('track.html', heading='TRACK', calsRemaining=(calories - calories_consumed))

@app.get('/clear')
def clearData():
    updateUser()
    if str(user['name']) == '' or str(user['weight']) == '' or str(user['sex']) == '' or str(user['height']) == '' or str(user['activity_level']) == '' or str(user['age']) == '':
        return redirect('/setup', 302)
    
    newDay()
    return redirect('/', 302)

# Determines the recommended caloric intake for a specific individual to lose 0.5 lbs a week
# Uses the Mifflin-St Jeor Equation:
#   BMR = 10W(kg) + 6.25H(cm) - 5A + 5 : Male
#   BMR = 10W + 6.25H - 5A - 161 : Female
# Light exercise factor: 1.375
# Moderate exercise factor: 1.55
# Hard exercise factor: 1.725
def determine_calories(sex, weight, height, activity_level, age) -> int:
    kg_convert = float(weight) / 2.2
    cm_convert = float(height) * 2.54

    activity = 0
    bmr = 0.0

    # Determine activity level factor
    if int(activity_level) == 1:
        activity = 1.375
    elif int(activity_level) == 2:
        activity = 1.55
    elif int(activity_level) == 3:
        activity = 1.725
    else:
        abort(400)

    if str(sex) == 'Male':
        local_cal = (10.0 * kg_convert) + (6.25 * cm_convert) - (5 * float(age)) + 5
        bmr = local_cal * activity
        
        # return the basal metabolic rate minus 250 calories. This caloric reduction is what contributes to the losing of 0.5 lbs a week
        return int(bmr) - 250
    if str(sex) == 'Female':
        local_cal = (10.0 * kg_convert) + (6.25 * cm_convert) - (5 * float(age)) - 161
        bmr = local_cal * activity

        # return the basal metabolic rate minus 250 calories. This caloric reduction is what contributes to the losing of 0.5 lbs a week
        return int(bmr) - 250
    else:
        abort(400)

# Calories per gram for protein, carbs, and fats
# protein: 4 cals/g
# carbs: 4 cals/g
# fats: 9 cals/g
def validateMeal(carbs, protein, fats, calories) -> bool:
    macro_cals = (4 * int(carbs)) + (4 * int(protein)) + (9 * int(fats))
    if abs(int(calories) - macro_cals) <= 10:
        return True
    else:
        abort(400);


## THIS IS WHERE THE PROGRAM STARTS

newDay()
updateUser()

# keep this condition at the bottom of the file
if __name__ == "__main__":
    app.run(debug=True)