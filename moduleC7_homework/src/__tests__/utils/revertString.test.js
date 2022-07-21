import {revertString} from "../../utils/revertString";
import {re} from "@babel/core/lib/vendor/import-meta-resolve";

describe("tests for revertString function", () => {
    it("should reverse string", () => {
        expect(revertString("abc")).toBe("cba");
        expect(revertString("")).toBe(("Пустая строка"));
    });
});