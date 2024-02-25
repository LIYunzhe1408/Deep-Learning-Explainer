<template>
  <div>
    <el-row gutter=40 type="flex" style="justify-content: center">
      <!-- Left -->
      <el-col  :span="7" >
        <div class="boxMain" style="height:500px;">
          <!-- DONE Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>IMAGE LEVEL</b></div>
            <div style="font-size: 14px; color: gray">Handle Image</div>
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

        </div>
      </el-col>

      <!--DONE Middle-->
      <el-col  :span="7">
        <div class="boxMain" style="height:500px;">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>OBJECT LEVEL</b></div>
            <div style="font-size: 14px; color: gray">Concepts After Semantic Segmentation</div>
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
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </el-tooltip>
        </div>
      </el-col>

      <!--Right-->
      <el-col  :span="7">
        <div class="boxMain" style="width: 100%; height:500px; ">
          <!-- Topic-->
          <div class="topicMain">
            <div style="font-size: 24px; margin-top: 20px"><b>COMPONENT LEVEL</b></div>
            <div style="font-size: 14px; color: gray">Concepts After Superpixel Segmentation</div>
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
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </el-tooltip>

        </div>
      </el-col>
    </el-row>
    <el-row style="display: flex; justify-content: end; margin-right: 120px">
<!--      <el-button icon="el-icon-view">Tree</el-button>-->
      <el-button icon="el-icon-search">Compare</el-button>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"
export default {
  name: "MainExtraction",
  data() {
    return {
      predict: false,
      selectModel: '1',
      selectedPic:{src: require('@/assets/img-3.png'), id:'n02123045', class: 'tabby'},
      semanticPic:{src: require('@/assets/tabby/Semantic Segmentation/6.png')},
      pixelPic: {src: require('@/assets/tabby/SuperPixel Segmentation/6-p.png')},
      subSSPics: [
        {src: require('@/assets/tabby/Semantic Segmentation/6-0.jpg'), id:3},
        {src: require('@/assets/tabby/Semantic Segmentation/6-1.jpg'), id:3},
      ],
      subPSPics: [
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-0.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-1.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-2.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-3.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-4.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-5.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-6.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-7.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-8.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-9.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-0-10.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-0.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-1.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-2.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-3.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-4.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-5.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-6.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-7.jpg'), id:3},
        {src: require('@/assets/tabby/SuperPixel Segmentation/6-1-8.jpg'), id:3}
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
      // this.subPics = []
      // for (let i = 0; i < 8; i++) {
      //   this.subPics.push(this.selectedPic)
      // }
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