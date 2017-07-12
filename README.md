### Add lib info
by fabric

pip install fabric

use fabric to install other lib and doc it

fabfile.py
```
from fabric.api import local

def install():
    local('pip install arrow') # arrow python时间库
```
fab install