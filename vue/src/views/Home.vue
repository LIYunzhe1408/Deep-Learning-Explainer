<template>
  <div>
      <el-dialog
          :visible.sync="dialogVisible"
          width="50%"
          :show-close="false"
          custom-class="addMicroDialog">
        <template slot="title">
          <div style="display: flex; align-items: center; justify-content: space-between">
            <b  style="color:black; font-size: 28px">Module Tips</b>
            <div class="close" @click="dialogVisible=false">
              <i class="el-icon-close" ></i>
            </div>
          </div>
        </template>
        <p class="dialogText" style="font-size: 20px;">
          <b>Options Bar Introduction</b>
        </p>
        <p class="dialogText" style="font-size: 18px;">
          The options bar provides <b>various image category data</b>, such as tabby cats, sorrel horses, and bulbuls. Additionally, as the foundation of the explanation method, knowledge acquisition based on image semantic segmentation plays a crucial role. The options bar offers <b>three semantic segmentation models</b>, allowing users to observe how different segmentation models impact the basis of explanations.
        </p>
        <p class="dialogText" style="font-size: 20px;">
          <b>Function Bar Introduction</b>
        </p>
        <p class="dialogText" style="font-size: 18px;">
          The main functional module processes the input image data, presents the prediction results of the deep neural network <b>GoogLeNet</b>, and visualizes the explanation of GoogLeNet's decision using the <b>Hierarchical Concept Embedding (HCE) method</b> through a heatmap. To obtain the explanation, click <b>Start Prediction</b> below the input image.
        </p>

        <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center">
          <el-button style="font-size:18px; background-color: #003262; color: white; padding: 15px; border-radius: 10px" @click="dialogVisible = false">Close</el-button>
        </div>

      </el-dialog>

    <div class="box">
      <Option/>
    </div>
    <Main/>
    <div style="display: flex; justify-content: center">
      <el-button @click="dialogVisible=true">Module Tips</el-button>
    </div>

  </div>
</template>

<script>
import Option from "@/components/OptionMain";
import Main from "@/components/Main";
import bus from "@/common/bus";
import axios from "axios";
export default {
  name: "home",
  components: {
    Option,
    Main
  },
  data(){
    return{
      dialogVisible: true
    }
  },
  methods:{
  },
  mounted() {
  }
}
</script>

<style scoped>
.box{
  margin: 0 10px 40px 10px;
  background-color: white;
  padding-left: 10px;
  border: gray ;
  border-radius: 10px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
}

.close{
  width: 50px;
  height: 50px;
  text-align: center;
  line-height: 50px;
  font-size: 20px
}

.close:hover{
  cursor: pointer;
  border: #003262 solid 2px;
}
/deep/.addMicroDialog {
  border-radius: 10px;
  border: white solid 2px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  /*height: 700px !important;*/
  /*overflow-y: scroll;*/
}

.dialogText{
  color: black;
  line-height: 30px;
  padding: 0 20px 0 20px
}
</style>
