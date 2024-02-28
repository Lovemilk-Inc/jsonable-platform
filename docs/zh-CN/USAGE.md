# jsonable-platform 使用方法

### 函数: `jsonable_platform.dumps(obj, fallback=None, **kwargs)`
* 将 Python 对象 转为 JSON 字符串

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      同时, 当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `ValueError`
    * \*\*kwargs: 任意符合内置 `json.dumps` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.dumps))
      > 注意: 暂不支持 `default` 参数, 且 `ensure_ascii` 参数 默认为 `False`

* 返回: JSON 格式的字符串

### 函数: `jsonable_platform.dump(obj, fp, fallback=None, **kwargs)`
* 将 Python 对象 直接写入文件

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fp: 写入的目标文件的 `FilePoint` (文件指针)
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      同时, 当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `ValueError`
    * \*\*kwargs: 任意符合内置 `json.dump` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.dump))
      > 注意: 暂不支持 `default` 参数, 且 `ensure_ascii` 参数 默认为 `False`

* 返回: `None`

### 函数: `jsonable_platform.loads(s, fallback=None, **kwargs)`
* 将 JSON 字符串 转回 Python 对象 (支持递归转换, 即一个对象的 `data` 是另一个非 JSON 原生支持的对象也可)

* 参数
    * s: 待转换的字符串, 应当符合 JSON 格式
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 任意 Python 对象 <br>
      同时, 当 `fallback` 未传入时, 会抛出 `ValueError`
    * \*\*kwargs: 任意符合内置 `json.loads` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.loads))
      > 注意: 暂不支持 `object_pairs_hook` 参数

* 返回: Python 对象

### 函数: `jsonable_platform.load(fp, **kwargs)`
* 将文件内容 转回 Python 对象 (支持递归转换, 即一个对象的 `data` 是另一个非 JSON 原生支持的对象也可)

* 参数
    * fp: 待转换的 `FilePoint` (文件指针), 文件内容应当符合 JSON 格式
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 任意 Python 对象 <br>
      同时, 当 `fallback` 未传入时, 会抛出 `ValueError`
    * \*\*kwargs: 任意符合内置 `json.load` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.load))
      > 注意: 暂不支持 `object_pairs_hook` 参数

* 返回: Python 对象

### 函数: `jsonable_platform.register(cls, *requirements)`
* 注册类, 以便查找与自动转换

* 参数: 
    * cls: 继承于 `JSONAbleABC` 且实现其方法的类, 具体实现方法请参阅 [自定义 jsonable 类](PLUGIN_ABOUT/CUSTOM_CLASS.md)
    * *requirements: (多个) 继承于 `JSONAbleABC` 且实现其方法的类, 优先使用该依赖项内匹配的类, 若找不到则在全局搜索并类编/解码

* 返回: `None`

### 函数: `jsonable_platform.unregister(cls)`
* 取消注册类

* 参数: 
    * cls: 继承于 `JSONAbleABC` 且实现其方法的类, 具体实现方法请参阅 [自定义 jsonable 类](PLUGIN_ABOUT/CUSTOM_CLASS.md)

* 返回: `None`

### 函数: `jsonable_platform.jsonable_encoder(obj, fallback=None)`
* 编码任意 JSON 原生支持 或 继承于 `JSONAbleABC` 的符合 jsonable 标准的对象

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      同时, 当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `ValueError`

* 返回: 当传入原生 JSON 支持的 Python 对象 时, 直接返回该对象, 否则尝试使用 jsonable 编码, 返回字典如下结构: `{ '<JSONABLE_PREFIX><对象名称>': JSONAbleEncodedDict }` <br>
其中, `JSONABLE_PREFIX` 为 `jsonable_platform.JSONABLE_PREFIX` 字符串常量

### 函数: `jsonable_platform.jsonable_decoder(object_pairs, fallback=None)`
* 解码 JSON 标准字符串回到 Python 对象

* 参数
    * object_pairs: 符合 内置 `json.load(s)` `object_pairs_hook` 参数回调函数第一个参数类型的 列表
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 任意 Python 对象 <br>
      同时, 当 `fallback` 未传入时, 会抛出 `ValueError`

* 返回: 含有 Python 对象的字典

### 函数: `jsonable_platform.directly_encoder(obj)`
* 编码任意 继承于 `JSONAbleABC` 的符合 jsonable 标准的对象

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象

* 返回: 尝试使用 jsonable 编码, 返回字典 (`JSONAbleEncodedDict`) 如下结构: `{ '<JSONABLE_PREFIX><对象名称>': JSONAbleEncodedDict }` <br>
其中, `JSONABLE_PREFIX` 为 `jsonable_platform.JSONABLE_PREFIX` 字符串常量. 如果编码失败, 则抛出 `ValueError`

### 函数: `jsonable_platform.directly_decoder(encoded)`
* 解码 `JSONAbleEncodedDict` 回 Python 对象

* 参数
    * encoded: `JSONAbleEncodedDict` 格式的字典

* 返回: Python 对象. 当所给的字典内 key (键) 非全部包括 `JSONAbleEncodedDict` 定义的 keys (键) 时, 抛出 `KeyError`; 当解码失败, 抛出 `ValueError`

### 类: `JSONAbleABC()`
* jsonable 基类, 实现类方法 `__jsonable_encode__` 和 `__jsonable_decode__` 后, 方可被转换

* 类方法: 请参阅 [自定义 jsonable 类](PLUGIN_ABOUT/CUSTOM_CLASS.md)

### 函数: `jsonable_platform.jsonable_prefix(prefix=None)`
* 设置 `JSONABLE_PREFIX` 的值, 仅限字符串

* 参数:
  * prefix: 值, 该值代表 jsonable 编码后的 keyname (键名) 前缀, 未传入或传入为 `None` 时, 返回当前已设定的 `JSONABLE_PREFIX`

* 返回: `None` 或 返回当前已设定的 `JSONABLE_PREFIX`

### 函数: `jsonable_platform.repr_classname(enable=None)`
* 设置 `REPR_CLASSNAME` 的值, 仅限 bool

* 参数:
  * enable: bool 值, 该值代表 是否使用 `repr(obj)` 作为 jsonable 编码后的 keyname (键名) 内容, 未传入或传入为 `None` 时, 返回当前已设定的 `REPR_CLASSNAME`

* 返回: `None` 或 返回当前已设定的 `REPR_CLASSNAME`
