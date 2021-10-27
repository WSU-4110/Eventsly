/*--------------------------------------------------*/
/*      CHAIN OF RESPONSIBILITY DESIGN PATTERN      */
/*               FOR LAB ASSIGNMENT 4               */
/*--------------------------------------------------*/

// Type to be tested by the concrete handler implementations (chains)
// Casts generic HTMLElements to HTMLInputElements to use its necessary class methods
class InputElement {
    private element: HTMLInputElement;

    constructor(element: Element) {
        this.element = element as HTMLInputElement; // cast to input element in order to validate properly
    }

    getInputElement(): HTMLInputElement {
        return this.element;
    }
}

// Handler Interface (base class)
interface InputValidator {
    isValid(inputElement: InputElement): boolean;
    setNextValidator(nextInputValidator: InputValidator): void;
}

// Class to build/connect the chain links in the Chain of Responsibility
class InputValidatorChainBuilder {
    private chain: Array<InputValidator>;

    constructor() {
        this.chain = Array<InputValidator>();
    }

    addLink(validator: InputValidator) {
        this.chain.push(validator);
        if (this.chain[this.chain.length- 2] != null) {
            this.chain[this.chain.length - 2].setNextValidator(validator);
        }
    }

    addLinkArray(validators: InputValidator[]) {
        for (let i = 0; i < validators.length; i++) {
            this.addLink(validators[i]);
        }
    }

    getChain(): InputValidator[] {
        return this.chain
    }
}


// Service class which provides simple methods to initiate the Chain of Responsibility for input validation
class InputValidatorService {
    private chain: InputValidatorChainBuilder;

    constructor() {
        this.chain = new InputValidatorChainBuilder();
    }

    addValidator(validator: InputValidator) {
        this.chain.addLink(validator);
    }

    addValidatorArray(validators: InputValidator[]) {
        this.chain.addLinkArray(validators);
    }

    testValidity(): boolean {
        let chain = this.chain.getChain();
        let inputElements = document.getElementsByTagName('INPUT');
        for (let i = 0; i < inputElements.length; i++) {
            let inputElement = new InputElement(inputElements[i]);
            console.log('testing input for field: ' + inputElement.getInputElement().id)

            if (!chain[0].isValid(inputElement)) {
                return false;
            }
        }
        return true;
    }

}

// Concrete Chain Link to validate the '#firstname' input field
class FirstNameValidator implements InputValidator {
    private nextInputValidator: InputValidator;

    isValid(inputElement: InputElement): boolean { // override interface
        let element = inputElement.getInputElement();

        if (element.id == 'firstname') {
            let minlength = element.minLength;
            let maxlength = element.maxLength;
            let span = document.getElementById('firstname-error');

            // Perform validations
            if (element.value.length < minlength) {
                let errorMessage = "First name must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                let errorMessage = "First name must be less than " + maxlength + " characters.";
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
    }

    setNextValidator(nextInputValidator: InputValidator) { // override interface
        this.nextInputValidator = nextInputValidator;
    }
}

// Concrete Chain Link to validate the '#lastname' input field
class LastNameValidator implements InputValidator {
    private nextInputValidator: InputValidator;

    isValid(inputElement: InputElement): boolean { // override interface
        let element = inputElement.getInputElement();

        if (element.id == 'lastname') {
            let minlength = element.minLength;
            let maxlength = element.maxLength;
            let span = document.getElementById('lastname-error');

            // Perform validations
            if (element.value.length < minlength) {
                let errorMessage = "Last name must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                let errorMessage = "Last name must be less than " + maxlength + " characters.";
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
    }

    setNextValidator(nextInputValidator: InputValidator) { // override interface
        this.nextInputValidator = nextInputValidator;
    }
}

// Concrete Chain Link to validate the '#phone' input field
class PhoneValidator implements InputValidator {
    private nextInputValidator: InputValidator;

    isValid(inputElement: InputElement): boolean { // override interface
        let element = inputElement.getInputElement();

        if (element.id == 'phone') {

            // Perform validations
            let minlength = element.minLength;
            let maxlength = element.maxLength;
            let span = document.getElementById('phone-error');

            if (element.value.length < minlength) {
                let errorMessage = "Phone Number must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                let errorMessage = "Phone Number must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (!RegExp('^[0-9]*$').test(element.value)) {
                let errorMessage = "Phone Number not in valid format. Must be 9-10 digits.";
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
    }

    setNextValidator(nextInputValidator: InputValidator) { // override interface
        this.nextInputValidator = nextInputValidator;
    }
}

// Concrete Chain Link to validate the '#email' input field
class EmailValidator implements InputValidator {
    private nextInputValidator: InputValidator;

    isValid(inputElement: InputElement): boolean { // override interface
        let element = inputElement.getInputElement();

        if (element.id == 'email') {

            // Perform validations
            let minlength = element.minLength;
            let maxlength = element.maxLength;
            let span = document.getElementById('email-error');

            if (element.value.length < minlength) {
                let errorMessage = "Email must be more than " + minlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (element.value.length > maxlength) {
                let errorMessage = "Email must be less than " + maxlength + " characters.";
                span.innerHTML = errorMessage;
                return false;
            }
            else if (!RegExp('^[^@]+@[^@]+\.[^@]+$').test(element.value)) {
                let errorMessage = "Email not in valid format: a@b.c";
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
    }

    setNextValidator(nextInputValidator: InputValidator) { // override interface
        this.nextInputValidator = nextInputValidator;
    }
}

// Concrete Chain Link to validate the '#username' input field
class UsernameValidator implements InputValidator {
    private nextInputValidator: InputValidator;

    isValid(inputElement: InputElement): boolean { // override interface
        let element = inputElement.getInputElement();

        if (element.id == 'username') {

            // Perform validations
            let minlength = element.minLength;
            let maxlength = element.maxLength;
            let span = document.getElementById('username-error');

            if (element.value.length < minlength) {
                let message = "Username must be more than " + minlength + " characters.";
                span.innerHTML = message;
                return false;
            }
            else if (element.value.length > maxlength) {
                let message = "Username must be less than " + maxlength + " characters.";
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

            console.log ('testing for field "' + inputElement.getInputElement().id +'" not implemented.')
            return true;
        }
    }

    setNextValidator(nextInputValidator: InputValidator) { // override interface
        this.nextInputValidator = nextInputValidator;
    }
}

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
                initLabelPos(input, label)
                countChars(input, span); // initialize counters to 0
                bindInputEvents(input, span, label);
            }
        }());
    }

/*---------------------------------------*/
/*    IMPLEMENTATION OF CLASS CREATED    */
/*          FOR LAB ASSIGNMENT 4         */
/*---------------------------------------*/
    let inputs = document.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].type.toLocaleLowerCase() == 'submit') {
            submit = inputs[i];
            break;
        }
    }

    let inputValidator = new InputValidatorService()
    inputValidator.addValidator(new FirstNameValidator());
    inputValidator.addValidator(new LastNameValidator());
    inputValidator.addValidator(new PhoneValidator());
    inputValidator.addValidator(new EmailValidator());
    inputValidator.addValidator(new UsernameValidator());

    // run validation test on 'submit' click
    submit.addEventListener('click', function () {
        let valid = inputValidator.testValidity();
        if (valid) {
            console.log('form inputs are valid\n')
        }
        else {
            console.log('form inputs are invalid\n');
        }
    })
}


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