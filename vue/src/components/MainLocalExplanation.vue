<template>
  <div>
    <div  style="display: flex; justify-content: start; margin-left: 5px">
            <!--最外面大框：可以加max-height-->
            <div class="boxMain" style="padding-bottom: 20px;">
              <div class="topicMain">
                <div style="display: flex; width: 100%; height:100%" >


                  <!--左侧大图-->
                  <div style="width:30%; height: 580px; display: flex; flex-wrap: wrap">
<!--                    <div style="font-size: 18px; margin-top: 20px"><b>Heatmap and Segmentation Result</b></div>-->
                    <div>

                      <div style="font-size: 18px; margin-top: 20px; width:400px"><b>Heatmap and Segmentation Results</b></div>
                      <div style="font-size: 12px; width:400px; color: gray">Visualization results at the object level and component level</div>

                    </div>
                    <div v-for="(item, index) in this.segResults">
                      <el-image
                          class="picBoxMain"
                          style="height: 210px; width: 210px; margin-left: 10px"
                          :src=item.src />
                    </div>
                  </div>


                  <div>
                    <div style="font-size: 18px; margin-top: 20px; margin-left: 20px"><b>Local Concept Tree Explanation</b></div>
                    <div style="font-size: 12px; color: gray; margin-left: 20px; wrap-option: wrap; max-width: 70%">There is a hierarchical relationship from the object level to the component level, and the score represents the contribution of the concept to the image category</div>

                    <div style="display: flex">
                      <div v-for="(cluster, index) in this.clusters">
                        <!--一列局部解释-->
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center">

                          <!--Object level explanation-1-->
                          <div class="boxMain" style="width: 300px; height: 120px; margin-top: 20px; margin-left: 20px">
                            <div style="height: 80%; display: flex; justify-content: space-between; align-items: stretch; margin-top: 10px" v-if="true">
                              <div style="display: flex; justify-content: center; align-items: center">
                                <el-image
                                    class="picBoxMain"
                                    style="height: 100px; width: 100px;"
                                    :src=cluster.src />
                                <div>
                                  <div class="tagContribution"><b>{{cluster.label}}</b></div>
                                  <el-tag  class="tagContribution" type="danger" color="red" effect="dark">{{cluster.score}}</el-tag>
                                </div>
<!--                                <el-tag  class="tagContribution" type="danger" color="red" effect="dark">{{cluster.label}}: {{cluster.score}}</el-tag>-->
                              </div>
                            </div>
                          </div>

                          <!--箭头表示关系-->
                          <div style="margin-left: 20px">
                            <el-image style="height:20px" :src="require('@/assets/向下箭头 (1).png')"></el-image>
                            <el-image style="height:20px" :src="require('@/assets/向下箭头 (1).png')"></el-image>
                          </div>

                          <!--Component level explanation-1-->
                          <div class="boxMain" style="width: 300px; margin-left: 20px; padding-bottom: 20px">
                            <div style="; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; margin-top: 20px" v-if="true">
                              <div v-for="(co, index) in cluster.contributors">
                                <div style="display: flex; justify-content: center; align-items: center">
                                  <el-image
                                      class="picBoxMain"
                                      style="height: 100px; width: 100px;"
                                      :src=co.src />
                                  <div>

                                    <div class="tagContributionCompo"><b>{{co.label}}</b></div>
                                    <el-tag  class="tagContributionCompo" type="danger" color="light red" effect="dark" >{{co.score}}</el-tag>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
    </div>
  </div>
</template>

<script>
import bus from "@/common/bus"
import axios from "axios";
export default {
  name: "MainExplanation",
  data() {
    return {
      selectedModel: 'deeplabv3',
      selectedPic:{src: require('@/assets/image data/mainline/tabby/handle image/6.jpg'), id:'6', class: 'tabby'},
      selectedClass: "tabby",
      segResults: {},
      clusters: {
      }
    }
  },
  methods: {
    resetLocalExplanation(){
      this.resetSegResult()
      console.log(this.selectedModel, this.selectedClass)
      axios({
        method: "get",
        params: {class: this.selectedClass, model: this.selectedModel, imageNum: this.selectedPic.id},
        url: 'http://localhost:8000/main/get_local_explanation_images/'
      }).then(res=> {
        this.clusters = res.data
        for (let key in this.clusters){
          this.clusters[key].src = 'data:image/jpeg;base64,' + this.clusters[key].src
          for (let i = 0; i < this.clusters[key].contributors.length; i++){
            this.clusters[key].contributors[i].src = 'data:image/jpeg;base64,' + this.clusters[key].contributors[i].src
          }
        }
        console.log(this.clusters)
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    resetSegResult(){
      axios({
        method: "get",
        params: {class: this.selectedClass, model: this.selectedModel, imageNum: this.selectedPic.id},
        url: 'http://localhost:8000/main/get_segmented_result/'
      }).then(res=> {
        this.segResults = res.data
        for (let key in this.segResults){
          this.segResults[key].src = 'data:image/jpeg;base64,' + this.segResults[key].src
        }
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    resetCluster(){
      this.segResults = {
        heatmapObj:{src: require('@/assets/image data/mainline/'+this.selectedPic.class+'/'+this.selectedModel+'/heatmap/'+this.selectedPic.id+'-o.jpg')},
        segImageObj:{src:require('@/assets/image data/mainline/'+this.selectedPic.class+'/'+this.selectedModel+'/patch-image/'+this.selectedPic.id+'.jpg')},
        heatmapCom:{src:require('@/assets/image data/mainline/'+this.selectedPic.class+'/'+this.selectedModel+'/heatmap/'+this.selectedPic.id+'-c.jpg')},
        segImageCom:{src:require('@/assets/image data/mainline/'+this.selectedPic.class+'/'+this.selectedModel+'/superpixel-image/'+this.selectedPic.id+'.jpg')}
      }

      for (let patch in this.clusters){
        for (let i = 0; i < this.clusters[patch].contributors.length; i++){
          this.clusters[patch].contributors[i].label = this.clusters[patch].label + "'s " + this.clusters[patch].contributors[i].label
        }
      }

    },
  },
  created() {
    bus.$on("toLocalEXPic", (data)=>{
      this.selectedPic = data
      // this.resetCluster()
      this.resetLocalExplanation()
    })
    bus.$on("toLocalEXModel", (data)=>{
      this.selectedModel = data
      // this.resetCluster()
      this.resetLocalExplanation()
    })
    // this.resetCluster()
  },
  mounted() {
    bus.$on("toLocalEXPic", (data)=>{
      this.selectedPic = data
      // this.resetCluster()
      this.resetLocalExplanation()
    })
    bus.$on("toLocalEXModel", (data)=>{
      this.selectedModel = data
      // this.resetCluster()
      this.resetLocalExplanation()
    })
    bus.$on("toLocalEXClass", (data)=>{
      this.selectedClass = data
      // this.resetCluster()
      this.resetLocalExplanation()
    })
    this.resetLocalExplanation()
  }
}
</script>

<style scoped>
.boxMain{
  /*margin-bottom: 20px;*/
  background-color: white;
  border: gray ;
  border-radius: 10px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  /*width: 100%;*/
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
  width: 140px;
  height: 30px;
  text-align: center;
  line-height: 30px;
  font-size: 14px;
  margin-left: 10px;
}
.tagContributionCompo{
  width: 140px;
  height: 30px;
  text-align: center;
  /*line-height: 30px;*/
  font-size: 11px;
  word-wrap: break-word;
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