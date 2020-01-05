from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline , Tab , Bar ,Line
from pyecharts.globals import ThemeType
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
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


#score
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


# rank
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

def bar_base2015() -> Bar:
    data=rank_year("rank_2015")
    print(data)
    x1 = [x for x in data.country.values[0:20]]
    y = [x for x in data['rank_2015'].values[0:20]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x1)
        .add_yaxis("2015年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2015年世界幸福指数在前二十的国家", subtitle=""))
    )
    return c


def bar_base2016() -> Bar:
    data = rank_year("rank_2016")
    print(data)
    x1 = [x for x in data.country.values[0:20]]
    y = [x for x in data['rank_2016'].values[0:20]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x1)
        .add_yaxis("2016年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2016年世界幸福指数在前二十的国家", subtitle=""))
    )
    return c


def bar_base2017() -> Bar:
    data = rank_year("rank_2017")
    print(data)
    x1 = [x for x in data.country.values[0:20]]
    y = [x for x in data['rank_2017'].values[0:20]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x1)
        .add_yaxis("2017年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2017年世界幸福指数在前二十的国家", subtitle=""))
    )
    return c



def bar_base2015_1() -> Bar:
    data=rank_year("rank_2015")
    print(data)
    x2 = [x for x in data.country.values[-20:]]
    y = [x for x in data.rank_2015.values[-20:]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x2)
        .add_yaxis("2015年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2015年世界幸福指数在后二十的国家", subtitle=""))
    )
    return c

def bar_base2016_1() -> Bar:
    data = rank_year("rank_2016")
    print(data)
    x2 = [x for x in data.country.values[-20:]]
    y = [x for x in data.rank_2016.values[-20:]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x2)
        .add_yaxis("2016年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2016年世界幸福指数在后二十的国家", subtitle=""))
    )
    return c


def bar_base2017_1() -> Bar:
    data = rank_year("rank_2017")
    print(data)
    x2 = [x for x in data.country.values[-20:]]
    y = [x for x in data.rank_2017.values[-20:]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(x2)
        .add_yaxis("2017年排名", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="2017年世界幸福指数在后二十的国家", subtitle=""))
    )
    return c


def rank_year(year):
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    # SQL = "SELECT `country`,`"+year+"` FROM ranks ORDER BY if(isnull("+year+"),1,0),"+year+" asc"
    SQL = "SELECT * FROM ranks"
    print(SQL)
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
    return data



#difference
def difference_bar() -> Timeline:
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    SQL = "SELECT * FROM difference"
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
    x = [x for x in data.country.values[0:20]]
    y = [x for x in data.difference.values[0:20]]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
            .add_xaxis(x)
            .add_yaxis("差值", y)
            .set_global_opts(title_opts=opts.TitleOpts(title="2015-2017年世界幸福分数的差值", subtitle="幸福感显著提高的前二十个国家"))
    )
    return c


#GDP
def GDP_bar() -> Bar:
    conn = mysql.connector.connect(**happiness)
    cursor=conn.cursor()
    SQL= "SELECT * FROM GDP"
    cursor.execute(SQL)
    u = cursor.fetchall()
    cols = cursor.description
    conn.commit()
    conn.close()
    col=[]
    for i in cols:
        col.append(i[0])
    data = list(map(list ,u))
    data = pd.DataFrame(data,columns=col)
    print(data)
    x4 = [x for x in data.country.values[0:11]]
    y1 = [x for x in data.GDP_2015.values[0:10]]
    y2 = [x for x in data.GDP_2016.values[0:10]]
    y3 = [x for x in data.GDP_2017.values[0:10]]
    y4 = [x for x in data.rank_difference.values[0:10]]
    x = x4
    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("排名差值", y4)
            .set_global_opts(title_opts=opts.TitleOpts(title="15-17年世界GDP与前十的幸福排名关系"))
    )
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis("2015年", y1)
            .add_yaxis("2016年", y2)
            .add_yaxis("2017年", y3)
    )
    bar.overlap(line)
    return bar





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

@app.route('/score',methods=['GET'])
def rank_next():
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM score"
    cursor.execute(_SQL)
    result = cursor.fetchall()
    conn.close()
    score_map().render(path="./templates/chart.html")
    with open("./templates/chart.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('score.html',
                           data = result,
                           all_item=all_item,
                           the_plot_all=plot_all)

@app.route('/difference',methods=['GET'])
def score_next():
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM difference"
    cursor.execute(_SQL)
    result = cursor.fetchall()
    conn.close()
    difference_bar().render(path="./templates/chart.html")
    with open("./templates/chart.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('difference.html',
                           data = result,
                           all_item=all_item,
                           the_plot_all=plot_all)


@app.route('/GDP',methods=['GET'])
def difference_next():
    conn = mysql.connector.connect(**happiness)
    cursor = conn.cursor()
    _SQL = "SELECT * FROM GDP"
    cursor.execute(_SQL)
    result = cursor.fetchall()
    conn.close()
    GDP_bar().render(path="./templates/chart.html")
    with open("./templates/chart.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('GDP.html',
                           data = result,
                           all_item=all_item,
                           the_plot_all=plot_all)

if __name__ == '__main__':
    app.run(debug=True,port=1999)
