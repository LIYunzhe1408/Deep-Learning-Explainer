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
        The right side of the options bar provides <b>category selection</b>, with available categories including sorrel horse and bulbul.
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The image semantic segmentation model selection bar offers three models: deeplabv3, fcn, and lraspp.
      </p>

      <p class="dialogText" style="font-size: 20px;">
        <b>Function Bar Introduction</b>
      </p>
      <p class="dialogText" style="font-size: 18px;">
        The <b>Concept Tree Construction Module</b> clusters different hierarchical image knowledge extracted from the same category. There is a hierarchical relationship between different levels. The clustered groups can be represented as understandable concepts, facilitating the calculation and explanation of each concept's contribution.
      </p>
      <p class="dialogText" style="font-size: 18px; color: #1890ff">
        <b><i>You can hover over the leaf nodes to view segmented images.</i></b>
      </p>

      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center">
        <el-button style="font-size:18px; background-color: #003262; color: white; padding: 15px; border-radius: 10px" @click="dialogVisible = false">Close</el-button>
      </div>
    </el-dialog>

    <div class="box">
      <OptionTree/>
    </div>

    <div style="display: flex; justify-content: start; margin-bottom: 20px; margin-left: 80px">
      <el-button @click="dialogVisible=true">Module Tips</el-button>
    </div>

    <MainTree/>

  </div>
</template>

<script>
import OptionTree from "@/components/OptionTree";
import MainTree from "@/components/MainTree";
export default {
  name: "Tree",
  components: {MainTree, OptionTree},
  data(){
    return{
      dialogVisible: true
    }
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