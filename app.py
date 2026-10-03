import json
from flask import Flask, render_template, request, jsonify
from models import init_db, SessionLocal, Grammar, record_attempt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grammar.db'

init_db(app)


@app.route('/')
def dashboard():
    db = SessionLocal()
    # allow filtering by level via ?level=A2
    level = request.args.get('level')
    if level:
        grammars = db.query(Grammar).filter(Grammar.notation == level).all()
    else:
        grammars = db.query(Grammar).all()
    # collect available levels for the filter
    levels = [r[0] for r in db.query(Grammar.notation).distinct().all()]
    # attach progress
    from models import get_progress_for
    progress = {}
    for g in grammars:
        progress[g.id] = get_progress_for(db, g.id)
    db.close()
    return render_template('dashboard.html', grammars=grammars, progress=progress, levels=levels, selected_level=level)


@app.route('/grammar/<int:gid>')
def grammar_page(gid):
    db = SessionLocal()
    g = db.query(Grammar).get(gid)
    from models import get_progress_for
    prog = get_progress_for(db, gid)
    db.close()
    if not g:
        return "Not found", 404
    data = json.loads(g.data)
    return render_template('grammar.html', grammar=g, data=data, progress=prog)


@app.route('/practice/<int:gid>')
def practice(gid):
    db = SessionLocal()
    g = db.query(Grammar).get(gid)
    db.close()
    if not g:
        return "Not found", 404
    data = json.loads(g.data)
    exercises = data.get('exercises', [])
    return render_template('practice.html', grammar=g, exercises=exercises)


@app.route('/api/check', methods=['POST'])
def api_check():
    payload = request.json or {}
    gid = payload.get('gid')
    qindex = int(payload.get('qindex', 0))
    answer = payload.get('answer', '')
    db = SessionLocal()
    g = db.query(Grammar).get(gid)
    if not g:
        db.close()
        return jsonify({'ok': False, 'error': 'grammar not found'})
    data = json.loads(g.data)
    exercises = data.get('exercises', [])
    if qindex >= len(exercises):
        db.close()
        return jsonify({'ok': False, 'error': 'exercise not found'})
    ex = exercises[qindex]
    correct = ex.get('a', '')
    ex_type = ex.get('type', 'short')
    correct_flag = answer.strip().lower() == correct.strip().lower()
    feedback = 'Seleccionaste: ' + answer if ex_type == 'mcq' else 'Respuesta verificada localmente.'

    record_attempt(db, g.id, correct_flag)
    db.close()
    return jsonify({'ok': True, 'correct': correct_flag, 'feedback': feedback})


@app.route('/api/progress/<int:gid>')
def api_progress(gid):
    db = SessionLocal()
    from models import get_progress_for
    prog = get_progress_for(db, gid)
    db.close()
    return jsonify({'ok': True, 'progress': prog})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
