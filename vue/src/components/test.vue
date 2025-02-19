<template>
  <div>
    <div id="start" class="box" style="margin-left: 500px ">Div 1</div>
    <div id="end" class="box">Div 2</div>
  </div>
</template>

<script>
import LeaderLine from 'leader-line'
export default {
  name: "test",
  mounted() {
    const startElement = document.getElementById('start'), endElement = document.getElementById('end');

    new LeaderLine(startElement, endElement, {color: 'black', size: 1});
  }
};
</script>

<style scoped>
.box {
  width: 100px;
  height: 100px;
  background-color: lightblue;
  margin: 20px;
}
</style>



