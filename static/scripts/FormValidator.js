/*--------------------------------------------------*/
/*      CHAIN OF RESPONSIBILITY DESIGN PATTERN      */
/*               FOR LAB ASSIGNMENT 4               */
/*--------------------------------------------------*/
// Type to be tested by the concrete handler implementations (chains)
// Casts generic HTMLElements to HTMLInputElements to use its necessary class methods
var InputElement = /** @class */ (function () {
    function InputElement(element) {
        this.element = element; // cast to input element in order to validate properly
    }
    InputElement.prototype.getInputElement = function () {
        return this.element;
    };
    return InputElement;
}());
// Class to build/connect the chain links in the Chain of Responsibility
var InputValidatorChainBuilder = /** @class */ (function () {
    function InputValidatorChainBuilder() {
        this.chain = Array();
    }
    InputValidatorChainBuilder.prototype.addLink = function (validator) {
        this.chain.push(validator);
        if (this.chain[this.chain.length - 2] != null) {
            this.chain[this.chain.length - 2].setNextValidator(validator);
        }
    };
    InputValidatorChainBuilder.prototype.addLinkArray = function (validators) {
        for (var i = 0; i < validators.length; i++) {
            this.addLink(validators[i]);
        }
    };
    InputValidatorChainBuilder.prototype.getChain = function () {
        return this.chain;
    };
    return InputValidatorChainBuilder;
}());
// Service class which provides simple methods to initiate the Chain of Responsibility for input validation
var InputValidatorService = /** @class */ (function () {
    function InputValidatorService() {
        this.chain = new InputValidatorChainBuilder();
    }
    InputValidatorService.prototype.addValidator = function (validator) {
        this.chain.addLink(validator);
    };
    InputValidatorService.prototype.addValidatorArray = function (validators) {
        this.chain.addLinkArray(validators);
    };
    InputValidatorService.prototype.testValidity = function () {
        var chain = this.chain.getChain();
        var inputElements = document.getElementsByTagName('INPUT');
        for (var i = 0; i < inputElements.length; i++) {
            var inputElement = new InputElement(inputElements[i]);
            console.log('testing input for field: ' + inputElement.getInputElement().id);
            if (!chain[0].isValid(inputElement)) {
                return false;
            }
        }
        return true;
    };
    return InputValidatorService;
}());
// Concrete Chain Link to validate the '#firstname' input field
var FirstNameValidator = /** @class */ (function () {
    function FirstNameValidator() {
    }
    FirstNameValidator.prototype.isValid = function (inputElement) {
        var element = inputElement.getInputElement();
        if (element.id == 'firstname') {
            var minlength = element.minLength;
            var maxlength = element.maxLength;
            var span = document.getElementById('firstname-error');
            // Perform validations
            if (element.value.length < minlength) {
                var errorMessage = "First name must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                var errorMessage = "First name must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            // Log in the developer debug console that the 'firstname' field is valid
            console.log('firstname valid\n');
            span.innerHTML = '';
            return true;
        }
        else {
            // Pass the inputElement to the next input validator in the chain to see if it should be validated there
            if (this.nextInputValidator != null) {
                return this.nextInputValidator.isValid(inputElement);
            }
            return true;
        }
    };
    FirstNameValidator.prototype.setNextValidator = function (nextInputValidator) {
        this.nextInputValidator = nextInputValidator;
    };
    return FirstNameValidator;
}());
// Concrete Chain Link to validate the '#lastname' input field
var LastNameValidator = /** @class */ (function () {
    function LastNameValidator() {
    }
    LastNameValidator.prototype.isValid = function (inputElement) {
        var element = inputElement.getInputElement();
        if (element.id == 'lastname') {
            var minlength = element.minLength;
            var maxlength = element.maxLength;
            var span = document.getElementById('lastname-error');
            // Perform validations
            if (element.value.length < minlength) {
                var errorMessage = "Last name must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                var errorMessage = "Last name must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            // Log in the developer debug console that the 'firstname' field is valid
            console.log('lastname valid\n');
            span.innerHTML = '';
            return true;
        }
        else {
            // Pass the inputElement to the next input validator in the chain to see if it should be validated there
            if (this.nextInputValidator != null) {
                return this.nextInputValidator.isValid(inputElement);
            }
            return true;
        }
    };
    LastNameValidator.prototype.setNextValidator = function (nextInputValidator) {
        this.nextInputValidator = nextInputValidator;
    };
    return LastNameValidator;
}());
// Concrete Chain Link to validate the '#phone' input field
var PhoneValidator = /** @class */ (function () {
    function PhoneValidator() {
    }
    PhoneValidator.prototype.isValid = function (inputElement) {
        var element = inputElement.getInputElement();
        if (element.id == 'phone') {
            // Perform validations
            var minlength = element.minLength;
            var maxlength = element.maxLength;
            var span = document.getElementById('phone-error');
            if (element.value.length < minlength) {
                var errorMessage = "Phone Number must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                var errorMessage = "Phone Number must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (!RegExp('^[0-9]*$').test(element.value)) {
                var errorMessage = "Phone Number not in valid format. Must be 9-10 digits.";
                span.innerHTML = errorMessage;
                return false;
            }
            // Log in the developer debug console that the 'firstname' field is valid
            console.log('phone valid\n');
            span.innerHTML = '';
            return true;
        }
        else {
            // Pass the inputElement to the next input validator in the chain to see if it should be validated there
            if (this.nextInputValidator != null) {
                return this.nextInputValidator.isValid(inputElement);
            }
            return true;
        }
    };
    PhoneValidator.prototype.setNextValidator = function (nextInputValidator) {
        this.nextInputValidator = nextInputValidator;
    };
    return PhoneValidator;
}());
// Concrete Chain Link to validate the '#email' input field
var EmailValidator = /** @class */ (function () {
    function EmailValidator() {
    }
    EmailValidator.prototype.isValid = function (inputElement) {
        var element = inputElement.getInputElement();
        if (element.id == 'email') {
            // Perform validations
            var minlength = element.minLength;
            var maxlength = element.maxLength;
            var span = document.getElementById('email-error');
            if (element.value.length < minlength) {
                var errorMessage = "Email must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                var errorMessage = "Email must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (!RegExp('^[^@]+@[^@]+\.[^@]+$').test(element.value)) {
                var errorMessage = "Email not in valid format: a@b.c";
                span.innerHTML = errorMessage;
                return false;
            }
            // Log in the developer debug console that the 'firstname' field is valid
            console.log('email valid\n');
            span.innerHTML = '';
            return true;
        }
        else {
            // Pass the inputElement to the next input validator in the chain to see if it should be validated there
            if (this.nextInputValidator != null) {
                return this.nextInputValidator.isValid(inputElement);
            }
            return true;
        }
    };
    EmailValidator.prototype.setNextValidator = function (nextInputValidator) {
        this.nextInputValidator = nextInputValidator;
    };
    return EmailValidator;
}());
// Concrete Chain Link to validate the '#username' input field
var UsernameValidator = /** @class */ (function () {
    function UsernameValidator() {
    }
    UsernameValidator.prototype.isValid = function (inputElement) {
        var element = inputElement.getInputElement();
        if (element.id == 'username') {
            // Perform validations
            var minlength = element.minLength;
            var maxlength = element.maxLength;
            var span = document.getElementById('username-error');
            if (element.value.length < minlength) {
                var message = "Username must be more than " + minlength + " characters.";
                span.innerHTML = message;
                return false;
            }
            else if (element.value.length > maxlength) {
                var message = "Username must be less than " + maxlength + " characters.";
                span.innerHTML = message;
                return false;
            }
            // Log in the developer debug console that the 'username' field is valid
            console.log('username valid\n');
            span.innerHTML = '';
            return true;
        }
        else {
            // Pass the inputElement to the next input validator in the chain to see if it should be validated there
            if (this.nextInputValidator != null) {
                return this.nextInputValidator.isValid(inputElement);
            }
            console.log('testing for field "' + inputElement.getInputElement().id + '" not implemented.');
            return true;
        }
    };
    UsernameValidator.prototype.setNextValidator = function (nextInputValidator) {
        this.nextInputValidator = nextInputValidator;
    };
    return UsernameValidator;
}());
/*----------------*/
/*      NOTE      */
/*----------------*/
// PASSWORD VALIDATION HAPPENS ON BACKEND OF APPLICATION, NOT NECESSARY TO REIMPLEMENT ON FRONT END
/*--------------------------------------------------*/
/*    CODE PRIOR TO FORMVALIDATOR IMPLEMENTATION    */
/*               FOR LAB ASSIGNMENT 4               */
/*--------------------------------------------------*/
var formItems = document.getElementsByClassName('form-item');
var submit = null;
window.onload = function () {
    for (var i = 0; i < formItems.length; i++) {
        (function () {
            var label = formItems[i].getElementsByTagName('LABEL')[0];
            var input = formItems[i].getElementsByClassName('form-input')[0];
            var span = formItems[i].getElementsByClassName('counter')[0];
            if (label && input) {
                initLabelPos(input, label);
                countChars(input, span); // initialize counters to 0
                bindInputEvents(input, span, label);
            }
        }());
    }
    /*---------------------------------------*/
    /*    IMPLEMENTATION OF CLASS CREATED    */
    /*          FOR LAB ASSIGNMENT 4         */
    /*---------------------------------------*/
    var inputs = document.getElementsByTagName('input');
    for (var i_1 = 0; i_1 < inputs.length; i_1++) {
        if (inputs[i_1].type.toLocaleLowerCase() == 'submit') {
            submit = inputs[i_1];
            break;
        }
    }
    var inputValidator = new InputValidatorService();
    inputValidator.addValidator(new FirstNameValidator());
    inputValidator.addValidator(new LastNameValidator());
    inputValidator.addValidator(new PhoneValidator());
    inputValidator.addValidator(new EmailValidator());
    inputValidator.addValidator(new UsernameValidator());
    // run validation test on 'submit' click
    submit.addEventListener('click', function () {
        var valid = inputValidator.testValidity();
        if (valid) {
            console.log('form inputs are valid\n');
        }
        else {
            console.log('form inputs are invalid\n');
        }
    });
};
/*--------------------------------------------------*/
/*    CODE PRIOR TO FORMVALIDATOR IMPLEMENTATION    */
/*               FOR LAB ASSIGNMENT 4               */
/*--------------------------------------------------*/
function bindInputEvents(input, span, label) {
    input.addEventListener('focusin', function () { moveLabelPos(label); });
    input.addEventListener('focusout', function () { defaultLabelPos(input, label); });
    input.addEventListener('input', function () { countChars(input, span); });
}
/* count the number of chars in the given input field */
function countChars(input, span) {
    span.innerHTML = input.value.length + '/' + input.getAttribute('maxlength');
}
/* move the labels outside of the inputs if page refreshes on submit with text in inputs */
function initLabelPos(input, label) {
    if (input.value.length > 0) {
        label.classList.add('move-label');
    }
}
/* move the labels outside of the inputs on focus */
function moveLabelPos(label) {
    if (!label.classList.contains('move-label')) {
        label.classList.add('move-label');
    }
}
/* move the labels to their default position inside of inputs */
function defaultLabelPos(input, label) {
    if (input.value.length == 0 && label.classList.contains('move-label')) {
        label.classList.remove('move-label');
    }
}
