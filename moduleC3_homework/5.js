class ElectricalAppliance {
    constructor(name, power){
        this.name = name;
        this.power = power;
        this.isPlugged = false;
    }
    plugIn() {
        if (this.isPlugged)
            console.log(`Error! ${this.name} is already plugged!`);
        else{
            console.log(this.name + " is plugged!");
            this.isPlugged = true;
        }
    }

    unplug() {
        if (this.isPlugged){
            console.log(this.name + " is unplugged!");
            this.isPlugged = false;
        }
        else
            console.log(`Error! ${this.name} is already unplugged!`);
    }
}

class Lamp extends ElectricalAppliance {
    constructor (name, brand, power, bulbType) {
        super(name, power);
        this.brand = brand;
        this.bulbType = bulbType;
        this.isPlugged = true;
    }
}

class Computer extends ElectricalAppliance {
    constructor(name, brand, power, type, functionality) {
        super(name, power);
        this.brand = brand;
        this.type = type;
        this.functionality = functionality;
        this.isPlugged = false;
    }
}

const tableLamp = new Lamp("Table lamp", "IKEA", 10, "LED");

const homePC = new Computer("Table PC", "ASUS", 1200, "laptop", "for work");

tableLamp.unplug();
homePC.plugIn();

console.log(homePC);
console.log(tableLamp);