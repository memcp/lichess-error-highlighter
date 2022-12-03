async function setAccessToken() {
    const accessTokenForm = document.querySelector('.access-token-form');
    const accessToken = accessTokenForm.elements['access_token'].value;
    await fetch(`http://127.0.0.1:5000/create-games/${accessToken}`)
    window.location.href = "http://127.0.0.1:5000/opening-stats";
}

const submitButton = document.querySelector('.set-access-token');
submitButton.addEventListener('click',  (e) => {
    e.preventDefault();
    setAccessToken()
})
