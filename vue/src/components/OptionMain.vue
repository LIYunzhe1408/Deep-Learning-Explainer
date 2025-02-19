<template>
  <div>
    <el-row>
      <!-- Option Pictures-->
      <!-- TODO 增加更多可以切换的图片-->
      <el-col :span="8" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around">
        <div style="line-height: 120px"><i class="el-icon-caret-left"/></div>

        <div v-for="item in optionPics" :key="item.id">
          <el-image v-if="item.id === selectedPic.id"
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
      <el-col :span="12">
        <div style="width:100%; height: 120px;"></div>
      </el-col>

      <!-- DONE Semantic Segmentation Model Chooser-->
      <el-col :span="3">
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
                       @click.native="selectModel(item)"> </el-option>
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
  name: "Option",
  data() {
    return {
      selectedModelID: '',
      selectedModel: '',
      selectedPic:'',

      // TODO [1] Get from backend
      optionPics: [],
      // TODO [2] Get from backend
      models: [
        {label: "deeplabv3", id: '1'},
        {label: "fcn", id: '2'},
        {label: "lraspp", id: '3'}
      ]
    }
  },
  methods: {
    // TODO [1] Get initial data here.
    // 1. this.optionPics
    // [advanced] 2. models
    fetchImage() {
      console.log("hello")
      axios.get('http://localhost:8000/main/get_image/')
          .then(response => {
            this.optionPics = response.data
            for (let i = 0; i < this.optionPics.length; i++){
              this.optionPics[i].src = 'data:image/jpeg;base64,' + response.data[i].src;
            }
            this.selectedPic = this.optionPics[this.optionPics.length-1]
            this.initModel()
            this.emit()
            // this.imageSrc = 'data:image/jpeg;base64,' + response.data.image;
          })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },

    // FIXME 启封选择更多图片
    selectPic(item) {
      this.selectedPic = item
      // this.selectedPic = this.optionPics[this.optionPics.length-1]
      bus.$emit("toMain", this.selectedPic);
    },
    selectModel(item) {
      bus.$emit("toMainModel", item)
    },
    emit() {
      bus.$emit("toMain", this.selectedPic)
      bus.$emit("toMainModel", this.selectedModel)
    },
    initModel() {
      this.selectedModel = this.models[0]
      this.selectedModelID = this.models[0].id
    }
  },
  mounted() {
    this.fetchImage()
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