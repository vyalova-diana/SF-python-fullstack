function checkValue(form, callback) {
    let width = Number(form.elements["width"].value);
    let height = Number(form.elements["height"].value);

    if ((width>=100 && width<=300) && (height>=100 && height<=300))
       callback(`https://picsum.photos/${width}/${height}`, displayResult);
    else
        resultNode.textContent = 'Одно из чисел вне диапазона от 100 до 300';

}

function useRequest(url, callback) {
    fetch(url)
    .then((response) => {return response.url;})
    .then((imgUrl) => { callback(imgUrl); })
    .catch(() => { console.log('error'); });
}

function displayResult(imgUrl) {
    resultNode.innerHTML = `
      <div class="card">
        <img
          src=${imgUrl};
          class="card-image"
          alt="img"/>
      </div>
    ` ;
}

const formNode = document.querySelector('.form-query');
const resultNode = document.querySelector('.j-result');

formNode.addEventListener("submit", function (event) {
    // stop form submission
    event.preventDefault();
    checkValue(this,useRequest);
});
