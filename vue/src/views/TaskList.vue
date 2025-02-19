<template>
  <div style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column">
    <div class="box" style="padding:20px 20px 20px 20px;
                            margin:20px 20px 20px 20px;
                            width: 800px;
                            display: flex;
                            justify-content: center;
                            border: gray solid 1px;
                            border-radius: 5px">
        <el-table
            ref="filterTable"
            :data="tableData"
            style="width: 100%">
          <el-table-column
              prop="id"
              label="编号"
              column-key="id"
              width="100"
          >
          </el-table-column>
          <el-table-column
              prop="model"
              label="语义分割模型"
              column-key="id">
          </el-table-column>
          <el-table-column
              prop="dataset"
              label="数据集">
          </el-table-column>
          <el-table-column
            align="center">
            <el-button type="primary" @click="pushToHome">查看</el-button>
          </el-table-column>
        </el-table>
    </div>

    <el-button type="primary" @click="pushToSubmission">新建任务</el-button>
  </div>
</template>

<script>
import bus from "@/common/bus";

export default {
  name: "TaskList",
  data(){
    return{
      tableData: [{
        id: '1',
        model: 'deeplabv3, fcn, lraspp',
        dataset: 'IMAGENET'
      },],
    }
  },
  methods:{
    pushToHome(){
      bus.$emit("toHomeView", 2)
      this.$router.push("/home")
    },
    pushToSubmission(){
      this.$router.push("/task")
    }
  }
}
</script>

<style scoped>

</style>