window.onload = function () {
    var formItems = document.getElementsByClassName('form-item');
    var textInputs = [];
    var submit = null;

    // set up form label positions and counters
    for (let i = 0; i < formItems.length; i++) {
        {
            let label = formItems[i].getElementsByTagName('LABEL')[0];
            let input = formItems[i].getElementsByTagName('INPUT')[0];
            let span = formItems[i].getElementsByClassName('counter')[0];
            if (label && input) {
                initLabelPos(input, label);
                countChars(input, span); // initialize counters to 0
                bindInputEvents(input, span, label);
                textInputs.push(input);
            }
            else if (input.getAttribute('type') == 'submit') {
                submit = input;
            }
        };
    }

    // front-end form validation
    var signup = document.getElementById('signup');
    submit.classList.add('disable-submit');
    submit.disabled = true;
    if (signup) {
        var formValidator = new InputValidatorService();
        formValidator.addValidatorArray([
            new FirstNameValidator(document.getElementById('firstname')),
            new LastNameValidator(document.getElementById('lastname'))
        ]);
    }
    signup.addEventListener('keyup', function () {
        let results = formValidator.testValidity();
        let validInputs = results[0];
        let invalidInputs = results[1];
        if (validInputs.length > 0) {
            for (let i = 0; i < validInputs.length; i++) {
                // do something - outline red?
            }
        }
        if (invalidInputs.length > 0) {
            for (let i = 0; i < invalidInputs.length; i++) {
                // do something - outline green?
            }
            if (!submit.classList.contains('disable-submit')) {
                submit.classList.add('disable-submit');
                submit.disabled = true;
            }
        }
        else {
            submit.classList.remove('disable-submit');
            submit.disabled = false;
        }

    });
}

function bindInputEvents(input, span, label) {
    input.addEventListener('focusin', function () { moveLabelPos(label); });
    input.addEventListener('focusout', function () { defaultLabelPos(input, label); });
    input.addEventListener('input', function () { countChars(input, span); });
}

/* count the number of chars in the given input field */
function countChars(input, span) {
    span.innerHTML = input.value.length + '/' + input.getAttribute('maxlength');
}

/* move the labels outside of the inputs on focus or when text in input */
function initLabelPos(input, label) {
    if (input.value.length > 0) {
        label.classList.add('move-label');
    }
}

function moveLabelPos(label) {
    if (!label.classList.contains('move-label')) {
        label.classList.add('move-label');
    }
}

function defaultLabelPos(input, label) {
    if (input.value.length == 0 && label.classList.contains('move-label')) {
        label.classList.remove('move-label');
    }
}