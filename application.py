from flask import Flask, render_template, request,jsonify
#rom flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
#import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os
import pandas as pd

application = Flask(__name__)
app=application

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:
                    cust_name=[]
                    cust_ratings=[]
                    cust_title=[]
                    cust_comment=[]
                    updated_comments=[]
                    value=[]

                    n=200
                    
                            # fake user agent to avoid getting blocked by Google
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            
                    
                    def get_flipkart_reviews(query, n):
                           base_url = f"https://www.flipkart.com/{query}/product-reviews/itmb1c4c827c8951?pid=MOBFWQ6BHJB7XAFV&lid=LSTMOBFWQ6BHJB7XAFVBSYD9U&marketplace=FLIPKART&page="
    
                           current_page = 1
                           while current_page <= n:
                               url = base_url + str(current_page)
                               response = requests.get(url)
        
        # Check if the response is successful
                               if response.status_code == 200:
                                  soup = BeautifulSoup(response.content, 'html.parser')
            
            
                                  for a in soup.findAll(attrs={'class':'_27M-vq'}):
                 
                                    name=a.find(attrs={'class':'_2sc7ZR _2V5EHH'})
                                    ratings=soup.find('div',attrs={'class':'_3LWZlK _1BLPMq'}) 
                                    value=ratings.text.strip()     
                                    title=a.find(attrs={'class':'_2-N8zT'})
                                    comments=a.find('div',attrs={'class':'t-ZTKy'})
                
                                    cust_name.append(name.text)
                                    cust_ratings.append(value)
                                    cust_title.append(title.text)
                                    cust_comment.append(comments.text)
 
                                    
                                  
                                  current_page +=1
                               else:
                                    print(f"Error fetching page {current_page}. Status code: {response.status_code}")
                                    break

# Example usage: Get reviews until page n for the product "iphone"
                    get_flipkart_reviews("apple-iphone-se-black-256-gb", n)
                    #client = pymongo.MongoClient("mongodb+srv://pratheek_bheemaiah:<password>@pratheek.rjobxyx.mongodb.net/?retryWrites=true&w=majority")
                    #db = client['image_scrap']
                    #review_col = db['image_scrap_data']
                    #review_col.insert_many(img_data) 
                    # 
                    # 
                    updated_comments = [item.replace("READ MORE"," ") for item in cust_comment]
                    Data=([cust_name,  cust_ratings,  cust_title,  updated_comments]) 



# Transpose the data to display it in rows
                    transposed_data = list(map(list, zip(*Data)))


                    df = pd.DataFrame(transposed_data, columns=["customer name",'customer Ratings','customer title','customer comment'])

                    print(df)
                    df.to_csv(r'C:\Users\Pavan\Desktop\flipdata5.csv')

         

                    return "file saved in csv formate"
                except Exception as e:
                    logging.info(e)
                    return 'something is wrong'
                #return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)