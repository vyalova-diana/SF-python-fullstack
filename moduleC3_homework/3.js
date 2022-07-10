function createObjWithoutProto() {
    return Object.create(null);
}

let test = createObjWithoutProto();
console.log(Object.getPrototypeOf(test));