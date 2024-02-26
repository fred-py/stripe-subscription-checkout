
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
  .then(({comboPrice, silverPrice, goldPrice, oneOffx1, oneOffx2}) => {
    const comboPriceInput = document.querySelector('#comboPrice');
    comboPriceInput.value = comboPrice;
    const silverPriceInput = document.querySelector('#silverPrice');
    silverPriceInput.value = silverPrice;
    const goldPriceInput = document.querySelector('#goldPrice');
    goldPriceInput.value = goldPrice;
    const oneOffx1Input = document.querySelector('#oneOffx1');
    oneOffx1Input.value = oneOffx1;
    const oneOffx2Input = document.querySelector('#oneOffx2');
    oneOffx2Input.value = oneOffx2;
  });
  
// Fetch the price for a specific product under One-off price
// NOTE: the bwlow was  added after the addition og the second one-offx2
function fetchPrice(priceType) {
  fetch(`/config?priceType=${priceType}`)
    .then(r => r.json())
    .then(data => {
      const priceInput = document.querySelector('#priceId');
      priceInput.value = data[priceType];
    });
}
  
document.querySelector('#one-off-btn-1').addEventListener('click', (event) => {
  event.preventDefault();
  fetchPrice('oneOffx1');
});
  
document.querySelector('#one-off-btn-2').addEventListener('click', (event) => {
  event.preventDefault();
  fetchPrice('oneOffx2');
});