<template>
  <div class="head">
    <el-row style="background-color: #003262">
      <el-col :span="4">
        <div class="mainTitle">EXPLAINER</div>
      </el-col>

      <el-col :span="4">
        <div class="subTitle" style="font-size: 15px; height:30px">HIERARCHICAL CONCEPT-BASED</div>
        <div class="subTitle" style="font-family: Britannic"><i>Figure Out What DNN Is Doing</i></div>
      </el-col>

      <el-col :span="11">
        <div style="width: 100%; height: 80px; display: flex; align-items: end; padding-bottom: 20px">
<!--          <el-select style="width: 12%" v-model="value4" @change="selectLanguage" placeholder="please Select">-->
<!--          <el-option-->
<!--              v-for="item in options"-->
<!--              :key="item.value"-->
<!--              :label="item.label"-->
<!--              :value="item.value">-->
<!--          </el-option>-->
<!--        </el-select>-->
        </div>

      </el-col>

      <el-col :span="2">
        <div style="width: 100%; height: 80px; display: flex; align-items: center; justify-content: center; padding: 3px 10px 0 0">
          <img style="width: 100%" src="@/assets/header/SHU.png">
        </div>
      </el-col>
      <el-col :span="2">
        <div style="width: 100%; height: 80px; display: flex; align-items: center; justify-content: center;">
          <img style="width: 75%" src="@/assets/header/ML.png">
        </div>
      </el-col>
      <el-col :span="1">
        <div style="width: 100%; height: 80px; display: flex; align-items: center; justify-content: center;">
          <div v-if="this.loggedIn===1"
               class="avatarModule"
               @click="$router.push('/settings')">
            <el-avatar  :size="40" :src=this.picture></el-avatar>
              <div class="me" style="color: lightgray; font-size: 14px" @click="openProfile">Me
              <i class="el-icon-caret-bottom"></i>
              </div>

          </div>
          <div v-if="this.loggedIn===0" class="signIn" style="" @click="login">Log In</div>
        </div>
      </el-col>
    </el-row>
    <div style="height: 5px; background-color: #9c6e11"></div>
  </div>
</template>

<script>
import bus from "@/common/bus";
import axios from "axios";

export default {
  name: "Header",
  data(){
    return{
      me: '',
      picture:'',
      options:[{
        value:'1',
        label:'中文'
      },
        {
          value:'2',
          label:'English'
        }],
      value4:'中文',
      langcn:'en',
      langen:'en',
      loggedIn: 1
    }
  },
  methods: {
    searchUser(){
      axios({
        method: "get",
        params: {},
        url: 'http://localhost:8000/main/add_user/'
      }).then(res=> {
        this.me = res.data["user"][0]
        this.me.picture = 'data:image/jpeg;base64, ' + this.me.picture
        this.picture = this.me.picture
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    login(){
      axios({
        method: "get",
        params: {},
        url: 'http://localhost:8000/main/clear_logIn/'
      }).then(res=> {
          console.log(res.data())
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });

      bus.$emit("toHomeView", 2)
      this.$router.push('/login')
    },
    selectLanguage(){
      if (this.value4==1){
        this.$i18n.locale = this.langen
        localStorage.lang = this.langen
      }else if (this.value4==2){
        this.$i18n.locale = this.langen
        localStorage.lang = this.langen
      }
    },
    openProfile() {

    }
  },
  mounted() {
    this.searchUser()
    bus.$on("toSideMenuANDHeader", (data)=>{
      this.loggedIn = data
    })
    bus.$on("toHeader", (data)=>{
      this.picture = data
    })

  }
}
</script>

<style scoped>
.head{
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
}
.mainTitle{
  text-align: center;
  width: 100%;
  height: 80px;
  line-height: 80px;
  font-family: Algerian;
  font-size: 44px;
  color: #fdb515;
  margin-left: 10px;
}
.subTitle{
  text-align: center;
  width: 100%;
  height: 50px;
  line-height: 50px;
  font-family: Algerian;
  font-size: 15px;
  color: whitesmoke
}
.me:hover{
  color: white !important;
  cursor: pointer;
}
.signIn{
  color: whitesmoke;
  border: solid 1px;
  border-radius: 5px;
  padding: 5px 5px 5px 5px
}
.signIn:hover{
  cursor: pointer;
}
.avatarModule{
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  margin-right: 20px
}
.avatarModule:hover{
  cursor: pointer;
}
</style>