# API ENDPOINTS
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO
from flask_api import FlaskAPI, status
import json


 # Initialize the Flask application
app = FlaskAPI(__name__, instance_relative_config=True)
asyncMode = None
socketio  = SocketIO(app, async_mode=asyncMode)


#Initialise the Data structures to be used to Capture Data
appUsers = []
appVendorAdmins = {}
appMeals = {}
appMenu = {}
appOrders = {}

appMeals["Rice with Beef"] = "2000"

# Define a route for the default URL, which loads the first page
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/admin')
def showAdmin():
    return render_template('/admin.html')  

@app.route('/customer')
def showCustomer():
    return render_template('/customer.html')   

@app.route('/orderhistory')
def showOrderHistory():
    return render_template('/orderhistory.html') 


# API ENDPOINTS
#Sign up a user either as a customer or vendor admin
@app.route('/auth/signup', methods=['POST'])
def signUp():
    userData = []
    #userPassword = request.form['password']
    userEmail = request.form.get('email')
    userPassword = request.form.get('password')
    userData.append(userEmail)
    userData.append(userPassword)
    appUsers.append(userData)
    return json.dumps(appUsers)

#authenticate customers or admin
@app.route('/auth/login', methods=['POST'])
def login():
    userData = []
    userEmail = request.form.get('email')
    userPassword = request.form.get('password')
    userData.append(userEmail)
    userData.append(userPassword)
    #check if user data exists
    if userData in appUsers:
        return json.dumps("User Logged in successfully")
    else:
        return json.dumps("Wrong email or Password")


#Return all the available meals to the vendor admin
@app.route('/meals', methods=['GET'])
def getAllMeals():
    return json.dumps(appMeals)

#Allow the vendor admin to add another meal option
@app.route('/meals', methods=['POST'])
def addMeal():
    # retrieve the meal option submitted
    meal = request.form.get('meal')
    mealPrice = request.form.get('meal_price')
    appMeals[str(meal)] = str(mealPrice)
    return jsonify(appMeals)

#Allow the ADMIN to edit a particular meal option
@app.route('/meals/<mealId>', methods=['PUT'])
def updateAMeal(mealId):
    if len(appMeals) > 0:
        mealID = request.form.get('meal_id')
        mealUpdate = request.form.get('meal_update')
        mealPrice = appMeals[mealID]
        appMeals.pop(mealID, None) #REMOVE THE PREVIOUS ENTRY
        appMeals[mealUpdate] = mealPrice #Add the New Entry
        return json.dumps("Meal Updated successfully")
    else:
        return json.dumps("Meals are Empty")

#Allow the admin to delete a particular meal option
@app.route('/meals/<mealId>', methods=['DELETE'])
def deleteAMeal(mealId):
    if len(appMeals) > 0:
        mealID = request.form.get('meal_id')
        del appMeals[mealID]
        return json.dumps("Meal Deleted successfully")
    else:
        return json.dumps("Meals are Empty")




#Allow the admin an operation to the set the menu of the day
@app.route('/menu', methods=['POST'])
def setMenuOfTheDay():
    meal = request.form.get('meal')
    mealPrice = appMeals[meal]
    appMenu[meal] = mealPrice
    return json.dumps(appMenu)

#Allow the authenticated users to view menu of the day
@app.route('/menu', methods=['GET'])
def getMenuOfTheDay():
    return json.dumps(appMenu)




#Allow the authenticated users to make orders from the menu of the day
@app.route('/orders', methods=['POST'])
def makeOrder():
    meal = request.form.get('meal')
    userId = request.form.get('user')
    appOrders[userId] = meal
    return json.dumps("Order Made successfully")

#Allow the user to modify an order they've already made
@app.route('/orders/<orderId>', methods=['PUT'])
def modifyOrder(orderId):
    if len(appOrders) > 0:
        orderID = request.form.get('order_id')
        orderUpdate = request.form.get('order_to_update')
        appOrders[orderID] = appOrders.pop(orderId)
        appOrders.pop(orderID, None) #REMOVE THE PREVIOUS ORDER ENTRY
        appOrders[orderID] = orderUpdate #Add the New Entry
        return json.dumps("Order Updated successfully")
    else:
        return json.dumps("Orders are Empty")

#Allow the Admin return all the Orders users have made
@app.route('/orders', methods=['GET'])
def  getAllOrders():
    return json.dumps(appOrders)


# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)
	# socketio.run(app, host="127.0.0.1", port=int("5556"), debug=True)
  
