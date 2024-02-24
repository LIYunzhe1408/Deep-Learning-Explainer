<template>
  <div>
    <el-row gutter=40 type="flex" style="justify-content: center">
      <el-col  :span="7" >
        <div class="boxMain" style="height:500px;">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>INPUT IMAGE</b></div>
            <div style="font-size: 14px; color: gray">Choose one image to be predicted by <a href="https://deci.ai/deep-learning-glossary/deep-neural-network-dnn/" class="highlighted">Deep Neural Network</a></div>
          </div>
          <el-tooltip placement="right">
            <div slot="content" style="display: flex; width:200px; flex-wrap: wrap">
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
              <el-image class="picBoxMain" style="width: 50px; height: 50px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src=Src3 />
            </div>
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=Src3>
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </el-tooltip>

          <el-switch
              v-model="switched"
              active-text="Predict">
          </el-switch>


        </div>
      </el-col>

      <!--Middle-->
      <el-col  :span="5">
        <div class="boxMain" style="height:170px;">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>OUTPUT</b></div>
            <div style="font-size: 14px; color: gray">Classification result by the DNN below</div>
          </div>
          <div style="width:60%; height: 40px; border-left: 5px #1890ff solid; background-color: lightblue; text-align: center; line-height: 40px;
          margin-top: 30px; font-size: 18px">
            <b>Tabby</b>
          </div>
<!--          <el-input-->
<!--              placeholder="Tabby"-->
<!--              :disabled="true"-->
<!--              style="width: 60%; margin-top: 40px">-->
<!--          </el-input>-->
        </div>
        <div class="boxMain" style=" height:310px;">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>DNN Model</b></div>
            <div style="font-size: 14px; color: gray">Pretrained Classification Model</div>
          </div>
          <el-tooltip placement="right">
            <div slot="content" style="display: flex; width:200px; flex-wrap: wrap">
              <el-image class="picBoxMain" style="width: 250px; height: 500px; margin-top: 40px; display: flex; justify-content: center; align-items: center" :src="require('@/assets/googleNet.png')" />
            </div>
          <el-image
              style="width: 180px; height: 160px; margin-top: 20px; margin-bottom: 20px"
              :src="require('@/assets/model.png')" />
          </el-tooltip>
          <el-tag effect="dark">GoogleNet</el-tag>
        </div>
      </el-col>

      <!--Right-->
      <el-col  :span="9">
        <div class="boxMain" style="width: 100%; height:500px; ">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>EXPLANATION</b></div>
            <div style="font-size: 14px; color: gray">Determine which concept part contributes the most</div>
          </div>

          <div style="display: flex; width: 100%; justify-content: space-evenly">
            <el-image class="picBoxMain"
                      style="height: 350px; width: 350px; margin-top: 40px"
                      :src="require('@/assets/cat.png')" />
            <div class="boxMain" style="width: 220px; margin-top: 40px;">
              <div style="margin-top: 20px; font-size: 20px; color: black"><b>Results</b></div>
              <div style="font-size: 12px; color: gray">Sorted By Contributions</div>
              <div style="height: 80%; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center; background-color:">
                <el-tag class="tagContribution" type="danger" color="red" effect="dark">Head</el-tag>
                <el-tag class="tagContribution" type="danger"  color="red" effect="dark" style="opacity: 60%">Breast</el-tag>
                <el-tag class="tagContribution" type="danger" color="red" effect="dark" style="opacity: 20%">Body</el-tag>
              </div>
            </div>
          </div>

        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Main",
  data() {
    return {
      predict:'',
      selectedPicSrc: this.Src3,
      Src3: require('@/assets/img-3.png'),
      switched: false
    }
  },
  methods: {
    selectPredict() {
      console.log(this.predict)
    }
  }
}
</script>

<style scoped>
.boxMain{
  margin-bottom: 20px;
  background-color: white;
  border: gray ;
  border-radius: 10px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  width: 100%;
  align-items: center;
  justify-content: flex-start;
  display: flex;
  flex-direction: column
}
.picBoxMain{
  margin-bottom: 20px;
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
}
.el-icon-picture-outline{
  font-size: 200px;
}
.tagContribution{
  width: 120px;
  height: 40px;
  text-align: center;
  line-height: 40px;
  font-size: 16px;
}
.topicMain{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-left:80px;
  width: 100%;
}
.highlighted:hover{
  color: #0a66c2;
  text-decoration: underline;
}
.highlighted{
  color: #0a66c2;
  text-decoration-line: none
}
</style>