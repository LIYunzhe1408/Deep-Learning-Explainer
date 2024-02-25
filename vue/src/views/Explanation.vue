<template>
  <div>
    <div class="box">
      <option-extraction/>
    </div>
    <MainExplanation/>
  </div>
</template>

<script>
import OptionExtraction from "@/components/OptionExtraction";
import MainExplanation from "@/components/MainExplanation";
export default {
  name: "Explanation",
  components: {MainExplanation, OptionExtraction}
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