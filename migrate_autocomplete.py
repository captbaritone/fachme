from fachme import app

from flask_sqlalchemy import SQLAlchemy
from fachme.learning_autocomplete_suggestions import LearningAutocompleteSuggestions

db = SQLAlchemy(app)
suggestor = LearningAutocompleteSuggestions(
        namespace=app.config.get('AUTOCOMPLETE_NAMESPACE'),
        port=app.config.get('REDIS_PORT'),
        db=app.config.get('REDIS_DB'),
        host=app.config.get('REDIS_HOST'))


class Autocomplete(db.Model):
    __tablename__ = 'autocomplete_log'
    id = db.Column('autocomplete_log_id', db.Integer, primary_key=True)
    data_type = db.Column('type', db.String())
    canonical_id = db.Column(db.String())
    ip = db.Column(db.String())
    search = db.Column('string', db.String())


user_previous_canonical = {}
for log in Autocomplete.query.filter_by(data_type='character').order_by(Autocomplete.id):
    previous = user_previous_canonical.get(log.ip)
    if previous and previous != log.canonical_id:
        suggestor.associate_canonical(previous, log.ip)
    suggestor.register_search(log.search, log.ip)
    user_previous_canonical[log.ip] = log.canonical_id
