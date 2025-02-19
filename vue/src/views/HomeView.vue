<template>
  <div class="home">
    <Header v-if="this.loggedIn===2"/>

    <el-container>
        <SideMenu v-if="this.loggedIn===2"/>

        <el-main >
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
import taskSubmission from "@/views/TaskSubmission";
import bus from "@/common/bus";
import logIn from "@/views/LogIn";
export default {
  name: 'HomeView',
  data() {
    return {
      isCollapse:true,
      asideW: "64px",
      loggedIn: 1
    }
  },
  methods: {
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideW = this.isCollapse ? "64px" : "200px"
    }
  },
  mounted() {
    bus.$on("toHomeView", (data)=>{
      this.loggedIn = data
    })
    // if (this.loggedIn !== 0)
    this.$router.push("/login").catch(error => {
      console.error('Error fetching image', error);
    });
  },
  components: {
    Header,
    Option,
    Main,
    SideMenu,
    taskSubmission,
    logIn
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
  background-color: #003262 !important;
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