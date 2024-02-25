<template>
  <div class="home">
    <Header/>

    <el-container>
        <SideMenu/>

        <el-main style="background-color:  #f5f5f5">
          <router-view/>
        </el-main>
    </el-container>
  </div>
</template>

<script>
import Header from "@/views/Header.vue";
import Option from "@/components/OptionMain.vue";
import Main from '@/components/Main'
import SideMenu from "@/views/SideMenu";
export default {
  name: 'HomeView',
  data() {
    return {
      isCollapse:true,
      asideW: "64px"
    }
  },
  methods: {
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideW = this.isCollapse ? "64px" : "200px"
    }
  },
  components: {
    Header,
    Option,
    Main,
    SideMenu
  }
}
</script>

<style>
.el-menu-item:hover {
  color: #fff !important;

}

.el-menu-item{

  height: 40px;
  line-height: 40px;
}

.el-menu-item.is-active{
  background-color: #1890ff !important;
  border-radius: 10px !important;
}

.el-aside{
  transition: .3s;
}

.el-header{
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  margin: 0 0 0 0;
  padding:0 0 0 0
}
</style>