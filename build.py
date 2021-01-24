import openpyxl
import shutil
import sys
import os
import re

# Input validation
if len(sys.argv)<2:
    print("Usage: python build.py <excel file>")
    exit(1)

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
def process_authors(data,i):
    authors=[]
    num=data[i]
    start=i+1
    for _ in range(num):
        author={
            "name":data[start],
            "desc":data[start+1],
            "img":data[start+2],
            "links":[]
        }
        num1=data[start+3]
        for a in range(num1):
            b=start+(a*2)+4
            author["links"].append({"name":data[b],"url":data[b+1]})
        authors.append(author)
        start+=(num1*2)+4
    return authors
def author_links(author):
    if len(author["links"]):
        return " | ".join(list(map(lambda x:"<a href=\"%s\">%s</a>"%(x["url"],x["name"]),author["links"])))
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
wb=openpyxl.load_workbook(sys.argv[1])
for row in wb.active.values:
    title=row[0]
    link=urlize_name(title)
    print("Generating %s"%link)
    desc=row[1]
    content_type=row[2]
    if content_type=="video":
        video=row[3]
        thumbnail=None
        authors=process_authors(row,4)
        names=", ".join(list(map(lambda x:x["name"],authors)))
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p></div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_video%(video,title,names,desc,biographies))
        output.close()
    elif content_type=="essay":
        a=4
        data=[]
        thumbnail=row[3]
        while type(row[a])!=int:
            if is_filename(row[a]): data.append("<img src=\"%s\"/>"%row[a])
            else: data.append("<p>%s</p>"%row[a])
            a+=1
        data="".join(data)
        authors=process_authors(row,a)
        names=", ".join(list(map(lambda x:x["name"],authors)))
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p></div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_essay%(thumbnail,title,names,desc,data,biographies))
        output.close()
    elif content_type=="gallery":
        a=4
        data=[]
        thumbnail=row[3]
        while type(row[a])!=int:
            if is_filename(row[a]): data.append("<img src=\"%s\"/>"%row[a])
            else: data.append("<p>%s</p>"%row[a])
            a+=1
        data="".join(data)
        authors=process_authors(row,a)
        names=", ".join(list(map(lambda x:x["name"],authors)))
        biographies="".join(list(map(lambda x:"<div class=\"author\"><div><h1>%s</h1><p>%s</p>%s</div><div><img src=\"%s\"></div></div>"%(x["name"],x["desc"],author_links(x),x["img"]),authors)))
        output=open("build/%s.html"%link,"w")
        output.write(template_gallery%(thumbnail,title,names,desc,data,biographies))
        output.close()
    else:
        print("Invalid content type '%s' provided"%content_type)
        sys.exit(1)
    projects.append({"title":title,"link":link,"authors":names,"desc":desc,"type":content_type,"thumbnail":thumbnail})

# Write index.html
file=open("src/index.html","r")
template=file.read()
file.close()
code="<hr>".join(list(map(lambda x:"<div thumbnail=\"%s\" class=\"%s\"><a href=\"%s.html\"><h1>%s</h1><h2>%s</h2><p>%s</p></a></div>"%(x["thumbnail"] or "",x["type"],x["link"],x["title"],x["authors"],x["desc"]),projects)))
file=open("build/index.html","w")
file.write(template%code)
file.close()
