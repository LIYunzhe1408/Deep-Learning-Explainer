<template>
  <div>
    <el-row gutter=20 type="flex" style="justify-content: center">
      <!-- Left -->
      <el-col  :span="9" >
        <div class="boxMain" style="height:500px;">
          <!-- DONE Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>INPUT IMAGE</b></div>
            <div style="font-size: 14px; color: gray">Choose one image to be predicted by <a href="https://deci.ai/deep-learning-glossary/deep-neural-network-dnn/" class="highlighted">Deep Neural Network</a></div>
          </div>


          <!-- TODO Move To Concept Extraction-->
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=selectedPic.src>
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          {{str}}
          <el-switch
              v-model="switched"
              active-text="Predict"
              @change="explainPic"
              style="margin-top: 20px">
          </el-switch>
        </div>
      </el-col>

      <!--DONE Middle-->
      <el-col  :span="6">
        <div class="boxMain" style="height:170px;">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>OUTPUT</b></div>
            <div style="font-size: 14px; color: gray">Classification result by the DNN below</div>
          </div>
          <!-- Output-->
          <div style="width:80%; height: 40px; border-left: 5px #1890ff solid; background-color: lightblue; text-align: center; line-height: 40px;
          margin-top: 30px; font-size: 18px">
            <span v-if="switched">
              <b>{{ selectedPic.class }} - {{selectedPic.id}} - {{selectModel}}</b>
            </span>
          </div>
        </div>

        <!-- Model -->
        <div class="boxMain" style=" height:310px;">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>DNN Model</b></div>
            <div style="font-size: 14px; color: gray">Pretrained Classification Model</div>
          </div>
          <el-tooltip placement="right">
            <div slot="content" style="display: flex; width:200px; flex-wrap: wrap">
              <el-image class="picBoxMain" style="width: 250px; height: 500px; display: flex; justify-content: center; align-items: center" :src="require('@/assets/googleNet.png')" />
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
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>EXPLANATION</b></div>
            <div style="font-size: 14px; color: gray">Determine which concept part contributes the most</div>
          </div>

          <div style="display: flex; width: 100%; height:80%; justify-content: space-evenly" >
            <el-image
                      class="picBoxMain"
                      style="height: 80%; width: 60%; margin-top: 40px"
                      :src=this.explainedPic />
            <div class="boxMain" style="width: 30%; height: 80%; margin-top: 40px;">
              <div style="margin-top: 20px; font-size: 20px; color: black"><b>Results</b></div>
              <div style="font-size: 12px; color: gray">Sorted By Contributions</div>
              <div style="height: 80%; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;" v-if="switched">
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
import bus from "@/common/bus"
export default {
  name: "Main",
  data() {
    return {
      predict: false,
      selectModel: '1',
      selectedPic:{src: require('@/assets/img-3.png'), id:'n02123045', class: 'tabby'},
      subPics: [
        {src: require('@/assets/img-3.png'), id:3},
        {src: require('@/assets/img-3.png'), id:3},
        {src: require('@/assets/img-3.png'), id:3},
        {src: require('@/assets/img-3.png'), id:3},
      ],
      explainedPic: '',
      switched: false
    }
  },
  methods: {
    explainPic() {
      this.explainedPic = this.switched ? require('@/assets/'+this.selectedPic.class+'.png') : ''
    },

  },
  mounted() {
      bus.$on("toMainPic", (data)=>{
        this.switched = false
        this.explainedPic = ''
        this.selectedPic = data
      })
      bus.$on("toMainModel", (data)=>{
        this.switched = false
        this.explainedPic = ''
        this.selectModel = data
      })


  },
  computed: {
    str: function () {
      this.subPics = []
      for (let i = 0; i < 8; i++) {
        this.subPics.push(this.selectedPic)
      }
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
.subPics{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 5px;
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center
}
</style>