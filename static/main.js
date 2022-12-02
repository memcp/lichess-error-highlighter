const winRates = document.querySelectorAll('.win-rate');


winRates.forEach((winRate) => {
  const percentage = winRate.childNodes[0].data;
  const floatValue = percentage.substring(0, percentage.length - 1);


  if (!floatValue) return;

  const color = (floatValue > 50.0) ? 'green' : 'red';
  winRate.classList.add(`${color}`)
});


