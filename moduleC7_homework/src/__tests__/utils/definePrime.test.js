import {definePrime} from "../../utils/definePrime";

describe("tests for definePrime function ",() => {
    const primeNumber =17;
    const complexNumber = 9;

    it("operate correctly with prime,complex and invalid numbers", () =>{
        expect(definePrime(primeNumber)).toBe(`Число ${primeNumber} - простое число`);
        expect(definePrime(complexNumber)).toBe(`Число ${complexNumber} - составное число`);
        expect(definePrime(1001)).toBe("Данные неверны");
    });

});

