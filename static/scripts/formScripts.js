var inputs = document.getElementsByTagName('input');
var labels = document.getElementsByTagName('label');
var formItems = document.getElementsByClassName('form-item');

window.onload = function () {
    for (var i = 0; i < formItems.length; i++) {
        (function () {
            var label = formItems[i].getElementsByTagName('LABEL')[0];
            var input = formItems[i].getElementsByClassName('form-input')[0];
            var span = formItems[i].getElementsByClassName('counter')[0];
            if (label && input) {
                console.log(label + ' ' + input.id + ' ' + span);
                initLabelPos(input, label)
                countChars(input, span); // initialize counters to 0
                bindInputEvents(input, span, label);
            }
        }());
    }
}

function bindInputEvents(input, span, label) {
    input.addEventListener('focusout', function () { isValid(input); });
    input.addEventListener('focusin', function () { moveLabelPos(label); });
    input.addEventListener('focusout', function () { defaultLabelPos(input, label); });
    input.addEventListener('input', function () { countChars(input, span); });
}

/* count the number of chars in the given input field */
function countChars(input, span) {
    span.innerHTML = input.value.length + '/' + input.getAttribute('maxlength');
}

/* check if the length in an input text field is between its constraints */
function isValid(input) {
    if (input.value.length >= input.getAttribute('minlength') && input.value.length <= input.getAttribute('maxlength')) {
        input.classList.remove('invalid');
    }
    else {
        input.classList.add('invalid');
    }
}

/* move the labels outside of the inputs on focus */
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