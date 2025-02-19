<template>
  <div>
    <el-row>

      <!-- DONE Transition Column-->
      <el-col :span="15">
        <div style="width:100%; height: 120px;display: flex;  justify-content: space-evenly; align-items: center">
          <div class="topicMain" style="background-color: darkorange; width: 18%; display: flex; align-items: center">
            <div class="treeTitle"><b>{{$t('level.imageLevel')}}</b></div>
          </div>
          <div class="topicMain" style="background-color: #42b983; width: 18%; display: flex; align-items: center">
            <div class="treeTitle"><b>{{$t('level.objectLevel')}}</b></div>
          </div>
          <div class="topicMain" style="background-color: #1890ff; width: 18%; display: flex; align-items: center">
            <div class="treeTitle"><b>{{$t('level.componentLevel')}}</b></div>
          </div>
        </div>
<!--        <div style="width:100%; height: 120px;"></div>-->
      </el-col>

      <!-- DONE Semantic Segmentation Model Chooser-->
      <el-col :span="3">
        <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">
          <div style="margin-bottom: 10px">
            <div style="font-size: 20px"><b>{{$t('option.class')}}</b></div>
            <div style="font-size: 14px; color: gray;">{{$t('option.classHint')}}</div>
          </div>

          <el-select filterable placeholder="Select Class"  v-model="selectedClass">
            <el-option v-for="item in classes"
                       :key="item"
                       :label="item"
                       :value="item"
                       @click.native="selectC(item)"> </el-option>
          </el-select>
        </div>
      </el-col>

      <!-- DONE Transition Column-->
      <el-col :span="1">
        <div style="width:100%; height: 120px;"></div>
      </el-col>

      <!-- DONE Semantic Segmentation Model Chooser-->
      <el-col :span="4">
        <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">
          <div style="margin-bottom: 10px">
            <div style="font-size: 20px"><b>{{$t('option.model')}}</b></div>
            <div style="font-size: 14px; color: gray;">{{$t('option.SegHint')}}</div>
          </div>

          <el-select filterable placeholder="Select Model"  v-model="selectedModel">
            <el-option v-for="item in models"
                       :key="item.id"
                       :label="item.label"
                       :value="item.id"
                       @click.native="selectM(item)"> </el-option>
          </el-select>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"

export default {
  name: "OptionTree",
  data() {
    return {
      classes: ["tabby", "bulbul", "sorrel"],
      models: [
        {label: "deeplabv3", id: '1'},
        {label: "fcn", id: '2'},
        {label: "lraspp", id: '3'}
      ],

      selectedModel: '1',
      selectedClass: "tabby",

    }
  },
  methods: {
    selectC(item) {
      bus.$emit("toMainTree", item)
    },
    selectM(item) {
      bus.$emit("toModel", item)
    }
  }
}
</script>

<style scoped>
.treeTitle{
  font-size: 16px;
  color: whitesmoke;
  /*background-color: #003A70;*/
  /*height: 40px;*/
  /*padding-left: 20px;*/
}
.treeHint{
  font-size: 10px;
  color: whitesmoke;
}

.topicMain{
  /*padding-left: 20px;*/
  background-color: #003A70;
  display: flex;
  flex-direction: column;
  width: 100%;
  justify-content: center;
  align-items: flex-start;
  line-height: 20px;
  border-radius: 10px;
  height:40px;
}
</style>