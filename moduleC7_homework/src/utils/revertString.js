export function revertString(str) {
    if (str){
        let revertedStr = "";

        for (let i = str.length - 1; i >= 0; i--) {
            revertedStr += str[i];
        }
        return revertedStr;
    }
   return "Пустая строка";
}