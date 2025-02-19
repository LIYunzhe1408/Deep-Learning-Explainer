<template>
  <div>
<!--      <div class="box">-->
<!--        <test></test>-->
<!--      </div>-->
    <setting-log/>
  </div>
</template>

<script>
import test from "@/components/test";
import settingLog from "@/components/SettingLog";
export default {
  name: "Setting",
  components: {test, settingLog},
  data(){
    return{
    }
  },
  methods: {
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