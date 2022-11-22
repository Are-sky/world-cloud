'''
@author:昼阳Helios
@Date: 2022-11-22 13:37
'''
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba
from fastapi import FastAPI
from pydantic import BaseModel
from MyResult import MyResult
import json
import uvicorn

app = FastAPI();
myResult = MyResult();
File_Prefix = "./";

# 3.png 的生成方法就是 请求 127.0.0.1:8000/creatCy/3 这个路径生成的
# 同理 你需要将你需要生成的词云原文本（.txt格式） UID 就是 xxx.txt 里的xxx
# mask_file_name 是你自定义词云轮廓图片 黑白轮廓图 这里我提供了中国地图的轮廓
@app.get("/creatCy/{UID}")
def creatCy(UID:str,mask_file_name:str=None):
    stopwords = open( File_Prefix + "stopwords.txt",encoding='utf-8');
    if mask_file_name is None:
        wcd=WordCloud(background_color='white',max_words=500,height=480,width=854,
             max_font_size=200,font_path="fonts/msyh.ttc",colormap="Reds",
             mode="RGBA",stopwords=stopwords,repeat=True,);
    else:
        mask=np.array(Image.open(File_Prefix + mask_file_name));
        wcd=WordCloud(background_color='white',max_words=500,height=480,width=854,
             max_font_size=200,font_path="fonts/msyh.ttc",colormap="Reds",mask=mask,
             mode="RGBA",stopwords=stopwords,repeat=True,);
    try:
        text_file=open(File_Prefix + UID + ".txt",encoding='utf-8');
        all_text = text_file.read();
    except IOError:
        return json.dumps(myResult.ERROR("读取文件出错").__dict__, ensure_ascii = False);
    finally:
        text_file.close();
    ss=" ".join(jieba.lcut(str(all_text.split("\n"))));
    wcd.generate(ss);
    wcd.to_file(File_Prefix + UID + ".png");
    return json.dumps(myResult.OK(File_Prefix+ UID + ".png").__dict__, ensure_ascii = False);


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True);