from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)


def calculate_similarity(text1, text2):
    inputs = tokenizer(text1, text2, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    similarity_score = torch.softmax(logits, dim=1)[0][0].item()  # Вероятность того, что тексты последовательны
    return similarity_score



@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        user_description = request.form['description']
        df['similarity'] = df['overview'].apply(lambda x: calculate_similarity(user_description, x))
        similar_movies = df.sort_values(by='similarity', ascending=False).head(5)
        movies = similar_movies[['title', 'similarity']].to_dict(orient='records')
        return jsonify({'movies': movies})
    return render_template('find.html')
