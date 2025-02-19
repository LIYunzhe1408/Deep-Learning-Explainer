<template>
  <div>
    <el-row>
      <!-- Option Pictures-->
      <!-- TODO 增加更多可以切换的图片-->
      <el-col :span="8" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around">
        <div style="line-height: 120px"><i class="el-icon-caret-left"/></div>

        <div v-for="item in optionPics" :key="item.id">
          <el-image v-if="item.id === picID"
                    class= "picBoxOptionActive"
                    :src="item.src"
                    @click="selectPic(item)"/>
          <el-image v-else
                    class= "picBoxOptionNotActive"
                    :src="item.src"
                    @click="selectPic(item)"/>
        </div>
        <div style="line-height: 120px"><i class="el-icon-caret-right"/></div>
      </el-col>

      <!-- DONE Transition Column-->
      <el-col :span="7">
        <div style="width:100%; height: 120px;">
          <el-button style="margin-top: 50px" @click="showDialog">Module Tips</el-button>
        </div>
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
                       @click.native="selectClass(item)"> </el-option>
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

          <el-select filterable placeholder="Select Model"  v-model="selectedModelID">
            <el-option v-for="item in models"
                       :key="item.id"
                       :label="item.label"
                       :value="item.id"
                       @click.native="selectModel(item.label)"> </el-option>
          </el-select>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"
import axios from "axios";

export default {
  name: "OptionExtraction",
  data() {
    return {
      // Get from ComparsionExtraction.vue
      selectedModelID: '1',
      models: [
        {label: "deeplabv3", id: '1'},
        {label: "fcn", id: '2'},
        {label: "lraspp", id: '3'}
      ],

      // Assigned by admin
      classes: ["tabby", "bulbul", "sorrel"],
      selectedClass: 'tabby',
      picID: '6',


      // TODO [1] Get from backend based on this.selectedClass
      optionPics: [
        {src: require('@/assets/image data/mainline/tabby/handle image/4.jpg'), id: '4', class: "tabby"},
        {src: require('@/assets/image data/mainline/tabby/handle image/5.jpg'), id: '5', class: "tabby"},
        {src: require('@/assets/image data/mainline/tabby/handle image/6.jpg'), id: '6', class: "tabby"},
      ],

    }
  },
  methods: {
    showDialog(){
      bus.$emit("toLocalEX", 1);
    },
    getOptionPics(){
      // optionPics
      axios({
        method: "get",
        params: {class: this.selectedClass},
        url: 'http://localhost:8000/main/get_option_pics/'
      }).then(res=> {
        this.optionPics = res.data
        for (let i = 0; i < this.optionPics.length; i++){
          this.optionPics[i].src = 'data:image/jpeg;base64,' + this.optionPics[i].src
        }
        // bus.$emit("toExtractionInit", {defaultPic:this.optionPics[2], selectedClass: this.selectedClass})
      })
    },
    selectPic(item) {
      this.picID = item.id
      bus.$emit("toLocalEXPic", item);
    },
    selectModel(item) {
      bus.$emit("toLocalEXModel", item)
    },
    selectClass(item) {
      this.selectedClass = item
      bus.$emit("toLocalEXClass", item)

      this.getOptionPics()
    }
  },
  mounted() {
    this.getOptionPics()
  }
}
</script>

<style scoped>
.el-icon-caret-left,.el-icon-caret-right{
  cursor: pointer;
}
.picBoxOptionNotActive{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
  width:120px;
  height: 120px;
  opacity: 60%
}
.picBoxOptionActive{
  background-color: white;
  border: black solid;
  border-width: 2px;
  border-radius: 20px;
  width:120px;
  height: 120px;
  opacity: 100%;
}
.picBoxOptionActive:hover, .picBoxOptionNotActive:hover{
  cursor: pointer;
}
</style>