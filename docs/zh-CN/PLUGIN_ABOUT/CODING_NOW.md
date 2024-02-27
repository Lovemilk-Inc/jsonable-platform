from typing import Self

# 开始编写插件
现在, 请打开 `<包名>/__init__.py` (如果没有, 请自行创建) 进行编辑

## 认识插件
本章将介绍插件的编写方式, 并介绍一些场景下的最佳实践.

### 插件的基本形式
一个插件需要满足以下三个条件:
1. 继承与 `JSONAbleABC` 类
2. 实现了 `JSONAbleABC` 的 `__jsonable_encode__` 和 `__jsonable_decode__` 方法
3. 对该类进行导出使得用户得以使用 `register` 函数注册和 `unregister` 取消注册, 或者插件提供了导出的方法在插件内部完成类似行为

例如, 如下即为一个合法的插件 <br>

[//]: # (~~JetBrains 的 LanguageTools 报了奇奇怪怪的错: "动词的修饰一般为‘形容词（副词）+地+动词’。您的意思是否是：合法地插", Koishi 群友 &#40;1096694717@qq.com&#41; 想让我试试: 非法地插~~ <br>)
(该插件实现了 内置 `datetime.datetime` 和 `datetime.timedelta` 的 Jsonable 类)

```python
from jsonable_platform import JSONAbleABC, Self, register, JSONAbleABCEncodedType
from datetime import datetime as std_datetime, timedelta as std_timedelta


class datetime(std_datetime, JSONAbleABC[float]):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.timestamp()

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        return cls.fromtimestamp(data)


class timedelta(std_timedelta, JSONAbleABC[float]):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.total_seconds()

    @classmethod
    def __jsonable_decode__(cls, obj: JSONAbleABCEncodedType) -> Self:
        return cls(seconds=obj)


register(datetime)
register(timedelta)
```

### 一般插件
一般的, 您只需在 `__init__.py` 引入 `jsonable-platform` 库 的 `JSONAbleABC, Self, register, JSONAbleABCEncodedType`, 然后引入 您想要实现 jsonable 的类 (以下简称 "标准类")并同时继承 `JSONAbleABC` 和 标准类 并实现 `JSONAbleABC` 相关方法即可 

例如, 如果您想要实现 `datetime.datetime` 的 jsonable

第一步, 引入与继承

引入相关库和类型
```python
from datetime import datetime
from jsonable_platform import JSONAbleABC  # 引入基类

class MyDatetime(datetime, JSONAbleABC):
    ...
```

第二步, 类方法与实现

您可以使用任何方式序列化反序列化, 在这里, 我将 使用 float 型 时间戳
```python
from datetime import datetime
from jsonable_platform import JSONAbleABC, Self, JSONAbleABCEncodedType  # 引入类型


class MyDatetime(datetime, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.timestamp()  # 返回时间戳, 下面会收到这个时间戳
    
    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        # 这里的 data 就是上面返回的 timestamp
        return cls.fromtimestamp(data)
    
    @classmethod
    def __jsonable_hash__(cls) -> str | None:
        # 这个函数是对象的 hash, hash 相同的对象会给到同一个 jsonable 类编解码
        return 
```
* `__jsonable_encode__(cls, obj)`
    * 编码对象, 在编码时会调用
     
    * 参数:
      * obj: 实例化后的对象
    
    * 返回: 可原生转为 JSON 的类型 (如 `str`, `int`, `float`, `list`, `dict` 等) 和/或 jsonable 实例 (比如您自己实现的 `MyDatetime` 的实例或他人实现的类的实例)
    > 当然, `dict[str, jsonable 实例]` `list[jsonable 实例]` 等也受支持, 这意味着您可以 嵌套编码. 为了避免一个 jsonable 类依赖另一个 jsonable 但后者未加载导致出现错误, 我们提供了 依赖声明, 以便维护依赖关系

    > 注: dict 的 keys (键) 不得为 jsonable 实例
* `__jsonable_decode__(cls, data)`
    * 解码对象, 在解码时会调用
     
    * 参数:
      * data: `__jsonable_encode__` 返回的内容 (如果您的依赖项没有报错, 在返回值中的 jsonable 实例除 id 外, 均与编码前相同)
    
    * 返回: 任意 Python Object, 不过应当 与自己的类型相同 或 为自己的子类的实例
* `__jsonable_hash__(cls)`
    * 获取对象的 hash

    * 返回: 如果返回 `None`, 则使用 类名 (`cls.__name__`) 转为 hash, 否则, 使用 该函数返回值

最后, 将类注册到 `jsonable-platform`, 以便自动搜索并编解码

```python
from datetime import datetime
from jsonable_platform import JSONAbleABC, Self, JSONAbleABCEncodedType, register  # 引入注册器


class MyDatetime(datetime, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.timestamp()  # 返回时间戳, 下面会收到这个时间戳
    
    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        # 这里的 data 就是上面返回的 timestamp
        return cls.fromtimestamp(data)
    
    @classmethod
    def __jsonable_hash__(cls) -> str | None:
        # 这个函数是对象的 hash, hash 相同的对象会给到同一个 jsonable 类编解码
        return 

register(MyDatetime)  # 注册类
```

当然, `register` 函数可以定义依赖, 使用如下方法:
```python
from jsonable_platform import register

register(<类>, <依赖00>, <依赖01>, ...)
```
其中, `类` 为您所编写的类, 后面的 `依赖\d\d` (此处 `\d` 代表自然数) 代表所需依赖, 理论上依赖无数量限制

## 注解


## 参考资料
1. <https://koishi.chat/zh-CN/guide/plugin/>
