// Service class which provides methods to initiate form validation given validators
var FormValidator = /** @class */ (function () {
    class FormValidator {
        constructor() {
            this.chain = Array();
        }

        addValidator(input) {
            var validator = new Validator(input);
            this.chain.push(validator)
        }

        getValidatorArray() {
            return this.chain;
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

    return FormValidator;
}());

var Validator = /** @class */ (function () {
    class Validator {
        constructor(input) {
            this.input = input;
        }

        getInput() {
            return this.input;
        }

        isValid() {
            return (this.validMinLength() && this.validMaxLength() && this.validPattern());
        }

        validMinLength() {
            let minLength = this.input.minLength;
            if (minLength > 0) {
                return (this.input.value.length > minLength);
            }
            return true;
        }

        validMaxLength() {
            let maxLength = this.input.maxLength;
            if (maxLength > 0) {
                return (this.input.value.length < maxLength);
            }
            return true;
        }

        validPattern() {
            let pattern = this.input.pattern;
            if (pattern) {
                let regex = new RegExp(pattern);
                return regex.test(this.input.value);
            }
            return true;
        }
    }

    return Validator;
}());

module.exports = { FormValidator: FormValidator, Validator: Validator }