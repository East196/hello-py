# hello-py

## start python

[my ipynb](https://nbviewer.jupyter.org/github/East196/hello-py/blob/master/hello_py.ipynb)

[appjar pythonbasic](http://appjar.info/pythonBasics/)

[cs231n python+numpy](http://cs231n.github.io/python-numpy-tutorial/)

[Think python](http://greenteapress.com/thinkpython/html/index.html)

## Add lib info by fabric

pip install fabric

use fabric to install other lib and doc it

fabfile.py

```
from fabric.api import local

def install():
    local('pip install arrow') # arrow python时间库
```

`fab install`

## jupyter

用nbviewer和github结合看ipynb那叫一个爽啊 <https://nbviewer.jupyter.org/github/shikanon/MyPresentations/blob/master/DeepLearning/LearnOfDeepLearning.ipynb>

nbviewer:`https://nbviewer.jupyter.org/`

github/用户名/项目名:`github/shikanon/MyPresentations/`

路径：`blob/master/DeepLearning/LearnOfDeepLearning.ipynb`

## time
https://blog.csdn.net/p9bl5bxp/article/details/54945920


## test
可以考虑用tdd方式写通用工具库
力挺py.test

## py2 to py3
自带`2to3 -w xxx.py`,可直接针对文件夹
文件编码问题可以使用 `with open("%s/%s.py" % (path, model["name"]), "w", encoding="utf-8") as fp:`
