# gittxt
给gif上加文字

pip install appJar pillow pyinstaller

appJar记得用稳定的版本0.82.1，否则~~~

pyinstaller gittxt.py -w -F

-w 去命令行
-F 打包成单一文件


# pillow无法安装提示zlib

## 错误提示
```
During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "E:\appdata\Temp\pip-install-8mkxvdse\pillow\setup.py", line 914, in <module>
    raise RequiredDependencyException(msg)
__main__.RequiredDependencyException:

The headers or library files could not be found for zlib,
a required dependency when compiling Pillow from source.

Please see the install instructions at:
   https://pillow.readthedocs.io/en/latest/installation.html

```
## 解决方案: 升级pip
-> 升级 pip 
### 错误提示
```
AttributeError: 'NoneType' object has no attribute 'bytes'
```
### 升级pip的三种方案
#### 直接pip升级
-> `pip install --upgrade pip`无效
#### 直接python升级
-> `python -m pip install --upgrade pip` ok
#### 虚拟环境中的升级
-> `easy_install -U pip` ok
