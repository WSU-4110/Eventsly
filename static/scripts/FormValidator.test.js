/**
 * @jest-environment jsdom
 */

const { TestWatcher } = require('@jest/core');
const FormValidator = require('./FormValidator');

// TESTING CLASS - VALIDATOR
describe('Validator tests', () => {
    test('Instantiating a Validator object with an input element should enable you to get that same input element from that Validator object', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.getInput()).toBe(testElement);
    })

    test('Sending the Validator an input with value length < minlength should return false', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.minLength = 2;
        testElement.value = 'a';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validMinLength(validator.validMinLength())).toBe(false);
    });

    test('Sending the Validator an input with value length > minlength should return true', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.minLength = 1;
        testElement.value = 'aa';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validMinLength(validator.validMinLength())).toBe(true);
    });

    test('Sending the Validator an input with value length > maxlength should return false', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.maxLength = 1;
        testElement.value = 'aa';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validMaxLength(validator.validMaxLength())).toBe(false);
    });

    test('Sending the Validator an input with value length < maxlength should return true', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.maxlength = 2;
        testElement.value = 'a';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validMaxLength(validator.validMaxLength())).toBe(true);
    });

    test('Sending the Validator an input with a value that does not meet the pattern criteria should return false', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.pattern = "[A-Z]{3}"; // must be 3 capital letters
        testElement.value = 'aaa';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validPattern()).toBe(false);
    });

    test('Sending the Validator a string that does meet the pattern criteria should return true', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.pattern = '[A-Z]{3}'; // must be 3 capital letters 
        testElement.value = 'AAA';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.validPattern()).toBe(true);
    });

    test('Sending the Validator an input element with a value that meets minlength, maxlength, and pattern requirements should return true', () => {
        let testElement = document.createElement('input');
        testElement.type = 'text';
        testElement.minLength = 1
        testElement.maxLength = 9;
        testElement.pattern = '[A-Z]{3}';
        testElement.value = 'AAA';

        let validator = new FormValidator.Validator(testElement);

        expect(validator.isValid()).toBe(true);
    });
});

// TESTING CLASS - FORMVALIDATOR
describe('FormValidator tests', () => {
    test('Adding inputs to the FormValidator should results in Validator objects for those inputs being added to the FormValidator chain', () => {
        let textElement = document.createElement('input');
        let passwordElement = document.createElement('input');
        let buttonElement = document.createElement('input');
        textElement.type = 'text';
        passwordElement.type = 'password';
        buttonElement.type = 'button';

        let expected = [new FormValidator.Validator(textElement), new FormValidator.Validator(passwordElement), new FormValidator.Validator(buttonElement)];

        let formValidator = new FormValidator.FormValidator();
        formValidator.addValidator(textElement);
        formValidator.addValidator(passwordElement);
        formValidator.addValidator(buttonElement);

        expect(formValidator.getValidatorArray()).toEqual(expect.arrayContaining(expected));
    });

    test('Testing 2 valid elements and 1 invalid element should result in an array of 2 arrays where the first array has the 2 valid elements and the 2nd array has the 1 invalid element', () => {
        let validElementOne = document.createElement('input');
        let validElementTwo = document.createElement('input');
        let invalidElement = document.createElement('input');
        
        validElementOne.type = 'text';
        validElementOne.minLength = 1;
        validElementOne.maxLength = 4;
        validElementOne.pattern = '[A-Z]{3}';
        validElementOne.value = 'AAA';
        
        validElementTwo.type = 'text';
        validElementTwo.minLength = 2;
        validElementTwo.maxLength = 5;
        validElementTwo.pattern = '[A-Z]{3}';
        validElementTwo.value = 'AAA';
        
        invalidElement.type = 'text';
        invalidElement.minLength = 3;
        invalidElement.maxLength = 3;
        invalidElement.pattern = '[A-Z]{3}';
        invalidElement.value = 'a';

        let expected = [[validElementOne, validElementTwo], [invalidElement]];

        let formValidator = new FormValidator.FormValidator();
        formValidator.addValidator(validElementOne);
        formValidator.addValidator(validElementTwo);
        formValidator.addValidator(invalidElement);

        expect(formValidator.testValidity()).toEqual(expect.arrayContaining(expected));
    });
})