

function checkValue(form, callback) {
    let value = Number(form.elements["number"].value);
    if (value>=1 && value<=10)
        callback(`https://picsum.photos/v2/list?limit=${value}`, displayResult);
    else
        resultNode.textContent = 'Число вне диапазона от 1 до 10';

}
function useRequest(url, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);

    xhr.onload = function() {
        if (xhr.status != 200) {
            console.log('Статус ответа: ', xhr.status);
        } else {
            const result = JSON.parse(xhr.response);
            if (callback) {
                callback(result);
            }
        }
    };

    xhr.onerror = function() {
        console.log('Ошибка! Статус ответа: ', xhr.status);
    };

    xhr.send();
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
console.log("init!!");

formNode.addEventListener("submit", function (event) {
    // stop form submission
    event.preventDefault();
    checkValue(this, useRequest);

});
