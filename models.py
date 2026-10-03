import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE = declarative_base()


class Grammar(BASE):
    __tablename__ = 'grammars'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    notation = Column(String(200))
    data = Column(Text)


class Progress(BASE):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    grammar_id = Column(Integer)
    attempts = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)


def init_db(app=None):
    db_url = os.getenv('DATABASE_URL', 'sqlite:///grammar.db')
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    BASE.metadata.create_all(engine)


engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///grammar.db'), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def record_attempt(db_session, grammar_id, correct: bool):
    # db_session should be a Session instance
    db = db_session
    prog = db.query(Progress).filter(Progress.grammar_id == grammar_id).first()
    if not prog:
        prog = Progress(grammar_id=grammar_id, attempts=0, correct=0, wrong=0)
        db.add(prog)
    prog.attempts = (prog.attempts or 0) + 1
    if correct:
        prog.correct = (prog.correct or 0) + 1
    else:
        prog.wrong = (prog.wrong or 0) + 1
    db.commit()


def get_progress_for(db_session, grammar_id):
    db = db_session
    prog = db.query(Progress).filter(Progress.grammar_id == grammar_id).first()
    if not prog:
        return {"attempts": 0, "correct": 0, "wrong": 0, "percent": 0}
    attempts = prog.attempts or 0
    correct = prog.correct or 0
    wrong = prog.wrong or 0
    percent = int((correct / attempts) * 100) if attempts > 0 else 0
    return {"attempts": attempts, "correct": correct, "wrong": wrong, "percent": percent}
