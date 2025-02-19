<template>
  <div>
    <div style="margin-left: 80px; margin-top: 20px">
      <div style="font-size: 24px;border-bottom: 2px solid lightgrey; width:80%; padding-bottom: 10px"><b>{{$t('sys.profile')}}</b></div>
      <el-row>
        <el-col :span="12">
          <div style="margin-top: 20px"><b>{{$t('sys.name')}}</b></div>
          <el-input style="width: 40%; margin-top: 5px" v-model="me.name"></el-input>
          <div>{{$t('sys.nameHint')}}</div>

          <div style="margin-top: 30px"><b>{{$t('sys.email')}}</b></div>
          <el-input style="width: 35%; margin-top: 5px" v-model="me.email"></el-input>
          <div>{{$t('sys.emailHint')}}</div>

          <el-button class="set-other-btn" style="margin-top: 20px; color: whitesmoke" @click="updateInfo"><b>{{$t('sys.update')}}</b></el-button>
        </el-col>
        <el-col :span="8">
          <div style="display: flex; justify-content: center; margin-top: 20px">
            <div><b>{{$t('sys.profilePicture')}}</b></div>
            <el-avatar :size="200" :src=this.me.picture></el-avatar>

          </div>

        </el-col>
      </el-row>

    </div>

    <div v-if="this.me.permission === 'Admin'">
      <div style="margin-left: 80px; margin-top: 40px">
        <div style="font-size: 24px;border-bottom: 2px solid lightgrey; width:95%; padding-bottom: 10px"><b>{{$t('sys.userM')}}</b></div>
      </div>

      <div class="box" style="padding:20px 20px 20px 20px; margin:20px 20px 20px 80px; width: 90%; display: flex; justify-content: center">
        <el-table
            :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
          <el-table-column
              :label="$t('sys.nameT')"
              prop="name"
              width="100px">
          </el-table-column>
          <el-table-column
              :label="$t('sys.emailT')"
              prop="email">
          </el-table-column>
          <el-table-column
              :label="$t('sys.instituionT')"
              prop="institution"
              width="400px">
          </el-table-column>
          <el-table-column
              :label="$t('sys.permissionT')"
              prop="permission">
            <template slot-scope="scope">
              <el-tag
                  :type="scope.row.permission === 'Admin' ? 'success' : 'primary'"
                  disable-transitions>{{scope.row.permission}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
              align="right">
            <template slot="header" slot-scope="scope">
              <!--            <el-input-->
              <!--                v-model="search"-->
              <!--                size="mini"-->
              <!--                placeholder="Search Name"/>-->
            </template>
            <template slot-scope="scope">
              <!--            <el-button-->
              <!--                size="mini"-->
              <!--                @click="handleEdit(scope.$index, scope.row)">Edit</el-button>-->

              <el-button
                  v-if="tableData.length!==0"
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">{{$t('sys.delete')}}</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>




    <div style="margin-left: 80px; margin-top: 40px">
      <div style="font-size: 24px;border-bottom: 2px solid lightgrey; width:95%; padding-bottom: 10px"><b>{{$t('sys.log')}}</b></div>
    </div>
    <div class="box" style="padding:20px 20px 20px 20px; margin:20px 20px 20px 80px; width: 90%; display: flex; justify-content: center">
      <el-table
          :data="log.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
          style="width: 100%">
        <el-table-column
            :label="$t('sys.logID')"
            prop="id"
            width="100px">
        </el-table-column>
        <el-table-column
            :label="$t('sys.time')"
            prop="updateTime"
            width="200px">
        </el-table-column>
        <el-table-column
            :label="$t('sys.user')"
            prop="user"
            width="250px">
        </el-table-column>
        <el-table-column
            :label="$t('sys.changeLog')"
            prop="changeLog">
        </el-table-column>
<!--        <el-table-column-->
<!--            label="Action">-->
<!--          <template slot-scope="scope">-->
<!--            <el-button-->
<!--                size="mini"-->
<!--                type="primary"-->
<!--                @click="handleEdit(scope.$index, scope.row)">View</el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SettingLog",
  data(){
    return {
      me:{
        name:'',
        email: '',
        id:'',
        picture: ''
      },

      user:{
        name: '',
        email: '',
        institution: '',
        permission:''
      },
      tableData: [],
      log:[
        {
          id: 0,
          updateTime: '2024-04-29 17:31:59',
          user:'Yunzhe',
          changeLog:'Log In. Update one dataset',
        }
      ],
      search: ''
    }
  },
  methods: {
    searchUser(){
      axios({
        method: "get",
        params: {},
        url: 'http://localhost:8000/main/add_user/'
      }).then(res=> {
        if (res.data["admin"].length !== 0)
            this.tableData = res.data["admin"]
        else
          this.tableData = res.data["user"]
        this.me = res.data["user"][0]
        this.me.picture = 'data:image/jpeg;base64, ' + this.me.picture
        this.searchLog()
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    searchLog(){
      axios({
        method: "get",
        params: {user: this.me.id, email: this.me.email},
        url: 'http://localhost:8000/main/search_log/'
      }).then(res=> {
        this.log = res.data
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
    },
    updateInfo(){
      axios({
        method: "get",
        params: {name: this.me.name, email: this.me.email, id: this.me.id},
        url: 'http://localhost:8000/main/update_profile/'
      }).then(res=> {
          console.log(res.data)
           this.$message({
             type:"success",
             message:"Update Success"
           });
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
      this.searchUser()
    },
    handleEdit(){

    },
    handleDelete(index, row){
      console.log(index, row)
      axios({
        method: "get",
        params: {id: row.id},
        url: 'http://localhost:8000/main/delete_user/'
      }).then(res=> {
        console.log(res.data)
      })
          .catch(error => {
            console.error('Error fetching image', error);
          });
      this.searchUser()
    }
  },
  mounted() {
    this.searchUser()
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
.set-other-btn{
  color: #fff;
  background-color: #1F883D;
}
</style>