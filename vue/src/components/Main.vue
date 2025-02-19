<template>
  <div>
    <el-row gutter=20 type="flex" style="justify-content: center">
      <!-- Left -->
      <el-col  :span="9" >
        <div class="boxMain" style="height:500px;">
          <!-- DONE Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('main.MainInput')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('main.MainInputHint')}}<a href="https://deci.ai/deep-learning-
            glossary/deep-neural-network-dnn/" class="highlighted">{{$t('main.MainInputHintHyper')}}<i class="el-icon-share"></i></a></div>
          </div>


          <!-- TODO Move To Concept Extraction-->
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=selectedPic.src>
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
            <el-switch
              class="switchStyle"
              v-model="switched"
              :active-text="$t('main.MainPredict')"
              @change="explainPic"
              style="margin-top: 20px; zoom: 1.2">
            </el-switch>
        </div>
      </el-col>

      <!--DONE Middle-->
      <el-col  :span="6">
        <div class="boxMain" style="height:170px;">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('main.MainOutput')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('main.MainOutputHint')}}</div>
          </div>
          <!-- Output-->
          <div style="width:80%; height: 40px; border-left: 5px #1890ff solid; background-color: lightblue;
          text-align: center; line-height: 40px;
          margin-top: 30px; font-size: 18px">
            <span v-if="switched">
              <b>{{ selectedPic.class }}</b>
            </span>
          </div>
        </div>

        <!-- Model -->
        <div class="boxMain" style=" height:310px;">
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('main.MainDNN')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('main.MainDNNHint')}}</div>
          </div>
          <el-tooltip placement="right">
            <div slot="content" style="display: flex; width:200px; flex-wrap: wrap">
              <el-image class="picBoxMain" style="width: 250px; height: 500px; display: flex; justify-content: center;
              align-items: center" :src="require('@/assets/googleNet.png')" />
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
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('main.MainEX')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('main.MainEXHint')}}</div>

            <div style="font-size: 14px; color: gray">The deeper the <b style="color: #ff0d57">red</b>, the more <b style="color: #ff0d57">positive</b>, the concept's influence on decision.</div>
            <div style="font-size: 14px; color: gray">The deeper the <b style="color: #007bc9">blue</b>, the more <b style="color: #007bc9">negative</b> the influence.</div>
          </div>


          <div style="display: flex; width: 100%; height:80%; justify-content: space-evenly" >
            <el-image
                      class="picBoxMain"
                      style="height: 80%; width: 60%; margin-top: 20px"
                      :src=this.explainedPic.src >
              <div slot="error" class="image-slot" style="text-align: center; line-height: 300px; font-size: 14px">
                <b>Please click 'Start Prediction' in first column</b>
              </div>
            </el-image>
            <div class="boxMain" style="width: 30%; height: 80%; margin-top: 20px;">
              <div style="margin-top: 20px; font-size: 20px; color: black"><b>{{$t('main.MainResults')}}</b></div>
              <div style="font-size: 12px; color: gray">{{$t('main.MainResultsHint')}}</div>
              <div style="height: 80%; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;" v-if="switched">
                <el-tag class="tagContribution" type="danger" color="red" effect="dark">{{ this.explainedPic.contributors.high }}</el-tag>
                <el-tag class="tagContribution" type="danger"  color="red" effect="dark" style="opacity: 60%">{{ this.explainedPic.contributors.medium }}</el-tag>
                <el-tag class="tagContribution" type="danger" color="red" effect="dark" style="opacity: 20%">{{ this.explainedPic.contributors.low }}</el-tag>
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
import axios from 'axios';
export default {
  name: "Main",
  data() {
    return {
      // Get from optionMain.vue
      selectedModel: {label: "deeplabv3", id: '1'},
      selectedPic:{src: require('@/assets/image data/mainline/tabby/handle image/6.jpg'), id:'6', class: 'tabby'},
      switched: false,
      predict: false,

      // DONE 0420 TODO [1] Get from backend
      explainedPic: {src:'', contributors:{high:'', medium:'', low:''}},
      // DONE 0420 TODO [2] Get from backend, need new script to get prediction label. Replace this.selectedPic.class to show in OUTPUT.
      predictedLabel: 'tabby'
    }
  },
  methods: {
    explainImage() {
      console.log(this.selectedModel.label, this.selectedPic.class)
      axios({
        method: "get",
        params: {model: this.selectedModel.label, class: this.selectedPic.class},
        url: 'http://localhost:8000/main/explain_image/'
      }).then(res=> {
        console.log(res)

        let potential_explainedPic = res.data;
        potential_explainedPic.src = 'data:image/jpeg;base64,' + res.data.src;
        this.explainedPic = this.switched ? potential_explainedPic : ''
        console.log(potential_explainedPic)
      })
    },
    explainPic() {
      this.explainImage()
    },

  },
  mounted() {
      bus.$on("toMain", (selectedPic)=>{
        if (this.selectedPic !== selectedPic){
          this.switched = false
          this.explainedPic = ''
          this.selectedPic = selectedPic
        }
      })
      bus.$on("toMainModel", (selectedModel)=>{
        if (this.selectedModel !== selectedModel) {
          this.switched = false
          this.explainedPic = ''
          this.selectedModel = selectedModel
        }
      })
    console.log("model: ", this.selectedModel)
  },
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
</style>