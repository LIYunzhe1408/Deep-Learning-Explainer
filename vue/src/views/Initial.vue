<template>
  <div>
    <div class="box">
      <Option/>
    </div>
    <Main/>
  </div>
</template>

<script>
import Option from "@/views/Option";
import Main from "@/views/Main";
export default {
  name: "initial",
  components: {
    Option,
    Main
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