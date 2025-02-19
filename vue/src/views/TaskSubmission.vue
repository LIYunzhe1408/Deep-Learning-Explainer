<template>
  <div style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column">

    <div class="box" style="padding:20px 20px 20px 20px; margin:20px 20px 20px 20px; width: 500px; display: flex; justify-content: center" v-if="submitted===0">
      <el-form ref="form" :model="form" label-width="60px">
        <el-form-item>
          <div style="font-size: 20px"><b>请选择任务配置</b></div>
        </el-form-item>
        <el-form-item label="模型">
          <el-select v-model="form.models" multiple placeholder="请选择模型">
            <el-option label="deeplabv3" value="deeplabv3"></el-option>
            <el-option label="fcn" value="fcn"></el-option>
            <el-option label="lraspp" value="lraspp"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据集">
          <el-select v-model="form.datasets" placeholder="请选择数据集">
            <el-option label="IMAGENET" value="IMAGENET"></el-option>
            <el-option label="PASCAL VOC 2012" value="PASCAL"></el-option>
            <el-option label="COCO 2017" value="COCO"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="returnToList">返回</el-button>
          <el-button type="primary" @click="submitted = 1">新建任务</el-button>

<!--          <el-button>取消</el-button>-->
        </el-form-item>
      </el-form>
    </div>


    <div class="box" style="padding:20px 20px 20px 20px; margin:20px 20px 20px 20px; display: flex; justify-content: center" v-if="submitted===1">
      <el-table
          ref="filterTable"
          :data="tableData"
          style="width: 100%">
        <el-table-column
            prop="date"
            label="任务"
            width="180"
            column-key="date"
        >
        </el-table-column>
        <el-table-column
            prop="name"
            label="进度"
            width="180" v-slot="scope">
          <el-progress :text-inside="true" :stroke-width="26" :percentage="scope.row.name"></el-progress>
        </el-table-column>
        <el-table-column
            prop="tag"
            label="状态"
            width="100"
            :filters="[{ text: '家', value: '家' }, { text: '公司', value: '公司' }]"
            :filter-method="filterTag"
            filter-placement="bottom-end">
          <template slot-scope="scope">
            <el-tag
                :type="scope.row.tag === '已完成' ? 'success' : 'primary'"
                disable-transitions>{{scope.row.tag}}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-button v-if="ready === 1" @click="pushToHome">完成</el-button>
  </div>
</template>

<script>
import bus from "@/common/bus";
import router from "@/router";

export default {
  name: "TaskSubmission",
  data(){
    return{
      form: {
        models: [],
        datasets: '',
      },

      tableData: [{
        date: '概念分割',
        name: 0,
        tag: '未开始'
      }, {
        date: '概念聚类',
        name: 0,
        tag: '未开始'
      }, {
        date: '概念树训练',
        name: 0,
        tag: '未开始'
      }, {
        date: '模型生成',
        name: 0,
        tag: '未开始'
      }],

      submitted: 0,
      ready: 0

    }
  },
  methods: {
    returnToList(){
      this.$router.push('/taskList')
      this.submitted = 1
    },
    pushToHome(){
      bus.$emit("toHomeView", 2)
      this.$router.push('/home')
    },
    selectModel(item) {
      // bus.$emit("toMainModel", item)
    },
    formatter(row, column) {
      return row.address;
    },
    addProgress(i){
      if (i === 0 && this.tableData[i].name < 100){
          this.tableData[i].tag = '进行中'
          this.tableData[i].name += 1
      } else if (i !==0 && this.tableData[i-1].name === 100 && this.tableData[i].name < 100){
          this.tableData[i].tag = '进行中'
          this.tableData[i].name += 1
      }
      if (this.tableData[i].name === 100)
        this.tableData[i].tag = '已完成'
      if (this.tableData[3].tag == '已完成')
        this.ready = 1
    }
  },
  updated() {
    if (this.submitted){
      for (let i = 0;  i < this.tableData.length; i++){

        let timeout = 20
        if (i === 2)
          timeout = 20
        this.timer = setInterval(this.addProgress, timeout, i)

      }
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
</style>