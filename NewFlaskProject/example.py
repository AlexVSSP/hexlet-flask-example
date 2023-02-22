import json
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, make_response, session
from random import randint

                                    ### Самостоятельная работа по курсу "Веб-разработка (Flask)" ###

# Это callable WSGI-приложение
app = Flask(__name__)

app.secret_key = "secret_key"

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']  # Этот список добавлен для урока "11. Поисковые формы"


# 5. Flask
@app.route('/')
def hello_world():
    return 'Hello, guys!'


# 6. Обработчики запросов и 7. HTTP-сессия
# Следующие 2 обработчика было закомитчены, чтобы не мешать следующим шагам курса
# @app.get('/users')  # Закоммичен, т.к. мешает уроку "16. CRUD"
# def users_get():
#     return 'GET /users'

# @app.post('/users') # Закоммичен, т.к. мешает уроку "11. Поисковые формы"
# def users():
#     return 'Users', 302


# 8. Динамические маршруты
@app.route('/courses/<int:id>')
def courses(id):
    return f'Course id: {id}'


# 9. Шаблонизатор
@app.route('/users/<int:id>')
def show_user(id):

    return render_template(
        'users/show.html',
        id=id,
        nickname=f'user-{id}'
    )


# # 11. Поисковые формы без куки
# @app.route('/users/')
# def filter_users():
# # Рабочая часть для самостоятельной работы "16. CRUD"
#     term = request.args.get('term', '')
#     with open('user_rep.json') as us:
#         b = json.loads(us.read())
#         filtered_users = list(filter(lambda user: str(term) in user['nickname'], b)) ######### ТЕСТ
#
#     if not filtered_users:
#         filtered_users = users
#
#     messages = get_flashed_messages(with_categories=True)  # Добавлено по заданию "15. Flash"
#     print(messages)                                        # Добавлено по заданию "15. Flash"
# # Конец части для "16. CRUD"
#
#     return render_template(
#         'users/index.html',
#         users=filtered_users,
#         search=term,
#         messages=messages
#     )


# 11. Поисковые формы с куки
@app.route('/users/')
def filter_users():
    term = request.args.get('term', '')

    if not request.cookies.get('users_cookie'):
        response = make_response(redirect('/users/'))
        response.set_cookie('users_cookie', '[]')
        return response

    else:
        all_users = json.loads(request.cookies.get('users_cookie'))
        filtered_users = list(filter(lambda user: str(term) in user['nickname'], all_users))

    if not filtered_users:
        filtered_users = all_users

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages
    )


# 13. Модифицирующие формы
def validate(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Nickname can't be blank"
    if len(user['nickname']) < 4:
        errors['nickname'] = "Nickname must be greater than 4 characters"
    if not user['email']:
        errors['email'] = "Email can't be blank"
    return errors


# 17. CRUD. Создание (два обработчика)
@app.route('/users/new')
def users_new():
    user = {'nickname': '',
            'email': ''}
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


# @app.post('/users')
# def users_post():
#     id = str(randint(11, 30))
#     user = request.form.to_dict()
#     user['id'] = id
#     errors = validate(user)
#     if errors:
#         return render_template(
#           'users/new.html',
#           user=user,
#           errors=errors,
#         )
#
#         # Тест для самостоятельной работы "16. CRUD"
#     with open('user_rep.json') as r:
#         data = json.loads(r.read())
#         data.append(user)
#
#     with open('user_rep.json', 'w') as file:
#         file.write(json.dumps(data, indent=4))
#         # Конец теста для "16. CRUD"
#
#         flash('User was added successfully', 'success')  # Добавлено по заданию "15. Flash"
#     return redirect(url_for('filter_users'), code=302)
#     # return redirect('/users', code=302) # Строчка исключена для выполнения задания "14. Именованные маршруты"


# 17. CRUD. Создание с куки (второй обработчик)
@app.post('/users')
def users_post():
    id = str(randint(1, 50))
    user = request.form.to_dict()
    user['id'] = id
    errors = validate(user)
    if errors:
        return render_template(
          'users/new.html',
          user=user,
          errors=errors,
        )

    all_users = json.loads(request.cookies.get('users_cookie', json.dumps([])))
    all_users.append(user)

    encoded_all_users = json.dumps(all_users)

    flash('User was added successfully', 'success')  # Добавлено по заданию "15. Flash"
    response = make_response(redirect(url_for('filter_users'), code=302))
    response.set_cookie('users_cookie', encoded_all_users)
    return response





# # 18. CRUD:Обновление без куки (два обработчика)
# @app.route('/users/<id>/edit')
# def edit_user(id):
#     repo = 'user_rep.json'
#     with open(repo) as r:
#         data = json.loads(r.read())
#     # user = data.find(id)
#     for element in data:
#         if element['id'] == id:
#             user = element
#     errors = []
#
#     return render_template(
#            'users/edit.html',
#            user=user,
#            errors=errors,
#     )
#
#
# @app.route('/users/<id>/patch', methods=['POST'])
# def patch_user(id):
#     repo = 'user_rep.json'
#     with open(repo) as r:
#         datas = json.loads(r.read())
#
#     for element in datas:
#         if element['id'] == id:
#             user = element
#
#     data = request.form.to_dict()
#
#     errors = validate(data)
#     if errors:
#         return render_template(
#             'users/edit.html',
#             user=user,
#             errors=errors,
#         ), 422
#
#     with open('user_rep.json') as f:
#         file = json.loads(f.read())
#         for user in file:
#             if user['id'] == id:
#                 user['nickname'] = data['nickname']
#                 user['email'] = data['email']
#     with open('user_rep.json', 'w') as f:
#         f.write(json.dumps(file, indent=4))
#
#     flash('User has been updated', 'success')
#     return redirect(url_for('filter_users'))


# 18. CRUD:Обновление c куки (два обработчика)
@app.route('/users/<id>/edit')
def edit_user(id):
    all_users = json.loads(request.cookies.get('users_cookie', json.dumps([])))
    for element in all_users:
        if element['id'] == id:
            user = element
    errors = []

    return render_template(
           'users/edit.html',
           user=user,
           errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    all_users = json.loads(request.cookies.get('users_cookie', json.dumps([])))

    for element in all_users:
        if element['id'] == id:
            user = element

    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422

    for user in all_users:
        if user['id'] == id:
            user['nickname'] = data['nickname']
            user['email'] = data['email']

    encoded_all_users = json.dumps(all_users)
    response = make_response(redirect(url_for('filter_users'), code=302))
    response.set_cookie('users_cookie', encoded_all_users)

    flash('User has been updated', 'success')
    return response


# # 19. CRUD: Удаление без куки (один обработчик)
# @app.route('/users/<id>/delete', methods=['POST'])
# def delete_user(id):
#     # repo = SchoolRepository()
#     repo = 'user_rep.json'
#     with open(repo) as r:
#         data = json.loads(r.read())
#
#         # repo.destroy(id)
#         for user in data:
#             if user['id'] == id:
#                 index = data.index(user)
#                 data.pop(index)
#     with open(repo, 'w') as r:
#         r.write(json.dumps(data, indent=4))
#
#     flash('User has been deleted', 'success')
#     return redirect(url_for('filter_users'))


# 19. CRUD: Удаление с куки (один обработчик)
@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    all_users = json.loads(request.cookies.get('users_cookie', json.dumps([])))

    for user in all_users:
        if user['id'] == id:
            index = all_users.index(user)
            all_users.pop(index)

    encoded_all_users = json.dumps(all_users)
    response = make_response(redirect(url_for('filter_users'), code=302))
    response.set_cookie('users_cookie', encoded_all_users)

    flash('User has been deleted', 'success')
    return response


# # 22. Сессия НЕ РАБОТАЕТ. НУЖНО РАЗБИРАТЬСЯ со всеми следующими обработчиками
# def get_user(form_email, repo):
#     email = form_email['email']
#     for user in repo:
#         if user['email'] == email:
#             return user
#
#
# @app.route('/users/sindex')
# def index_session():
#     messages = get_flashed_messages(with_categories=True)
#     current_user = session.get('user')
#     return render_template(
#         'users/index_session.html',
#         messages=messages,
#         current_user=current_user,
#         )
#
#
# @app.route('/users/sindex/session/new', methods=['POST'])
# def session_new():
#     user_email = request.form.to_dict()
#     all_users = json.loads(request.cookies.get('users_cookie', json.dumps([])))
#
#     current_user = get_user(user_email, all_users)
#     if current_user:
#         session['user'] = current_user
#     else:
#         flash('Wrong email')
#     return redirect(url_for('index_session'))


