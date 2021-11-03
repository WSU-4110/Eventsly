// Service class which provides methods to initiate form validation given validators
var InputValidatorService = /** @class */ (function () {
    class InputValidatorService {
        constructor() {
            this.chain = Array();
        }

        addValidator(input) {
            var validator = new Validator(input);
            this.chain.push(validator)
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

var Validator = /** @class */ (function () {
    class Validator {
        constructor(input) {
            this.input = input;
        }

        isValid() {
            var minLength = this.input.minLength;
            var maxLength = this.input.maxLength;
            var pattern = this.input.pattern;

            if (minLength > 0) {
                if (this.input.value.length < minLength) return false;
            }

            if (maxLength > 0) {
                if (this.input.value.length > maxLength) return false;
            }

            if (pattern) {
                var regex = new RegExp(pattern);
                if (!regex.test(this.input.value)) return false;
            }

            return true;
        }
    }

    return Validator;
}());