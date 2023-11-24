from app.models import User, Expense


def test_create_user():
    user = User('testuser', 'testpassword')

    assert user.username == 'testuser'
    assert user.check_password('testpassword')


def test_check_password():
    user = User('testuser', 'testpassword')

    assert user.check_password('testpassword')
    assert not user.check_password('wrong')


def test_set_password():
    user = User('testuser', 'testpassword')

    user.set_password("newpassword")

    assert user.check_password('newpassword')


def test_user_repr():
    user = User('testuser', 'testpassword')

    assert user.__repr__() == f'<User(id={user.id}, username=testuser)>'


def test_create_expense():
    expense = Expense(100, 'test expense', 'Food', '2023-11-23')

    assert expense.amount == 100
    assert expense.description == 'test expense'
    assert expense.category == 'Food'
    assert expense.date == '2023-11-23'


def test_expense_repr():
    expense = Expense(100, 'test expense', 'Food', '2023-11-23')

    assert expense.__repr__(
    ) == f"<Expense(id={expense.id}, amount=100, description=test expense, category=Food, date=2023-11-23)>"
