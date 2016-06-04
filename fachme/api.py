from collections import defaultdict

from flask import jsonify
from flask import session
from flask import request
from learning_autocomplete_suggestions import LearningAutocompleteSuggestions

from fachme import app
from fachme.models import Character

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy(app)
suggestor = LearningAutocompleteSuggestions(
        namespace=app.config.get('AUTOCOMPLETE_NAMESPACE'),
        port=app.config.get('REDIS_PORT'),
        db=app.config.get('REDIS_DB'),
        host=app.config.get('REDIS_HOST'))


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get('q', '')
    suggestor.register_search(query, session.sid)

    characters = Character.matching_string(query, limit=10)

    matching_ids = [c.id for c in characters]

    results = [c.json() for c in characters]
    for character in results:
        character['first_guess'] = 0

    suggested_ids = suggestor.suggestion_generator(query, ignore_values=matching_ids)

    first_guess = True
    for id in suggested_ids:
        if len(results) >= 10:
            break

        character = Character.query.get(id)

        if not character:
            continue

        character_json = character.json()
        # The frontend code is a bit odd, and needs us to mark the first item
        # that is a suggestion or "guess"
        character_json['first_guess'] = 1 if first_guess else 0
        if first_guess:
            first_guess = False

        results.append(character_json)

    return jsonify(results)


@app.route("/selected/<canonical>")
def selected(canonical):
    """
    Tell the server that you have made a selection from the autocomplete menu
    """
    suggestor.associate_canonical(canonical, session.sid)
    return jsonify({'status': 'SUCCESS'})


@app.route("/fachme")
def fachme():
    resume = request.args.get('resume', '').split(',')

    # Unused
    request.args.get('offset', 0)

    # Oh God this is not efficient, but it's all going away soon, so I won't
    # bother to figure out the right way. It works!
    fach = [Character.query.get(id).json() for id in _fachme(resume)]

    return jsonify(fach)


def _fachme(resume):
    """
    Terrible implementation ported grossly from PHP. Please don't look at this :(
    """

    # Sanatize input
    resume = [str(int(id)) for id in resume]

    context = {
        "avg_recordings_per_singer": 3.874,
        "avg_recordings_per_character": 4.537,
        "min_recordings": 10,
        "year_window": 3,
        "character_a_ids": ', '.join(resume)}

    query = """
    SELECT
        C_A.character_id AS character_a,
        s_p_a.recording_id AS recording_a,
# weight singers based on the number of recordings for the average singer
        1 / (SELECT COUNT(*) FROM singer_pairs WHERE singer_id = S_A.singer_id) / {avg_recordings_per_singer} AS singer_a_pop,
        s_p_b.recording_id AS recording_b,
        C_B.character_id AS character_b,
        C_B.character_name AS character_b_name,
# weight characters based on the number of recordings for the average character
        1 / (SELECT COUNT(*) FROM singer_pairs WHERE character_id = C_B.character_id) / {avg_recordings_per_character} AS character_b_pop,

# Informational
        C_B.character_name AS character_name,
        C_B.character_id AS character_id,
        C_B.common_english_name,
        operas.opera_wikipedia_url,
        operas.opera_id AS opera_id,
        operas.title AS title,
        composers.composer_last_name AS composer_last_name
    FROM
        characters AS C_A
    LEFT JOIN
        singer_pairs AS s_p_a ON C_A.character_id = s_p_a.character_id
    LEFT JOIN
        recordings AS R_A ON s_p_a.recording_id = R_A.recording_id
    LEFT JOIN
        singers AS S_A ON s_p_a.singer_id = S_A.singer_id
    LEFT JOIN
        singer_pairs AS s_p_b ON S_A.singer_id = s_p_b.singer_id
    LEFT JOIN
        recordings AS R_B ON s_p_b.recording_id = R_B.recording_id
    LEFT JOIN
        characters AS C_B ON s_p_b.character_id = C_B.character_id

# Informational
    LEFT JOIN
        operas ON C_B.opera_id = operas.opera_id
    LEFT JOIN
        composers ON operas.composer_id = composers.composer_id
    WHERE
        C_A.character_id IN ({character_a_ids})
        AND
        C_B.character_id NOT IN ({character_a_ids})
        AND
# Require minu
        (SELECT COUNT(*) FROM singer_pairs WHERE singer_id = S_A.singer_id) > {min_recordings}
        AND
        (SELECT COUNT(*) FROM singer_pairs WHERE character_id = C_B.character_id) > {min_recordings}
        AND
        (R_A.year >= R_B.year - {year_window} AND R_A.year <= R_B.year + {year_window})
# Ignore old versions of table rows
        AND C_A.old_character_id = 0
        AND C_B.old_character_id = 0
        AND R_A.old_recording_id = 0
        AND R_B.old_recording_id = 0
        AND S_A.old_singer_id = 0
    """.format(**context)

    result = db.engine.execute(text(query).execution_options(autocommit=True))
    objs = []
    related = defaultdict(lambda: dict(weight=0))

    character_a_pops = {}
    singer_a_pops = defaultdict(dict)
    character_b_pops = defaultdict(lambda: defaultdict(dict))

    # Calculate the totals for the singers and the characters
    for obj in result:
        character_a_pops[obj.character_a] = 1
        singer_a_pops[obj.character_a][obj.recording_a] = obj.singer_a_pop

        character_b_pops[obj.character_a][obj.recording_a][obj.recording_b] = obj.character_b_pop
        # Store in memory for the second iteration
        objs.append(obj)

    for obj in objs:
        related[obj.character_b]['weight'] += (
            (1 / sum(character_a_pops.values())) *
            (obj.singer_a_pop / sum(singer_a_pops[obj.character_a].values())) *
            (obj.character_b_pop / sum(character_b_pops[obj.character_a][obj.recording_a].values()))
        )

    related = sorted(related.iteritems(), key=lambda (k, v): v['weight'], reverse=True)

    ids = [r[0] for r in related]

    return ids
