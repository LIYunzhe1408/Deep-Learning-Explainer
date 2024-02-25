<template>
  <div>
    <el-row gutter=40 type="flex" style="justify-content: start; margin-left: 5px">
      <!-- Left -->
      <el-col  :span="12" >
        <div class="boxMain" style="height:200px; background-color: whitesmoke">
          <!-- DONE Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>Heatmap Contributions</b></div>
            <div style="font-size: 14px; margin-top: 10px">Built like a spreadsheet, project tables give you a live canvas to filter,</div>
            <div>sort, and group issues and pull requests. Tailor them to your needs with</div>
            <div>custom fields and saved views.</div>
            <span>
              <el-button style="margin-top: 20px; background-color: lightgray">Get Started</el-button>
              <el-button style="margin-top: 20px; background-color: lightgray" @click="compareHeatmap">Compare</el-button>
            </span>

          </div>
        </div>



        <div style="display: flex; flex-direction: column" v-if="compare">
          <div class="boxMain" style="height:210px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly">
            <div style="width:150px"><b>Object Level</b></div>
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>DeepLabV3</el-tag>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>FCN</el-tag>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>LARSPP</el-tag>
            </div>
          </div>







          <div class="boxMain" style="height:210px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly">
            <div style="width:150px"><b>Component Level</b></div>
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>DeepLabV3</el-tag>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>FCN</el-tag>
            </div>

            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
              <el-image
                  class="picBoxMain"
                  style="height: 140px; width: 140px; margin-bottom: 10px"
                  :src=this.explainedPic />
              <el-tag>LARSPP</el-tag>
            </div>
          </div>
        </div>
      </el-col>


      <el-col :span="11">
        <div style="display: flex; flex-direction: column;">
          <div style="flex:1;">
            <div class="boxMain" style="height:320px;">
              <div class="topicMain">
                <div style="font-size: 18px; margin-top: 20px"><b>Object Level Heatmap</b></div>

                <div style="display: flex; width: 100%; justify-content: start" >
                  <el-image
                      class="picBoxMain"
                      style="height: 230px; width: 230px; margin-top: 20px"
                      :src=this.explainedPic />
                  <div class="boxMain" style="width: 220px; height: 230px; margin-top: 20px; margin-left: 20px">
                    <div style="margin-top: 20px; font-size: 20px; color: black"><b>Results</b></div>
                    <div style="font-size: 12px; color: gray">Sorted By Contributions</div>
                    <div style="height: 80%; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;" v-if="true">
                      <el-tag class="tagContribution" type="danger" color="red" effect="dark">Tabby</el-tag>
                      <el-tag class="tagContribution" type="danger"  color="red" effect="dark" style="opacity: 60%">Background</el-tag>
                      <el-tag class="tagContribution" type="danger" color="red" effect="dark" style="opacity: 20%">Else</el-tag>
                    </div>
                  </div>
                </div>

              </div>
            </div>
            <div style="width: 95%;"><el-divider></el-divider></div>
          </div>
          <div style="flex:1">
            <div class="boxMain" style="height:320px;">
              <div class="topicMain">
                <div style="font-size: 18px; margin-top: 20px"><b>Component Level Heatmap</b></div>

                <div style="display: flex; width: 100%; justify-content: start" >
                  <el-image
                      class="picBoxMain"
                      style="height: 230px; width: 230px; margin-top: 20px"
                      :src=this.explainedPic />
                  <div class="boxMain" style="width: 220px; height: 230px; margin-top: 20px; margin-left: 20px">
                    <div style="margin-top: 20px; font-size: 20px; color: black"><b>Results</b></div>
                    <div style="font-size: 12px; color: gray">Sorted By Contributions</div>
                    <div style="height: 80%; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;" v-if="true">
                      <el-tag class="tagContribution" type="danger" color="red" effect="dark">Head</el-tag>
                      <el-tag class="tagContribution" type="danger"  color="red" effect="dark" style="opacity: 60%">Breast</el-tag>
                      <el-tag class="tagContribution" type="danger" color="red" effect="dark" style="opacity: 20%">Body</el-tag>
                    </div>
                  </div>
                </div>
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
  name: "MainExplanation",
  data() {
    return {
      compare: false,
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
    compareHeatmap() {
      this.compare = !this.compare
    }

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
  width: 100px;
  height: 30px;
  text-align: center;
  line-height: 30px;
  font-size: 14px;
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