<template>
  <div>
    <div class="box">
      <optionExtraction/>
    </div>
    <MainExtraction/>
  </div>

</template>

<script>
import optionExtraction from "@/components/OptionExtraction";
import MainExtraction from "@/components/MainExtraction";
export default {
  name: "Extraction",
  components: {
    MainExtraction,
    optionExtraction
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