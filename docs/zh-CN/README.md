# jsonable-platform
适用于 Python 的 自定义类 JSON 转换框架

> 您可以自定义 Python 类, 通过继承 转换基类 后, 即可将您所写的一切类转化为 JSON 字符串, 持久化于 JSON 文件中

> [!Important]
> 本框架仍在 Beta 阶段, **切勿** 用于生产环境

## 新手入门
* ### 安装
  * 在您所需求的项目 Python 环境下, 在终端中运行如下内容即可安装
```shell
pip install jsonable-platform
```

* ### 使用
  1. ### 定义类
     * 作为 Python 初学者, 您可以安装其他作者编写的适用于本平台的 Pypi 包, 根据命名规则, 其包名应当以 `jsonable-platform-` 开头.
     选择合适的 Pypi 包 安装即可
  
     * 作为进阶用户, 您可以 [自定义 jsonable 类, 详情请参阅此处](PLUGIN_ABOUT/CUSTOM_CLASS.md) <br>
     学习自定义 jsonable 类的方法后, 您可以编写适用于 `jsonable-platform` 的插件并发布. 教程请参阅 [插件编写](PLUGIN_ABOUT/PLUGIN_START.md)
  
  2. ### 编解码
     * 本模块提供了类似于 Python 官方 `json` 库的接口, 您只需使用 `dump`, `dumps`, `load`, `loads` 即可使用
     更为详细的使用文档, 请参阅 [jsonable-platform 使用方法](USAGE.md)
     > 注意: dump(s) 的 `default` 参数和 load(s) 的 `object_pairs_hook` 参数不可用
