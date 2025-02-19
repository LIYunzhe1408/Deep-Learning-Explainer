<template>
  <div style="width: 100%;justify-content: center; display: flex; margin-top: 32px; flex-direction: column; align-items: center">
    <div style="width: 16%;">
      <div style="text-align: center; margin-bottom: 32px">
        <el-avatar :src="require('@/assets/HCE.png')" :size="70"></el-avatar>
      </div>

      <h1 style="color:#1F2328; text-align: center; font-family: Cambria; margin-bottom: 32px">{{$t('logIn.signInHint')}}</h1>
      <div v-if="showErrorMessage===1" style="background-color: #ffebe9; padding: 16px; border-radius: 6px; border: #ff818266 solid 1px">
        Incorrect username or password.
        <span class="close">
          <el-icon  @click.native="closeError" class="el-icon-close"></el-icon>
        </span>

      </div>
      <div style="background-color: #F6F8FA;
                border-radius: 5px;
                margin-top: 16px;
                border:#d0d7deb3 solid 1px;
                font-size: 14px;
                width: 100%;
                padding:16px">
        <label style="margin-bottom: 8px; text-align: left; display: block; font-size: 14px; font-family: Arial; line-height: 1.5">{{$t('logIn.userHint')}}</label>
        <el-input style="margin-bottom: 16px" v-model="userName">

        </el-input>

        <div style="display:flex; justify-content: space-between">
          <label style="margin-bottom: 8px; text-align: left; display: block; font-size: 14px; font-family: Arial; line-height: 1.5">{{$t('logIn.password')}}</label>
          <div class="hint" style="text-align: right; font-family: Arial; line-height: 1.5" >{{$t('logIn.passwordHint')}}</div>
        </div>

        <el-input style="margin-bottom: 16px" v-model="password" show-password>

        </el-input>
        <el-button v-if="show===0" class="signInBtn" @click="checkLogIn">{{$t('logIn.signIn')}}</el-button>
        <el-button v-if="show===1" class="signInBtn" style="opacity: 60%" @click="checkLogIn">{{$t('logIn.signIning')}}</el-button>
      </div>


      <div style="border-radius: 5px;
                margin-top: 16px;
                border:#d0d7deb3 solid 1px;
                padding:16px;
                width: 100%;
                font-size: 14px;
                color: #0969DA;
                line-height: 26px;
                text-align: center">
<!--        <div><b>Sign in with a passkey</b></div>-->
        <div><span style="color: black">{{$t('logIn.newToHCE')}}</span> {{$t('logIn.createAccount')}}</div>
      </div>
    </div>


  </div>
</template>

<script>
import bus from "@/common/bus";
import axios from "axios";

export default {
  name: "LogIn",
  data(){
    return{
      userName:'liyunzhe.jonas@outlook.com',
      password:'',
      loggedIn: 0,
      showErrorMessage: 0,
      show: 0
    }
  },
  methods: {
    closeError(){
      this.showErrorMessage = 0
    },
    checkLogIn(){
      this.show = 1
      axios({
        method: "get",
        params: {user_name: this.userName, password: this.password},
        url: 'http://localhost:8000/main/check_loggedIn/'
      }).then(res=> {
          this.searchUser()
          console.log(res.data)
          if (res.data["verification"]){
            this.loggedIn = 1
            this.$router.push('/home')
            bus.$emit("toHomeView", 2)
            bus.$emit("toSideMenuANDHeader", this.loggedIn)
            setTimeout(() => {
              bus.$emit("toSideMenuANDHeader", this.loggedIn)
            }, 100);
          } else{
            this.show = 0
            this.showErrorMessage = 1
            // this.$message.error("Incorrect username or password.");
          }
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    searchUser(){
      axios({
        method: "get",
        params: {},
        url: 'http://localhost:8000/main/add_user/'
      }).then(res=> {
        this.me = res.data["user"][0]
        this.me.picture = 'data:image/jpeg;base64, ' + this.me.picture
        setTimeout(() => {
          bus.$emit("toHeader", this.me.picture)
        }, 100);
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
  },
  beforeDestroy() {
    // bus.$emit("toSideMenuANDHeader", this.loggedIn)
  },
}
</script>

<style scoped>
.signInBtn{
  background-color: #1F883D;
  color: white;
  width: 100%;
  font-size: 14px;
  border-radius: 6px;
  font-family: Arial;
}
.hint{
  color: #0969DA;
  text-align: right;
  font-size: 12px;
}
.hint:hover{
  cursor: pointer;
}
.close{
  color: red;
  font-size: 16px;
  float: right;
  font-weight: bold;
}
.close:hover{
  cursor: pointer;
}
</style>