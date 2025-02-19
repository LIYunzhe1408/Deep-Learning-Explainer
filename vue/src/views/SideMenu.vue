<template>
  <el-aside :width="asideW" style="min-height: 91.9vh; background-color: #001D39" >
    <el-menu router style="border: None" :collapse="isCollapse" :collapse-transition="false" background-color="#001D39" text-color="rgb(255,255,255,0.65)" active-text-color="#fff" :default-active="$route.path">
      <el-menu-item index="/home">
        <i class="el-icon-house"></i>
        <span slot="title" style="font-size: 14px;">{{$t('sideMenu.home')}}</span>
      </el-menu-item>
      <el-menu-item index="/extraction">
        <i class="el-icon-s-data"></i>
        <span slot="title" style="font-size: 14px">{{$t('sideMenu.extraction')}}</span>
      </el-menu-item>
      <el-menu-item  index="/tree">
        <i class="el-icon-grape"></i>
        <span slot="title" style="font-size: 14px">{{$t('sideMenu.tree')}}</span>
      </el-menu-item>
      <el-menu-item index="/localExplanation">
        <i class="el-icon-location"></i>
        <span slot="title" style="font-size: 14px">{{$t('sideMenu.localExplanation')}}</span>
      </el-menu-item>
      <el-menu-item index="/explanation">
        <i class="el-icon-connection"></i>
        <span slot="title" style="font-size: 14px">{{$t('sideMenu.explanation')}}</span>
      </el-menu-item>
<!--      <el-menu-item index="/settings" v-if="loggedIn">-->
<!--        <i class="el-icon-setting"></i>-->
<!--        <span slot="title" style="font-size: 14px">{{$t('sideMenu.sys')}}</span>-->
<!--      </el-menu-item>-->
    </el-menu>

    <i class="el-icon-s-unfold" v-if="!visible" @click="handleCollapse" style="size: 300px; margin: 25px 0 0 25px; color: white"></i>
    <i class="el-icon-s-fold" v-if="visible" @click="handleCollapse" style="size: 300px; margin: 25px 0 0 110px; color: white"></i>
  </el-aside>
</template>

<script>
import bus from "@/common/bus";

export default {
  name: "SideMenu",
  data() {
    return {
      isCollapse:true,
      asideW: "64px",
      ml: '',
      visible: false,
      loggedIn: false
    }
  },
  methods: {
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideW = this.isCollapse ? "64px" : "140px"
      this.visible = !this.visible
    }
  },
  mounted() {
    bus.$on("toSideMenuANDHeader", (data)=>{
      this.loggedIn = data
    })
  }
}
</script>

<style scoped>
.el-icon-s-unfold, .el-icon-s-fold{
  cursor: pointer;
}
</style>