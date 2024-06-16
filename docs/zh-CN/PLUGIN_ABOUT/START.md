# 发布您自己的 `jsonable-platform` 插件

> [!NOTE]
> `<>` (尖括号) 代表该参数必选, `[]` (方括号) 代表该参数可选, 使用时无需输入括号, 括号内字段代表 参数名称 或 您应当填入的内容的名称

# 准备工作
### 安装 依赖管理和打包工具
Poetry 是适用于 Python 的依赖管理和打包工具, 使用其比手动配置 Python 项目文件更为迅速高效与简便.

#### 安装 poetry
```shell
pip install poetry
```

安装完成后, 尝试使用 `poetry --version` 检查是否安装成功.
如果输出类似 `Poetry (version <d>.<d>.<d>)` (其中, `d` 代表任意整数) 即代表安装成功
> 如果您不希望污染全局 Python 环境, 可以创建虚拟环境后, 在虚拟环境内安装


### 初始化包与包配置文件
现在, 您可以运行如下指令以初始化包 (注意在项目根目录打开终端)

```shell
poetry new <项目名称>
```
其中, `项目名称` 代表您所创建的 Pypi 包的名称 (以下简称 "包名"), 仅可使用 半角英文字母 (大小写均可), 下划线 (`_`), 连字符 (`-`)
> Poetry 会自动将 `-` 转化为 `_`, 安装时请使用您输入的原始包名, 但引入 (`import`) 时请使用以 `_` 连接的名称

现在, 您应该会看到如下目录
```diff
<项目名称>
├── pyproject.toml
├── README.md
├── <包名>
│   └── __init__.py
└── tests
    └── __init__.py
```
(参考: <https://python-poetry.org/docs/basic-usage/>)
> 如果您不知道文件有什么作用, 请不要随意修改

首先让我们关注插件目录中的 `pyproject.toml` 文件. 这个文件非常重要, 它包含了要发布插件的一切元信息.

打开上述文件, 您会看到它大概长这样:
```toml
[tool.poetry]
name = "<包名>"
version = "0.1.0"
description = ""
authors = ["<Your Name> <<name@example.com>>"]
readme = "README.md"
packages = [{include = "poetry_demo"}]

[tool.poetry.dependencies]
python = "^3.7"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```
其中, 较为主要的字段如下

|          字段名称           |   作用    |                                                    描述                                                    |
|:-----------------------:|:-------:|:--------------------------------------------------------------------------------------------------------:| 
|    tool.poetry.name     |   包名    |    该包名用于区分包的唯一性, 不应当于现存于 Pypi 的包名重复 <br> 同时, 根据 jsonable-platform 的命名规则, 应当以 `jsonable_platform_` 开头     |
|   tool.poetry.version   |   包版本   |                       包的版本号, 区分不同版本, 不得发同一个版本的包, 一般不得回滚版本 ~~(废话, 如果乐意, 可以每天更新一个玩~~                       |
| tool.poetry.description |  包的描述   |                                             介绍给别人知道您的包干什么用的                                              |
|   tool.poetry.authors   |  作者列表   |      格式见上方示例, 用于表达作者 ~~(虽然 DMCA[^dmca] 和这里的作者不一定有什么关系, 但是就是您写一下才能以作者的身份 发出 年轻人的第一份 DMCA[^dmca] ?~~       |
|   tool.poetry.readme    | 自述文件的路径 |                               自述文件用于介绍项目 和/或 部署流程, 建议使用 `Markdown`[^md] 格式                               |
|  tool.poetry.packages   | 包的本地路径  | 应当符合 Python 包格式, Poetry 假设您的包包含一个与项目根目录中的 tool.poetry.name 同名的包. 若无, 请填充 tool.poetry.packages 以指定您的包及其位置 |
> 请注意: 包名和版本号都是唯一的. 包名不能与其他已经发布的包相同, 而同一个包的同一个版本号也只能发布一次. 如果出现了包名冲突或版本号冲突, 则会在之后的发布流程中出现错误提示. 您可以自行根据错误提示更改包名或更新插件版本.

修改上述文件, 填写相关信息, 保存后即可完成 初始化 的全部流程了
> 上述文件 `tool.poetry.authors` 字段 `Your Name` 代表您的用户名, 空格隔开用尖括号包裹的为您的邮箱, 格式如下 `<name@example.com>`, 两边尖括号不可省去

更多 关于 `pyproject.toml` 的详细内容, 请参阅 [The pyproject.toml file | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/pyproject) 

### 下一步, [开始编写插件](CODING_NOW.md)

## 参考资料
1. <https://koishi.chat/zh-CN/guide/develop/publish.html>
2. <https://python-poetry.org/docs/basic-usage/>

[^dmca]: <https://www.dmca.com/> 或 <https://zh.wikipedia.org/wiki/数字千年版权法>
[^md]: <https://zh.wikipedia.org/wiki/Markdown>
