from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    request,
    abort
)
import os
import requests
from dotenv import load_dotenv
from page_analyzer.seo import get_seo
from page_analyzer.url import validate, normalize
import page_analyzer.db as db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    urls = db.get_urls_with_checks()

    return render_template('urls.html', urls=urls, messages=messages)


@app.post('/urls')
def post_url():
    form_data = request.form.to_dict()
    url = form_data.get('url')
    errors = validate(url)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template(
            'index.html',
            url_name=url,
            messages=get_flashed_messages(with_categories=True)
        ), 422

    url = normalize(url)
    existing_url = db.get_url_by_name(url)

    if not existing_url:
        id = db.add_url(url)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
        id = existing_url.id

    return redirect(url_for('show_url', id=id))


@app.get('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url_by_id(id)

    if not url:
        abort(404)
    checks = db.get_checks_for_url(id)
    return render_template(
        'url.html',
        url=url,
        checks=checks,
        messages=messages
    )


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = db.get_url_by_id(id).name

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    page = get_seo(res.text)
    page_data = {
        'url_id': id,
        'status_code': res.status_code,
        'title': page[0],
        'h1': page[1],
        'description': page[2]
    }
    db.add_check(page_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'error.html',
        title='Страница не найдена'
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        'error.html',
        title='Внутренняя ошибка сервера'
    ), 500
