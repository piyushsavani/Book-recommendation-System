from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
df_all_book_name = pickle.load(open('df_all_book_name.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():       
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].values.tolist(),
                           author=popular_df['Book-Author'].values.tolist(),
                           Image=popular_df['Image-URL-M'].values.tolist(),
                           votes=popular_df['num_ratings'].values.tolist(),
                           rating=np.round(popular_df['avg_ratings'].values.tolist(),2)
                           )
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback', methods=["POST"] )
def feedback():
    return render_template('feedback.html')    

@app.route('/contact')
def contact():
    return render_template('contact.html')    

@app.route('/recommend_books',methods=["POST"])
def recommend_books(): 
    user_input = request.form.get('user_input')
    if user_input not in df_all_book_name:
        return render_template('select.html')   
    else:    
        index = np.where(pt.index==user_input)[0][0]    
        similar_items = sorted(list(enumerate(similarity_score[index])), key = lambda x : x[1], reverse = True)[1:5] 

        data=[] 
        for i in similar_items:
            item=[]
            temp_df=books[books['Book-Title']==pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)     
    
    return render_template('recommend_books.html', data=data)



if __name__ == '__main__':
  app.run(debug=False)