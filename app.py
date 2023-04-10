
from flask import Flask,render_template,request
import pickle
import numpy as np

Top_movies = pickle.load(open('Top_movies.pkl','rb'))
indices = pickle.load(open('indices.pkl','rb'))
metadata = pickle.load(open('metadata.pkl','rb'))
cosine_sim = pickle.load(open('cosine_sim.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           movie_name = list(Top_movies['title'].values),
                           votes=list(Top_movies['vote_count'].values),
                           rating=list(Top_movies['vote_average'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies',methods=['post'])

def recommend():
    title = request.form.get('user_input')

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    data=metadata['title'].iloc[movie_indices]
    print( data)
    data = []
    for i in movie_indices:
        item = []
        temp_df = metadata[metadata['title'] == indices.index[i]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        
        data.append(item)
        # return data
    return render_template('recommend.html',data=data)
    # return data

if __name__ == '__main__':
    app.run(debug=True)