from flask import Flask, render_template, request, url_for
import numpy as np
import pickle

app = Flask(__name__)

table = pickle.load(open('table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

@app.route('/')
def recommendUI():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['GET', 'POST'])
def recommend():
    book_name = request.form.get('user_input')
    book_name = book_name.lower()
    index = np.where(table.index==book_name)[0][0]
    items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1], reverse=True)[1:5]
    data = []
    for i in items:
        item = []
        temp_df = books[books['New-Name']==table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)