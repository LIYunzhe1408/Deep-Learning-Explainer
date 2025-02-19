<template>
  <div>
<!--        <OptionExplanation/>-->
      <MainExplanation/>
  </div>
</template>

<script>
import OptionExplanation from "@/components/OptionExplanation";
import MainExplanation from "@/components/MainExplanation";
export default {
  name: "Explanation",
  components: {MainExplanation, OptionExplanation},
  data(){
    return{
      chosen: false
    }
  },
  methods: {
    changeStatus(){
      this.chosen = !this.chosen
    }
  }
}
</script>

<style scoped>
.box{
  margin: 0 10px 40px 10px;
  background-color: white;
  padding-left: 10px;
  border: gray ;
  border-radius: 10px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
}
</style>