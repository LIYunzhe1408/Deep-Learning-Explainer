<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Header from "@/views/Header.vue";
import Option from "@/components/OptionMain.vue";
import Side from "@/views/SideMenu"
import SideMenu from "@/views/SideMenu";
export default {
  name: "app",
  components: {
    SideMenu,
    Header,
    Option,
    Side
  }
}
</script>

<style>

#app{
  position:absolute;
  top:0;
  right:0;
  bottom:0;
  left:0;
}
</style>