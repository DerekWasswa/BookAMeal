
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
	
}
