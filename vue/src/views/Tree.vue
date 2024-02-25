<template>
  <div>
    <div class="box">
      <OptionTree/>
    </div>
    <MainTree/>
  </div>
</template>

<script>
import OptionTree from "@/components/OptionTree";
import MainTree from "@/components/MainTree";
export default {
  name: "Tree",
  components: {MainTree, OptionTree}
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