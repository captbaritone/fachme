from fachme import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy(app)


class Composer(db.Model):
    __tablename__ = 'composers'
    id = db.Column('composer_id', db.Integer, primary_key=True)
    first_name = db.Column('composer_first_name', db.String())
    last_name = db.Column('composer_last_name', db.String())


class Opera(db.Model):
    __tablename__ = 'operas'
    id = db.Column('opera_id', db.Integer, primary_key=True)
    title = db.Column(db.String())
    wikipedia_url = db.Column('opera_wikipedia_url', db.String())
    composer_id = db.Column(db.Integer, db.ForeignKey('composers.composer_id'))
    composer = db.relationship('Composer', primaryjoin="Composer.id == Opera.composer_id")


class Character(db.Model):
    # TODO(captbaritone): Ignore old DB rows with `old_character_id`
    __tablename__ = 'characters'
    id = db.Column('character_id', db.Integer, primary_key=True)
    name = db.Column('character_name', db.String())
    english_name = db.Column('common_english_name', db.String())
    opera_id = db.Column(db.Integer, db.ForeignKey('operas.opera_id'))
    opera = db.relationship('Opera', primaryjoin="Opera.id == Character.opera_id")

    @classmethod
    def matching_string(cls, string, limit=10):
        return cls.query.filter(
            or_(
                cls.name.like('%' + string + '%'),
                cls.english_name.like('%' + string + '%')
            )
        ).limit(limit).all()

    def json(self):
        return {
            'opera': {
                'title': self.opera.title,
                'wikipedia': self.opera.wikipedia_url,
                'composer': {
                    'name': self.opera.composer.last_name
                }
            },
            'id': self.id,
            'name': self.name}
