<template>
    <div style="display: flex; flex-direction: column;align-items: center">

      <div class="boxMain" style="width: 70%; background-color: whitesmoke">
        <!-- DONE Topic-->
        <div class="topicMain">
          <div style="font-size: 24px; margin-top: 20px"><b>{{$t('extraction.topic')}}</b></div>
          <div style="font-size: 16px; margin:20px 80px 20px 80px; width: 80%">
            <p>{{$t('extraction.sentence-1')}}</p>
            <p>{{$t('extraction.sentence-2')}}</p>
            <p style="margin-top: 5px">{{$t('extraction.sentence-3')}}</p>

            <div style="margin-top: 10px;">
              <b>{{$t('extraction.sentence-4')}}</b>
              <p style="">{{$t('extraction.sentence-5')}}</p>
              <p style="">{{$t('extraction.sentence-6')}}</p>
              <p style="">{{$t('extraction.sentence-7')}}</p>
            </div>
          </div>
        </div>
      </div>

      <el-table style="width: 70%" :data="modelData" stripe @selection-change="handleSelectionChange">
        <el-table-column
            prop="modelName"
            :label="$t('extraction.modelName')"
            width="180"
            align="center">
        </el-table-column>
        <el-table-column
            prop="PixelAccuracy"
            :label="$t('extraction.PixelAccuracy')"
            width="180"
            align="center">
        </el-table-column>
        <el-table-column
            prop="MIoU"
            :label="$t('extraction.MIoU')"
            width="180"
            align="center">
        </el-table-column>
        <el-table-column :label="$t('extraction.Image')" align="center">
          <template slot-scope="scope">
            <el-image
                style="height: 80px"
                :src="getImgUrl(scope.row)"
                :preview-src-list="Object.values(SegSample.src)">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column
            type="selection"
            width="55">
        </el-table-column>

      </el-table>

<!--      <el-row style="margin-top: 20px;">-->
<!--        <el-col :span="19">-->
<!--          <div style="width: 100%; height: 30px"></div>-->
<!--        </el-col>-->
<!--        <el-col :span="4">-->
<!--          <el-button type="primary" disabled>{{$t('extraction.change')}}</el-button>-->
<!--        </el-col>-->
<!--      </el-row>-->
    </div>
</template>

<script>
import bus from "@/common/bus"
import axios from "axios";
export default {
  name: "ComparisonExtraction",
  data(){
    return {
      modelData:[],

      // TODO Get from backend - 240420 DONE
      SegSample: {},
      selectedModels: [{label:'deeplabv3', id:'1'}]
    }
  },
  methods:{
    init() {
      // modelData, SegSample
      axios.get('http://localhost:8000/main/get_seg_sample/')
          .then(response => {
            this.SegSample = response.data
            for (let name in this.SegSample.src)
            {
              this.SegSample.src[name] = 'data:image/jpeg;base64,' + this.SegSample.src[name];
            }
          })
          .catch(error => {
            console.error('Error fetching image', error);
          });
      axios.get('http://localhost:8000/main/get_seg_metrics/')
          .then(response => {
            this.modelData = response.data
          })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    getImgUrl(row){
      return(this.SegSample.src[row.modelName])
    },
    handleSelectionChange(rows){
      this.selectedModels = []
      for (let i=0; i < rows.length; i++){
        let modelName = rows[i].modelName
        let id =  rows[i].id
        this.selectedModels.push({label:modelName, id:id})
      }
    },
  },
  // TODO Get this.SegSample from backend
  created() {
    this.init()
  },
  beforeDestroy() {
    bus.$emit("toOptionEx", this.selectedModels);
  }
}
</script>

<style scoped>
.boxMain{
  margin-bottom: 40px;
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
.topicMain{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /*margin-left:80px;*/
  width: 100%;
}
</style>