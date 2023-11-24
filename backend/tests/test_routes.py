from datetime import date
from app import app, db
from app.models import User, Expense
import pytest
from flask_login import login_user

# User route tests


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_get_all_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200

    data = response.json

    assert isinstance(data, list)
    assert len(data) == 0


def test_get_user_by_id(client):
    with app.app_context():
        user = User('user123', 'pass123')
        db.session.add(user)
        db.session.commit()

        response = client.get(f'/api/users/{user.id}')
        assert response.status_code == 200

        data = response.json

        assert data['id'] == user.id
        assert data['username'] == 'user123'


def test_add_user(client):
    with app.app_context():
        user_data = {'username': 'testuser', 'password': 'testpassword'}

        response = client.post('/api/users', json=user_data)
        assert response.status_code == 200

        data = response.json
        assert data['message'] == 'User added successfully'

        user = User.query.filter_by(username='testuser').first()
        assert user.username == 'testuser'
        assert user.check_password('testpassword')


def test_update_user(client):
    with app.app_context():
        user = User('testuser', 'testpassword')
        db.session.add(user)
        db.session.commit()

        updated_data = {'username': 'updateduser',
                        'password': 'updatedpassword'}
        response = client.put(f'/api/users/{user.id}', json=updated_data)

        assert response.status_code == 200

        data = response.json
        assert data['message'] == 'User updated successfully'

        updated_user = db.session.get(User, user.id)
        assert updated_user.username == 'updateduser'
        assert updated_user.check_password('updatedpassword')


def test_delete_user(client):
    with app.app_context():
        user = User('testuser', 'testpassword')
        db.session.add(user)
        db.session.commit()

        response = client.delete(f'/api/users/{user.id}')

        assert response.status_code == 200
        data = response.json
        assert data['message'] == 'User deleted successfully'

        deleted_user = db.session.get(User, user.id)
        assert deleted_user is None

# Expense route tests


def test_get_all_expenses(client):
    with app.test_request_context():
        testing_user = User('testuser', 'testpassword')
        db.session.add(testing_user)
        db.session.commit()
        login_user(testing_user)

        response = client.get('/api/expenses')
        assert response.status_code == 200

        data = response.json

        assert isinstance(data, list)
        assert len(data) == 0


def test_get_expense_by_id(client):
    with app.test_request_context():
        with app.app_context():
            testing_user = User('testuser', 'testpassword')
            db.session.add(testing_user)
            db.session.commit()
            login_user(testing_user)

            expense = Expense(100, 'test expense', 'Test', '2023-11-23')
            db.session.add(expense)
            db.session.commit()

            response = client.get(f'/api/expenses/{expense.id}')
            assert response.status_code == 200

            data = response.json

            assert data['id'] == expense.id
            assert data['amount'] == 100
            assert data['description'] == 'test expense'
            assert data['category'] == 'Test'
            assert data['date'] == '2023-11-23'


def test_add_expense(client):
    with app.test_request_context():
        with app.app_context():
            testing_user = User('testuser', 'testpassword')
            db.session.add(testing_user)
            db.session.commit()
            login_user(testing_user)

            expense_data = {'amount': 100, 'description': 'test expense',
                            'category': 'Test', 'date': '2023-11-23'}

            response = client.post('/api/expenses', json=expense_data)
            assert response.status_code == 200

            data = response.json
            assert data['message'] == 'Expense added successfully'

            expense = Expense.query.filter_by(
                amount=100, description='test expense', category='Test', date='2023-11-23').first()
            assert expense.amount == 100
            assert expense.description == 'test expense'
            assert expense.category == 'Test'
            assert expense.date == '2023-11-23'


def test_update_expense(client):
    with app.test_request_context():
        with app.app_context():
            testing_user = User('testuser', 'testpassword')
            db.session.add(testing_user)
            db.session.commit()
            login_user(testing_user)

            expense = Expense(100, 'test expense', 'Test', '2023-11-23')
            db.session.add(expense)
            db.session.commit()

            updated_data = {'amount': 200, 'description': 'updated expense',
                            'category': 'Updated', 'date': '2023-11-23'}
            response = client.put(
                f'/api/expenses/{expense.id}', json=updated_data)

            assert response.status_code == 200

            data = response.json
            assert data['message'] == 'Expense updated successfully'

            updated_expense = db.session.get(Expense, expense.id)
            assert updated_expense.amount == 200
            assert updated_expense.description == 'updated expense'
            assert updated_expense.category == 'Updated'


def test_delete_user(client):
    with app.test_request_context():
        with app.app_context():
            testing_user = User('testuser', 'testpassword')
            db.session.add(testing_user)
            db.session.commit()
            login_user(testing_user)

            expense = Expense(100, 'test expense', 'Test', '2023-11-23')
            db.session.add(expense)
            db.session.commit()

            response = client.delete(f'/api/expenses/{expense.id}')

            assert response.status_code == 200
            data = response.json
            assert data['message'] == 'Expense deleted successfully'

            deleted_expense = db.session.get(Expense, expense.id)
            assert deleted_expense is None


# Authentication route tests

def test_register(client):
    # Registering new user
    response = client.post(
        '/api/register', json={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 201

    data = response.json
    assert data['message'] == 'Registration successful'

    # Registering with an existing username
    response = client.post(
        '/api/register', json={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 400

    data = response.json
    assert data['message'] == 'Username already exists. Choose another one'


def test_login(client):
    with app.app_context():
        user = User('testuser', 'testpassword')
        db.session.add(user)
        db.session.commit()

        response = client.post(
            '/api/login', json={'username': 'testuser', 'password': 'testpassword'})
        assert response.status_code == 200

        data = response.json
        assert data['message'] == "Login successful"


def test_logout(client):
    with app.test_request_context():
        with app.app_context():
            testing_user = User('testuser', 'testpassword')
            db.session.add(testing_user)
            db.session.commit()
            login_user(testing_user)

            response = client.post('/api/logout')
            assert response.status_code == 200

            data = response.json

            assert data['message'] == "Logout successful"
