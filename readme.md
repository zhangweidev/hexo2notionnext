# hexo2notionnext 
一个简单的 hexo 导入到 [NotionNext](https://github.com/tangly1024/NotionNext) database 的脚本



当然，下面是一个适用于您的Hexo数据导入到Notion的开源库的Readme示例：

# Hexo to NotionNext

该项目是一个用于将基于Hexo的博客文章导入到Notion的开源库。它使用Python和Notion API来实现导入。该项目旨在帮助将现有的Hexo博客文章迁移到 NotionNext 中。

## 准备工作

在使用此库之前，您需要完成以下准备工作：

1. NotionNext Database 
   准备工作参看 https://tangly1024.com/article/vercel-deploy-notion-next 

2. Hexo 博客的 _post 目录

3. clone 库到本地,并安装项目依赖 
```
git clone git@github.com:zhangweidev/hexo2notionnext.git
cd hexo2notionnext 
pip install -r requirements.txt 
```
   
## 使用

在安装完库之后，需要修改配置文件的配置
```
token_v2: <your_token>
database_url: <your_notion_database_url>"
hexo_post_path: <your_hexo_post_path>
```

token_v2 : notion.so   cookie 中 token_v2 的值
database_url: notionNext 页面的地址,如果没有 [Duplicate](https://tanghh.notion.site/02ab3b8678004aa69e9e415905ef32a5?v=b7eb215720224ca5827bfaa5ef82cf2d) 到自己的 notion 中.
hexo_post_path: 本地 Hexo 目录 的 `source/_post` 目录


配置完成后,使用以下命令将Hexo文章导入到Notion中：

```
python hexo2notionnext.py 
```
也可以指定配置文件
```
python hexo2notionnext.py  -c config.yaml 
```


## 贡献

如果您想要为该项目做出贡献，可以通过以下步骤：

1. Fork该项目。
2. 创建一个新的分支，进行您的更改。
3. 提交您的更改并创建一个Pull Request。

我们欢迎任何贡献，包括但不限于代码贡献，文档编写和错误修复。

## 许可证

该项目使用MIT许可证。有关更多信息，请参见LICENSE文件。