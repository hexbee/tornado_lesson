from data.user_modules import User, session

# row = session.query(User).filter_by(username='demo').all()
# row = session.query(User).filter(User.username == 'demo').all()
# row = session.query(User).filter(User.username != 'demo').all()
# row = session.query(User).filter(User.username == 'demo')
# row = session.query(User).all()
row = session.query(User.username).filter(User.username != 'demo').all()

print row
