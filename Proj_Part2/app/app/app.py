import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
import logging

from flask import Flask, abort, render_template

import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
        (SELECT COUNT(*) n_series FROM series)
    JOIN
        (SELECT COUNT(*) n_atores FROM atores)
    JOIN
        (SELECT COUNT(*) n_generos FROM generos)
    JOIN
        (SELECT COUNT(*) n_escritores FROM escritores)
    JOIN
        (SELECT COUNT(*) n_personagens FROM personagens)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Series
@APP.route('/series/')
def list_series():
    series = db.execute(
        '''
        SELECT idSerie, titulo, tituloOriginal, dataLancamento, temporadas, episodios, classificacao, nrVotos
        FROM series
        ORDER BY idSerie
        ''').fetchall()
    return render_template('series-list.html', series=series)


@APP.route('/series/<int:id>/')
def get_serie(id):
  series = db.execute(
      '''
      SELECT *
      FROM series
      WHERE idSerie = ?
      ''', [id]).fetchone()

  if series is None:
      abort(404, 'Id Serie {} não existe.'.format(id))

  generos = db.execute(
      '''
      SELECT idGenero, tipo
      FROM series NATURAL JOIN generos
      WHERE idSerie = ?
      ORDER BY idGenero
      ''', [id]).fetchall()

  atores = db.execute(
      '''
      SELECT idAtor, nomeA, dataNascimento, dataFalecimento
      FROM personagens NATURAL JOIN atores
      WHERE idSerie = ?
      ORDER BY idAtor
      ''', [id]).fetchall()

  personagens = db.execute(
    '''
    SELECT idPersonagem, nomeP
    FROM series NATURAL JOIN personagens
    WHERE idSerie = ?
    ORDER BY idPersonagem;
    ''', [id]).fetchall()

  escritores = db.execute(
      '''
      SELECT idEscritores, nomeE, dataNascimento, dataFalecimento
      FROM escritores_series NATURAL JOIN escritores
      WHERE idSerie = ?
      ORDER BY idSerie
      ''', [id]).fetchall()
  return render_template('series.html',
            series=series, generos=generos, atores=atores, personagens=personagens, escritores=escritores)

@APP.route('/series/search/<expr>/')
def search_serie(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  series = db.execute(
      '''
      SELECT idSerie, titulo
      FROM series
      WHERE titulo LIKE ?
      ''', [expr]).fetchall()
  return render_template('series-search.html',
            search=search,series=series)

# Atores
@APP.route('/atores/')
def list_atores():
    atores = db.execute('''
      SELECT idAtor, nomeA, dataNascimento, dataFalecimento
      FROM atores
      ORDER BY idAtor
    ''').fetchall()
    return render_template('atores-list.html', atores=atores)


@APP.route('/atores/<int:id>/')
def view_series_by_actor(id):
  atores = db.execute(
    '''
    SELECT *
    FROM atores
    WHERE idAtor = ?
    ''', [id]).fetchone()

  if atores is None:
      abort(404, 'Id Ator {} não existe.'.format(id))

  series = db.execute(
    '''
    SELECT idSerie, titulo
    FROM series
    WHERE idSerie in (SELECT idSerie from personagens WHERE idAtor = ?)
    ORDER BY idSerie
    ''', [id]).fetchall()

  return render_template('atores.html',
            atores=atores, series=series)

@APP.route('/atores/search/<expr>/')
def search_ator(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  atores = db.execute(
      '''
      SELECT idAtor, nomeA
      FROM atores
      WHERE nomeA LIKE ?
      ''', [expr]).fetchall()
  return render_template('atores-search.html',
            search=search,atores=atores)

# Generos
@APP.route('/generos/')
def list_generos():
    generos = db.execute('''
      SELECT idGenero, tipo
      FROM generos
      ORDER BY idGenero
    ''').fetchall()
    return render_template('generos-list.html', generos=generos)

@APP.route('/generos/<int:id>/')
def view_series_by_genero(id):
  generos = db.execute(
    '''
    SELECT *
    FROM generos
    WHERE idGenero = ?
    ''', [id]).fetchone()

  if generos is None:
      abort(404, 'Id Genero {} não existe.'.format(id))

  series = db.execute(
    '''
    SELECT idSerie, titulo
    FROM series NATURAL JOIN generos
    WHERE idGenero = ?
    ORDER BY idSerie
    ''', [id]).fetchall()

  return render_template('generos.html',
            generos=generos, series=series)

# Personagens
@APP.route('/personagens/')
def list_personagens():
    personagens = db.execute('''
      SELECT idPersonagem, nomeP
      FROM personagens
      ORDER BY idPersonagem
    ''').fetchall()
    return render_template('personagens-list.html', personagens=personagens)

@APP.route('/personagens/<int:id>/')
def view_series_by_personagens(id):
  personagens = db.execute(
    '''
    SELECT *
    FROM personagens
    WHERE idPersonagem = ?
    ''', [id]).fetchone()

  if personagens is None:
      abort(404, 'Id Personagem {} não existe.'.format(id))

  series = db.execute(
    '''
    SELECT idSerie, titulo
    FROM series NATURAL JOIN personagens
    WHERE idPersonagem = ?
    ORDER BY idSerie
    ''', [id]).fetchall()

  atores = db.execute(
    '''
    SELECT idAtor, nomeA
    FROM series NATURAL JOIN personagens NATURAL JOIN Atores
    WHERE idAtor = ?
    GROUP BY nomeA
    ORDER BY idAtor
    ''', [id]).fetchall()

  return render_template('personagens.html',
            personagens=personagens, series=series, atores=atores)

@APP.route('/personagens/search/<expr>/')
def search_personagem(expr):
   search = { 'expr': expr }
   expr = '%' + expr + '%'
   personagens = db.execute(
       '''
       SELECT idPersonagem, nomeP
       FROM personagens
       WHERE nomeP LIKE ?
       ''', [expr]).fetchall()
   return render_template('personagens-search.html',
             search=search,personagens=personagens)

# Escritores
@APP.route('/escritores/')
def list_escritores():
    escritores = db.execute('''
      SELECT idEscritores, nomeE, dataNascimento, dataFalecimento
      FROM escritores
      ORDER BY idEscritores
    ''').fetchall()
    return render_template('escritores-list.html', escritores=escritores)


@APP.route('/escritores/<int:id>/')
def view_series_by_escritores(id):
  escritores = db.execute(
    '''
    SELECT *
    FROM escritores
    WHERE idEscritores = ?
    ''', [id]).fetchone()

  if escritores is None:
      abort(404, 'Id Escritor {} não existe.'.format(id))

  series = db.execute(
    '''
    SELECT idSerie, titulo
    FROM series NATURAL JOIN escritores_series
    WHERE idEscritores = ?
    ORDER BY idSerie
    ''', [id]).fetchall()

  return render_template('escritores.html',
            escritores=escritores, series=series)

@APP.route('/escritores/search/<expr>/')
def search_escritor(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  escritores = db.execute(
      '''
      SELECT idEscritores, nomeE
      FROM escritores
      WHERE nomeE LIKE ?
      ''', [expr]).fetchall()
  return render_template('escritores-search.html',
            search=search,escritores=escritores)
