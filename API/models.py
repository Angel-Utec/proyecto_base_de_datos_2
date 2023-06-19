# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 


database_path='postgresql://postgres:1@localhost:5432/BD2'

#Configuracion
db=SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    with app.app_context():
        db.create_all()

#Modelos
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text,nullable = False)
    publication = db.Column(db.Text,nullable = False)
    author = db.Column(db.Text, nullable = False)
    date = db.Column(db.Text,nullable = False)
    year = db.Column(db.Float,nullable = False)
    month = db.Column(db.Float,nullable = False)
    content = db.Column(db.Text,nullable = False)

    #Metodo que formatee el objeto a json para devolverlo a mi API y que no de errores
    def format(self):
        return {
            'id':self.id,
            'title':self.title,
            'publication':self.publication,
            'author':self.author,
            'date':self.date,
            'year':self.year,
            'month':self.month,
            'content':self.content
        }

    #Metodo que permite la inserción de un post a través de nuestra API
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()