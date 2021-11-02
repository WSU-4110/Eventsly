// Service class which provides methods to initiate form validation given validators
var InputValidatorService = /** @class */ (function () {
    class InputValidatorService {
        constructor() {
            this.chain = Array();
        }

        addValidatorArray(validators) {
            for (var i = 0; i < validators.length; i++) {
                this.chain.push(validators[i]);
            }
        }

        testValidity() {
            var invalidInputs = [];
            var validInputs = [];
            var results = [validInputs, invalidInputs];
            for (var i = 0; i < this.chain.length; i++) {
                if (this.chain[i].isValid()) {
                    validInputs.push(this.chain[i].input);
                }
                else {
                    invalidInputs.push(this.chain[i].input);
                }
            }
            return results;
        }
    }
    return InputValidatorService;
}());

var FirstNameValidator = /** @class */ (function () {
    class FirstNameValidator {
        constructor(input) {
            this.input = input;
        }

        isValid() {
            var minlength = this.input.minLength;
            var maxlength = this.input.maxLength;
            // var span = document.getElementById('firstname-error');

            // Perform validations
            if (this.input.value.length < minlength) {
                // var errorMessage = "First name must be more than " + minlength + " characters.";
                // span.innerHTML = errorMessage;
                return false;
            }
            else if (this.input.value.length > maxlength) {
                // var errorMessage = "First name must be less than " + maxlength + " characters.";
                // span.innerHTML = errorMessage;
                return false;
            }
            // Log in the developer debug console that the 'firstname' field is valid
            // console.log('firstname valid\n');
            // span.innerHTML = '';
            return true;
        }

        getInput() {
            return this.input;
        }
    }
    return FirstNameValidator;
}());

// Concrete Chain Link to validate the '#lastname' input field
var LastNameValidator = /** @class */ (function () {
    class LastNameValidator {
        constructor(input) {
            this.input = input;
        }

        isValid(input) {
            var minlength = this.input.minLength;
            var maxlength = this.input.maxLength;
            // var span = document.getElementById('lastname-error');

            // Perform validations
            if (this.input.value.length < minlength) {
                // var errorMessage = "Last name must be more than " + minlength + " characters.";
                // span.innerHTML = errorMessage;
                return false;
            }
            else if (this.input.value.length > maxlength) {
                // var errorMessage = "Last name must be less than " + maxlength + " characters.";
                // span.innerHTML = errorMessage;
                return false;
            }

            // Log in the developer debug console that the 'firstname' field is valid
            // console.log('lastname valid\n');
            // span.innerHTML = '';
            return true;
        }

        getInput() {
            return this.input;
        }
    }
    return LastNameValidator;
}());

// Concrete Chain Link to validate the '#phone' input field
// var PhoneValidator = /** @class */ (function () {
//     class PhoneValidator {
//         constructor() {
//         }
//         isValid(input) {

//             if (input.id == 'phone') {
//                 // Perform validations
//                 var minlength = input.minLength;
//                 var maxlength = input.maxLength;
//                 var span = document.getElementById('phone-error');
//                 if (input.value.length < minlength) {
//                     var errorMessage = "Phone Number must be more than " + minlength + " characters.";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 else if (input.value.length > maxlength) {
//                     var errorMessage = "Phone Number must be less than " + maxlength + " characters.";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 else if (!RegExp('^[0-9]*$').test(input.value)) {
//                     var errorMessage = "Phone Number not in valid format. Must be 9-10 digits.";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 // Log in the developer debug console that the 'firstname' field is valid
//                 console.log('phone valid\n');
//                 span.innerHTML = '';
//                 return true;
//             }
//             else {
//                 // Pass the input to the next input validator in the chain to see if it should be validated there
//                 if (this.nextInputValidator != null) {
//                     return this.nextInputValidator.isValid(input);
//                 }
//                 return true;
//             }
//         }
//         setNextValidator(nextInputValidator) {
//             this.nextInputValidator = nextInputValidator;
//         }
//     }
//     return PhoneValidator;
// }());

// Concrete Chain Link to validate the '#email' input field
// var EmailValidator = /** @class */ (function () {
//     class EmailValidator {
//         constructor() {
//         }
//         isValid(input) {

//             if (input.id == 'email') {
//                 // Perform validations
//                 var minlength = input.minLength;
//                 var maxlength = input.maxLength;
//                 var span = document.getElementById('email-error');
//                 if (input.value.length < minlength) {
//                     var errorMessage = "Email must be more than " + minlength + " characters.";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 else if (input.value.length > maxlength) {
//                     var errorMessage = "Email must be less than " + maxlength + " characters.";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 else if (!RegExp('^[^@]+@[^@]+\.[^@]+$').test(input.value)) {
//                     var errorMessage = "Email not in valid format: a@b.c";
//                     span.innerHTML = errorMessage;
//                     return false;
//                 }
//                 // Log in the developer debug console that the 'firstname' field is valid
//                 console.log('email valid\n');
//                 span.innerHTML = '';
//                 return true;
//             }
//             else {
//                 // Pass the input to the next input validator in the chain to see if it should be validated there
//                 if (this.nextInputValidator != null) {
//                     return this.nextInputValidator.isValid(input);
//                 }
//                 return true;
//             }
//         }
//         setNextValidator(nextInputValidator) {
//             this.nextInputValidator = nextInputValidator;
//         }
//     }
//     return EmailValidator;
// }());

// Concrete Chain Link to validate the '#username' input field
// var UsernameValidator = /** @class */ (function () {
//     class UsernameValidator {
//         constructor() {
//         }
//         isValid(input) {

//             if (input.id == 'username') {
//                 // Perform validations
//                 var minlength = input.minLength;
//                 var maxlength = input.maxLength;
//                 var span = document.getElementById('username-error');
//                 if (input.value.length < minlength) {
//                     var message = "Username must be more than " + minlength + " characters.";
//                     span.innerHTML = message;
//                     return false;
//                 }
//                 else if (input.value.length > maxlength) {
//                     var message = "Username must be less than " + maxlength + " characters.";
//                     span.innerHTML = message;
//                     return false;
//                 }
//                 // Log in the developer debug console that the 'username' field is valid
//                 console.log('username valid\n');
//                 span.innerHTML = '';
//                 return true;
//             }
//             else {
//                 // Pass the input to the next input validator in the chain to see if it should be validated there
//                 if (this.nextInputValidator != null) {
//                     return this.nextInputValidator.isValid(input);
//                 }
//                 console.log('testing for field "' + input.getelement().id + '" not implemented.');
//                 return true;
//             }
//         }
//         setNextValidator(nextInputValidator) {
//             this.nextInputValidator = nextInputValidator;
//         }
//     }
//     return UsernameValidator;
// }());