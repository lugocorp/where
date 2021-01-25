import shutil
import json
import sys
import os
import re

# Set up build folder
shutil.rmtree("build",ignore_errors=True)
os.makedirs("build")
shutil.copyfile("src/jquery-3.5.1.min.js","build/jquery-3.5.1.min.js")
shutil.copyfile("src/about.html","build/about.html")
shutil.copyfile("src/style.css","build/style.css")
shutil.copyfile("src/script.js","build/script.js")
shutil.copytree("res","build/res")

# Functions
def is_filename(name):
    return re.match("^[A-Za-z0-9\/\-_\.]+\.\w+$",name)
def urlize_name(name):
    return re.sub("[^\d\w\s]","",name.lower()).replace(" ","-")
def process_authors(database,names):
    return list(filter(lambda x:x["name"] in names,database))
def author_links(author):
    if "links" in author and len(author["links"]):
        return " | ".join(list(map(lambda x:"<a href=\"%s\">%s</a>"%(x["url"],x["name"]),author["links"])))
    return ""
def get_query(x):
    return ("%s %s %s"%(x["title"],x["desc"]," ".join(x["authors"].split(", ")))).lower()
def get_font(x):
    if "font" in x:
        return " style='font-family:\"%s\"'"%x["font"]
    return ""

# Open template files
file=open("src/video.html","r")
template_video=file.read()
file.close()
file=open("src/essay.html","r")
template_essay=file.read()
file.close()
file=open("src/gallery.html","r")
template_gallery=file.read()
file.close()

# Read Excel sheet
projects=[]
file=open("data.json","r")
data=json.loads(file.read())
file.close()
for post in data["posts"]:
    if not len(post["name"]): continue
    title=post["name"]
    link=urlize_name(title)
    print("Generating %s"%link)
    desc=post["desc"]
    content_type=post["type"]
    if content_type=="video":
        video=post["content"]
        thumbnail=None
        authors=process_authors(data["authors"],post["authors"])
        names=", ".join(post["authors"])
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p>%s</div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],author_links(x),x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_video%(video,title,names,desc,biographies))
        output.close()
    elif content_type=="essay":
        content=[]
        thumbnail=post["thumbnail"]
        for line in post["content"]:
            if is_filename(line): content.append("<img src=\"%s\"/>"%line)
            else: content.append("<p%s>%s</p>"%(get_font(post),line))
        content="".join(content)
        authors=process_authors(data["authors"],post["authors"])
        names=", ".join(post["authors"])
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p>%s</div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],author_links(x),x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_essay%(thumbnail,title,names,desc,content,biographies))
        output.close()
    elif content_type=="gallery":
        content=[]
        thumbnail=post["thumbnail"]
        for line in post["content"]:
            if is_filename(line): content.append("<img src=\"%s\"/>"%line)
            else: content.append("<p%s>%s</p>"%(get_font(post),line))
        content="".join(content)
        authors=process_authors(data["authors"],post["authors"])
        names=", ".join(post["authors"])
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p>%s</div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],author_links(x),x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_gallery%(thumbnail,title,names,desc,content,biographies))
        output.close()
    else:
        print("Invalid content type '%s' provided"%content_type)
        sys.exit(1)
    projects.append({"title":title,"link":link,"authors":names,"desc":desc,"type":content_type,"thumbnail":thumbnail})

# Write index.html
file=open("src/index.html","r")
template=file.read()
file.close()
code="".join(list(map(lambda x:"<div query=\"%s\" thumbnail=\"%s\" class=\"%s\"><a href=\"%s.html\"><h1>%s</h1><h2>%s</h2><p>%s</p></a><hr></div>"%(get_query(x),x["thumbnail"] or "",x["type"],x["link"],x["title"],x["authors"],x["desc"]),projects)))
file=open("build/index.html","w")
file.write(template%code)
file.close()
