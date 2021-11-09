window.onload = function () {
    var formItems = document.getElementsByClassName('content-box');
    var submit = null;
    var formValidator = new FormValidator();

    for (let i = 0; i < formItems.length; i++) {
        {
            let label = formItems[i].getElementsByTagName('LABEL')[0];
            let input = formItems[i].getElementsByTagName('INPUT')[0];
            let span = formItems[i].getElementsByClassName('counter')[0];
            
            if (label && input) {
                // set up label positions and counters
                initLabelPos(input, label);
                bindInputEvents(input, label);

                if (span) {
                    countChars(input, span); // initialize counters to 0
                    input.addEventListener('input', function () { countChars(input, span); });
                }

                // add a validator for this input
                formValidator.addValidator(input);
            }
            else if (input.getAttribute('type') == 'submit') {
                submit = input;
            }
        };
    }

    // check if signup form exists on page
    var signup = document.getElementById('signup');
    if (signup) {
        submit.classList.add('disable-submit');
        submit.disabled = true;
        signup.addEventListener('keyup', function () {
            let results = formValidator.testValidity();
            let validInputs = results[0];
            let invalidInputs = results[1];
            if (validInputs.length > 0) {
                for (let i = 0; i < validInputs.length; i++) {
                    if ((validInputs[i]).value.length > 0) {
                        validInputs[i].classList.remove('invalid-field');
                        validInputs[i].classList.add('valid-field');
                    }
                    else {
                        validInputs[i].classList.remove('valid-field')
                        validInputs[i].classList.remove('invalid-field');
                    }
                }
            }
            if (invalidInputs.length > 0) {
                for (let i = 0; i < invalidInputs.length; i++) {
                    if ((invalidInputs[i]).value.length > 0) {
                        invalidInputs[i].classList.remove('valid-field');
                        invalidInputs[i].classList.add('invalid-field');
                    }
                    else {
                        invalidInputs[i].classList.remove('valid-field')
                        invalidInputs[i].classList.remove('invalid-field');
                    }
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

}

function bindInputEvents(input, label) {
    input.addEventListener('focusin', function () { moveLabelPos(label); });
    input.addEventListener('focusout', function () { defaultLabelPos(input, label); });
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