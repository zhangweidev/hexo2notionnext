# Hexo to NotionNext

## [中文](README.md) [English](README.EN.md)

A simple tool to import Hexo posts into a [NotionNext](https://github.com/tangly1024/NotionNext) database.

The database used in nobelium lacks the "category" column compared to NotionNext, but it can still be used.

# Usage

Before using this tool, you need to do the following:

1. A NotionNext database. Please refer to https://tangly1024.com/article/vercel-deploy-notion-next for preparation instructions.

2. The _post directory of your Hexo blog.

3. Installation

```
pip install hexo2notionnext 
```


4. After installing the tool, create a configuration file named config.yaml with the following configuration:

```
token_v2: <your_token>
database_url: <your_notion_database_url>
hexo_post_path: <your_hexo_post_path>
sulg_format: ':year-:day-:month-:name'
```
**token_v2**

The value of the token_v2 in the cookie of notion.so.

**database_url**

The URL of your NotionNext page. If not, duplicate it to your own Notion.

**hexo_post_path**

The source/_posts directory of the local Hexo directory.

**sulg_format**

The format of the path reference is https://hexo.io/docs/permalinks/, excluding :id.

5. After configuring, use the following command to import Hexo posts into the NotionNext database:

```
hexo2notionnext -c config.yaml 
```

## Issues

**For those getting 'HTTPError( requests.exceptions.HTTPError: Invalid input.)'**

If this issue occurs:

1. Run `pip show notion` on the terminal
2. Get the package location of the Notion and access its contents (e.g. /usr/local/lib/python3.9/site-packages/notion).
3. Change line 280 in store.py to limit: 100
https://github.com/paperboi/kindle2notion/issues/14

## Thanks

https://github.com/Cobertos/md2notion

https://github.com/jamalex/notion-py

## License

The MIT License.