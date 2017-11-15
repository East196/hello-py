
# xgboost in windows
http://www.picnet.com.au/blogs/guido/post/2016/09/22/xgboost-windows-x64-binaries-for-download/
```
git clone https://github.com/dmlc/xgboost.git xgboost_install_dir
copy lib xgboost.dll (downloaded from this page) into the xgboost_install_dir\python-package\xgboost\ directory
cd xgboost_install_dir\python-package\
python setup.py install
```
dll文件在页面上直接下载，我用的:[xgboost.dll](http://ssl.picnet.com.au/xgboost/20171116/x64_gpu/xgboost.dll)


# matplotlib backend 问题
Backend Qt5Agg is interactive backend. Turning interactive mode on.
解决方案：
[CSDN](http://blog.csdn.net/u012654847/article/details/78357758)
[官网](http://matplotlib.org/users/shell.html)
With the TkAgg backend, which uses the Tkinter user interface toolkit, you can use matplotlib from an arbitrary non-gui python shell. Just set your backend : TkAgg and interactive : True in your matplotlibrc file (see Customizing matplotlib) and fire up python. Then:
```
from pylab import *
plot([1,2,3])
xlabel('hi mom')
```
> 用everything找matplotlibrc很方便