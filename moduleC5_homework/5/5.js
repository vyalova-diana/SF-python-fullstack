function checkValue(form, callback) {
    let page = Number(form.elements["page"].value);
    let limit = Number(form.elements["limit"].value);

    let isPageValid = page>=1 && page<=10;
    let isLimitValid = limit>=1 && limit<=10;

    if (isPageValid && isLimitValid)
            callback(`https://picsum.photos/v2/list?page=${page}&limit=${limit}`, displayResult);
    else if (isPageValid)
            resultNode.textContent = 'Лимит вне диапазона от 1 до 10';
        else if (isLimitValid)
            resultNode.textContent = 'Номер страницы вне диапазона от 1 до 10';
        else
            resultNode.textContent = 'Номер страницы и лимит вне диапазона от 1 до 10';
}

function useRequest(url, callback) {
    fetch(url)
    .then((response) => {return response.json();})
    .then((jsonList) => {
        localStorage.setItem('myJSON', JSON.stringify(jsonList));
        callback(jsonList); })
    .catch(() => { console.log('error'); });
}

function displayResult(apiData) {
    let cards = '';

    apiData.forEach(item => {
        const cardBlock = `
      <div class="card">
        <img
          src="${item.download_url}"
          class="card-image"
        />
        <p>${item.author}</p>
      </div>
    `;
        cards = cards + cardBlock;
    });

    resultNode.innerHTML = cards;
}

const formNode = document.querySelector('.form-query');
const resultNode = document.querySelector('.j-result');

window.addEventListener('load', () => {
    const myJSON = localStorage.getItem('myJSON');

    if (myJSON) {
        // Если данные в localStorage есть - просто выводим их
        displayResult(JSON.parse(myJSON));
    }

});
formNode.addEventListener("submit", function (event) {
    // stop form submission
    event.preventDefault();
    checkValue(this,useRequest);
});
