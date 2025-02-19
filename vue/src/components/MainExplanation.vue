<template>
  <div>

    <el-row gutter=40 type="flex" style="justify-content: start; margin-left: 5px; margin-top: 30px">
      <!-- Left -->
      <el-col :span="1"></el-col>
      <el-col :span="11">
        <div style="height: 40px;
             margin: 0 0 0 20px;
             font-size: 32px;
             line-height: 40px;
             color: #003A70;
             padding-bottom: 50px"><b>Impact of Different Semantic Segmentation Algorithms on Explanation Results and Metrics</b></div>
        <p style="margin: 40px 0 20px 20px; font-size: 18px; line-height: 30px">
          Explanation faithfulness is measured by <b>SSC</b> and <b>SDC</b>.
          The <b>Smallest Sufficient Concepts (SSC)</b> represent the minimal set of concepts required for the model to correctly classify an image, assessing the <b>representational ability</b> of concepts.
          The <b>Smallest Destroying Concepts (SDC)</b> refer to a set of concepts, the removal of which results in poor or incorrect classification, reflecting their **necessity for model decisions** and measuring trustworthiness.
        </p>
        <p style="margin: 10px 0 20px 20px; font-size: 18px; line-height: 30px">
          Explanation consistency is measured by <b>ISSC</b> and <b>ISDC</b>.
          <b>Instance Smallest Sufficient Concepts (ISSC)</b> and <b>Instance Smallest Destroying Concepts (ISDC)</b> extend SSC and SDC to rank concepts by importance for each image.
          Similar to the SSC/SDC pre-computation, ISSC and ISDC modify the ranked concepts and measure classification probability changes before and after modifications, quantifying <b>local explanation performance</b> for a single image or class.
        </p>
        <div style="height: 40px;
             margin: 40px 0 0 30px;
             font-size: 30px;
             line-height: 40px;
             color: #4E79A7;"><b>Metric Data</b></div>
        <div style="
             margin: 0 0 20px 30px;
             font-size: 16px;
             line-height: 40px;
             color: grey;">Faithfulness and consistency metrics across different image categories</div>

        <div style="margin: 0 0 20px 30px;
                    padding: 0 0 0 5px;
                    line-height: 30px;
                    font-size: 15px;
                    background-color: #E9F3F2;
                    color: #333333;
                    "><b>Consistency Metrics: ISSC and ISDC Scores</b></div>
        <el-table
            style="margin-left: 30px;"
            class="boxMain"
            :data="ISSCISDCMetrics"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="cellStyleISSC">
          <el-table-column
              prop="class"
              label="CLASS">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              {{this.column1}}
            </template>
            <el-table-column
                prop="ISSC.fcn"
                label="FCN"
                width="100">
            </el-table-column>
            <el-table-column
                  prop="ISSC.lraspp"
                  label="LRASPP"
                  width="100">
            </el-table-column>
            <el-table-column
                prop="ISSC.deeplabv3"
                label="DeepLabv3"
                width="100">
            </el-table-column>

          </el-table-column>
          <el-table-column>
            <template slot="header">
              {{this.column2}}
            </template>
            <el-table-column
                prop="ISDC.fcn"
                label="FCN"
                width="100">
            </el-table-column>
            <el-table-column
                prop="ISDC.lraspp"
                label="LRASPP"
                width="100">
            </el-table-column>
            <el-table-column
                prop="ISDC.deeplabv3"
                label="DeepLabv3"
                width="100">
            </el-table-column>
          </el-table-column>
        </el-table>

        <div style="margin: 0 0 20px 30px;
                    padding: 0 0 0 5px;
                    line-height: 30px;
                    font-size: 15px;
                    background-color: #E9F3F2;
                    color: #333333;
                    "><b>Explanation Faithfulness Metric: SSC Scores (Higher is better)</b></div>
        <el-table
            style="margin-left: 30px"
            class="boxMain"
            :data="SSCMetrics"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="cellStyleSSC">
          <el-table-column
              prop="model"
              label="Model">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              SSC(add top-d most important concept)
            </template>
            <el-table-column
                prop="index.d1"
                label="d=1"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d2"
                label="d=2"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d3"
                label="d=3"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d4"
                label="d=4"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d5"
                label="d=5"
                width="100">
            </el-table-column>
          </el-table-column>
        </el-table>


        <div style="margin: 0 0 20px 30px;
                    padding: 0 0 0 5px;
                    line-height: 30px;
                    font-size: 15px;
                    background-color: #E9F3F2;
                    color: #333333;
                    "><b>Explanation Faithfulness Metric: SDC Scores (Lower is better)</b></div>
        <el-table
            style="margin-left: 30px"
            class="boxMain"
            :data="SDCMetrics"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="cellStyleSDC">
          <el-table-column
              prop="model"
              label="Model">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              SDC(minus top-d most important concept)
            </template>
            <el-table-column
                prop="index.d1"
                label="d=1"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d2"
                label="d=2"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d3"
                label="d=3"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d4"
                label="d=4"
                width="100">
            </el-table-column>
            <el-table-column
                prop="index.d5"
                label="d=5"
                width="100">
            </el-table-column>
          </el-table-column>
        </el-table>
      </el-col>



<!--      <el-col :span="1"></el-col>-->
      <el-col  :span="11" >

          <div style="height: 40px;
             border-bottom: lightgray solid 1px;
             margin-bottom: 20px;
             margin-left: 80px;
             font-size: 30px;
             line-height: 40px;
             color: #4E79A7;
             width: 80%;
             padding-bottom: 50px;"><b>Comparison of Explanation Heatmaps</b></div>
          <OptionExplanation style="margin-left: 60px; width: 85%"></OptionExplanation>

        <div style="width: 80%; margin-left: 80px">
          <div style="margin: 0 0 20px 0;
                    padding: 0 0 0 20px;
                    line-height: 30px;
                    font-size: 18px;
                    background-color: #003A70;
                    color: white;
                    "><b>{{$t('level.objectLevel')}}</b></div>
          <div style="display: flex; flex-direction: column">
            <div class="boxMain" style="height:210px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly">

              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Obj.deeplabv3 />
                <el-tag>DeepLabV3</el-tag>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Obj.fcn />
                <el-tag>FCN</el-tag>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Obj.lraspp />
                <el-tag>LRASPP</el-tag>
              </div>
            </div>


            <div style="margin: 0 0 20px 0;
                    padding: 0 0 0 20px;
                    line-height: 30px;
                    font-size: 18px;
                    background-color: #003A70;
                    color: white;
                    "><b>{{$t('level.componentLevel')}}</b></div>
            <div class="boxMain" style="height:210px; display: flex; flex-direction: row; align-items: center; justify-content: space-evenly">
              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Compo.deeplabv3 />
                <el-tag>DeepLabV3</el-tag>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Compo.fcn />
                <el-tag>FCN</el-tag>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
                <el-image
                    class="picBoxMain"
                    style="height: 140px; width: 140px; margin-bottom: 10px"
                    :src=this.compareList.Compo.lraspp />
                <el-tag>LRASPP</el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import bus from "@/common/bus"
import OptionExplanation from "@/components/OptionExplanation";
import axios from "axios";
export default {
  name: "MainExplanation",
  components: {OptionExplanation},
  data() {
    return {
      // https://blog.csdn.net/yehaocheng520/article/details/118543885
      column1: '$$ISSC^{d}_{X^k}, d=5$$',
      column2: '$$ISDC^{d}_{X^k}, d=5$$',
      column3: '$$SSC$$',
      column4: '$$SDC(minus top-d most important concept)$$',
      ISSCISDCMetrics: [],
      SSCMetrics: [],
      SDCMetrics: [],
      selectedPic:{src: require('@/assets/image data/mainline/tabby/handle image/6.jpg'), id:'6', class: 'tabby'},
      selectedClass: 'tabby',
      compareList: {}
    }
  },
  methods: {
    cellStyleISSC({ row, column, rowIndex, columnIndex }){
      if (rowIndex === 0 && (columnIndex === 3 || columnIndex === 6) ||
          rowIndex === 1 && (columnIndex === 1 || columnIndex === 3 || columnIndex === 6) ||
          rowIndex === 2 && (columnIndex === 1 || columnIndex === 5) ||
          rowIndex === 3 && (columnIndex === 3 || columnIndex === 6)) {
        return 'font-weight: bold; color: black; text-align: center'; // 加粗第一行第一列
      }
      return 'text-align: center';
    },
    cellStyleSSC({ row, column, rowIndex, columnIndex }){
      if (rowIndex === 0 && (columnIndex === 2) ||
          rowIndex === 1 && (columnIndex === 3 || columnIndex === 4 || columnIndex === 5) ||
          rowIndex === 2 && (columnIndex === 1 || columnIndex === 5)) {
        return 'font-weight: bold; color: black; text-align: center'; // 加粗第一行第一列
      }
      return 'text-align: center';
    },
    cellStyleSDC({ row, column, rowIndex, columnIndex }){
      if (rowIndex === 2 && (columnIndex === 1 || columnIndex === 2 || columnIndex === 3 || columnIndex === 4 || columnIndex === 5)) {
        return 'font-weight: bold; color: black; text-align: center'; // 加粗第一行第一列
      }
      return 'text-align: center';
    },

    formatMath(){
      setTimeout(()=>{
        this.$nextTick(()=>{
          if(this.MathJax.isMathjaxConfig){
            this.MathJax.initMathjaxConfig();
          }
          //这个地方的hello是对应要渲染数学公式的dom的class
          this.MathJax.MathQueue('hello');
        })
      },100)
    },
    getMetrics(){
      axios({
        method: "get",
        params: {},
        url: 'http://localhost:8000/main/get_explanation_metrics/'
      }).then(res=> {
        this.ISSCISDCMetrics = res.data["ISSCISDCMetrics"]
        this.SSCMetrics = res.data["SSCMetrics"]
        this.SDCMetrics = res.data["SDCMetrics"]
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    resetCompare(){
        axios({
          method: "get",
          params: {class: this.selectedClass, imageNum: this.selectedPic.id},
          url: 'http://localhost:8000/main/get_explanation_comparison_images/'
        }).then(res=> {
          this.compareList = res.data
          for (let key in this.compareList){
            for (let model in this.compareList[key]){
              this.compareList[key][model] = 'data:image/jpeg;base64, ' + this.compareList[key][model]
            }
          }
        })
            .catch(error => {
              console.error('Error fetching image', error);
            });
    }

  },
  created() {
    this.formatMath();
    bus.$on("toMainPic", (data)=>{
      this.selectedPic = data
      this.resetCompare()
    })
    bus.$on("toExplanationClass", (data)=>{
      this.selectedClass = data
      this.resetCompare()
    })
    this.resetCompare()
    this.getMetrics()


  }
}
</script>

<style scoped>
.boxMain{
  margin-bottom: 20px;
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
.picBoxMain{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
}
.el-icon-picture-outline{
  font-size: 200px;
}
.tagContribution{
  width: 100px;
  height: 30px;
  text-align: center;
  line-height: 30px;
  font-size: 14px;
}
.topicMain{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-left:80px;
  width: 100%;
}
.highlighted:hover{
  color: #0a66c2;
  text-decoration: underline;
}
.highlighted{
  color: #0a66c2;
  text-decoration-line: none
}
.subPics{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 5px;
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center
}
</style>