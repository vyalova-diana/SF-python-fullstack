const parser = new DOMParser();

const xmlString = `
  <list>
  <student>
    <name lang="en">
      <first>Ivan</first>
      <second>Ivanov</second>
    </name>
    <age>35</age>
    <prof>teacher</prof>
  </student>
  <student>
    <name lang="ru">
      <first>Петр</first>
      <second>Петров</second>
    </name>
    <age>58</age>
    <prof>driver</prof>
  </student>
</list>
`;

const result = {
    list: []
};

const xmlDOM = parser.parseFromString(xmlString, "text/xml");

const listNode = xmlDOM.querySelector("list");
const studentNodeList = listNode.querySelectorAll("student");

studentNodeList.forEach(function(studentItem) {
    let name = studentItem.querySelector("name").querySelector("first").textContent + " " +
        studentItem.querySelector("name").querySelector("second").textContent;
    let age = Number(studentItem.querySelector("age").textContent);
    let prof = studentItem.querySelector("prof").textContent;
    let lang = studentItem.querySelector("name").getAttribute("lang");

    let student = {
        name:name,
        age:age,
        prof:prof,
        lang:lang
    };

    result.list.push(student);
});

console.log(result);