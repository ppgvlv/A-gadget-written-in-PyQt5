from pyecharts.charts import Pie
from pyecharts import options as opts

data = [
    {'id': 2, 'a_type': '收入', 'record_time': '2023-01-01', 'type': '理财', 'money': '99.99', 'mark': '发放啊福娃发',
     'uid': 1},
    {'id': 4, 'a_type': '收入', 'record_time': '2020-01-01', 'type': '理财', 'money': '1000.00', 'mark': 'afwfawfawf',
     'uid': 1},
    {'id': 5, 'a_type': '收入', 'record_time': '2023-08-13', 'type': '工资', 'money': '59999.00', 'mark': 'afwa',
     'uid': 1}]

echarts_data = {}
for row in data:
    if row['type'] not in echarts_data:
        echarts_data[row['type']] = row['money']
    else:
        echarts_data[row['type']] += row['money']

c = (
    Pie()
    .add("", [[k, v] for k, v in echarts_data.items()])
    # .set_global_opts(title_opts=opts.TitleOpts(title="Pie-月度开支"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)

c.render()
