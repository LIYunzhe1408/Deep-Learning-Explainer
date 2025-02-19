<template>
  <div>
<!--    <div class="topicMain"><b>聚类概念树</b></div>-->
<!--    <el-row style="margin-bottom: 20px;">-->
<!--      <el-col :span="3" style=" display: flex">-->


<!--      </el-col>-->
<!--    </el-row>-->
    <el-row gutter=40 type="flex" style="justify-content: center">
      <el-col :span="1"></el-col>
      <el-col  :span="24" >
        <div class="boxMain" style="background-color: darkorange" id="start">
          <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 10px; flex-wrap: wrap">
            <div v-for="item in handleImage" :key="item.id">
              <el-image class="picBoxOption" :src="item.src"></el-image>
            </div>
          </div>
          <div style="margin-left: 10px; color: whitesmoke; font-size: 24px; text-align: center"><b>{{$t('level.imageLevel')}}</b></div>
        </div>
      </el-col>
    </el-row>





    <el-row gutter=40 type="flex" style="justify-content: center">
      <el-col :span="1">

      </el-col>
      <el-col  :span="23">

        <div class="objLevel" style="background-color: #42b983">
<!--          <div style="text-align: center; font-size: 22px"><b>Object Level</b></div>-->
          <div class="objectLevelContainerLayout" style="">
            <div v-for="(item, index) in this.patches.clusters" :key="index" :id="index+1">
              <div class="objectLevelImageContainer">
                <div v-if="className === patches.class" v-for="i in item">
                  <el-image class="picBoxOption" :src="i"></el-image>
                </div>
              </div>
            </div>
          </div>
          <div style="margin-left: 10px; color: whitesmoke; font-size: 24px;"><b>{{$t('level.objectLevel')}}</b></div>
        </div>

      </el-col>
    </el-row>




    <el-row gutter=40 type="flex" style="justify-content: center">
      <el-col :span="1">

      </el-col>
      <!--DONE Middle-->
      <el-col  :span="23">

        <div class="boxMain" style="background-color: #1890ff; margin-top: 60px;">
          <div style="display: flex; justify-content: space-evenly; flex-wrap: wrap; margin-top: 20px">
            <div v-for="(item, index) in this.superpixels.clusters" :key="index">
              <el-tooltip placement="left">
                <div slot="content" style="display: flex; max-width:400px; flex-wrap: wrap; justify-content: stretch; ">
                  <div class="componentLevelImageContainer" style="width: 260px">
                    <div v-if="className === patches.class" v-for="i in item.images">
                      <el-image class="picBoxOption" :src="i"></el-image>
                    </div>
                  </div>
                </div>
                <div class="node"  :id="index+10"></div>
              </el-tooltip>
            </div>
          </div>
          <div style="margin-left: 10px; color: whitesmoke; font-size: 24px;"><b>{{$t('level.componentLevel')}}</b></div>
        </div>
        <div style="display: flex; justify-content: center">
          <el-tag style="color: black">Hover over the leaf nodes to view segmented images.</el-tag>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LeaderLine from 'leader-line'
import bus from "@/common/bus"
import axios from "axios";

export default {
  name: "MainTree",
  data() {
    return {
      selectedClass: "tabby",
      selectedModel: "deeplabv3",
      className: "tabby",
      handleImage: [],

      patches: {},

      superpixels: {},
      lines: []
    }
  },
  methods: {
    createLine(startElement, endElement, path) {
      return new LeaderLine(startElement, endElement, {
        size: 2,
        startSocket: 'bottom',
        endSocket: 'top',
        path: path,
        // dash: {animation: true},
        startPlugColor: 'black',
        endPlugColor: 'black',
        gradient: true,
        // hide: true
      })
    },
    drawPatchLines(patches) {
      const startElementObj = document.getElementById('start')
      console.log("-----------------------------------drawLines")
      console.log(startElementObj)
      // console.log("patch cluster: ", patches.clusters.length)
      for (let i = 0; i < patches.clusters.length; i++) {
        const endElement = document.getElementById((i + 1).toString())
        console.log(endElement)
        this.lines.push(this.createLine(startElementObj, endElement, 'grid'))
        // }
      }
    },
    drawSuperpixelLines(superpixel){
      for (let i = 0; i < this.patches.clusters.length; i++){
        const startElementCompo = document.getElementById((i+1).toString())
        for (let j = 0; j < this.superpixels.clusters.length; j++) {
          if (this.superpixels.clusters[j].belongToPatch === i) {
            const endElement = document.getElementById((j+10).toString())
            this.lines.push(this.createLine(startElementCompo, endElement, 'none'))
          }
        }
      }
    },
    getInitialImages(){
      // 初始，换pic，换model，换class
      let params = {class: this.selectedClass, model: this.selectedModel}
      axios({
        method: "get",
        params: params,
        url: 'http://localhost:8000/main/get_tree_images/'
      }).then(res=> {
        // console.log("handle------------------------------------------------")
        this.handleImage = res.data["handleImages"]
        for (let i = 0; i < this.handleImage.length; i++){
          this.handleImage[i].src = 'data:image/jpeg;base64,' + this.handleImage[i].src
        }
        // console.log("patches------------------------------------------------")

        let last_patch_len = 0
        if (this.patches==={}){
          last_patch_len = this.patches.clusters.length
        }
        this.patches = res.data["patches"]
        for (let i = 0; i < this.patches.clusters.length; i++){
          for (let j = 0; j < this.patches.clusters[i].length; j++){
            this.patches.clusters[i][j] = 'data:image/jpeg;base64,' + this.patches.clusters[i][j]
          }
        }
        // console.log(this.patches)
        // console.log("superpixel------------------------------------------------")
        this.superpixels = res.data["superpixels"]
        for (let i = 0; i < this.superpixels.clusters.length; i++){
          for (let j = 0; j < (this.superpixels.clusters[i]).images.length; j++){
            this.superpixels.clusters[i].images[j] = 'data:image/jpeg;base64,' + this.superpixels.clusters[i].images[j]
          }
        }
        // console.log(this.superpixels)
      })
      .catch(error => {
        console.error('Error fetching image', error);
      });

    },
  },

  beforeMount() {
    this.getInitialImages()

    bus.$on("toMainTree", (data)=>{

      this.selectedClass = data
      this.className = this.selectedClass
      this.getInitialImages()
      console.log(this.lines.length)

    })
    bus.$on("toModel", (data)=>{
      // for (let i = 0; i < this.lines.length; i++){
      //   this.lines[i].remove()
      // }
      this.selectedModel = data.label
      this.getInitialImages()
    })
  },
  mounted() {
    // function createLine(startElement, endElement, path) {
    //   return new LeaderLine(startElement, endElement, {
    //     size: 3,
    //     startSocket: 'bottom',
    //     endSocket: 'top',
    //     path: path,
    //     dash: {animation: true},
    //     startPlugColor: '#040409',
    //     endPlugColor: '#8b969b',
    //     gradient: true,
    //     // hide: true
    //   })
    // }
    //
    // // let lines = []
    // // Object level
    // const startElementObj = document.getElementById('start')
    // for (let i = 0; i < this.patches.clusters.length; i++){
    //   const endElement = document.getElementById((i+1).toString())
    //   this.lines.push(createLine(startElementObj, endElement, 'grid'))
    // }
    //
    //
    // // Component Level
    //
    // for (let i = 0; i < this.patches.clusters.length; i++){
    //   const startElementCompo = document.getElementById((i+1).toString())
    //   for (let j = 0; j < this.superpixels.clusters.length; j++) {
    //     if (this.superpixels.clusters[j].belongToPatch === i) {
    //       const endElement = document.getElementById((j+10).toString())
    //       this.lines.push(createLine(startElementCompo, endElement, 'none'))
    //     }
    //   }
    // }

  },
  updated() {

    console.log("-----------------------------------Updated")
    for (let i = 0; i < this.lines.length; i++){
      this.lines[i].remove()
    }
    this.lines.length = 0
    console.log("patch cluster: ", this.patches.clusters.length, "line length: ", this.lines.length)
    // if (this.lines.length < this.patches.clusters.length){
    // this.getInitialImages()
    // }
    if (this.lines.length < this.patches.clusters.length+this.superpixels.clusters.length)
      this.drawPatchLines(this.patches)
    if (this.lines.length < this.patches.clusters.length+this.superpixels.clusters.length)
      this.drawSuperpixelLines(this.superpixels)
    console.log(this.lines)
  },
  beforeDestroy() {
    function showLine(lines, index){
      lines[index].hide()
    }
    for (let i = 0; i < this.lines.length; i++){
      showLine(this.lines, i)
    }
    for (let i = 0; i < this.lines.length; i++){
      this.lines[i].remove()
    }
    this.lines.length = 0
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
  /*align-items: center;*/
  justify-content: start;
  display: flex;
  flex-direction: column;
  /*flex-wrap: wrap;*/
}
.picBoxMain{
  margin-bottom: 20px;
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
}

.picBoxOption{
  background-color: white;
  border: lightgray solid;
  border-width: 1px;
  border-radius: 20px;
  width:85px;
  height: 85px;
}
.objectLevelContainerLayout{
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  flex-wrap: wrap;
  margin-top: 20px;
  /*justify-content: center*/
}
.objectLevelImageContainer{
  display:flex;
  flex-wrap: wrap;
  width: 435px;
  /*margin-right: 60px;*/
  text-align: center;
  /*margin-bottom: 20px;*/
  background-color: white;
  border: #565454 solid;
  border-width: 2px;
  border-radius: 20px;
  background-color: rgba(208, 214, 224, 0.99);
}
.componentLevelImageContainer{
  display:flex;
  flex-wrap: wrap;
  width: 260px;
  text-align: center;
  background-color: white;
  border: #565454 solid;
  border-width: 2px;
  border-radius: 20px;
  background-color: rgba(208, 214, 224, 0.99);
}
.node{
  border-radius: 50%;
  background-color: #a6b4c0;
  width: 40px;
  height: 40px
}
.node:hover{
  background-color: rgba(68, 117, 173, 0.98);
  cursor: pointer;
}
.treeTitle{
  font-size: 20px;
  color: gray;
  /*background-color: #003A70;*/
  /*height: 40px;*/
  /*padding-left: 20px;*/
}
.treeHint{
  font-size: 10px;
  color: whitesmoke;
}

.topicMain{
  display: flex;
  flex-direction: column;
  width: 40%;
  margin-left: 60px;
  font-size: 30px;
  color: #003A70;
}
.objLevel{
  margin-bottom: 20px;
  border: gray ;
  border-radius: 10px;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  width: 100%;
  justify-content: start;
  display: flex;
  flex-direction: column;
  background-color: lightgray;
  margin-top: 40px;
  color: gray
}
.objLevel:hover{
  background-color: #42b983;
  color: whitesmoke;
}
</style>