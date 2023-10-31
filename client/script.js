/* Fetch prices and update the form */
fetch("/config")
  .then(r => r.json())
  .then(({basicPrice, proPrice, premPrice}) => {
    const basicPriceInput = document.querySelector('#basicPrice');
    basicPriceInput.value = basicPrice;
    const proPriceInput = document.querySelector('#proPrice');
    proPriceInput.value = proPrice;
    const premPriceInput = document.querySelector('#premPrice');
    premPriceInput.value = premPrice;
  })
