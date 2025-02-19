<template>
  <div>
    <el-dialog
        :visible.sync="dialogVisible"
        width="50%"
        :show-close="false"
        custom-class="addMicroDialog">
      <template slot="title">
        <div style="display: flex; align-items: center; justify-content: space-between">
          <b style="color:black; font-size: 28px">Module Tips</b>
          <div class="close" @click="dialogVisible=false">
            <i class="el-icon-close"></i>
          </div>
        </div>
      </template>
      <p class="dialogText" style="font-size: 20px;">
        <b>Options Bar Introduction</b>
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The left side of the options bar provides <b>various images of the same category</b>, with the default category being the tabby cat.
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The right side of the options bar offers <b>category selection</b>, with available options including sorrel horse and bulbul.
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The image semantic segmentation model selection bar offers three models: deeplabv3, fcn, and lraspp.
      </p>

      <p class="dialogText" style="font-size: 20px;">
        <b>Function Bar Introduction</b>
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The left side of the function bar displays the <b>multi-level knowledge acquisition results</b> for the current image of the selected category, along with the <b>heatmap showing the contribution of each concept to the image category</b>. From top to bottom, these represent the object level and component level.
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The right side of the function bar displays the <b>current image of the selected category</b>, along with the <b>contribution scores and concept names</b> at different levels. The scores decrease from top to bottom, with higher scores indicating a greater contribution of the concept to the image category.
      </p>

      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center">
        <el-button style="font-size:18px; background-color: #003262; color: white; padding: 15px; border-radius: 10px" @click="dialogVisible = false">Close</el-button>
      </div>
    </el-dialog>

    <div v-if="!chosen">
      <div class="box">
        <optionLocalExplanation/>
      </div>
      <mainLocalExplanation/>
    </div>
  </div>
</template>


<script>
import optionLocalExplanation from "@/components/OptionLocalExplanation";
import mainLocalExplanation from "@/components/MainLocalExplanation";
import bus from "@/common/bus";
export default {
  name: "Explanation",
  components: {mainLocalExplanation, optionLocalExplanation},
  data(){
    return{
      chosen: false,
      dialogVisible: true
    }
  },
  methods: {
    changeStatus(){
      this.chosen = !this.chosen
    }
  },
  mounted() {
    bus.$on("toLocalEX", (data)=>{
      this.dialogVisible = data
    })
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