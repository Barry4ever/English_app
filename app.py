import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import init_db, SessionLocal, Grammar, record_attempt

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    openai = None
    OPENAI_AVAILABLE = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grammar.db'

init_db(app)


def ai_generate(heading: str):
    """Generate rich grammar content using OpenAI if available, else return detailed placeholders.

    Request a JSON object with keys:
      - explanation: detailed explanation
      - structure: structure summary
      - examples: list of {sentence, notes}
      - common_errors: list
      - exercises: list of exercises with fields: type (short/mcq/fill), q, a, options (for mcq), difficulty
    """
    if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
        # Use the new OpenAI Python client interface if available
        try:
            client = openai.OpenAI()
        except Exception:
            client = openai
        system = (
            "Eres un asistente que responde SOLO JSON válido.\n"
            "Devuelve un objeto JSON con: explanation (texto largo), structure (texto), examples (lista de objetos {sentence, notes}), "
            "common_errors (lista de strings), exercises (lista). Cada ejercicio: {type, q, a, difficulty, options?}. "
            "Genera al menos 6 ejercicios de distintas dificultades y tipos."
        )
        user = f"Genera una explicación extensa, ejemplos anotados y ejercicios variados para: {heading}"
        resp = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=1500,
        )
        # robustly extract the assistant text
        try:
            text = resp.choices[0].message.content
        except Exception:
            try:
                text = resp.choices[0].message['content']
            except Exception:
                try:
                    text = resp['choices'][0]['message']['content']
                except Exception:
                    text = str(resp)
        # Try to extract JSON from the response
        try:
            data = json.loads(text)
        except Exception:
            import re
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                try:
                    data = json.loads(m.group(0))
                except Exception:
                    data = {"generated": text}
            else:
                data = {"generated": text}
        return data

    # Detailed fallback content when no OpenAI key is present
    examples = [
        {"sentence": "I love coffee — so do I.", "notes": "'so' + subject + auxiliary (do) used to agree with a positive statement."},
        {"sentence": "She doesn't like tea, and neither do I.", "notes": "'neither' + auxiliary (do) + subject used to agree with a negative statement."},
        {"sentence": "They can swim, and so can we.", "notes": "Use 'so' with modal auxiliary + subject to agree."},
    ]
    exercises = [
        {"type": "short", "q": "Completa con 'so' o 'neither': He finished early, ____ did I.", "a": "so", "difficulty": "easy"},
        {"type": "fill", "q": "Rellena: I don't like spinach. ____ do I.", "a": "neither", "difficulty": "easy"},
        {"type": "mcq", "q": "¿Cuál es correcta? 'She can dance, ____?'", "options": ["so can I", "neither can I", "so do I"], "a": "so can I", "difficulty": "medium"},
        {"type": "short", "q": "Transforma: 'I am hungry.' -> respuesta corta de acuerdo usando 'so'.", "a": "so am I", "difficulty": "medium"},
        {"type": "fill", "q": "Rellena: I didn't see the movie. ____ _____ I.", "a": "neither did", "difficulty": "hard"},
        {"type": "mcq", "q": "Selecciona la forma correcta: 'They won't come, ____?'", "options": ["will they", "won't they", "do they"], "a": "will they", "difficulty": "hard"},
    ]
    return {
        "explanation": (
            "Uso detallado: 'so' se usa para mostrar acuerdo con una afirmación positiva. "
            "Se coloca antes del auxiliar y sujeto. 'neither' se usa para mostrar acuerdo con una negación, "
            "y la estructura típica es 'neither + auxiliar + sujeto'. En oraciones con modales o tiempos compuestos, "
            "se conserva el auxiliar correspondiente (can, have, will, etc.). Ejemplos y ejercicios incluyen notas y variaciones."
        ),
        "structure": "Afirmativa: so + auxiliar + sujeto. Negativa: neither + auxiliar + sujeto.",
        "examples": examples,
        "common_errors": [
            "Usar 'so' en vez de 'neither' para afirmaciones negativas.",
            "Omitir el auxiliar correcto después de 'so' o 'neither'.",
        ],
        "exercises": exercises,
    }


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


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        heading = request.form.get('heading')
        data = ai_generate(heading)
        db = SessionLocal()
        g = Grammar(title=heading, notation=heading, data=json.dumps(data))
        db.add(g)
        db.commit()
        db.refresh(g)
        db.close()
        return redirect(url_for('grammar_page', gid=g.id))
    return render_template('create.html')


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
    # Simple check, case-insensitive exact match; if OpenAI available, use it for grading
    correct_flag = False
    feedback = ''
    if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
        try:
            client = openai.OpenAI()
        except Exception:
            client = openai
        prompt = (
            f"Evalúa si la respuesta '{answer}' responde correctamente a la pregunta. "
            f"Respuesta correcta: '{correct}'. Devuelve JSON: {{'correct': bool, 'explanation': str}}"
        )
        resp = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{"role":"user","content":prompt}],
            max_tokens=300,
        )
        try:
            # extract text robustly
            try:
                eval_text = resp.choices[0].message.content
            except Exception:
                try:
                    eval_text = resp.choices[0].message['content']
                except Exception:
                    eval_text = resp['choices'][0]['message']['content']
            out = json.loads(eval_text)
            correct_flag = bool(out.get('correct'))
            feedback = out.get('explanation', '')
        except Exception:
            # fallback
            correct_flag = answer.strip().lower() == correct.strip().lower()
            feedback = 'Respuesta evaluada automáticamente.'
    else:
        # Local grading with some heuristics per type
        if ex_type == 'mcq':
            correct_flag = answer.strip().lower() == correct.strip().lower()
            feedback = 'Seleccionaste: ' + answer
        elif ex_type == 'fill':
            correct_flag = answer.strip().lower() == correct.strip().lower()
            feedback = 'Respuesta verificada localmente.'
        else:
            # short answer: exact match fallback
            correct_flag = answer.strip().lower() == correct.strip().lower()
            feedback = 'Respuesta verificada localmente.'

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


@app.route('/api/regenerate/<int:gid>', methods=['POST'])
def api_regenerate(gid):
    """Regenerate grammar content using AI and update stored data.

    Requires OPENAI_API_KEY to be set in environment where the server runs.
    """
    if not OPENAI_AVAILABLE or not os.getenv('OPENAI_API_KEY'):
        return jsonify({'ok': False, 'error': 'OpenAI API key not configured on server'}), 400
    db = SessionLocal()
    g = db.query(Grammar).get(gid)
    if not g:
        db.close()
        return jsonify({'ok': False, 'error': 'grammar not found'}), 404
    # call ai_generate to get new data
    new_data = ai_generate(g.title)
    try:
        g.data = json.dumps(new_data, ensure_ascii=False)
        db.add(g)
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        return jsonify({'ok': False, 'error': str(e)}), 500
    db.close()
    return jsonify({'ok': True, 'message': 'Regenerated', 'data': new_data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
