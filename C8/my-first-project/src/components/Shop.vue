<template>
  <div class="test">
    <div class="card" v-for="(phone,key) in phones" :key="key">
      <h3>{{phone.name}}</h3>
      <div>{{phone.price}}</div>
      <div class="counter">
        <button class="btn" v-on:click="DecCount(phone)">-</button>
        <input type="number" v-model="phone.amount" pattern="\d*"  min="0">
        <button class="btn" @click="IncCount(phone)">+</button>
      </div>
      <div class="total">{{CalcTotalPerItem(phone)}}</div>
    </div>
    <div class="total">Итого: {{Total}}</div>
  </div>
</template>


<script>
export default {
  name: "Shop",
  components: {},

  data() {
    return {
      phones: [
        {
          name: "a",
          price: 10,
          amount: 0
        },
        {
          name: "b",
          price: 1090,
          amount: 0
        },
        {
          name: "c",
          price: 1000,
          amount: 0
        },
        {
          name: "d",
          price: 13430,
          amount: 0
        }
      ]
    };
  },
  computed: {
    Total () {
      let sum = 0;
      this.phones.forEach(phone => {
        sum += phone.price * phone.amount;
      });
      return sum;
      }
  },
  methods: {
    CalcTotalPerItem(phone) {
      return phone.amount*phone.price;
    },
    IncCount(phone){
      return phone.amount++;
    },
    DecCount(phone){
      return phone.amount !== 0 ? phone.amount-- : phone.amount;
    }
  }
}
</script>

<style scoped lang="less">
.test{
  display: flex;
  flex-direction: column;
  align-items: center;
  row-gap: 10px;
}
.card{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  width: 30%;
  border: 2px solid #000000;
  border-radius: 5px;

  h3{
    margin: 0;
  }
  .counter{
    display: flex;

    input{
      width: 3em;
      text-align: center;
    }
  }
}
</style>