
// AUTHENTICATION EVENT HANDLERS

function signIn() {
    alert("Yay!");
}

function redirectSignUp(){
	var signin_block = document.getElementById("signin_block");
	var signup_block = document.getElementById("signup_block");
	
	signup_block.classList.remove("block_off_screen");
	signin_block.classList.toggle("block_off_screen");
}

function signUp(){
	alert("Yay!");
}

function redirectSignIn(){
	var signin_block = document.getElementById("signin_block");
	var signup_block = document.getElementById("signup_block");
	
	signup_block.classList.toggle("block_off_screen");
	signin_block.classList.remove("block_off_screen");
}


// CUSTOMER EVENT HANDLERS
function menuOfTheDay(){
	var day_menu_block = document.getElementById("day_menu_block");
	var order_history_block = document.getElementById("order_history_block");

	order_history_block.classList.toggle("block_off_screen");
	day_menu_block.classList.remove("block_off_screen");

}

function customerOrderHistory(){
	var day_menu_block = document.getElementById("day_menu_block");
	var order_history_block = document.getElementById("order_history_block");

	day_menu_block.classList.toggle("block_off_screen");
	order_history_block.classList.remove("block_off_screen");
}





// ADMIN EVENT HANDLERS
function meals(){
	var add_a_meal_block = document.getElementById("add_meal_item_block");
	var manage_meals_block = document.getElementById("manage_meals_block");
	var menu_of_the_day_block = document.getElementById("menu_of_the_day_block");
	var user_orders_block = document.getElementById("user_orders_block");
	var orders_history_block = document.getElementById("orders_history_block");

	manage_meals_block.classList.remove("block_off_screen");

	menu_of_the_day_block.classList.remove("block_off_screen");
	user_orders_block.classList.remove("block_off_screen");
	orders_history_block.classList.remove("block_off_screen");
	add_a_meal_block.classList.remove("block_off_screen");

	menu_of_the_day_block.classList.toggle("block_off_screen");
	user_orders_block.classList.toggle("block_off_screen");
	orders_history_block.classList.toggle("block_off_screen");
	add_a_meal_block.classList.toggle("block_off_screen");
}

function menuOfTheDay(){
	var add_a_meal_block = document.getElementById("add_meal_item_block");
	var manage_meals_block = document.getElementById("manage_meals_block");
	var menu_of_the_day_block = document.getElementById("menu_of_the_day_block");
	var user_orders_block = document.getElementById("user_orders_block");
	var orders_history_block = document.getElementById("orders_history_block");

	menu_of_the_day_block.classList.toggle("block_off_screen");
	menu_of_the_day_block.classList.remove("block_off_screen");

	manage_meals_block.classList.remove("block_off_screen");
	user_orders_block.classList.remove("block_off_screen");
	orders_history_block.classList.remove("block_off_screen");
	add_a_meal_block.classList.remove("block_off_screen");

	manage_meals_block.classList.toggle("block_off_screen");
	user_orders_block.classList.toggle("block_off_screen");
	orders_history_block.classList.toggle("block_off_screen");
	add_a_meal_block.classList.toggle("block_off_screen");
}

function orders(){
	var add_a_meal_block = document.getElementById("add_meal_item_block");
	var manage_meals_block = document.getElementById("manage_meals_block");
	var menu_of_the_day_block = document.getElementById("menu_of_the_day_block");
	var user_orders_block = document.getElementById("user_orders_block");
	var orders_history_block = document.getElementById("orders_history_block");


	user_orders_block.classList.remove("block_off_screen");

	manage_meals_block.classList.remove("block_off_screen");
	menu_of_the_day_block.classList.remove("block_off_screen");
	orders_history_block.classList.remove("block_off_screen");
	add_a_meal_block.classList.remove("block_off_screen");

	manage_meals_block.classList.toggle("block_off_screen");
	menu_of_the_day_block.classList.toggle("block_off_screen");
	orders_history_block.classList.toggle("block_off_screen");
	add_a_meal_block.classList.toggle("block_off_screen");
}

function orderHistory(){
	var add_a_meal_block = document.getElementById("add_meal_item_block");
	var manage_meals_block = document.getElementById("manage_meals_block");
	var menu_of_the_day_block = document.getElementById("menu_of_the_day_block");
	var user_orders_block = document.getElementById("user_orders_block");
	var orders_history_block = document.getElementById("orders_history_block");

	orders_history_block.classList.remove("block_off_screen");

	manage_meals_block.classList.remove("block_off_screen");
	menu_of_the_day_block.classList.remove("block_off_screen");
	user_orders_block.classList.remove("block_off_screen");
	add_a_meal_block.classList.remove("block_off_screen");

	manage_meals_block.classList.toggle("block_off_screen");
	menu_of_the_day_block.classList.toggle("block_off_screen");
	user_orders_block.classList.toggle("block_off_screen");
	add_a_meal_block.classList.toggle("block_off_screen");
}

function addAMeal(){

	var add_a_meal_block = document.getElementById("add_meal_item_block");
	var manage_meals_block = document.getElementById("manage_meals_block");
	var menu_of_the_day_block = document.getElementById("menu_of_the_day_block");
	var user_orders_block = document.getElementById("user_orders_block");
	var orders_history_block = document.getElementById("orders_history_block");

	add_a_meal_block.classList.remove("block_off_screen");

	orders_history_block.classList.remove("block_off_screen");
	manage_meals_block.classList.remove("block_off_screen");
	menu_of_the_day_block.classList.remove("block_off_screen");
	user_orders_block.classList.remove("block_off_screen");

	orders_history_block.classList.toggle("block_off_screen");
	manage_meals_block.classList.toggle("block_off_screen");
	menu_of_the_day_block.classList.toggle("block_off_screen");
	user_orders_block.classList.toggle("block_off_screen");

}

