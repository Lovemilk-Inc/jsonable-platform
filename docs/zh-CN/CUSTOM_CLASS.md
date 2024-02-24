# 自定义 jsonable 类

  * ## jsonable 定义
    * 一般的, 我们认为凡是继承于 `JSONAbleABC` 并且实现了 `__jsonable_encode__` 和 `__jsonable_decode__` 两个类方法的类均称为 jsonable 类

  * ## 自定义 encode 和 decode 方法
    * 我们需要实现上述方法, 以使得可将 该类 转化为 JSON 字符串
    * 下面是示例 (以 datetime 为例)
```python
from datetime import datetime as std_datetime
from jsonable_platform import JSONAbleABC, Self, JSONAbleABCEncodedType, register
  
# 继承 JSONAbleABC 和原始的 datetime, `JSONAbleABC[<type>]` `type` 同时代表了 `__jsonable_encode__` 返回值 和 `__jsonable_decode__` 参数 `obj` 的类型
class datetime(std_datetime, JSONAbleABC[float]):
    # 实现类方法 __jsonable_encode__, 返回一个可转为 JSON 的 Python 基本类型 或 jsonable 类 实例化后的对象
    # 此处实际返回 float 
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.timestamp()
        
    # 实现类方法 __jsonable_decode__, 将转换后的 float 重新转回 Python 的 datetime 对象
    # 此处返回 jsonable 的 datetime 对象 
    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        return cls.fromtimestamp(data)
    
register(datetime)  # 将 datetime 注册到转换器中, 以便自动查找并转换
```
  * 类方法详解
      * `__jsonable_encode__`, 必须实现, 第一个参数为待转换的对象, 返回编码后的可转换为 JSON 的 Python 基本类型 或 jsonable 类 实例化后的对象
          > 注意: Python 字典的键 (key) 不能为 jsonable 类 实例化后的对象, 其他元素均可为 jsonable 类 实例化后的对象
      * `__jsonable_decode__`, 必须实现, 第一个参数为 编码后的对象, 将编码后的 可转为JSON的 Python 基本类型 转为自己的实例, 如果有多层嵌套, 转换器会自动处理, 无需手动转换
      * `__jsonable_hash__`, 可选, 用于查找编码后的类 hash 和 目标类, 默认返回 `None`, 如果返回为 字符串, 则使用该字符串作为 hash

  * ## 注册类
     * 使用 `register` 函数注册类, 后会根据类型匹配并自动调用 `__jsonable_encode__` 类方法
     * 同样的, 您可以使用 `unregister` 取消注册类
