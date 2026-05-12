from pathlib import Path


MODELO_PATH = Path(__file__).resolve().parent.parent / "modelo_ia.pkl"

CATEGORIAS_CLAVE = {
    "Infraestructura": [
        "hueco",
        "via",
        "calle",
        "anden",
        "puente",
        "alcantarilla",
        "semaforo",
        "poste",
        "parque",
    ],
    "Servicios Publicos": [
        "agua",
        "energia",
        "luz",
        "alumbrado",
        "basura",
        "recoleccion",
        "acueducto",
        "alcantarillado",
    ],
    "Seguridad": [
        "robo",
        "hurto",
        "atraco",
        "violencia",
        "inseguridad",
        "vandalismo",
        "riña",
        "amenaza",
    ],
    "Medio Ambiente": [
        "contaminacion",
        "ruido",
        "arbol",
        "quema",
        "escombros",
        "rio",
        "basura",
        "ambiental",
    ],
    "Transporte": [
        "bus",
        "transporte",
        "trafico",
        "trancon",
        "ruta",
        "taxi",
        "paradero",
        "movilidad",
    ],
    "Salud": [
        "salud",
        "hospital",
        "clinica",
        "ambulancia",
        "plaga",
        "mosquitos",
        "enfermedad",
        "sanitario",
    ],
}

PALABRAS_INVALIDAS = [
    "prueba",
    "asdf",
    "qwerty",
    "jajaj",
    "spam",
    "test",
]


def entrenar_modelo(textos, etiquetas):
    try:
        import joblib
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
    except ImportError as exc:
        raise RuntimeError("Instala scikit-learn y joblib para entrenar el modelo.") from exc

    vectorizador = TfidfVectorizer()
    x = vectorizador.fit_transform(textos)
    modelo = MultinomialNB()
    modelo.fit(x, etiquetas)
    joblib.dump((vectorizador, modelo), MODELO_PATH)


def predecir_categoria(texto):
    if MODELO_PATH.exists():
        try:
            import joblib

            vectorizador, modelo = joblib.load(MODELO_PATH)
            x = vectorizador.transform([texto])
            prediccion = modelo.predict(x)[0]
            confianza = max(modelo.predict_proba(x)[0])
            return prediccion, round(float(confianza), 2)
        except Exception:
            pass

    return predecir_categoria_por_reglas(texto)


def predecir_categoria_por_reglas(texto):
    texto_normalizado = texto.lower()
    puntajes = {
        categoria: sum(1 for palabra in palabras if palabra in texto_normalizado)
        for categoria, palabras in CATEGORIAS_CLAVE.items()
    }
    categoria, puntaje = max(puntajes.items(), key=lambda item: item[1])

    if puntaje == 0:
        return "Requiere revision", 0.25

    confianza = min(0.95, 0.45 + (puntaje * 0.15))
    return categoria, round(confianza, 2)


def evaluar_validez(texto, confianza):
    texto_limpio = " ".join(texto.lower().split())

    if len(texto_limpio) < 30:
        return "Posiblemente invalida", "El reporte tiene muy poca informacion."

    if any(palabra in texto_limpio for palabra in PALABRAS_INVALIDAS):
        return "Posiblemente invalida", "El texto parece una prueba o contenido no relacionado."

    if confianza < 0.45:
        return "Requiere revision", "La IA no encontro suficientes señales para clasificar con seguridad."

    return "Valida", "El reporte contiene informacion suficiente para iniciar revision."


def analizar_denuncia(titulo, descripcion):
    texto = f"{titulo} {descripcion}".strip()
    categoria, confianza = predecir_categoria(texto)
    validez, motivo = evaluar_validez(texto, confianza)

    return {
        "categoria_predicha": categoria,
        "confianza": confianza,
        "validez": validez,
        "motivo": motivo,
    }
