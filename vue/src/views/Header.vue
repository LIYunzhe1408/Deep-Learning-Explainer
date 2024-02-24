<template>
  <div class="head">
    <el-row style="background-color: #1b1f23">
      <el-col :span="3">
        <div class="mainTitle">EXPLAINER</div>
      </el-col>

      <el-col :span="3">
        <div class="subTitle" style="font-size: 15px; height:30px">HIERARCHICAL CONCEPT-BASED</div>
        <div class="subTitle" style="font-family: Britannic"><i>Figure Out What DNN Is Doing</i></div>
      </el-col>

      <el-col :span="13">
        <div style="width: 100%; height: 80px;"></div>
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
          <div style="display: flex; flex-direction: column; justify-content: flex-end; align-items: center;  margin-right: 20px">
            <el-avatar  :size="40" :src="require('@/assets/avatar.jpg')"></el-avatar>
              <div class="me" style="color: lightgray; font-size: 14px" @click="openProfile">Me
              <i class="el-icon-caret-bottom"></i>
              </div>

          </div>

        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
export default {
  name: "Header",
  methods: {
    openProfile() {

    }
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
  font-size: 40px;
  color: whitesmoke;
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
</style>