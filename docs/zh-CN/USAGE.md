# jsonable-platform 使用方法

### 函数: `jsonable_platform.dumps(obj, fallback=None, **kwargs)`
* 将 Python 对象 转为 JSON 字符串

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `TypeError`
    * \*\*kwargs: 任意符合内置 `json.dumps` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.dumps))
      > 注意: 暂不支持 `default` 参数, 且 `ensure_ascii` 参数 默认为 `False`

* 返回: JSON 格式的字符串

### 函数: `jsonable_platform.dump(obj, fp, fallback=None, **kwargs)`
* 将 Python 对象 直接写入文件

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fp: 写入的目标文件的 `FilePoint` (文件指针)
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `TypeError`
    * \*\*kwargs: 任意符合内置 `json.dump` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.dump))
      > 注意: 暂不支持 `default` 参数, 且 `ensure_ascii` 参数 默认为 `False`

* 返回: `None`

### 函数: `jsonable_platform.loads(s, **kwargs)`
* 将 JSON 字符串 转回 Python 对象 (支持递归转换, 即一个对象的 `data` 是另一个非 JSON 原生支持的对象也可)

* 参数
    * s: 待转换的字符串, 应当符合 JSON 格式
    * \*\*kwargs: 任意符合内置 `json.loads` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.loads))
      > 注意: 暂不支持 `cls` 参数
    > 如果您在 编码时 使用了 `fallback` 参数, 您可能需要使用 `object_hook` 和/或 `object_pairs_hook` 参数以解码

* 返回: Python 对象

### 函数: `jsonable_platform.load(fp, **kwargs)`
* 将文件内容 转回 Python 对象 (支持递归转换, 即一个对象的 `data` 是另一个非 JSON 原生支持的对象也可)

* 参数
    * fp: 待转换的 `FilePoint` (文件指针), 文件内容应当符合 JSON 格式
    * \*\*kwargs: 任意符合内置 `json.load` 函数的键值参数 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.load))
      > 注意: 暂不支持 `cls` 参数
    > 如果您在 编码时 使用了 `fallback` 参数, 您可能需要使用 `object_hook` 和/或 `object_pairs_hook` 参数以解码

* 返回: Python 对象

### 函数: `jsonable_platform.register(cls)`
* 注册类, 以便查找与自动转换

* 参数: 
    * cls: 继承于 `JSONAbleABC` 且实现其方法的类, 具体实现方法请参阅 [自定义 jsonable 类](./CUSTOM_CLASS.md)

* 返回: `None`

### 函数: `jsonable_platform.unregister(cls)`
* 取消注册类

* 参数: 
    * cls: 继承于 `JSONAbleABC` 且实现其方法的类, 具体实现方法请参阅 [自定义 jsonable 类](./CUSTOM_CLASS.md)

* 返回: `None`

### 函数: `jsonable_platform.jsonable_encoder(obj, fallback=None)`
* 编码任意 JSON 原生支持 或 继承与 `JSONAbleABC` 的符合 jsonable 标准的对象

* 参数
    * obj: 符合 JSON 标准且仅含有 JSON 原生支持 或 基于 `JSONAbleABC` 实现的可转化为 JSON 字符串的对象
    * fallback: 选填, 默认为 `None`, 当 本模块 无法转换对象时, 将该对象作为第一个参数传入 `fallback`, 其应当返回 `JSONAbleEncodedDict` 格式的 `dict` <br>
      当 `fallback` 返回值不是 `JSONAbleEncodedDict` 时, 会抛出 `TypeError`

* 返回: 当传入原生 JSON 支持的 Python 对象 时, 直接返回该对象, 否则尝试使用 jsonable 编码, 返回字典如下结构: `{ '<JSONABLE_PREFIX><对象名称>': JSONAbleEncodedDict }` <br>
其中, `JSONABLE_PREFIX` 为 `jsonable_platform.JSONABLE_PREFIX` 字符串常量

### 类: `jsonable_platform.JSONAbleDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None)`
* 继承于内置 `json.decoder.JSONDecoder`, 实现了 `decode` 方法

* 参数: 与 内置 `json.decoder.JSONDecoder` 相同 (详情请参阅 [此处](https://docs.python.org/zh-cn/3.12/library/json.html#json.JSONDecoder))
