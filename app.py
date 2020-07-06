from flask import Flask,render_template,request
import sqlite3 as sql
from urllib.request import urlopen
from bs4 import BeautifulSoup

app=Flask(__name__)

def connect(dbname):
    try:
        db=sql.connect(f"{dbname}.db")
        cur=db.cursor()
        return db,cur
    except Exception as e:
        print("Error" ,e)
        exit(2)

# def fetchnews(dbname):
# db,cur=connect(dbname)
#     cur.execute('SELECT * FROM News ORDER BY id DESC LIMIT 1')
#     lastrec=cur.fetchone()
#     newslist=[]
#     for var in range(1,3):
#         url='https://www.moneycontrol.com/news/business/stocks/page-{0}'.format(var)
#         data=urlopen(url)
#         soup=BeautifulSoup(data,'lxml')
#         li=soup.find_all('li',{'class':'clearfix'})
#         li=li[::-1]
#         for div in li:
#             try:
#                 link=div.find('a')['href']
#                 title=div.find('a')['title']
#                 desc=div.find('p').text
#                 if link==lastrec[4]:
#                     break
#                 newslist.append([link,text])
#             except:
#                 pass
#         if link==lastrec[3]:
#             break
            
#     if len(newslist)!=0:        
#             newslist=newslist[::-1]
#             for val in newslist:
#                 cur.execute("""INSERT INTO News(title,description,sentiment,link)
#                     VALUES(?,?,?,?)""",(title.strip(),desc.strip(),0,link))
#                 db.commit()
#     db.close()
#     return None




@app.route('/')
def index():
#     for name in ['indiainfoline','cnbctv18']:
#         fetchnews(name)
#     db,cur=connect('indiainfoline')
#     cur.execute("""SELECT * FROM (
#    SELECT * FROM News ORDER BY id DESC LIMIT 5
#     )Var1
#    ORDER BY id ASC;""")
#     news1=cur.fetchall()
#     news1=news1[::-1]
#     db.close()

    db,cur=connect('moneycontrol')
    cur.execute("""SELECT * FROM (
   SELECT * FROM News ORDER BY id DESC LIMIT 8
    )Var1
   ORDER BY id ASC;""")
    news=cur.fetchall()
    news=news[::-1]
    db.close()
    return render_template('index.html',data1=enumerate(news,start=1))


@app.route('/moneycontrol/')
def mnycntrl():
    db,cur=connect('moneycontrol')
    cur.execute("SELECT * FROM News")
    news=cur.fetchall()
    news=news[::-1]
    db.close()
    return render_template('money_control.html',data1=enumerate(news,start=1))


@app.route('/part_mncntrl_news/', methods=['POST'])
def part_mnctrl_news():
    if request.method == 'POST':
        word=request.form['search']
        db,cur=connect('moneycontrol')
        cur.execute('Select * from News')
        news_list=cur.fetchall()
        word=word.lower()
        data=[]
        for news in news_list:
            if word in news[1].lower():
                data.append(news)
    db.close()
    return render_template("mnctrl_newser.html",data=enumerate(data,start=1))


if __name__ == "__main__":  
    app.run(debug = True) 
