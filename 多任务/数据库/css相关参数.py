'''

1、盒子模型：
        width: 100px; 内容部分的宽度
        height:100px; 内容部分的高度
        padding: 10px; padding内边距，设置的是距离,可以设置4个值，同时定义内外盒子的长宽，padding定义内外
                        盒子的间距
        margin: 10px; 外边距，设置的是距离（占用一段距离，未必显示出来）
                    1、margin-top和margin-bottom之间的距离为盒子中最大的外边距
                    2、margin-left和margin-right之间的距离为盒子的外边距之和
        border: solid yellow 5px; 外边框，是外边的框体结构，此处设置为实体，黄色，框宽5
                        1、边框线型solid/dashed/dotted/double
                        2、粗细
                        3、颜色
        background-color: dodgerblue; 内容的背景颜色
        overflow:hidden  当内容溢出时，可用。相关参数，visible默认值，内容处于溢出状态
                         hidden：内容被剪裁，溢出部分不可见
                         scroll：滚动条显示，溢出部分可通过滚动条查看
                         auto：如果内容溢出，则以滚动条显示其余内容
        overflow_x:x轴显示滚动条，_yy轴滚动条，没有xy轴都显示滚动条
        text-overflow指定文本溢出内容的属性
                         clip：修剪文本，不显示溢出部分
                         ellipsis：显示省略号代表修剪的文本
                         string：使用指定字符串代表被修剪的文本
                         注意：该属性，必须和overflow：hidden；white-space：nowrap一起使用
    如果出现两个图片重叠，可能是设置的盒子的宽高有冲突，两部分定义
        float: left并排显示两个盒子，盒子之间没有间隔
        display:inline-block 也是并排显示两个盒子，只是盒子之间有间隔
'''