# Debug Notes

## Vue组件间相互传值 Passing Values Between Vue Components
Feb 25 2024
### Requirement background
在主页面中，`@/components/Option.vue`菜单栏和核心功能栏`@/components/Main.Vue`相互独立，互为兄弟组件，同为`@/views/Home.vue`的子组件。
`@/components/Option.vue`中选择的图片和`@/components/Main.Vue`中进行预测和解释的图片直接关联，因此需要一个变量将`@/components/Option.vue`中选中的图片ID传给`@/components/Main.Vue`

### Solution
由于设计兄弟组件的值传递，故需要一个中间区域挂载传递的值。
1. 创建`@/common/bus.js`
```javascript
// 把一些数据挂载到公共的地方
import Vue from "vue";
export default new Vue;
```
2. 在`@/components/Option.vue`引入`@/common/bus.js`，编写传递值的方法，其中`bus.$emit`中的toMain是另一个组件中接受数据的`event`
```Vue
<script>
import bus from "@/common/bus"

export default {
  name: "Option",
  data() {
    return {
      picID: 'pic3',
    }
  },
  methods: {
    selectPic() {
      bus.$emit("toMain", this.picID);
    }
  }
}
</script>
```
3. 在`@/components/Main.Vue`引入`@/common/bus.js`，编写mount方法，用箭头函数将data赋值给当前组件中的变量
```vue
<script>
import bus from "@/common/bus"
export default {
  name: "Main",
  data() {
    return {
      selectPicID: '',
    }
  },
  mounted() {
      bus.$on("toMain", (data)=>{
        this.selectPicID = data
      })
  }
}
</script>
```

## V-for和V-if的灵活运用展示图片
Feb 25 2024
### Requirement background
用`el-image`一个个渲染图片太麻烦

### Solution
```vue
        <div v-for="item in optionPics" :key="item.id">
          <el-image v-if="item.id === picID"
                    class= "picBoxOptionActive"
                    :src="item.src"
                    @click="selectPic(item.id)"/>
          <el-image v-else
                    class= "picBoxOptionNotActive"
                    :src="item.src"
                    @click="selectPic(item.id)"/>
        </div>
```

## `el-option`用`@click`无法触发事件
Feb 25 2024
### Requirement background
点击下拉框的选项触发事件

### Solution
使用`@click.native=""`
```vue
          <el-select filterable placeholder="Select Model"  v-model="select">
            <el-option v-for="item in models"
                       :key="item.id"
                       :label="item.label"
                       :value="item.id"
                       @click.native="selectModel(item.id)"> </el-option>
          </el-select>
```