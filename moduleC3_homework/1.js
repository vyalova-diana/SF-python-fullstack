function printObject (obj) {
    for (let prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            console.log(prop, obj[prop]);
        }
    }
}

let obj = {prop1: 1, prop2: "2"};
printObject(obj);
