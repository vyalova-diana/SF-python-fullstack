function checkValue(form) {
    let page = Number(form.elements["page"].value);
    let limit = Number(form.elements["limit"].value);

    let isPageValid = page>=1 && page<=10;
    let isLimitValid = limit>=1 && limit<=10;

    if (isPageValid && isLimitValid)
        return `https://picsum.photos/v2/list?page=${page}&limit=${limit}`;
    else if (isPageValid)
        throw new Error(`Лимит вне диапазона от 1 до 10`);
    else if (isLimitValid)
        throw new Error(`Номер страницы вне диапазона от 1 до 10`);
    else
        throw new Error(`Номер страницы и лимит вне диапазона от 1 до 10`);
}

async function useRequest(url) {
    let response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    else{
        let jsonResponse = await response.json();
        localStorage.setItem('myJSON', JSON.stringify(jsonResponse));
        return jsonResponse;

    }
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
formNode.addEventListener("submit", async function (event) {
    // stop form submission
    event.preventDefault();

    try {
        let checkResult = checkValue(this);
        let requestResult = await useRequest(checkResult);
        displayResult(requestResult);
    }
    catch(e){
        resultNode.innerHTML = e.message;
    }

});
