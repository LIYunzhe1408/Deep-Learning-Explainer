<template>
  <div>
    <el-row>
      <!-- Option Pictures-->
      <!-- TODO 增加更多可以切换的图片-->
      <el-col :span="6" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around">
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
      <el-col :span="10">
        <div style="width:100%; height: 120px;"></div>
      </el-col>

      <!-- DONE Semantic Segmentation Model Chooser-->
      <el-col :span="3">
        <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">
          <div style="margin-bottom: 10px">
            <div style="font-size: 20px"><b>Class</b></div>
            <div style="font-size: 14px; color: gray;">To Explain</div>
          </div>

          <el-select filterable placeholder="Select Class"  v-model="selectClass">
            <el-option v-for="item in classes"
                       :key="item"
                       :label="item"
                       :value="item"
                       @click.native="selectModel(item)"> </el-option>
          </el-select>
        </div>
      </el-col>

      <!-- DONE Transition Column-->
      <el-col :span="1">
        <div style="width:100%; height: 120px;"></div>
      </el-col>

      <!-- DONE Semantic Segmentation Model Chooser-->
      <el-col :span="3">
        <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">
          <div style="margin-bottom: 10px">
            <div style="font-size: 20px"><b>Model</b></div>
            <div style="font-size: 14px; color: gray;">Semantic Segmentation</div>
          </div>

          <el-select filterable placeholder="Select Model"  v-model="selectModel">
            <el-option v-for="item in models"
                       :key="item.id"
                       :label="item.label"
                       :value="item.id"
                       @click.native="selectModel(item.id)"> </el-option>
          </el-select>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"

export default {
  name: "OptionExtraction",
  data() {
    return {
      selectModel: '1',
      selectClass: 'tabby',
      picID: '6',
      optionPics: [
        {src: require('@/assets/tabby/4.png'), id: '4', class: "tabby"},
        {src: require('@/assets/tabby/5.png'), id: '5', class: "tabby"},
        {src: require('@/assets/tabby/6.png'), id: '6', class: "tabby"},
      ],
      classes: [
        "tabby", "bulbul", "sorrel"
      ],
      models: [
        {label: "DeepLabV3", id: '1'},
        {label: "FCN", id: '2'},
        {label: "LSRAPP", id: '3'}
      ]
    }
  },
  methods: {
    selectPic(item) {
      this.picID = item.id
      bus.$emit("toMainPic", item);
    },
    selectModel(id) {
      this.selectModel = id
      bus.$emit("toMainModel", this.selectModel)
    }
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