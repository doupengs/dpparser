```
     _                                      
  __| |_ __  _ __   __ _ _ __ ___  ___ _ __ 
 / _` | '_ \| '_ \ / _` | '__/ __|/ _ \ '__|
| (_| | |_) | |_) | (_| | |  \__ \  __/ |   
 \__,_| .__/| .__/ \__,_|_|  |___/\___|_|   
      |_|   |_|        v-0.0.1                      规则...就是用来打破的
```

## 介绍

- 这是一个网页解析器模块
- 主要将 re 和 xpath 相结合封装在一起，支持连贯的操作
- 如果你是一名python爬虫爱好者，这个模块你也许会感兴趣

#### 实例化

```python
# coding: utf-8

import requests
from dpparser import Parser

url = 'http://www.xxx.com'
response = requests.get(url)
response.encoding = 'utf-8'

root = Parser(data=response.text, response=response, url=url)

# 没有 data 和 url 可以根据 response 得出
# root = Parser(data=response.text, url=url)
# root = Parser(response=response)
```

#### 实例化后 root 的属性与方法

```python
root.data
root.response
root.url

root.xpathall(xpath)
root.xpathone(xpath)
root.reall(pattern)
root.reone(pattern)
root.resub(pattern, goalStr, count=0)

root.unocode()
root.bytes(encoding='utf8')
root.int()
root.float()
root.datetime(timeStrFormat="%Y-%m-%d %H:%M:%S", returnStrType=True)
```

- 具体使用参看[示例](https://github.com/doupengs/dpparser/blob/master/test.py)


