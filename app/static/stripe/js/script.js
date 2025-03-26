
/* Fetch prices and update the form 

This code will check if the elements exist 
before trying to update their values

index.html should contain the following elements: 
comboPrice, silverPrice, goldPrice

If any of these elements are missing, the server will 
return a POST request with non-type value
*/

fetch("/config")
  .then(r => r.json())
  .then(({comboPrice, silverPrice, goldPrice, oneOff}) => {
    const comboPriceInput = document.querySelector('#comboPrice');
    comboPriceInput.value = comboPrice;
    const silverPriceInput = document.querySelector('#silverPrice');
    silverPriceInput.value = silverPrice;
    const goldPriceInput = document.querySelector('#goldPrice');
    goldPriceInput.value = goldPrice;
    // One-off option is now on enquiry only = no direct payment option 
    //const oneOffInput = document.querySelector('#oneOff');
    //oneOffInput.value = oneOff;
  });


