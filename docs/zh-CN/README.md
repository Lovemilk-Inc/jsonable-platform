# jsonable-platform
适用于 Python 的 自定义类 JSON 转换框架

> [!Important]
> 本框架仍在 Beta 阶段, **切勿** 用于生产环境

## 介绍
您可以自定义 Python 类, 通过继承 转换基类 后, 即可将您所写的一切类转化为 JSON 字符串, 持久化于 JSON 文件中

并且, 使用 本框架 对 JSON 进行标记的方法实现自动转换, 不会如 内置 `pickle` 库般加载第三方代码或二进制文件, 无法通过引入外部模块 和/或 代码的方式对您的应用进行注入攻击

当然, 安全是有代价的! <br>
本框架 无法对原生的 Python 对象 进行编解码, 需要您自行实现, 不过好在不难 <br>
什么? 你迫不及待想试一试了? [让我们开始阅读文档吧!](#文档)

## 文档
* [函数 类 的使用方法详解](USAGE.md)
* [插件编写与入门](PLUGIN_ABOUT/START.md)

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
     学习自定义 jsonable 类的方法后, 您可以编写适用于 `jsonable-platform` 的插件并发布. 教程请参阅 [插件编写](PLUGIN_ABOUT/START.md)
  
  2. ### 编解码
     * 本模块提供了类似于 Python 官方 `json` 库的接口, 您只需使用 `dump`, `dumps`, `load`, `loads` 即可使用
     更为详细的使用文档, 请参阅 [jsonable-platform 使用方法](USAGE.md)
     > 注意: dump(s) 的 `default` 参数和 load(s) 的 `object_pairs_hook` 参数不可用

## 关于项目
* 本项目名称可读作: json + able (able 读 /əbəl/) + platform, 听起来像: json(单词读音) 啊(轻声) able(去掉 a 发的音) platform(单词读音)
