# -*- coding: utf-8 -*-
#Para ejecutar:
#1. Ir a la carpeta backend
#2. SET FLASK_APP=server
#3. SET FLASK_ENV=development
#4. flask run
import backend
from unicodedata import name
from flask import(
    Flask,
    abort,
    jsonify,
    request
)
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from models import setup_db, Post, Query
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#Paginación
db = SQLAlchemy()
TODOS_PER_PAGE=1000000

def paginate(request,selection,isDescendent):
    if isDescendent:                #Cuando se crea con CURL, muestra solo los últimos recursos creados
        start = len(selection)-TODOS_PER_PAGE
        end = len(selection)
    
    else:
        page=request.args.get('page',1,type=int)  #request.args.get trae los recursos especificados por el usuario por query parameters (luego del '?' en el url viene los query parameters)
        start = (page-1)*TODOS_PER_PAGE
        end = start+TODOS_PER_PAGE
    
    resources = [resource.format() for resource in selection]
    current_resources= resources[start:end]
    return current_resources

#API

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins="*", max_age=10)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/posts', methods=['GET'])      
    def get_posts():
        selection=Post.query.order_by('id').all()
        posts=paginate(request,selection,False)
      
        if (len(posts))==0:
            abort(404) 

        return jsonify({    #Las claves estarán ordenadas en orden alfabético
            'success': True,
            'posts': posts,
            'total_posts': len(selection)
        })

    @app.route('/posts', methods=['POST'])
    def create_post():
        body=request.get_json()
        title = body.get('title',None)
        publication = body.get('publication', None)
        author = body.get('author',None)
        date = body.get('date', None)
        year = body.get('year', None)
        month = body.get('month', None)
        content = body.get('content', None)

        if author is None or title is None or publication is None or content is None:
            abort(422)
        
        #AGREGAR LA FUNCION DE TOKENIZADOR
        post = Post(title=title,publication=publication,author=author,date=date, year=year, month=month, content=content)
        post.insert()
        new_post_id=post.id
        new_post_title=post.title
        
        selection = Post.query.order_by('id').all()
        current_posts=paginate(request,selection,True)

        
        return jsonify({
            'success': True,
            'created': new_post_id,
            'title': new_post_title,
            'posts': current_posts,
            'total_posts': len(selection)
        })

    @app.route('/parser', methods=['POST'])      
    def parser():
        Query.query.delete()
        db.session.commit()
        body = request.get_json()
        busqueda_input = body.get('busqueda_input')
        top_k = body.get('top_k')

        if busqueda_input is None or top_k is None:
            abort(422)

        stemmer = SnowballStemmer("english")
        stop_words = stopwords.words('english')
        archivo = open("./stopwords.txt", "r", encoding="utf-8")
        contenido = archivo.read()
        stoplist = contenido.split()
        filtro = []
        for x in range(97, 123):
            filtro.append(chr(x))
        tokens = []
        tokens_prepro = word_tokenize(busqueda_input)
        print(tokens_prepro)
        # for token in tokens_prepro:
        #     token_lower = token.lower()
        #     if token_lower not in stop_words and len(token_lower) >= 3:
        #         token_res = stemmer.stem(token_lower)
        #         tokens.append(token_res)

        for token in tokens_prepro:
            token_min = token.lower()
            if len(token_min) >= 3 and token_min not in stoplist and token_min != "" and token not in stop_words:
                token_res = stemmer.stem(token_min)
                tokens.append(token_res)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(tokens)
        print("Entrando a resultados")
        tokenizado = backend.tokenizar(tokens)
        print(tokenizado)
        resultados = backend.matrizk(tokenizado,top_k)
        # for res in tokens:
        #     query = Query()
        print("Procesado")
        print(resultados)
        return jsonify({
            'success': True,
            'query': tokens,
        })
    
    @app.route('/parser', methods=['GET'])
    def get_parser():
        selection=Query.query.order_by('id').all()
        query=paginate(request,selection,False)
      
        if (len(query))==0:
            abort(404) 

        return jsonify({    #Las claves estarán ordenadas en orden alfabético
            'success': True,
            'query': query,
            'total_query': len(selection)
        })
    # @app.route('/parser_enviar', methods=['GET'])  
    # def comparar(lista_tuplas, texto, n):
    # # Tokenización del texto de entrada
    #     tokens = word_tokenize(texto)

    #     # Filtrar las tuplas que contienen tokens en el texto de entrada
    #     tuplas_coincidentes = []
    #     for tupla in lista_tuplas:
    #         if any(token in tupla[0] for token in tokens):
    #             tuplas_coincidentes.append(tupla)

    #     # Ordenar las tuplas por valor numérico de forma descendente
    #     tuplas_ordenadas = sorted(tuplas_coincidentes, key=lambda x: x[1], reverse=True)

    #     # Obtener las primeras "n" tuplas con los valores más altos
    #     tuplas_resultantes = tuplas_ordenadas[:n]

    #     return tuplas_resultantes
    
    @app.route('/posts/<post_id>',methods=['DELETE'])  
    def delete_post(post_id):
        error_404=False
        try:
            post = Post.query.filter(Post.id==post_id).one_or_none()
            if post is None:
                error_404=True
                abort(404)
            
            post.delete()

            selection = Post.query.order_by('id').all()
            posts = paginate(request,selection,True)

            return jsonify({
                'success': True,
                'deleted': post_id,
                'posts': posts,
                'total_posts': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)  
            else:
                abort(500)
    #Manejo de errores

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }),404

    @app.errorhandler(422)
    def unprocessable (error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'internal server error'
        }),500

    @app.errorhandler(403)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 403,
            'message': 'forbidden'
        }),403
    

    return app