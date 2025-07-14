document.querySelectorAll('.pricing-button').forEach(button => {
  button.disabled = true; // Disable buttons initially
});

  function setPriceInputs({oneBin2weeks, oneBin4weeks, oneBin8weeks, oneBinOneOff,
    twoBins2weeks, twoBins4weeks, twoBins8weeks, twoBinsOneOff, 
    threeBins2weeks, threeBins4weeks, threeBins8weeks, threeBinsOneOff,
    publishableKey}) {
    const oneb2wInput = document.querySelector('#oneBin2weeks');
    const oneb4wInput = document.querySelector('#oneBin4weeks');
    const oneb8wInput = document.querySelector('#oneBin8weeks');
    const onebInput = document.querySelector('#oneBinOneOff');
    
    const twob2wInput = document.querySelector('#twoBins2weeks');
    const twob4wInput = document.querySelector('#twoBins4weeks');
    const twob8wInput = document.querySelector('#twoBins8weeks');
    const twobInput = document.querySelector('#twoBinsOneOff');

    const threeb2wInput = document.querySelector('#threeBins2weeks');
    const threeb4wInput = document.querySelector('#threeBins4weeks');
    const threeb8wInput = document.querySelector('#threeBins8weeks');
    const threebInput = document.querySelector('#threeBinsOneOff');

    // If any of the priceInputs are null the function will fail
    if (!oneb2wInput || !oneb4wInput || !oneb8wInput || !onebInput
        || !twob2wInput || !twob4wInput || !twob8wInput || !twobInput
        || !threeb2wInput || !threeb4wInput || !threeb8wInput || !threebInput
      ) {
      console.error('Price input elements not found');
      document.querySelector('#error-message').textContent = 'Error: Pricing inputs missing.';
      return false;
    }
    oneb2wInput.value = oneBin2weeks || '';
    oneb4wInput.value = oneBin4weeks || '';
    oneb8wInput.value = oneBin8weeks || '';
    onebInput.value = oneBinOneOff || '';

    twob2wInput.value = twoBins2weeks || '';
    twob4wInput.value = twoBins4weeks || '';
    twob8wInput.value = twoBins8weeks || '';
    twobInput.value = twoBinsOneOff || '';

    threeb2wInput.value = threeBins2weeks || '';
    threeb4wInput.value = threeBins4weeks || '';
    threeb8wInput.value = threeBins8weeks || '';
    threebInput.value = threeBinsOneOff || '';

    console.log('Inputs set:', {
      oneb2w: oneb2wInput.value,
      oneb4w: oneb4wInput.value,
      oneb8w: oneb8wInput.value,
      oneb: onebInput.value,
      
      twob2w: twob2wInput.value,
      twob4w: twob4wInput.value,
      twob8w: twob8wInput.value,
      twob: twobInput.value,

      threeb2w: threeb2wInput.value,
      threeb4w: threeb4wInput.value,
      threeb8w: threeb8wInput.value,
      threeb: threebInput.value,
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
