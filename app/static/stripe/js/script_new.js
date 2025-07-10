
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

function setPriceInputs({
    oneBin2weeks, oneBin4weeks, oneBin8weeks, oneBinOneOff,
    twoBins2weeks, twoBins4weeks, twobins8weeks, twoBinsOneOff, 
    threeBins2weeks, threeBins4weeks, threeBins8weeks, threeBinsOneOff,
    publishableKey}) {
  const oneb2wPriceInput = document.querySelector('#oneBin2weeks');
  const oneb4wPriceInput = document.querySelector('#oneBin4weeks');
  const oneb8wPriceInput = document.querySelector('#oneBin8weeks');
  const onebOneOffPriceInput = document.querySelector('#onesBinOneOff');
  const twob2wPriceInput = document.querySelector('#twoBins2weeks');
  const twob4wPriceInput = document.querySelector('#twoBins4weeks');
  const twob8wPriceInput = document.querySelector('#twoBins8weeks');
  const twobOneOffPriceInput = document.querySelector('#twoBinsOneOff');
  const threeb2wPriceInput = document.querySelector('#threeBins2weeks');
  const threeb4wPriceInput = document.querySelector('#threeBins4weeks');
  const threeb8wPriceInput = document.querySelector('#threeBins8weeks');
  const threebOneOffPriceInput = document.querySelector('#threeBinsOneOff');
  if (
    !oneb2wPriceInput || !oneb4wPriceInput || !oneb8wPriceInput || !onebOneOffPriceInput ||
    !twob2wPriceInput || !twob4wPriceInput || !twob8wPriceInput || !twobOneOffPriceInput ||
    !threeb2wPriceInput || !threeb4wPriceInput || !threeb8wPriceInput || !threebOneOffPriceInput
  ) {
    console.error('Price input elements not found');
    document.querySelector('#error-message').textContent = 'Error: Pricing inputs missing.';
    return false;
  }
  // Set input values
  oneb2wPriceInput.value = oneBin2weeks || '';
  oneb4wPriceInput.value = oneBin4weeks || '';
  oneb8wPriceInput.value = oneBin8weeks || '';
  onebOneOffPriceInput.value = oneBinOneOff || '';
  twob2wPriceInput.value = twoBins2weeks || '';
  twob4wPriceInput.value = twoBins4weeks || '';
  twob8wPriceInput.value = twobins8weeks || '';
  twobOneOffPriceInput.value = twoBinsOneOff || '';
  threeb2wPriceInput.value = threeBins2weeks || '';
  threeb4wPriceInput.value = threeBins4weeks || '';
  threeb8wPriceInput.value = threeBins8weeks || '';
  threebOneOffPriceInput.value = threeBinsOneOff || '';
  console.log('Inputs set:', {
    oneBin2weeks: oneb2wPriceInput.value,
    oneBin4weeks: oneb4wPriceInput.value,
    oneBin8weeks: oneb8wPriceInput.value,
    oneBinOneOff: onebOneOffPriceInput.value,
    twoBins2weeks: twob2wPriceInput.value,
    twoBins4weeks: twob4wPriceInput.value,
    twoBins8weeks: twob8wPriceInput.value,
    twoBinsOneOff: twobOneOffPriceInput.value,
    threeBins2weeks: threeb2wPriceInput.value,
    threeBins4weeks: threeb4wPriceInput.value,
    threeBins8weeks: threeb8wPriceInput.value,
    threeBinsOneOff: threebOneOffPriceInput.value
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
