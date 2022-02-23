########CODIGO DE EJECUCION########
#uvicorn main:app --reload
###################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import pickle
from pydantic import BaseModel

import pandas as pd 
import json

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_absolute_error

class Rating(BaseModel):
    votes : float
    duration : float
    budget_code : float
    rating : float

class Recomendation(BaseModel):
    title : str

app = FastAPI(title='Movie Predictions Server', version="1.0")

origins = [ 
 "*",  
] 

app.add_middleware( 
 CORSMiddleware, 
 allow_origins=origins, 
 allow_credentials=True, 
 allow_methods=["*"], 
 allow_headers=["*"], 
) 

@app.on_event("startup")
def load_model():
    global model_p
    model_p = pickle.load(open('ml_model_prediction.pkl', 'rb'))
    global model_r
    model_r = pickle.load(open('ml_model_recomendation.pkl', 'rb'))
    global list_d
    list_d =  pd.read_csv("dataset_numbers.csv")
    global list_r
    list_r =  pd.read_csv("dataset_letters.csv")
    global features
    global cos_sim
    
@app.get("/")
def authors():
    data = [{
            "author": "Josue Andres Macas Caraguay",
            "email": "josue.macas@unl.edu.ec",
            "org": "CIS-UNL",
            },
            {
            "author": "Jorge Gustavo Tandazo Cueva",
            "email": "jorge.tandazo@unl.edu.ec",
            "org": "CIS-UNL",
            }]
    return data
   
@app.get("/list_movies/")
async  def list_movies(): 
    list_d.rename(columns={'IMDb Rating':'IMDb_Rating'})
    listJSON = list_d.head(100).to_json(orient = 'table')
    return  json.loads(listJSON)

@app.post("/predict/")
async  def rating_IMDb(rating: Rating):

    data = [[float(rating.votes),float(rating.duration),float(rating.budget_code)]]
    result = model_p.predict(data).tolist()[0]
    rf_acc = mean_absolute_error([rating.rating], [result])

    return {"data":rating,"rating_IMDb": result, "absolute_mean_error" : float(str(rf_acc)),}

@app.post("/recomendation/")
async  def recomendation_movie(r: Recomendation):
    
    # data = [[float(rating.votes),float(rating.duration)]]
    # result = model_r.fit_predict(data)
    print(r.title)
    

    def combine_columncontent(row):
        return row['Duration'] +  " " + row['Country'] + " " + row['Language'] + " " + row['Director'] + " " +row['Description']+ " " +row['IMDb Rating']+ " " +row['Cast']+ " " +row['Year']+ " " +row['Rating']+ " " +row['Genre']       
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(list_r['All Columns'])

    cos_sim = cosine_similarity(count_matrix)
    features = list_r[['Title']].reset_index()
    def recommend(movie): 
        
        content_title = features[features['Title'] == movie].index[0] 
        features.sort_index(inplace=True)
        
        sim_scores = pd.Series(cos_sim[content_title]).sort_values(ascending=False) 
    
        simbtw_content = pd.DataFrame({ 'Score' : sim_scores[1:100]}).reset_index() 
        simbtw_content = simbtw_content.merge(features) 
        simbtw_content = simbtw_content[['Title','Score']] 
        
        return simbtw_content

    result = recommend(r.title)
    print(result.head())
    
    
    resultJSON = result.head().to_json(orient = 'table')
    return  json.loads(resultJSON)


