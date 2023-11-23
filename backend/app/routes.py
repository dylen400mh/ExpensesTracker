from flask import jsonify, request
from app import app, db
from app.models import User, Expense
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required

# User routes


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_data)


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {'id': user.id, 'username': user.username}
    return jsonify(user_data)


@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'})


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    # update user details provided in request
    if 'username' in data:
        user.username = data['username']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    updated_user_data = {'id': user.id, 'username': user.username}
    return jsonify({'message': 'User updated successfully', 'user': updated_user_data})


@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})

# Expense routes


@app.route('/api/expenses', methods=['GET'])
@login_required
def get_all_expenses():
    expenses = Expense.query.all()
    expenses_data = [{'id': expense.id, 'amount': expense.amount, 'description': expense.description,
                      'category': expense.category, 'date': expense.date} for expense in expenses]
    return jsonify(expenses_data)


@app.route('/api/expenses/<int:id>', methods=['GET'])
@login_required
def get_expense_by_id(id):
    expense = Expense.query.get(id)
    expense_data = {'id': expense.id, 'amount': expense.amount, 'description': expense.description,
                    'category': expense.category, 'date': expense.date}
    return jsonify(expense_data)


@app.route('/api/expenses', methods=['POST'])
@login_required
def add_expense():
    data = request.get_json()

    amount = data.get('amount')
    description = data.get('description')
    category = data.get('category')
    date = data.get('date')

    new_expense = Expense(amount, description, category, date)

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'})


@app.route('/api/expenses/<int:id>', methods=['PUT'])
@login_required
def update_expense(id):
    expense = Expense.query.get(id)

    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    data = request.get_json()

    # update expense based on data received
    if 'amount' in data:
        expense.amount = data['amount']

    if 'description' in data:
        expense.description = data['description']

    if 'category' in data:
        expense.category = data['category']

    if 'date' in data:
        expense.date = data['date']

    db.session.commit()

    updated_expense_data = {'id': expense.id, 'amount': expense.amount, 'description': expense.description,
                            'category': expense.category, 'date': expense.date}

    return jsonify({'message': 'Expense updated successfully', 'user': updated_expense_data})


@app.route('/api/expenses/<int:id>', methods=["DELETE"])
@login_required
def delete_expense(id):
    expense = Expense.query.get(id)

    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully'})


# Login / Registration routes


@app.route('/api/login', methods=['POST'])
def login():
    form = LoginForm(request.get_json())

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Login unsuccessful. Please check your credentials'}), 401


@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/register', methods=['POST'])
def register():
    form = RegistrationForm(request.get_json())

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return jsonify({'message': 'Username already exists. Choose another one'}), 400

        new_user = User(form.username.data, form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 201
    return jsonify({'message': "Registration unsuccessful. Please check your input"}), 400
