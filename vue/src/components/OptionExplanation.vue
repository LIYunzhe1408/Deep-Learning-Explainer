<template>
  <div>
    <div class="box" style="display: flex">
      <div style="display:flex; margin: 5px 0 5px 0; justify-content: space-around; width: 50%">
        <div style="line-height: 100px"><i class="el-icon-caret-left"/></div>

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
        <div style="line-height: 100px"><i class="el-icon-caret-right"/></div>
      </div>

      <div style="margin-left: 80px">
        <div style="width:100%; height: 100px;display: flex; flex-direction: column; justify-content: center">
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
      </div>
<!--      <el-row>-->
<!--        &lt;!&ndash; Option Pictures&ndash;&gt;-->
<!--        &lt;!&ndash; TODO 增加更多可以切换的图片&ndash;&gt;-->
<!--&lt;!&ndash;        <el-col :span="12" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around"></el-col>&ndash;&gt;-->
<!--        <el-col :span="8" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around">-->
<!--          <div style="line-height: 120px"><i class="el-icon-caret-left"/></div>-->

<!--          <div v-for="item in optionPics" :key="item.id">-->
<!--            <el-image v-if="item.id === picID"-->
<!--                      class= "picBoxOptionActive"-->
<!--                      :src="item.src"-->
<!--                      @click="selectPic(item)"/>-->
<!--            <el-image v-else-->
<!--                      class= "picBoxOptionNotActive"-->
<!--                      :src="item.src"-->
<!--                      @click="selectPic(item)"/>-->
<!--          </div>-->
<!--          <div style="line-height: 120px"><i class="el-icon-caret-right"/></div>-->
<!--        </el-col>-->

<!--        &lt;!&ndash; DONE Transition Column&ndash;&gt;-->
<!--        &lt;!&ndash;      <el-col :span="11">&ndash;&gt;-->
<!--        &lt;!&ndash;        <div style="width:100%; height: 120px;"></div>&ndash;&gt;-->
<!--        &lt;!&ndash;      </el-col>&ndash;&gt;-->

<!--        &lt;!&ndash; DONE Semantic Segmentation Model Chooser&ndash;&gt;-->
<!--        <el-col :span="3">-->
<!--          <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">-->
<!--            <div style="margin-bottom: 10px">-->
<!--              <div style="font-size: 20px"><b>{{$t('option.class')}}</b></div>-->
<!--              <div style="font-size: 14px; color: gray;">{{$t('option.classHint')}}</div>-->
<!--            </div>-->

<!--            <el-select filterable placeholder="Select Class"  v-model="selectClass">-->
<!--              <el-option v-for="item in classes"-->
<!--                         :key="item"-->
<!--                         :label="item"-->
<!--                         :value="item"-->
<!--                         @click.native="selectClass(item)"> </el-option>-->
<!--            </el-select>-->
<!--          </div>-->
<!--        </el-col>-->
<!--      </el-row>-->
    </div>

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
      bus.$emit("toMainPic", item);
    },
    selectClass(item) {
      // this.picID = '6'
      this.selectedClass = item
      this.getOptionPics()
      bus.$emit("toExplanationClass", item)
    }
  },
  mounted() {
    this.getOptionPics()
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
.el-icon-caret-left,.el-icon-caret-right{
  cursor: pointer;
}
.picBoxOptionNotActive{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
  width:100px;
  height: 100px;
  opacity: 60%
}
.picBoxOptionActive{
  background-color: white;
  border: black solid;
  border-width: 2px;
  border-radius: 20px;
  width:100px;
  height: 100px;
  opacity: 100%;
}
.picBoxOptionActive:hover, .picBoxOptionNotActive:hover{
  cursor: pointer;
}
</style>