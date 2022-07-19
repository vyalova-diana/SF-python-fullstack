function checkValue(form) {
    let width = Number(form.elements["width"].value);
    let height = Number(form.elements["height"].value);

    if ((width>=100 && width<=300) && (height>=100 && height<=300))
       return `https://picsum.photos/${width}/${height}`;
    else
        throw new Error(`Одно из чисел вне диапазона от 100 до 300`);

}

async function useRequest(url) {
    let response = await fetch(url);
    if (response.ok) {
        return response.url;
    }
    else{
        throw new Error(`HTTP error! status: ${response.status}`);
    }
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

formNode.addEventListener("submit", async function (event) {
    // stop form submission
    event.preventDefault();
    resultNode.innerHTML = "";

    try {
        let checkResult = checkValue(this);
        let requestResult = await useRequest(checkResult);
        displayResult(requestResult);
    }
    catch(e){
        resultNode.innerHTML = e.message;
    }

});
