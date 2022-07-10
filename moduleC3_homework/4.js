function ElectricalAppliance(name, power) {
    this.name = name;
    this.power = power;
    this.isPlugged = false;
}

ElectricalAppliance.prototype.plugIn = function() {
    if (this.isPlugged)
        console.log(`Error! ${this.name} is already plugged!`);
    else{
        console.log(this.name + " is plugged!");
        this.isPlugged = true;
    }
};

ElectricalAppliance.prototype.unplug = function() {
    if (this.isPlugged){
        console.log(this.name + " is unplugged!");
        this.isPlugged = false;
    }
    else
        console.log(`Error! ${this.name} is already unplugged!`);
};

function Lamp(name, brand, power, bulbType) {
    this.name = name;
    this.brand = brand;
    this.power = power;
    this.bulbType = bulbType;
    this.isPlugged = true;
}

Lamp.prototype = new ElectricalAppliance();

function Computer(name, brand, power, type, functionality) {
    this.name = name;
    this.brand = brand;
    this.power = power;
    this.type = type;
    this.functionality = functionality;
    this.isPlugged = false;
}

Computer.prototype = new ElectricalAppliance();

const tableLamp = new Lamp("Table lamp", "IKEA", 10, "LED");

const homePC = new Computer("Table PC", "ASUS", 1200, "laptop", "for work");

tableLamp.plugIn();
homePC.plugIn();

tableLamp.unplug();
homePC.unplug();

console.log(tableLamp);
console.log(homePC);
