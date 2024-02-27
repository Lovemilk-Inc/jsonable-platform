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
~~JetBrains 的 LanguageTools 报了奇奇怪怪的错: "动词的修饰一般为‘形容词（副词）+地+动词’。您的意思是否是：合法地插", Koishi 群友 (1096694717@qq.com) 想让我试试: 非法地插~~ <br>
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

## 注解


## 参考资料
1. <https://koishi.chat/zh-CN/guide/plugin/>
