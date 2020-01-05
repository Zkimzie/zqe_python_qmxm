# zqe_python_qmxm
### python_qmxm
- [github_url](https://github.com/Zkimzie/zqe_python_qmxm)
- [pythonanywhere URL]()

#### Project Structure
    -static
        - bootstarp.css
        -echarts.min.js
    -templates
        - rank.html
        - score.html
        - difference.html
        - GDP.html
        - rank.html
        - result.html
        - selection.html
        - chart.html
        - chart1.html
        - chart2.html
    - app.py
    - happiness.sql



##### 数据传递描述：
1. 创建一个happiness的数据库，创建item表，为下拉框引入参数，引入相关的.csv数据文件
![](https://github.com/Zkimzie/zqe_python_qmxm/blob/master/image/%E6%95%B0%E6%8D%AE%E5%BA%93.jpg?raw=true)
2. import mysql.connector
```
happiness={
    "host":"127.0.0.1",
    "user":"root",
    "password":"123456789",
    "database":"happiness"
}
#菜单栏查询
conn = mysql.connector.connect(**happiness)
cursor = conn.cursor()
_SQL = "SELECT item_name FROM  item"
cursor.execute(_SQL)
results = cursor.fetchall()
print(results)
all_item=list();
for (i,) in results:
    all_item.append(i)
conn.close()
```
*索取item数据*




##### HTML档描述：
- base.html:基础页面，引用了bootstrap导航模板，导航栏选择score、rank、difference、GDP对应页面
- result.html：主页面，主要功能:展示数据表格、下拉选择跳转数据界面
- selection.html：下拉框查找路由跳转界面，展示对应的图表
- difference.html：2015年-2017年世界幸福分数差值路由跳转界面，展示对应的图表及结论
- GDP.html：2015年-2017年世界GDP与前十的幸福排名路由跳转界面，展示对应的图表及结论
- rank.html：2015-2017年世界幸福指数路由跳转界面，展示对应的图表及结论
- score.html：2015-2017年世界幸福分数路由跳转界面，展示对应的图表及结论
- chart.html:渲染图表生成的html
- chart1.html：渲染rank2015-2017年世界幸福指数在前二十的国家的html
- chart2.html：渲染rank2015-2017年世界幸福指数在后二十的国家的html


##### Python档描述：
```
from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline , Tab , Bar ,Line
from pyecharts.globals import ThemeType
from flask_bootstrap import Bootstrap
```
模块引用

```
happiness={
    "host":"127.0.0.1",
    "user":"root",
    "password":"123456789",
    "database":"happiness"
}
#菜单栏查询
conn = mysql.connector.connect(**happiness)
cursor = conn.cursor()
_SQL = "SELECT item_name FROM  item"
cursor.execute(_SQL)
results = cursor.fetchall()
print(results)
all_item=list();
for (i,) in results:
    all_item.append(i)
conn.close()
```

连接数据库happiness，建立游标，执行数据查询语句，得到items，遍历结果即得到下拉框选项的集合

```
def score_map() -> Timeline:
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    SQL = "SELECT * FROM score"
    cursor.execute(SQL)
    u = cursor.fetchall()
    cols = cursor.description
    conn.commit()
    conn.close()
    col = []
    for i in cols:
        col.append(i[0])
    data = list(map(list, u))
    data = pd.DataFrame(data, columns=col)
    print(data)
```
 
连接数据库，建立游标，执行查询语句，获取score列名和结果集，将列名添加到表头集合中，将查询的数据转化为表格式数据，同理可得rank、difference、GDP


```
    tl = Timeline()
    for i in range(2015, 2018):
        map0 = (
            Map()
                .add(
                "世界幸福分数", list(zip(list(data.country), list(data["score_{}".format(i)]))), "world", is_map_symbol_show=False
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}年世界幸福分数".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                     font_style="italic")),
                # 设置副标题样式，进行图例说明
                visualmap_opts=opts.VisualMapOpts(min_=data['score_2016'].min(), max_=data['score_2016'].max(), series_index=0),
            )
        )
        tl.add(map0, "{}".format(i))
    return tl
```
score图的代码

```
def rank_page1() -> Tab:
    tab = Tab()
    bar_base2015().render_notebook()
    bar_base2016().render_notebook()
    bar_base2017().render_notebook()
    tab.add(bar_base2015(), "2015年前二十排名")
    tab.add(bar_base2016(), "2016年前二十排名")
    tab.add(bar_base2017(), "2017年前二十排名")
    return tab

def rank_page2() -> Tab:
    tab=Tab()
    bar_base2015_1().render_notebook()
    bar_base2016_1().render_notebook()
    bar_base2017_1().render_notebook()
    tab.add(bar_base2015_1(), "2015年后二十排名")
    tab.add(bar_base2016_1(), "2016年后二十排名")
    tab.add(bar_base2017_1(), "2017年后二十排名")
    return tab
```
定义rank2015-2017年前20名国家的函数和2015-2017年后20名国家的函数，生成柱状图


##### Web App动作描述：
```
@app.route('/',methods=['GET'])
def main():
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM ranks"
    cursor.execute(_SQL)
    result = cursor.fetchall()
    cols = cursor.description
    col = []
    for i in cols:
        col.append(i[0])
    conn.close()
    return render_template('results.html',
                           data = result,
                           cols=cols,
                           all_item=all_item)
```
主页路由，连接数据库，建立游标，查询ranks数据，返回results页面

```
@app.route('/selection',methods=['POST'])
def item_select() -> 'html':
    selection = request.form["the_selected"]
    print(selection) # 检查用户输入

    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM "+ selection
    print(_SQL)
    cursor.execute(_SQL)
    result = cursor.fetchall()
    cols = cursor.description
    col = []
    for i in cols:
        col.append(i[0])
    if selection == "score":
        score_map().render(path="./templates/chart.html")
        with open("./templates/chart.html", encoding="utf8", mode="r") as f:
            plot_all = "".join(f.readlines())
    elif selection == "ranks":
        rank_page1().render(path="./templates/chart1.html")
        with open("./templates/chart1.html", encoding="utf8", mode="r") as f1:
            plot_all1 = "".join(f1.readlines())
        rank_page2().render(path="./templates/chart2.html")
        with open("./templates/chart2.html", encoding="utf8", mode="r") as f2:
            plot_all2 = "".join(f2.readlines())
        return render_template('selection.html',
                               data=result,
                               cols=cols,
                               all_item=all_item,
                               the_plot_all1=plot_all1,
                               the_plot_all2=plot_all2)
    elif selection == "GDP":
        GDP_bar().render(path="./templates/chart.html")
        with open("./templates/chart.html", encoding="utf8", mode="r") as f:
            plot_all = "".join(f.readlines())
    elif selection == "difference":
        difference_bar().render(path="./templates/chart.html")
        with open("./templates/chart.html", encoding="utf8", mode="r") as f:
            plot_all = "".join(f.readlines())
    return render_template('selection.html',
                           data = result,
                           cols=cols,
                           all_item=all_item,
                           the_plot_all=plot_all)
```
表单选择路由，获取表单传过来的the_selected的参数，连接数据库，建立游标，查询传过来的参数对应的表，执行数据查询语句，获取结果集和列名，将列名添加到表头集合中。判断参数类型，根据类型绘制相应的图表，最终返回结果集，表头集合和图表。

```
@app.route('/rank',methods=['GET'])
def main_next():
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM ranks"
    cursor.execute(_SQL)
    result = cursor.fetchall()
    conn.close()
    rank_page1().render(path="./templates/chart1.html")
    with open("./templates/chart1.html", encoding="utf8", mode="r") as f1:
        plot_all1 = "".join(f1.readlines())
    rank_page2().render(path="./templates/chart2.html")
    with open("./templates/chart2.html", encoding="utf8", mode="r") as f2:
        plot_all2 = "".join(f2.readlines())
    return render_template('rank.html',
                           data = result,
                           all_item=all_item,
                           the_plot_all1=plot_all1,
                           the_plot_all2=plot_all2
                           )
```
rank页面路由，为主页的下一页，连接数据库，建立游标，执行查询语句，根据结果集绘制图表，打开绘制好的界面，同理可得score、difference、GDP


