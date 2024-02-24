<template>
  <div>
    <el-row style="display: flex; ">
      <el-col :span="6" style="display:flex; margin: 5px 0 5px 0; justify-content: space-around">
        <div style="line-height: 120px"><i class="el-icon-caret-left"/></div>
        <el-image id="pic1"
                  class="picBoxOptionNotActive"
                  :src="require('@/assets/img-1.png')"
                  @click="selectPic"/>
        <el-image id="pic2"
                  class="picBoxOptionNotActive"
                  :src="require('@/assets/img-2.png')" />
        <el-image id="pic3"
                  class="picBoxOptionActive"
                  :src="require('@/assets/img-3.png')" />
        <div style="line-height: 120px"><i class="el-icon-caret-right"/></div>
      </el-col>


      <el-col :span="14">
        <div style="width:100%; height: 120px;"></div>
      </el-col>

      <el-col :span="3">
        <div style="width:100%; height: 120px;display: flex; flex-direction: column; justify-content: center">
          <div style="margin-bottom: 10px">
            <div style="font-size: 20px"><b>Model</b></div>
            <div style="font-size: 14px; color: gray;">Semantic Segmentation</div>
          </div>

          <el-select filterable placeholder="Select Model"  v-model="select">
            <el-option v-for="item in models" :key="item.id" :label="item.label" :value="item.label"></el-option>
          </el-select>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Option",
  data() {
    return {
      select: 'DeepLabV3',
      picID: 'pic3',
      models: [
        {label: "DeepLabV3", id: '1'},
        {label: "FCN", id: '2'},
        {label: "LSRAPP", id: '3'}
      ]
    }
  },
  methods: {
    selectPic() {

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