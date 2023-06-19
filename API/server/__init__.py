# -*- coding: utf-8 -*-
#Para ejecutar:
#1. Ir a la carpeta backend
#2. SET FLASK_APP=server
#3. SET FLASK_ENV=development
#4. flask run

from unicodedata import name
from flask import(
    Flask,
    abort,
    jsonify,
    request
)

from flask_cors import CORS

from models import setup_db, Post

#Paginación

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