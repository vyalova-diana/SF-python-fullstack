function checkPropInObj (str, obj) {
    return (str in obj);
}

let obj = {prop1: 1, prop2: "2"};
console.log(checkPropInObj("prop2",obj));