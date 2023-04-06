# Hexo to NotionNext

## [中文](README.md) [English](README.EN.md)



一个简单的 hexo 导入到 [NotionNext](https://github.com/tangly1024/NotionNext) database 的库


[nobelium](https://github.com/craigary/nobelium) 的 databse 相比 NotionNext 少了 category 的列, nobelium 也是可以使用的. 

## 使用

在使用此库之前，您需要完成以下准备工作：

1. NotionNext Database 
   准备工作参看 https://tangly1024.com/article/vercel-deploy-notion-next 

2. Hexo 博客的 _post 目录


3. 安装
```
pip install hexo2notionnext 
```

4. 在安装完库之后，创建配置文件 config.yaml 的配置
```
token_v2: <your_token>
database_url: <your_notion_database_url>
hexo_post_path: <your_hexo_post_path>
sulg_format: ':year-:day-:month-:name'
```


**token_v2**
  
  notion.so  cookie 中 token_v2 的值

**database_url**
  
  notionNext 页面的地址,如果没有 [Duplicate](https://tanghh.notion.site/02ab3b8678004aa69e9e415905ef32a5?v=b7eb215720224ca5827bfaa5ef82cf2d) 到自己的 notion 中.

**hexo_post_path**
  
  本地 Hexo 目录 的 `source/_posts` 目录

**sulg_format**
  
  路径的格式参考 https://hexo.io/zh-cn/docs/permalinks ,不支持 :id,  



5. 配置完成后,使用以下命令将Hexo文章导入到NotionNext 的 database 中：

```
hexo2notionnext -c config.yaml 
```

## 问题
- For those getting 'HTTPError( requests.exceptions.HTTPError: Invalid input.)' 
  出现这个问题 
1. 在终端上运行 `pip show notion`
2. 获取 notion 包位置并访问其内容（例如`/usr/local/lib/python3.9/site-packages/notion` ）。
3. 将 `store.py`  第 280 行更改为 `limit: 100`
https://github.com/paperboi/kindle2notion/issues/14 

    
## 感谢

https://github.com/Cobertos/md2notion 

https://github.com/jamalex/notion-py

## 许可证

The MIT License.