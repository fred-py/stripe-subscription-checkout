
/* Fetch prices and update the form 

This code will check if the elements exist 
before trying to update their values

index.html should contain the following elements: 
comboPrice, silverPrice, goldPrice

If any of these elements are missing, the server will 
return a POST request with non-type value
*/

/* ORIGINAL CODE
fetch("/config")
  .then(r => r.json())
  .then(({comboPrice, silverPrice, goldPrice}) => {
    const comboPriceInput = document.querySelector('#comboPrice');
    comboPriceInput.value = comboPrice;
    const silverPriceInput = document.querySelector('#silverPrice');
    silverPriceInput.value = silverPrice;
    const goldPriceInput = document.querySelector('#goldPrice');
    goldPriceInput.value = goldPrice;
  });
*/

document.querySelectorAll('.pricing-button').forEach(button => {
  button.disabled = true; // Disable buttons initially
});

function setPriceInputs({oneBin2weeks, oneBin4weeks, oneBin8weeks, oneBinOneOff, publishableKey}) {
  const oneb2wPriceInput = document.querySelector('#oneBin2weeks');
  const oneb4wPriceInput = document.querySelector('#oneBin4weeks');
  const oneb8wPriceInput = document.querySelector('#oneBin8weeks');
  const onebOneOffPriceInput = document.querySelector('#oneBinOneOff');
  if (!oneb2wPriceInput || !oneb4wPriceInput || !oneb8wPriceInput || !onebOneOffPriceInput) {
    console.error('Price input elements not found');
    document.querySelector('#error-message').textContent = 'Error: Pricing inputs missing.';
    return false;
  }
  comboPriceInput.value = oneBin2weeks || '';
  silverPriceInput.value = oneBin4weeks || '';
  goldPriceInput.value = oneBin8weeks || '';
  goldPriceInput.value = oneBinOneOff || '';
  console.log('Inputs set:', {
    combo: comboPriceInput.value,
    silver: silverPriceInput.value,
    gold: goldPriceInput.value
  });
  // Initialize Stripe
  const stripe = Stripe(publishableKey);
  // Enable buttons
  document.querySelectorAll('.pricing-button').forEach(button => {
    button.disabled = false;
  });
  return true;
}

function fetchConfig(retries = 3, delay = 1000) {
  fetch("/config")
    .then(r => {
      if (!r.ok) throw new Error(`HTTP error! Status: ${r.status}`);
      return r.json();
    })
    .then(data => {
      console.log('Config response:', data);
      setPriceInputs(data);
    })
    .catch(error => {
      console.error('Fetch /config failed:', error);
      if (retries > 0) {
        console.log(`Retrying fetch (${retries} attempts left)...`);
        setTimeout(() => fetchConfig(retries - 1, delay * 2), delay);
      } else {
        document.querySelector('#error-message').textContent = 'Error loading pricing. Please refresh the page.';
      }
    });
}

fetchConfig();

document.querySelectorAll('.pricing-button').forEach(button => {
  button.addEventListener('click', (e) => {
    const form = button.closest('form');
    const priceInput = form.querySelector('input[name="priceId"]');
    if (!priceInput.value) {
      //e.preventDefault(); this disables button if priceID is missin
      console.error('Price ID missing for form:', form);
      document.querySelector('#error-message').textContent = 'Error: Price not loaded. Please wait and try again.';
    } else {
      console.log('Submitting form with priceId:', priceInput.value);
    }
  });
});
