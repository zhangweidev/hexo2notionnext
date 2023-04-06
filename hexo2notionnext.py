import io
import os.path
import glob
import yaml
import argparse
from pathlib import Path
from notion.block import PageBlock
from notion.client import NotionClient
from md2notion.upload import upload
from datetime import datetime

from  dateutil.parser import parse

from notion.collection import NotionDate

# read hexo post file,return sorted list
def read_post_file(hexo_post_path): 
    hexo_post_path = os.path.abspath(hexo_post_path) 
    pathname = os.path.join(hexo_post_path,"**/*.md")    
   
    bloglist= [] 
    index = 0
    for fp in glob.glob(pathname, recursive=True):  
        index += 1
        sulg = fp.removeprefix(hexo_post_path).lstrip("/").rstrip(".md")
        # print(index,sulg) 

        with open(fp, "r", encoding="utf-8") as mdFile:
            # Preprocess the Markdown frontmatter into yaml code fences
            try: 
                mdStr = mdFile.read() 
                mdStr = mdStr.strip('-').strip() 
                mdChunks = mdStr.split("---",1) 
                header = yaml.safe_load(mdChunks[0])
                content = mdChunks[1]

                title = header.get('title',"")

                date = header.get('date')
                
                if  isinstance(date, str):
                    date = parse(date)
                if  not isinstance(date, datetime):     
                    f_create_time = os.path.getctime(fp)
                    date= datetime.fromtimestamp(f_create_time)
                categories = header.get('categories')
                tags = header.get('tags')
                if categories:
                    if isinstance(categories, str):
                        categories =categories
                    if isinstance(categories, list) and len(categories)>0:
                        categories = categories[0]
                 
                page ={
                    "filepath": fp,
                    "title": title,
                    "slug": sulg,
                    "date":date,
                    "content":content,
                    "category":categories,
                    "tags":tags 
                }
                bloglist.append(page)
            except Exception as e:
                print(f"read file {fp} error: {e}")
 
    bloglist.sort(key=lambda x:x['date'].timestamp(),reverse=True)
    return bloglist 

def import_notion(token_v2, database_url,bloglist):
    client = NotionClient( token_v2=token_v2)
    cv = client.get_collection_view(database_url)
    index = 0
    for page in bloglist:
        index += 1
        try:
            title = page.get("title")
            sulg = page.get("slug")
            date = page.get("date")
            categories = page.get("category")
            tags = page.get("tags")
            content = page.get("content")
            fp = page.get("filepath") 

            row = cv.collection.add_row()
            row.type = "Post"
            row.status= "Published"
            row.title=title
            row.summary=content[0:200]+"..."
            row.slug=sulg
            row.category=categories
            row.tags=tags
            row.date=NotionDate(date)

            mdFile = io.StringIO(content)
            mdFile.__dict__["name"] = fp  # Set this so we can resolve images later

            pageName = os.path.basename(fp)[:40]

            # newPage = page.children.add_new(PageBlock, title=pageName)
            print(f"{index}/{len(bloglist)}:Uploading {fp} to Notion.so at page {pageName}")
            # Get the image relative to the markdown file in the flavor that Hexo
            # stores its images (in a folder with the same name as the md file)
 
            def convertImagePath(imagePath, mdFilePath):
                return Path(mdFilePath).parent / Path(mdFilePath).stem / Path(imagePath)
            upload(mdFile, row, imagePathFunc=convertImagePath)
        
        except Exception as e:
                print(f"   Uploading {fp} error: {e}")



def main():

    parser = argparse.ArgumentParser(description='Hexo import to NotionNext database .')
    parser.add_argument('-c', type=str,help='config file',default="config.yaml")
    args = parser.parse_args() 
    conf=yaml.safe_load(open(args.c,'r',encoding='utf-8'))
  
    token_v2 = conf["token_v2"]
    database_url = conf["database_url"]
    hexo_post_path = conf["hexo_post_path"]

    bloglist = read_post_file(hexo_post_path) 

    import_notion(token_v2, database_url,bloglist)


if __name__ == "__main__":
    main()