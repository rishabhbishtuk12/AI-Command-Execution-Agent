let display = document.getElementById('display');
let currentInput = '';

function appendSymbol(symbol) {
    currentInput += symbol;
    updateDisplay(currentInput);
}

function updateDisplay(value) {
    display.value = value;
}

function clearDisplay() {
    currentInput = '';
    updateDisplay(currentInput);
}

function deleteLast() {
    currentInput = currentInput.slice(0, -1);
    updateDisplay(currentInput);
}

function calculate() {
    try {
        const result = eval(currentInput); // Note: eval() is used for simplicity, not recommended for production code due to security risks.
        updateDisplay(result);
        currentInput = result.toString();
    } catch {
        updateDisplay('Error');
        currentInput = '';
    }
}