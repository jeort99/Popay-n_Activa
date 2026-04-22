from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def entrenar_modelo(textos, etiquetas):
    vectorizador = TfidfVectorizer()
    X = vectorizador.fit_transform(textos)
    modelo = MultinomialNB()
    modelo.fit(X, etiquetas)
    joblib.dump((vectorizador, modelo), 'modelo_ia.pkl')

def predecir_categoria(texto):
    vectorizador, modelo = joblib.load('modelo_ia.pkl')
    X = vectorizador.transform([texto])
    prediccion = modelo.predict(X)[0]
    confianza = max(modelo.predict_proba(X)[0])
    return prediccion, confianza
