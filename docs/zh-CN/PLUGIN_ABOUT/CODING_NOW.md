# 开始编写插件
现在, 请打开 `<包名>/__init__.py` (如果没有, 请自行创建) 进行编辑

## 认识插件
首先, 容我介绍插件的编写方式, 并介绍一些场景下的最佳实践.

### 插件的基本形式
一个插件需要满足以下三个条件:
1. 有类继承于 `JSONAbleABC` 类
2. 该类实现了 `JSONAbleABC` 的 `__jsonable_encode__` 和 `__jsonable_decode__` 方法, 并确保输入数据正确情况下可以正常编解码
3. 对该类进行导出使得用户得以使用 `register` 函数注册和 `unregister` 取消注册, 或者 插件提供了 导出的方法 或 自动 在插件内部完成类似行为

例如, 如下即为一个合法的插件 <br>

[//]: # (~~JetBrains 的 LanguageTools 报了奇奇怪怪的错: "动词的修饰一般为‘形容词（副词）+地+动词’。您的意思是否是：合法地插", Koishi 群友 &#40;1096694717@qq.com&#41; 想让我试试: 非法地插~~ <br>)
(该插件实现了 内置 `datetime.datetime` 和 `datetime.timedelta` 的 Jsonable 类)

```python
from jsonable_platform import JSONAbleABC, Self, register, JSONSupportedTypes
from datetime import datetime as std_datetime, timedelta as std_timedelta


class datetime(std_datetime, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return obj.timestamp()

    @classmethod
    def __jsonable_decode__(cls, data: JSONSupportedTypes) -> Self:
        return cls.fromtimestamp(data)


class timedelta(std_timedelta, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return obj.total_seconds()

    @classmethod
    def __jsonable_decode__(cls, obj: JSONSupportedTypes) -> Self:
        return cls(seconds=obj)


register(datetime)
register(timedelta)
```

### 一般插件
一般的, 您只需在 `__init__.py` 引入 `jsonable-platform` 库 的 `JSONAbleABC, Self, register, JSONSupportedTypes`, 然后引入 您想要实现 jsonable 的类 (以下简称 "标准类")并同时继承 `JSONAbleABC` 和 标准类 并实现 `JSONAbleABC` 相关方法即可 

例如, 如果您想要实现 `datetime.datetime` 的 jsonable

#### 1. 引入与继承

引入相关库和类型
```python
from datetime import datetime
from jsonable_platform import JSONAbleABC  # 引入基类

class MyDatetime(datetime, JSONAbleABC):
    ...
```

#### 2. 类方法与实现

您可以使用任何方式序列化反序列化, 在这里, 我将 使用 float 型 时间戳
```python
from datetime import datetime
from jsonable_platform import JSONAbleABC, Self, JSONSupportedTypes  # 引入类型


class MyDatetime(datetime, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return obj.timestamp()  # 返回时间戳, 下面的 `__jsonable_decode__` 会收到这个时间戳
    
    @classmethod
    def __jsonable_decode__(cls, data: JSONSupportedTypes) -> Self:
        # 这里的 data 就是上面的 `__jsonable_encode__` 返回的 timestamp
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
    > 当然, `dict[str, jsonable 实例]` `list[jsonable 实例]` 等也受支持, 这意味着您可以 嵌套编码. 为了避免一个 jsonable 类依赖另一个 jsonable 但后者未加载导致出现错误, 我们提供了 [依赖声明](#依赖声明), 以便维护依赖关系

    > 注: dict 的 keys (键) 不得为 jsonable 实例
* `__jsonable_decode__(cls, data)`
    * 解码对象, 在解码时会调用
     
    * 参数:
      * data: `__jsonable_encode__` 返回的内容 (如果您的依赖项没有报错, 在返回值中的 jsonable 实例除 id 外, 均与编码前相同)
    
    * 返回: 任意 Python Object, 不过应当 与自己的类型相同 或 为自己的子类的实例
* `__jsonable_hash__(cls)`
    * **该函数并非必须实现** 获取对象的 hash

    * 返回: 如果返回 `None` (`JSONAbleABC` 默认返回), 则使用 类名 (`cls.__name__`) 作为 hash, 否则, 使用 该函数返回值, 且返回值必须为 `str`

#### 3. 将类注册到 `jsonable-platform`, 以便自动搜索并编解码

```python
register(MyDatetime)  # 注册类
```

这样, 当您使用 本框架 编解码 JSON 时, 会将 `MyDatetime` 实例转为 JSON 字符串 或 进行相反操作, 您无需手动转换即可持久化存储 Python 对象

### 依赖声明
使用 `register` 函数可以声明依赖, 使用方法如下:
```python
from jsonable_platform import register

register(<cls>, <requirement01>, <requirements02>, ...)
```
其中, `cls` 为您所编写的类, 后面的 `requirement*` 代表所需依赖, 理论上依赖无数量限制

这样, 您就可以使您的类优先在依赖项 (`requirements`) 中搜索并编解码, 而不会受到 外部重名 或 重 hash 类 的影响
> 在新版本 (>=0.0.4.0) 中, 已经区分了 自定义 hash 和 默认搜索的类, 大大减少了上述情况的发生

### 下一步, [发布插件](PUBLISH.md)

## 参考资料
1. <https://koishi.chat/zh-CN/guide/plugin/>
