import * as index from "../index";


xdescribe('sum', () => {
    test('adds 1 + 2 to equal 3', () => {
        expect(index.sum(1, 2)).toBe(3);
    });
    test('adds 1 + 0 to equal 1', () => {
        expect(index.sum(1, 0)).toBe(1);
    });

});

xdescribe('my beverage', () => {
    test('is delicious', () => {
        expect(index.myBeverage.delicious).toBeTruthy();
    });

    test('is not sour', () => {
        expect(index.myBeverage.sour).toBeFalsy();
    });
});
