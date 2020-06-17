# =============================================================================
# 10.2 PDF文本解析基础 by 王宇韬
# =============================================================================

# 1.解析第一页的文本信息
import pdfplumber
pdf = pdfplumber.open('公司A理财公告.PDF')  # 打开PDF文件
pages = pdf.pages  # 通过pages属性获取所有页的信息，此时pages是一个列表
page = pages[0]  # 获取第一页内容
text = page.extract_text()  # 通过
print(text)  # 打印第一页内容
pdf.close()  # 关闭PDF文件

# 2.解析全部页数的文本信息
import pdfplumber
pdf = pdfplumber.open('公司A理财公告.PDF')
pages = pdf.pages
text_all = []
for page in pages:  # 遍历pages中每一页的信息
    text = page.extract_text()  # 提取当页的文本内容
    text_all.append(text)  # 通过列表.append()方法汇总每一页内容
text_all = ''.join(text_all)  # 把列表转换成字符串
print(text_all)  # 打印全部文本内容
pdf.close()
