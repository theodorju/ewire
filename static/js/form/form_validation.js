var ERROR_COLOR = "red";
var ERROR_WIDTH = "2px";

/**
 * 
 * @param {String} email Contact form email address
 * Validate if the addressed enter by the user is valid 
 */
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

/**
 * 
 * @param {object} element Contact form input element
 * Return default border color and border width to use when resetting the form 
 */
function getDefaultStyle(element) {
	computedStyle = window.getComputedStyle(element);
	borderColor = computedStyle.borderColor;
	borderWidth = computedStyle.borderWidth;
	color = computedStyle.color;

	return [borderColor, borderWidth, color]

}

/**
 * 
 * @param {object} element Contact form element
 * @param {String} message Error message
 * If validation of input element fails, set a red error message
 * and increase the border width of the element
 */
function setInputError(element, message) {
	element.placeholder = message;
	element.style.borderColor = ERROR_COLOR;
	element.style.borderWidth = ERROR_WIDTH;
}

function setInvalidEmail(element) {
	element.style.color = ERROR_COLOR;
	element.style.borderColor = ERROR_COLOR;
	element.style.borderWidth = ERROR_WIDTH;

	emailMessage = document.querySelector("#emailError");
	emailMessage.className = "invalidEmail-error";

}

// Get form and form input elements
const form = document.getElementById("contactForm");
const username = form.querySelector("#username");
const email = form.querySelector("#email");
const message = form.querySelector("#message");

// Get default color and width for form elements
const [usernameBorderColor, usernameBorderWidth, usernameColor] = getDefaultStyle(username);

// Add event lintener on the form and validatate each of the inputs
form.addEventListener('submit', e => {
	e.preventDefault();
	
	let isInvalid = false;

	// If no username is set
	if(username.value.trim() === "") {
		setInputError(username, "Name cannot be blank");
		isInvalid = true;
	}

	// If no email is set
	emailValue = email.value.trim();
	if (emailValue === "") {
		setInputError(email, "Email cannot be blank");
		isInvalid = true;
	} else if (!validateEmail(emailValue)) {
		setInvalidEmail(email);
		isInvalid = true;
	}

	// If no message is set
	if (message.value.trim() === ""){
		setInputError(message, "Message cannot be blank");
		isInvalid = true;
	}

	// Submit the form if validation was successful
	if (!isInvalid) {
		form.submit();
	}

});

// Add event listener on document click to reset input arrays
// if the input is not validated correctly
document.addEventListener(`click`, resetForm);

function resetForm(event){
	if (!event.target.closest(`#username #email #message`)){

		username.placeholder = "Your name *";
		username.style.borderColor = usernameBorderColor;
		username.style.borderWidht = usernameBorderWidth;

		email.placeholder = "Your email *";
		email.style.borderColor = usernameBorderColor;
		email.style.borderWidht = usernameBorderWidth;
		email.style.color = usernameColor;
		emailMessage = document.querySelector("#emailError");
		emailMessage.className = "invalidEmail";

		message.placeholder = "Your message *";
		message.style.borderColor = usernameBorderColor;
		message.style.borderWidht = usernameBorderWidth;
	}
}
