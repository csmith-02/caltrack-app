# caltrack-app

Contributors: Connor Smith

This project is a calorie calculator that uses the Mifflin-St Jeor Equation to determine the number of calories
an individual should eat everyday to lose 0.5 lbs per week. 0.5 lbs/week is the recommended rate to lose weight
while maintaining a healthy lifestyle.

The equation is from: https://www.calculator.net/calorie-calculator.html

It uses characteristics such as height, weight, sex, age, and your activity level to determine your daily caloric intake.

This project was done using HTML, CSS, and Flask (a python-based micro web framework).

To run this application:

You will need Python as well as Git installed.

1) Install Python on your local machine.
Link: https://www.python.org/downloads/

2) Install Git on your local machine.
Link: https://gitforwindows.org/

3) Run this git command in your command prompt (terminal, Git Bash, etc.) to clone the repository to your local machine.
git clone https://github.com/csmith-02/caltrack-app.git

4) In your command prompt, change directory into the "caltrack-app" folder.

5) Create a virtual environment in this "caltrack-app" folder and run the virtual environment. Do this by running these commands in your command prompt at the same location.
   When running the virtual environment, run the "source" command that corresponds to your operating system.

python -m venv venv

source venv/Scripts/activate (Windows)
source venv/bin/activate (Mac)

6) In the same location in your command prompt, run the command:
pip install -r requirements.txt

*This will install all dependencies you need (including Flask, Jinja, and PyAutoGUI)


7) Finally, in the "caltrack-app" directory/location, type one of these two commands in your command prompt to run:

python app.py

OR

flask run