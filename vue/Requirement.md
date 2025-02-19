> Comments
> * TODO [1] Basic requirements to get data from backend.
> * TODO [2] Advanced requirements to add features.


<h1>/home</h1>

<h2>OptionMain.vue</h2>


TODO [1]

`optionPics`:
```vue
[
    {
      src: require('@/assets/image data/mainline/sorrel/handle image/6.jpg'), 
      id: 'n02389026', 
      class: "sorrel"
    }
]
```
TODO [2]

`models`:
```vue
[
    {
      label: "DeepLabV3", 
      id: '1'
    }
]
```

<h2>Main.vue</h2>
TODO [1]

`explainedPic`
```vue
{
  src: require('@/assets/image data/mainline/'+this.selectedPic.class+'/deeplabv3/heatmap/6-c.jpg'),
  contributors: 
                {
                  high: 'Head',
                  medium: 'Body',
                  low: 'Foot'
                }
}
```
`explainPic()`: function should be programed in backend
```vue
// function: getExplainedPic(selectedModel, selectedPic)
// Output is {src:"", contributors:{}}
this.explainedPic = this.switched ? getExplainedPicSrc(selectedModel, selectedPic) : ''
```
TODO [2]
```vue
// Get from backend, need new script to get prediction label. Replace this.selectedPic.class to show in OUTPUT.
predictedLabel: 'tabby'
```


<h1>/extraction</h1>
