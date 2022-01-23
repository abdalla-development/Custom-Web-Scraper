from flask_wtf import FlaskForm
from selenium import webdriver
import time
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

food_type = ""
choices_list = []
name = ""
user_input = ""
table_title = ""
portion_size = ""
calories = ""
total_fat = ""
saturated_fat = ""
cholesterol = ""
sodium = ""
total_carbohydrate = ""
dietary_fiber = ""
sugar = ""
protein = ""
vitamin_d = ""
calcium = ""
iron = ""
potassium = ""
pie_chart = ""
bar_chart = ""
chart_title = ""
last_chart = ""


def get_choices():
    global choices_list
    choice = []
    # Initializing selenium
    chrome_driver_path = "C:/Code Devolopment/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("https://www.nutritionvalue.org/")
    # Food Search
    food_search = driver.find_element_by_id("food_query")
    food_search.send_keys(f"{food_type}")
    food_search_submit = driver.find_element_by_xpath('//*[@id="main"]/tbody/tr[5]/td/form/input')
    food_search_submit.click()
    # Get the Food choices to select from
    food_table = driver.find_elements_by_class_name("left")
    for x in range(1, len(food_table) - 1):
        choice.append(food_table[x].text)
    choices_list = choice
    driver.quit()


def user_choice():
    # Initializing selenium
    chrome_driver_path = "C:/Code Devolopment/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("https://www.nutritionvalue.org/")
    # Food Search
    food_search = driver.find_element_by_id("food_query")
    food_search.send_keys(f"{food_type}")
    food_search_submit = driver.find_element_by_xpath('//*[@id="main"]/tbody/tr[5]/td/form/input')
    food_search_submit.click()
    # User Choice
    option = driver.find_element_by_partial_link_text(f"{user_input}")
    option.click()
    time.sleep(5)
    # Get The Data
    global total_fat, table_title, portion_size, calories, saturated_fat, cholesterol, sodium, total_carbohydrate
    global dietary_fiber, sugar, protein, vitamin_d, calcium, iron, potassium, pie_chart, bar_chart, chart_title, last_chart
    table_title = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[1]/td').text
    portion_size = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[3]/td[2]').text
    calories = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[5]/td[2]').text
    total_fat = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[10]/td[2]/b').text
    saturated_fat = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[12]/td[2]').text
    cholesterol = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[14]/td[2]').text
    sodium = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[16]/td[2]').text
    total_carbohydrate = driver.find_element_by_xpath(
        '//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[18]/td[2]').text
    dietary_fiber = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[20]/td[2]').text
    sugar = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[22]/td[2]').text
    protein = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[24]/td[2]').text
    vitamin_d = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[26]/td[2]').text
    calcium = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[28]/td[2]').text
    iron = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[30]/td[2]').text
    potassium = driver.find_element_by_xpath('//*[@id="nutrition-label"]/tbody/tr/td/table/tbody/tr[32]/td[2]').text
    pie_chart = driver.find_element_by_xpath(
        '//*[@id="main"]/tbody/tr[4]/td/table/tbody/tr[4]/td[3]/img[1]').get_attribute("src")
    bar_chart = driver.find_element_by_xpath(
        '//*[@id="main"]/tbody/tr[4]/td/table/tbody/tr[4]/td[3]/img[2]').get_attribute("src")
    chart_title = driver.find_element_by_xpath(
        '//*[@id="main"]/tbody/tr[4]/td/table/tbody/tr[7]/td[3]/table[2]/tbody/tr[1]/th').text
    last_chart = driver.find_element_by_xpath(
        '//*[@id="main"]/tbody/tr[4]/td/table/tbody/tr[7]/td[3]/table[2]/tbody/tr[2]/td/img').get_attribute("src")
    driver.quit()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class FoodForm(FlaskForm):
    food = StringField(label='Food Name', validators=[DataRequired()])
    submit = SubmitField(label='Enter')


@app.route("/", methods=["GET", "POST"])
def home():
    global food_type
    form = FoodForm()
    if request.method == "GET":
        return render_template("index.html", form=form)
    else:
        if form.validate_on_submit():
            food_type = form.data['food']
            return redirect(url_for('choices'))


@app.route("/choices")
def choices():
    global name
    if request.method == "GET":
        get_choices()
        last = len(choices_list)
        return render_template("choices.html", food_list=choices_list, len=last)


@app.route("/choice/<value>")
def choice_name(value):
    global user_input
    user_input = value
    user_choice()
    return redirect(url_for('data'))


@app.route("/data")
def data():
    chart = {"pie_chart": pie_chart, "bar_chart": bar_chart, "third_title": chart_title, "last_chart": last_chart}
    table = {"Portion Size": portion_size, "Calories": calories, "Total Fat": total_fat, "Saturated Fat": saturated_fat,
             "Cholesterol": cholesterol, "Sodium": sodium, "Total Carbohydrate": total_carbohydrate,
             "Dietary Fiber": dietary_fiber, "Sugar": sugar, "Protein": protein, "Vitamin D": vitamin_d,
             "Calcium": calcium, "Iron": iron, "Potassium": potassium}
    return render_template("data.html", figures=chart, table_data=table)


if __name__ == "__main__":
    app.run(debug=True)

