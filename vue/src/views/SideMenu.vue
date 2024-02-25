<template>
  <el-aside :width="asideW" style="min-height: 91.9vh; background-color: #001529" >
    <el-menu router style="border: None" :collapse="isCollapse" :collapse-transition="false" background-color="#001529" text-color="rgb(255,255,255,0.65)" active-text-color="#fff" :default-active="$route.path">
      <el-menu-item index="/home">
        <i class="el-icon-house"></i>
        <span slot="title" style="font-size: 14px;">Home</span>
      </el-menu-item>
      <el-menu-item index="/extraction">
        <i class="el-icon-s-data"></i>
        <span slot="title" style="font-size: 14px">Concept Extraction</span>
      </el-menu-item>
      <el-menu-item  index="/tree">
        <i class="el-icon-grape"></i>
        <span slot="title" style="font-size: 14px">Concept Tree</span>
      </el-menu-item>
      <el-menu-item index="/explanation">
        <i class="el-icon-connection"></i>
        <span slot="title" style="font-size: 14px">Explanation</span>
      </el-menu-item>
      <el-menu-item index="/settings">
        <i class="el-icon-setting"></i>
        <span slot="title" style="font-size: 14px">System</span>
      </el-menu-item>
    </el-menu>

    <i class="el-icon-s-unfold" v-if="!visible" @click="handleCollapse" style="size: 300px; margin: 25px 0 0 25px; color: white"></i>
    <i class="el-icon-s-fold" v-if="visible" @click="handleCollapse" style="size: 300px; margin: 25px 0 0 170px; color: white"></i>
  </el-aside>
</template>

<script>
export default {
  name: "SideMenu",
  data() {
    return {
      isCollapse:true,
      asideW: "64px",
      ml: '',
      visible: false
    }
  },
  methods: {
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideW = this.isCollapse ? "64px" : "200px"
      this.visible = !this.visible
    }
  },
}
</script>

<style scoped>
.el-icon-s-unfold, .el-icon-s-fold{
  cursor: pointer;
}
</style>