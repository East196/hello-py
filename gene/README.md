
# 使用说明
1. 安装python3
2. `pip install -r req.txt`
3. python gene.py

# 模块说明
## gene.py
结合model模型，tpl模板生成代码

## model.py
模型设置，格式yaml
| 字段     | 说明     |
| :------------- | :------------- |
| name       | 名称       |
| label       | 显示的名称，一般是中文       |
| doc       | 描述       |
| items       | 下级字段       |
| -name       | 字段名称       |
| -label       | 字段显示       |
| -type       | 字段类型       |
| -doc       | 字段描述       |


## tpl.py
模板设置，格式jinja2
