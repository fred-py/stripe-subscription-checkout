// Imported in _debug.html when Flask debug is set to True


//Resource: https://realpython.com/flask-javascript-frontend-for-rest-api/#sprinkle-in-some-javascript

// First AJAX function (Asynchronous JS & XML)
// Makes GET HTTP request with API when getData is called
function getData(endpoint, callback) {  // defines function with params endpoint & callback
    // creates new XMLHttpRequest obj used to make requests
    const request = new XMLHttpRequest();
    // Binds the .onreadystateChange() event to request
    // It triggers when .readyState() is changed by sending the request request.send()
    request.onreadystatechange = () => {
        // Check for the value of 4
        if (request.readyState === 4) {
            // Calls the callback func with the response
            callback(request.response);
        }
    };
    // Initialises request with a GET HTTP action and provided endpoint url
    request.open("GET", endpoint);
    // Sends the request and triggers .onreadystatechange() when done
    request.send();
}


class DebugForm {
    constructor() {
        this.debugCard = document.querySelector(".debug-card");
        this.form = this.debugCard.querySelector(".debug-form");
        this.clearButton = this.form.querySelector("button[data-action='clear']");
        this.clearButton.addEventListener(
            "click",
            // Call to .bind() allows event handler to call
            // the 'this' keyword as if it were an instance of the DebugForm
            // Binding allows the handler to have access to all the properties
            // defined in the constructor, like this.debugCard  
            this.handleClearClick.bind(this) 
        );
        // Triggers API request
        this.sendButton = this.form.querySelector("button[data-action='read']");
        this.sendButton.addEventListener("click", this.handleSendClick.bind(this));

    }
    //clear the <code> element button with the data-action='clear' attribute is clicked
    handleClearClick(event) {
        event.preventDefault();  // Prevents page reload when the button is clicked
        let code = this.debugCard.querySelector("code");
        code.innerText = "";
    }

    handleSendClick(event) {
        event.preventDefault();
        const input = document.querySelector(".debug-card input");
        const endpoint = input.value;
        getData(endpoint, this.showResponse);
    }

    showResponse(data) {
        // callback function, executed once getData() runs successfully
        const debugCard = document.querySelector(".debug-card");
        let code = debugCard.querySelector("code");
        code.innerText = data;
    }
}

// Wait for DOM to load before instantiating
document.addEventListener("DOMContentLoaded", () => {
    new DebugForm();
});
