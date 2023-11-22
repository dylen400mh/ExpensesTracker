from flask import jsonify, request
from app import app, db
from app.models import User, Expense

# User routes


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username,
                   'password_hash': user.password_hash} for user in users]
    return jsonify(users_data)


@app.route('api/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {'id': user.id, 'username': user.username,
                 'password_hash': user.password_hash}
    return jsonify(user_data)


@app.route('api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'})


@app.route('api/users/<int:id>', methods=['PUT'])
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

    updated_user_data = {
        'id': user.id, 'username': user.username, 'password_hash': user.password_hash}
    return jsonify({'message': 'User updated successfully', 'user': updated_user_data})


@app.route('api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})

# Expense routes


@app.route('api/expenses', methods=['GET'])
def get_all_expenses():
    expenses = Expense.query.all()
    expenses_data = [{'id': expense.id, 'amount': expense.amount, 'description': expense.description,
                      'category': expense.category, 'date': expense.date} for expense in expenses]
    return jsonify(expenses_data)


@app.route('api/expenses/<int:id>', methods=['GET'])
def get_expense_by_id(id):
    expense = Expense.query.get(id)
    expense_data = {'id': expense.id, 'amount': expense.amount, 'description': expense.description,
                    'category': expense.category, 'date': expense.date}
    return jsonify(expense_data)


@app.route('api/expenses', methods=['POST'])
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


@app.route('api/expenses/<int:id>', methods=['PUT'])
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


@app.route('api/expenses/<int:id>', methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get(id)

    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully'})