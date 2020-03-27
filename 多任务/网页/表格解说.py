'''
主体：
<table> ：定义表格，表格的边界标签，必定包裹表格的其他元素标签
<tr> ：定义表格的行
<th>：定义表格的表头，需要被<tr>包裹
<td>：定义表格的单元，需要被<tr>包裹
<thead>：定义表格的页眉，表格分组标签，可将表格分割
<tbody>：定义表格的主体，表格分组标签，可将表格分割
<tfoot>：定义表格的页脚，表格分组标签，可将表格分割
<caption>：定义表格标题

属性：
colspan=value 合并列
rowspan=value 合并行
align = left/center/right 水平对齐方式
valign = top/bottom/middle/baseline 垂直对齐方式
cellpadding=value 单元边沿与其内容之间的空白
cellspacng=value 单元格之间的空白

表格的css属性：
caption-side: top/bottom/left/right设置表格标题放置的位置
            说明：left、right位置只有火狐识别，top，bottom IE7以上版本支持
border-spacing:value 单元格间距
background-imge:图片路径
'''