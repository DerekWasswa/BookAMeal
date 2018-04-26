# API ENDPOINTS
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO

 # Initialize the Flask application
app = Flask(__name__)
asyncMode = None
socketio  = SocketIO(app, async_mode=asyncMode)

#Initialise the Data structures to be used to Capture Data
appUsers = []
appVendorAdmins = {}
appMeals = {}
appMenu = {}
appOrders = {}

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

#Sign up a user either as a customer or vendor admin
@app.route('/auth/signup', methods=['POST'])
def signUp():
    pass

#authenticate customers or admin
@app.route('/auth/login', methods=['POST'])
def login():
    pass    

#Return all the available meals to the vendor admin
@app.route('/meals', methods=['GET'])
def getAllMeals():
    pass

#Allow the vendor admin to add another meal option
@app.route('/meals', methods=['POST'])
def addMeal():
    pass

#Allow the ADMIN to edit a particular meal option
@app.route('/meals/<mealId>', methods=['PUT'])
def updateAMeal():
    pass

#Allow the admin to delete a particular meal option
@app.route('/meals/<mealId>', methods=['DELETE'])
def deleteAMeal():
    pass

#Allow the admin an operation to the set the menu of the day
@app.route('/menu', methods=['POST'])
def setMenuOfTheDay():
    pass

#Allow the authenticated users to view menu of the day
@app.route('/menu', methods=['GET'])
def getMenuOfTheDay():
    pass

#Allow the authenticated users to make orders from the menu of the day
@app.route('/orders', methods=['POST'])
def makeOrder():
    pass

#Allow the user to modify an order they've already made
@app.route('/orders/<orderId>', methods=['PUT'])
def modifyOrder():
    pass

#Allow the Admin return all the Orders users have made
@app.route('/orders', methods=['GET'])
def  getAllOrders():
    pass


# Run the app :)
if __name__ == '__main__':
	socketio.run(app, host="127.0.0.1", port=int("5556"), debug=True)
  
