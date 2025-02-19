<template>
  <div>
    <el-row gutter=40 type="flex" style="justify-content: center">
      <!-- Left -->
      <el-col  :span="7" >
        <div class="boxMain" style="height:500px;">
          <!-- DONE Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('level.imageLevel')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('level.imageLevelHint')}}</div>
          </div>


          <!-- TODO Move To Concept Extraction-->
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=selectedPic.src>
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>

        </div>
      </el-col>

      <!--DONE Middle-->
      <el-col  :span="7">
        <div class="boxMain" style="height:500px;">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('level.objectLevel')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('level.objectLevelHint')}}</div>
          </div>
          <!-- Output-->
          <el-tooltip placement="left">
            <div slot="content" style="display: flex; max-width:400px; flex-wrap: wrap; justify-content: stretch; ">
              <div v-for="value in subSSPics" :key="value.id">
                <el-image class="subPics" :src="value.src" />
              </div>
            </div>
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=semanticPic.src>
              <div slot="error" class="image-slot" style="text-align: center; line-height: 300px; font-size: 16px">
                <b>Please select an image</b>
              </div>
            </el-image>
          </el-tooltip>
          <el-tag>Hover over the image to view details</el-tag>

        </div>
      </el-col>

      <!--Right-->
      <el-col  :span="7">
        <div class="boxMain" style="width: 100%; height:500px; ">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>{{$t('level.componentLevel')}}</b></div>
            <div style="font-size: 14px; color: gray">{{$t('level.componentLevelHint')}}</div>
          </div>

          <el-tooltip placement="right">
            <div slot="content" style="display: flex; max-width:400px; flex-wrap: wrap; justify-content: stretch">
              <div v-for="value in subPSPics" :key="value.id">
                <el-image class="subPics" :src="value.src" />
              </div>
            </div>
            <el-image class="picBoxMain"
                      style="width: 300px; height: 300px; margin-top: 40px; display: flex; justify-content: center; align-items: center"
                      :src=pixelPic.src>
              <div slot="error" class="image-slot" style="text-align: center; line-height: 300px; font-size: 16px">
                <b>Please select an image</b>
              </div>
            </el-image>
          </el-tooltip>
          <el-tag>Hover over the image to view details</el-tag>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"
import axios from "axios";

export default {
  name: "MainExtraction",
  data() {
    return {
      selectedClass: '',
      selectedModel: '',
      selectedPic:{src: require('@/assets/image data/mainline/tabby/handle image/6.jpg'), id:'6', class: 'tabby'},
      semanticPic:'',
      pixelPic: '',
      subSSPics: '',
      subPSPics: ''
    }
  },
  methods: {
    // getImgs(){semanticPic, pixelPic, subsspics, subpspics},
    resetImages(){
      // 初始，换pic，换model，换class
      let params = {class: this.selectedPic.class, model: this.selectedModel.label, imageNum: this.selectedPic.id}
      axios({
        method: "get",
        params: params,
        url: 'http://localhost:8000/main/get_extraction_pics/'
      }).then(res=> {
        // console.log(res.data)
        this.subSSPics = res.data["SS"]

        this.semanticPic = res.data["semanticPic"]
        this.pixelPic = res.data["pixelPic"]
        this.semanticPic.src = 'data:image/jpeg;base64,' + this.semanticPic.src
        this.pixelPic.src = 'data:image/jpeg;base64,' + this.pixelPic.src
        for (let i = 0; i < this.subSSPics.length; i++){
          this.subSSPics[i].src = 'data:image/jpeg;base64,' + this.subSSPics[i].src
        }

        this.subPSPics = res.data["PS"]
        for (let i = 0; i < this.subPSPics.length; i++){
          this.subPSPics[i].src = 'data:image/jpeg;base64,' + this.subPSPics[i].src
        }
        // console.log(this.semanticPic)
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    }
  },
  mounted() {
    // this.resetImages()
  },
  beforeMount() {

    bus.$on("toExtractionInit", (data)=>{
      console.log('hhhhhhhhhhhhhhhhhhhhhhhhh', data)
      this.selectedPic = data.defaultPic
      this.selectedClass = data.selectedClass

      this.resetImages()
    })
    bus.$on("toExtractionModel", (data)=>{
      console.log('aaaaaaaaaaa', data)
      this.selectedModel = data

      this.resetImages()
    })
    bus.$on("toEXPic", (data)=>{
      console.log('sssssssssss', data)
      this.selectedPic = data
      this.resetImages()
    })
    bus.$on("toEXModel", (data)=>{
      console.log('dddddddddddd', data)
      this.selectedModel = data
      this.resetImages()
    })
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