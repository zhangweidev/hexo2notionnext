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
import hashlib


typ = "notionnext"

def sulg_hash(slug,date):
    sha = hashlib.sha1() 
    sha.update((slug + str(int(date.timestamp()))).encode()) 
    sha1 = sha.hexdigest()[:12]
    return sha1


def _format_parse(data: dict, s: str):
    result = s
    for key,value in data.items():
        if value:
            result = result.replace(f':{key}', value)
    return result.replace("//", "/")

def sulg_format_parse(page: dict, s: str): 
    sulg_dcit={} 

    sulg_dcit["year"] = page.get("date").strftime("%Y") 
    sulg_dcit["month"] = page.get("date").strftime("%m") 
    sulg_dcit["day"] = '{:02d}'.format(page.get("date").day)
    sulg_dcit["i_month"] = '{:d}'.format( page.get("date").month)
    sulg_dcit["i_day"] = '{:d}'.format(page.get("date").day)
    sulg_dcit["hour"] = page.get("date").strftime("%H")
    sulg_dcit["minute"] = page.get("date").strftime("%M")
    sulg_dcit["second"] = page.get("date").strftime("%S")
    sulg_dcit["title"] = page.get("title","").replace(" ", "")  
    category = page.get("category")  
    sulg_dcit["category"] = "/".join(category) if category else ""
    sulg_dcit["name"] = page.get("name","")
    sulg_dcit["post_tile"]=page.get("post_title","")
    sulg_dcit["hash"] = sulg_hash(sulg_dcit["title"],page.get("date")) 
    return _format_parse(sulg_dcit,s)
 

# read hexo post file,return sorted list
def read_post_file(hexo_post_path,sulg_format): 
    hexo_post_path = os.path.abspath(hexo_post_path) 
    pathname = os.path.join(hexo_post_path,"**/*.md")    
   
    bloglist= [] 
    index = 0
    for fp in glob.glob(pathname, recursive=True):   
        index += 1
        # sulg = fp.removeprefix(hexo_post_path).lstrip("/").rstrip(".md")
        title = os.path.relpath(fp, hexo_post_path).replace(" ", "")
        name = os.path.basename(fp).rstrip(".md").strip()

        with open(fp, "r", encoding="utf-8") as mdFile:
            # Preprocess the Markdown frontmatter into yaml code fences
            try: 
            
                mdStr = mdFile.read() 
                mdStr = mdStr.strip('-').strip() 
                mdChunks = mdStr.split("---",1) 
                header = yaml.safe_load(mdChunks[0])
                content = mdChunks[1]

                post_title = header.get('title',"").replace(" ", "") 
                date = header.get('date')
            
                if  isinstance(date, str):
                    date = parse(date)
                if  not isinstance(date, datetime):     
                    f_create_time = os.path.getctime(fp)
                    date= datetime.fromtimestamp(f_create_time)
              
                tags = header.get('tags')
                categories = header.get('categories')
                if categories:
                    if isinstance(categories, str):
                        categories = [categories]
                    elif isinstance(categories, list) and all(isinstance(c, str) for c in categories):
                        # 将所有的元素转换为字符串类型， 
                        categories = [str(c) for c in categories]
                       
                 
                page ={
                    "filepath": fp,
                    "post_title": post_title,
                    "title": title,
                    "name":name,
                    "date":date,
                    "content":content,
                    "category":categories,
                    "tags":tags 
                }

                page["sulg"] = sulg_format_parse(page,sulg_format) 
                bloglist.append(page)
            except Exception as e:
                print(f"read file {fp} error: {e}")
 
    bloglist.sort(key=lambda x:x['date'].timestamp(),reverse=True)
    return bloglist 

def import_notion(token_v2, database_url,bloglist,):
    global typ

    client = NotionClient( token_v2=token_v2)
    cv = client.get_collection_view(database_url)
    index = 0
    for page in bloglist:
        index += 1
        try:
            # print(f"{index}/{len(bloglist)}:Uploading {page.get('filepath')}")
            # print("    ",page)
            
            content = page.get("content") 
            fp = page.get("filepath") 

            row = cv.collection.add_row()
            row.type = "Post"
            row.status= "Published"
            row.title=page.get("name") 
            row.summary=content[0:200]+"..."
            row.slug= page.get("sulg") 

            if typ != "nobelium" :
                category =  page.get("category")
                if category:
                    row.category= category[0]
            row.tags=page.get("tags")
            row.date=NotionDate( page.get("date"))

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
    global typ
    parser = argparse.ArgumentParser(description='Hexo import to NotionNext database .')
    parser.add_argument('-c', type=str,help='config file',default="config.yaml")
    args = parser.parse_args() 
    conf=yaml.safe_load(open(args.c,'r',encoding='utf-8'))
    
    typ = conf["type"]  

    token_v2 = conf["token_v2"]
    database_url = conf["database_url"]
    hexo_post_path = conf["hexo_post_path"]
    sulg_format = conf.get("sulg_format",":year/:month/:day/:title")
 
    bloglist = read_post_file(hexo_post_path,sulg_format) 

    import_notion(token_v2, database_url,bloglist)


if __name__ == "__main__":
    main()