<template>
  <div>

    <div v-if='chosen'>
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
          The left side of the options bar provides <b>various images of the same category</b>, with the default category being tabby cat.
        </p>
        <p class="dialogText" style="font-size: 18px;">
          The right side of the options bar offers <b>category selection</b>, with available options including sorrel horse and bulbul.
        </p>
        <p class="dialogText" style="font-size: 18px;">
          Additionally, the models available in the <b>image semantic segmentation model selection bar</b> depend on your choice in the previous step. If needed, you can click the <b style="color: #1890ff">Return</b> button at the bottom of this module to reselect a model.
        </p>

        <p class="dialogText" style="font-size: 20px;">
          <b>Function Bar Introduction</b>
        </p>
        <p class="dialogText" style="font-size: 18px;">
          The <b>Hierarchical Knowledge Acquisition Module</b> performs <b>semantic segmentation and superpixel segmentation</b> on the input image, dividing the original image into <b>object-level</b> and <b>component-level</b> patches and fragments. This enables the extraction of knowledge at different levels for further processing.
        </p>

        <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center">
          <el-button style="font-size:18px; background-color: #003262; color: white; padding: 15px; border-radius: 10px" @click="dialogVisible = false">Close</el-button>
        </div>
      </el-dialog>

      <div class="box">
        <optionExtraction/>
      </div>
      <MainExtraction/>
    </div>
    <div v-if="!chosen">
      <ComparisonExtraction></ComparisonExtraction>
    </div>
    <el-row style="margin-top: 20px;">
      <el-col :span="19">
        <div style="width: 100%; height: 80px;"></div>
      </el-col>
      <el-col :span="4">
        <el-button v-if="chosen" @click="dialogVisible=true">Module Tips</el-button>
        <el-button v-if="!chosen" type="primary" @click="changeStatus">{{$t('utils.confirm')}}</el-button>
        <el-button v-if="chosen" type="primary" @click="changeStatus">{{$t('utils.return')}}</el-button>
      </el-col>
    </el-row>

  </div>

</template>

<script>
import optionExtraction from "@/components/OptionExtraction";
import MainExtraction from "@/components/MainExtraction";
import ComparisonExtraction from "@/components/ComparisonExtraction";
export default {
  name: "Extraction",
  components: {
    MainExtraction,
    optionExtraction,
    ComparisonExtraction
  },
  data(){
    return {
      chosen: false,
      dialogVisible: false
    }
  },
  methods: {
    changeStatus(){
      this.chosen = !this.chosen
      if (this.chosen)
        this.dialogVisible = true
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