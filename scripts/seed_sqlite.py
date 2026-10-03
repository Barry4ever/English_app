import sqlite3
import json
import os

DB_PATH = os.getenv('DB_PATH', 'grammar.db')

EXERCISE_HUB = {
    'title': 'Perfect English Grammar: ejercicios de gramática',
    'url': 'https://www.perfect-english-grammar.com/grammar-exercises.html',
}

EXAM_LINKS = [
    {
        'title': 'Cambridge B1 Preliminary: simulacros y pruebas oficiales de muestra',
        'url': 'https://www.cambridgeenglish.org/exams-and-tests/qualifications/preliminary/preparation/#exam-essentials',
    },
    {
        'title': 'Cambridge B1 Preliminary: formato oficial del examen',
        'url': 'https://www.cambridgeenglish.org/exams-and-tests/qualifications/preliminary/format/',
    },
]


def topic(title, explanation, structure, examples, errors, exercise_urls):
    return {
        'title': title,
        'data': {
            'explanation': explanation,
            'structure': structure,
            'examples': [
                {'sentence': sentence, 'notes': notes}
                for sentence, notes in examples
            ],
            'common_errors': errors,
            'practice_links': [
                {'title': label, 'url': url} for label, url in exercise_urls
            ] + [EXERCISE_HUB],
            'exam_links': EXAM_LINKS,
        },
    }


topics = [
    topic(
        'Present simple and present continuous; action and non-action verbs',
        'El present simple describe rutinas, hechos estables y estados: «I work in a library». El present continuous expresa acciones en curso o situaciones temporales: «I am working from home this week». Los verbos de acción suelen admitir ambas formas, pero los verbos de estado (por ejemplo, know, believe, need y belong) normalmente no se usan en continuous cuando conservan su significado de estado. Algunos cambian de significado según la forma: «I think it is useful» expresa una opinión; «I am thinking about it» describe el proceso de reflexionar.',
        'Present simple: sujeto + verbo base (+ -s en he/she/it); do/does para preguntas y negativas.\nPresent continuous: sujeto + am/is/are + verbo-ing.\nLos verbos de estado suelen ir en simple, salvo usos dinámicos con otro significado.',
        [
            ('Maya usually takes the bus, but today she is cycling.', 'Rutina frente a una acción temporal que ocurre hoy.'),
            ('I know the answer, but I am thinking about the question.', 'Know expresa un estado; am thinking describe una actividad mental en curso.'),
            ('This soup tastes spicy.', 'Taste describe una característica; no se usa aquí en continuous.'),
        ],
        ['Usar el present continuous con know o believe para expresar un estado.', 'Olvidar -s en la tercera persona del present simple.', 'Confundir una rutina con una situación temporal.'],
        [('Present simple o continuous: ejercicio de elección', 'https://www.perfect-english-grammar.com/present-simple-present-continuous-1.html')],
    ),
    topic(
        'Future forms: present continuous, be going to, will and won’t',
        'El present continuous se usa para planes personales ya acordados, normalmente con una hora o fecha: «We are meeting Ana at six». Be going to expresa una intención decidida antes de hablar o una predicción basada en indicios visibles. Will suele servir para decisiones espontáneas, ofrecimientos, promesas y predicciones u opiniones; won’t forma la negativa. La elección depende de cómo conoce o interpreta el hablante el futuro, no solo de una traducción literal de «futuro».',
        'Plan acordado: am/is/are + verbo-ing.\nIntención o indicio: am/is/are going to + verbo base.\nDecisión, promesa o predicción: will / won’t + verbo base.',
        [
            ('I am seeing the dentist on Friday.', 'Cita acordada.'),
            ('Look at those clouds; it is going to rain.', 'Predicción basada en una señal presente.'),
            ('I will carry that bag for you.', 'Ofrecimiento espontáneo.'),
        ],
        ['Usar will para todos los planes, incluso los ya acordados.', 'Olvidar be en be going to.', 'Añadir to después de will.'],
        [('Ejercicio de formas de futuro', 'https://www.perfect-english-grammar.com/future-tenses-form-mixed-exercise-1.html')],
    ),
    topic(
        'Present perfect and past simple',
        'El past simple sitúa una acción en un periodo terminado, indicado o entendido por el contexto: yesterday, in 2022, last week. El present perfect relaciona una experiencia o resultado pasado con el presente, o habla de un periodo que todavía no ha terminado. Por eso no suele combinarse con una fecha pasada ya cerrada. En preguntas sobre experiencias se usa a menudo ever; para preguntar cuándo ocurrió algo concreto, se cambia al past simple.',
        'Past simple: sujeto + pasado; did/didn’t + verbo base en preguntas y negativas.\nPresent perfect: sujeto + have/has + participio pasado.',
        [
            ('We visited Edinburgh last April.', 'Past simple con un periodo terminado.'),
            ('I have visited Edinburgh twice.', 'Experiencia vital sin fecha concreta.'),
            ('Have you finished the report yet?', 'Se pregunta por un resultado relevante ahora.'),
        ],
        ['Combinar present perfect con yesterday o ago.', 'Usar el pasado en vez del participio después de have/has.', 'Preguntar «When have you…?» por un momento terminado.'],
        [('Past simple o present perfect: ejercicios', 'https://www.perfect-english-grammar.com/past-simple-present-perfect-1.html')],
    ),
    topic(
        'Present perfect with for and since; present perfect continuous',
        'For indica la duración completa de un periodo («for three months»), mientras que since marca el momento en que empezó («since March»). El present perfect simple suele destacar el hecho, el estado o el resultado; el continuous destaca la actividad y su duración, a menudo cuando continúa o acaba de terminar. Los verbos de estado normalmente conservan el simple: «I have known her for years».',
        'Duración/estado: have/has + participio + for/since.\nActividad: have/has + been + verbo-ing.\nFor + periodo; since + punto de inicio.',
        [
            ('Lena has lived here since 2021.', 'Since introduce el momento de inicio; el estado continúa.'),
            ('We have been waiting for forty minutes.', 'For marca la duración de una actividad en curso.'),
            ('I have known Sam for a long time.', 'Know es un verbo de estado y normalmente va en simple.'),
        ],
        ['Usar since con una duración («since two years»).', 'Confundir have been doing con have done cuando importa la actividad.', 'Usar el continuous normalmente con verbos de estado.'],
        [('Present perfect simple y continuous', 'https://www.perfect-english-grammar.com/present-perfect-present-perfect-continuous-1.html')],
    ),
    topic(
        'Choosing between comparatives and superlatives',
        'El comparativo establece una diferencia entre dos personas, objetos o situaciones, a menudo con than. El superlativo identifica el extremo dentro de un grupo y suele llevar the. Los adjetivos cortos suelen formar -er/-est; los largos suelen usar more/most. Hay formas irregulares frecuentes, como good, better, the best. Se elige según se comparen dos elementos o se destaque uno frente a un conjunto.',
        'Comparativo: adjetivo + -er / more + adjetivo + than.\nSuperlativo: the + adjetivo + -est / the most + adjetivo.\nIrregulares: good–better–the best; bad–worse–the worst.',
        [
            ('The train is faster than the coach.', 'Comparación entre dos medios de transporte.'),
            ('This is the most comfortable chair in the room.', 'Se destaca una silla dentro de un grupo.'),
            ('My second attempt was better than the first.', 'Better es el comparativo irregular de good.'),
        ],
        ['Usar the con un comparativo («the faster than»).', 'Olvidar the ante un superlativo.', 'Duplicar marcas: «more easier».'],
        [('Comparativos', 'https://www.perfect-english-grammar.com/comparative-adjectives-exercise-1.html'), ('Superlativos', 'https://www.perfect-english-grammar.com/superlatives-exercise-1.html')],
    ),
    topic(
        'Articles: a/an, the and no article',
        'A y an presentan un sustantivo contable singular que no es específico o que se menciona por primera vez; la elección depende del sonido inicial, no de la letra. The señala algo identificable para quien habla y escucha, ya mencionado o único en el contexto. No se usa artículo normalmente con plurales o incontables cuando se habla de manera general: «Books are useful», «Water is essential». Los nombres de lenguas, comidas y la mayoría de nombres propios también suelen aparecer sin artículo.',
        'a + sonido consonántico; an + sonido vocálico.\nthe + referente concreto/identificable.\nSin artículo + plural o incontable en sentido general.',
        [
            ('I saw a fox near the station. The fox was looking for food.', 'A presenta el animal; the retoma el referente conocido.'),
            ('She is an engineer.', 'An precede un sonido vocálico.'),
            ('Children need sleep.', 'Plural general sin artículo.'),
        ],
        ['Elegir a/an por la ortografía y no por el sonido.', 'Usar the para generalizaciones.', 'Omitir the cuando el referente ya está identificado.'],
        [('Ejercicios de artículos y usos sin artículo', 'https://www.perfect-english-grammar.com/articles-exercise-1.html')],
    ),
    topic(
        'Obligation and prohibition: have to, must and should',
        'Have to y must expresan obligación. Have to suele presentar una norma o necesidad externa; must suele expresar una obligación fuerte desde el punto de vista de quien habla, aunque el contexto puede variar. Mustn’t significa que algo está prohibido. Don’t have to significa que no es necesario, no que esté prohibido. Should ofrece consejo o recomendación menos fuerte.',
        'Obligación: have/has to + verbo base; must + verbo base.\nProhibición: mustn’t + verbo base.\nAusencia de obligación: don’t/doesn’t have to.\nConsejo: should/shouldn’t + verbo base.',
        [
            ('Visitors have to show their tickets at the entrance.', 'Obligación establecida por una regla.'),
            ('You mustn’t touch the paintings.', 'Prohibición.'),
            ('You should back up your files regularly.', 'Consejo.'),
        ],
        ['Interpretar don’t have to como prohibición.', 'Añadir -s a must o should.', 'Usar mustn’t cuando se quiere decir que algo no es obligatorio.'],
        [('Modal verbs of obligation', 'https://www.perfect-english-grammar.com/modal-verbs-of-obligation-exercise-1.html')],
    ),
    topic(
        'Ability and possibility: can, could and be able to',
        'Can expresa capacidad o posibilidad en presente y se usa en peticiones informales. Could describe una capacidad general en el pasado o una posibilidad menos segura. Para señalar que alguien logró completar una acción concreta en el pasado, suele usarse was/were able to, especialmente con verbos como escape, finish o reach. Be able to permite expresar capacidad en tiempos donde can no tiene una forma propia, como el infinitivo o el present perfect.',
        'Presente: can/can’t + verbo base.\nCapacidad general pasada: could/couldn’t + verbo base.\nÉxito concreto pasado: was/were able to + verbo base.\nOtros tiempos: be able to conjugado.',
        [
            ('Nora can speak three languages.', 'Capacidad actual.'),
            ('When I was six, I could swim quite well.', 'Capacidad general en el pasado.'),
            ('Despite the smoke, the firefighters were able to rescue everyone.', 'Logro concreto completado.'),
        ],
        ['Usar could para cualquier logro puntual pasado sin considerar el contexto.', 'Añadir to después de can.', 'Olvidar conjugar be en be able to.'],
        [('Modal verbs of ability', 'https://www.perfect-english-grammar.com/modal-verbs-of-ability-exercise-1.html')],
    ),
    topic(
        'Past tenses: simple, continuous and perfect',
        'El past simple cuenta acciones terminadas y acontecimientos principales. El past continuous presenta una acción en desarrollo en un momento pasado o como contexto; un acontecimiento breve puede interrumpirla. El past perfect sitúa una acción antes de otra referencia pasada. En narraciones, estos tiempos ayudan a ordenar los hechos y a distinguir el fondo de los acontecimientos que hacen avanzar la historia.',
        'Past simple: verbo en pasado.\nPast continuous: was/were + verbo-ing.\nPast perfect: had + participio pasado.',
        [
            ('We were having dinner when the lights went out.', 'Acción en curso interrumpida por un hecho puntual.'),
            ('She had left before I arrived.', 'La salida ocurrió antes de la llegada.'),
            ('They found the keys under the sofa.', 'Acontecimiento terminado que hace avanzar la narración.'),
        ],
        ['Usar past continuous para una sucesión de hechos terminados.', 'Olvidar had en el past perfect.', 'Usar past perfect para todo el relato en vez de marcar anterioridad.'],
        [('Past simple y continuous', 'https://www.perfect-english-grammar.com/past-simple-past-continuous-exercise-1.html'), ('Past perfect', 'https://www.perfect-english-grammar.com/past-perfect-exercise-3.html')],
    ),
    topic(
        'Past and present habits and states',
        'El present simple describe hábitos y estados actuales. Used to expresa hábitos o estados pasados que ya no son ciertos o habituales. Would puede describir acciones repetidas en el pasado, pero no suele expresar estados como live o know. Be used to + nombre o verbo en -ing significa estar acostumbrado a algo; get used to describe el proceso de acostumbrarse.',
        'Hábito/estado actual: present simple.\nHábito o estado pasado ya terminado: used to + verbo base.\nAcción pasada repetida: would + verbo base.\nEstar acostumbrado: be/get used to + nombre o verbo-ing.',
        [
            ('I used to live near the sea, but now I live in the city.', 'Estado pasado que ha cambiado.'),
            ('Every summer, we would visit our cousins in Wales.', 'Acción repetida en una etapa pasada.'),
            ('She is used to working at night.', 'Está habituada a trabajar de noche.'),
        ],
        ['Usar would para estados pasados.', 'Confundir used to do con be used to doing.', 'Poner el verbo en pasado después de used to.'],
        [('Used to y hábitos pasados', 'https://www.perfect-english-grammar.com/used-to-exercise-2.html')],
    ),
    topic(
        'Passive voice in all tenses',
        'La voz pasiva pone el foco en la acción o en quien la recibe, especialmente cuando el agente no se conoce, no importa o se sobreentiende. El objeto de la activa pasa a sujeto y be adopta el tiempo de la oración; el verbo principal va en participio. El agente se añade con by solo si aporta información útil. La pasiva se puede formar en varios tiempos, aunque algunas combinaciones son poco frecuentes en el uso cotidiano.',
        'Sujeto paciente + be conjugado en el tiempo correspondiente + participio pasado (+ by + agente).\nPresent simple: is made. Past simple: was made. Present perfect: has been made. Future: will be made.',
        [
            ('The library is cleaned every evening.', 'Pasiva en present simple; importa el proceso habitual.'),
            ('Our road was repaired last month.', 'Pasiva en past simple.'),
            ('The invitations have been sent.', 'Pasiva en present perfect; se destaca el resultado.'),
        ],
        ['Olvidar una forma de be.', 'Usar el pasado simple en vez del participio.', 'Añadir by cuando el agente no aporta nada.'],
        [('Pasiva en varios tiempos', 'https://www.perfect-english-grammar.com/passive-exercise-5.html')],
    ),
    topic(
        'Modals of deduction: might, can’t and must',
        'Estos modales expresan cuánto cree el hablante que una deducción es cierta a partir de indicios. Must indica una conclusión muy probable; can’t expresa que algo parece imposible; might señala una posibilidad sin certeza. Aquí must no expresa obligación. Para deducir sobre el pasado se usa modal + have + participio: must have left, can’t have seen, might have forgotten.',
        'Deducción presente: must / can’t / might + verbo base.\nDeducción pasada: must / can’t / might + have + participio pasado.',
        [
            ('The lights are on, so they must be at home.', 'Conclusión muy probable.'),
            ('That can’t be Priya; she is in another country.', 'El contexto hace que la hipótesis parezca imposible.'),
            ('He might have missed the earlier train.', 'Posibilidad sobre un hecho pasado.'),
        ],
        ['Usar mustn’t para una deducción negativa en vez de can’t.', 'Añadir to después del modal.', 'Omitir have en una deducción sobre el pasado.'],
        [('Modal verbs of probability', 'https://www.perfect-english-grammar.com/modal-verbs-of-probability-exercise-1.html')],
    ),
    topic(
        'First conditional and choosing between conditionals',
        'El first conditional habla de una condición futura real o posible y de su resultado probable. Para elegir entre condicionales, identifica primero si describes una verdad general (zero), una posibilidad futura (first) o una situación hipotética presente/futura (second). La cláusula con if normalmente no lleva will en el first conditional; el resultado puede llevar will, un modal o un imperativo.',
        'Zero: if + present simple, present simple.\nFirst: if + present simple, will/can/may + verbo base.\nSecond: if + past simple, would/could + verbo base.',
        [
            ('If it rains tomorrow, we will take the train.', 'Posibilidad futura: first conditional.'),
            ('If you heat ice, it melts.', 'Verdad general: zero conditional.'),
            ('If I had more free time, I would learn Italian.', 'Situación hipotética: second conditional.'),
        ],
        ['Poner will inmediatamente después de if en el first conditional.', 'Usar el first para una situación imaginaria.', 'Confundir la forma pasada del second con un pasado real.'],
        [('First, second and third conditionals', 'https://www.perfect-english-grammar.com/first-second-third-conditionals-exercise.html')],
    ),
    topic(
        'Choosing between gerunds and infinitives',
        'Después de algunos verbos se usa el gerundio (verbo-ing), y después de otros, el infinitivo con to; estos patrones se aprenden junto con cada verbo. Tras preposiciones se usa normalmente -ing. Algunos verbos admiten ambas formas con un cambio de significado: stop doing es dejar una actividad, mientras que stop to do es detenerse para hacer otra cosa. El infinitivo también expresa con frecuencia propósito.',
        'Preposición + verbo-ing.\nVerbo + gerundio: enjoy doing, avoid doing.\nVerbo + to-infinitive: decide to do, hope to do.\nPropósito: to + verbo base.',
        [
            ('Ravi enjoys cooking for his friends.', 'Enjoy va seguido de gerundio.'),
            ('We decided to leave before dark.', 'Decide va seguido de infinitivo con to.'),
            ('She stopped to answer the phone.', 'Se detuvo con el propósito de contestar.'),
        ],
        ['Usar to-infinitive después de una preposición.', 'Elegir la forma verbal sin comprobar el patrón del verbo.', 'Confundir stop doing y stop to do.'],
        [('Gerunds and infinitives', 'https://www.perfect-english-grammar.com/gerunds-and-infinitives-exercise-1.html')],
    ),
    topic(
        'Reported speech: statements and questions',
        'El estilo indirecto comunica lo que alguien dijo sin repetir necesariamente sus palabras exactas. Si el verbo introductor está en pasado, suele producirse un cambio de tiempo verbal y también pueden cambiar pronombres, expresiones de tiempo y referencias de lugar según la situación. Las preguntas indirectas usan el orden de una oración afirmativa y no llevan do/does/did. Las preguntas de sí/no suelen introducirse con if o whether.',
        'Afirmación: said (that) + oración; told + persona + (that) + oración.\nPregunta con palabra interrogativa: asked + palabra + sujeto + verbo.\nPregunta sí/no: asked + if/whether + sujeto + verbo.',
        [
            ('“I am tired,” Mia said. → Mia said (that) she was tired.', 'El present pasa a past al informar desde un contexto pasado.'),
            ('“Where do you work?” he asked. → He asked where I worked.', 'La pregunta indirecta utiliza orden afirmativo.'),
            ('“Have you seen my keys?” Ana asked. → Ana asked if I had seen her keys.', 'If introduce una pregunta indirecta de sí/no.'),
        ],
        ['Conservar el orden interrogativo en una pregunta indirecta.', 'Usar tell sin indicar a quién se habló.', 'Cambiar automáticamente los tiempos cuando el contexto no lo requiere.'],
        [('Reported speech: afirmaciones y preguntas', 'https://www.perfect-english-grammar.com/reported-speech-exercise-4.html'), ('Reported questions', 'https://www.perfect-english-grammar.com/reported-speech-exercise-6.html')],
    ),
    topic(
        'Third conditional',
        'El third conditional imagina un pasado diferente y el resultado que habría tenido. Se usa para hablar de arrepentimientos, críticas o consecuencias hipotéticas; no cambia lo que realmente ocurrió. La cláusula con if lleva past perfect y el resultado suele llevar would have + participio. También son posibles could have o might have para expresar capacidad o posibilidad.',
        'If + past perfect, would/could/might have + participio pasado.\nLas dos cláusulas pueden cambiar de orden; no se usa would en la cláusula con if.',
        [
            ('If we had booked earlier, we would have paid less.', 'Pasado hipotético y resultado imaginado.'),
            ('She could have caught the bus if she had left on time.', 'Could have expresa un resultado posible que no ocurrió.'),
            ('If I had known about the change, I might have joined you.', 'Might have expresa una posibilidad pasada.'),
        ],
        ['Usar would have en la cláusula con if.', 'Olvidar had o el participio pasado.', 'Confundir una hipótesis pasada con una posibilidad futura.'],
        [('Third conditional', 'https://www.perfect-english-grammar.com/third-conditional-exercise-1.html')],
    ),
    topic(
        'Quantifiers',
        'Los cuantificadores expresan cantidad y dependen de si el sustantivo es contable o incontable. Many y a few acompañan contables; much y a little, incontables. A lot of se usa con ambos y es habitual en afirmativas. Some aparece con frecuencia en afirmativas y ofrecimientos; any, en preguntas y negativas. Few/little sugieren una cantidad escasa, mientras que a few/a little indican que hay algo, aunque no mucho.',
        'Contables: many, (a) few, several.\nIncontables: much, (a) little.\nAmbos: a lot of, some, any, enough.\nHow many + plural; how much + incontable.',
        [
            ('We have a few minutes before the film starts.', 'A few + sustantivo contable plural; quedan algunos.'),
            ('There isn’t much milk left.', 'Much acompaña al incontable milk en una negativa.'),
            ('Would you like some water?', 'Some es habitual en ofrecimientos.'),
        ],
        ['Usar many con un sustantivo incontable.', 'Confundir few con a few y little con a little.', 'Usar any solo en negativas y olvidar preguntas.'],
        [('Some y any', 'https://www.perfect-english-grammar.com/some-and-any-exercise-1.html'), ('A little y a few', 'https://www.perfect-english-grammar.com/a-little-a-few-exercise-1.html')],
    ),
    topic(
        'Defining and non-defining relative clauses',
        'Una defining relative clause identifica de qué persona o cosa se habla y no se separa con comas. Una non-defining clause añade información extra sobre un referente ya identificado y se delimita con comas. Who suele referirse a personas, which a cosas y where a lugares; that puede sustituir a who o which en muchas defining clauses, pero no se usa normalmente en las non-defining. El pronombre puede omitirse cuando es objeto en una defining clause.',
        'Defining: nombre + who/which/that/where + cláusula (sin comas).\nNon-defining: nombre, + who/which/where + cláusula, (con comas; sin that).',
        [
            ('The book that you lent me is fascinating.', 'La cláusula identifica qué libro; that es objeto.'),
            ('My aunt, who lives in Bristol, is visiting us.', 'Información adicional sobre una persona ya identificada.'),
            ('This is the café where we first met.', 'Where introduce el lugar relacionado con la acción.'),
        ],
        ['Poner comas en una defining clause.', 'Usar that en una non-defining clause.', 'Omitir el pronombre cuando funciona como sujeto.'],
        [('Defining relative clauses', 'https://www.perfect-english-grammar.com/relative-clauses-exercise-1.html'), ('Pronombres relativos', 'https://www.perfect-english-grammar.com/relative-pronouns-exercise.html')],
    ),
    topic(
        'Question tags',
        'Las question tags son preguntas breves al final de una afirmación. Se usan para comprobar información o invitar a la otra persona a confirmar algo. Normalmente una afirmación positiva lleva una tag negativa, y una afirmación negativa lleva una tag positiva. La tag repite el auxiliar de la oración; si no hay auxiliar, se usa do/does/did. Con I am se suele usar aren’t I?',
        'Afirmativa + auxiliar negativo + pronombre?\nNegativa + auxiliar positivo + pronombre?\nSin auxiliar: do/does/did.\nI am…, aren’t I?',
        [
            ('You have met my brother, haven’t you?', 'Afirmación positiva y tag negativa con have.'),
            ('She doesn’t drive, does she?', 'Afirmación negativa y tag positiva con does.'),
            ('Let’s take a break, shall we?', 'Invitación con la tag convencional shall we?'),
        ],
        ['Repetir el sujeto nominal en vez de usar un pronombre.', 'Usar un auxiliar distinto del de la oración.', 'Hacer la tag del mismo signo que la afirmación.'],
        [('Índice de ejercicios de gramática', 'https://www.perfect-english-grammar.com/grammar-exercises.html')],
    ),
]


def seed_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # create tables if needed
    cur.execute('''CREATE TABLE IF NOT EXISTS grammars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        notation TEXT,
        data TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grammar_id INTEGER,
        attempts INTEGER DEFAULT 0,
        correct INTEGER DEFAULT 0,
        wrong INTEGER DEFAULT 0
    )''')
    conn.commit()
    # Replace the previous levels and their progress with the supplied B1 syllabus.
    cur.execute('DELETE FROM progress')
    cur.execute('DELETE FROM grammars')
    conn.commit()
    for item in topics:
        cur.execute(
            'INSERT INTO grammars (title, notation, data) VALUES (?, ?, ?)',
            (item['title'], 'B1', json.dumps(item['data'], ensure_ascii=False)),
        )
    conn.commit()
    cur.execute('SELECT COUNT(*) FROM grammars WHERE notation = ?', ('B1',))
    total = cur.fetchone()[0]
    print(f'Replaced grammar content with {total} B1 topics; cleared old progress.')
    conn.close()


if __name__ == '__main__':
    seed_sqlite()
