from user_modules import User, session


def add_user():
    session.add(User(username='user_a', password='aaa123'))
    # session.add_all(
    #     [
    #         User(username='user_b', password='bbb123'),
    #         User(username='user_c', password='ccc123')
    #     ]
    # )
    session.commit()


def search_user():
    # row = session.query(User).all()
    # print row
    # row = session.query(User).filter_by(id=1).all()
    # print row
    row = session.query(User).filter(User.username=='user_c').all()
    print row[0].locked


def update_user():
    row = session.query(User).filter_by(username='user_c').update({User.password: 'CCC123'})
    session.commit()


def delete_user():
    row = session.query(User).filter_by(username='user_c')[0]
    print row
    session.delete(row)
    session.commit()


if __name__ == '__main__':
    add_user()
    # search_user()
    # update_user()
    # delete_user()
    print User.all()
    # print User.by_id(1)
    # print User.by_name('user_c')
