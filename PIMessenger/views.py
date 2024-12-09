from PIMessenger import app, db
from PIMessenger.models import Events, Accounts, Chats
from PIMessenger.utils import upload_items
from flask import render_template, jsonify, request

@app.route('/')
@app.route('/events')
def events():
    events_data = Events.query.all()
    chats_data = db.session.query(Chats.name, Chats.messenger_ID).all()
    return render_template('EventsPage.html', events_data=events_data, chats_data=chats_data)
    
@app.route('/accounts')
def accounts():
    accounts_data = Accounts.query.all()
    return render_template('AccountsPage.html', accounts_data=accounts_data)
    
@app.route('/chats')
def chats():
    chats_data = Chats.query.all()
    accounts_data = db.session.query(Accounts.username).all()
    return render_template('ChatsPage.html', chats_data=chats_data, accounts_data=accounts_data)
    

@app.route('/events/upload', methods=['POST'])
def upload_events():
    # TODO: add upload to table logic here
    if request.method != 'POST':
        return jsonify({'message': 'Error'}), 405

    upload_items(Events, 'items', 'id', db.session)
    return jsonify({'message': 'Success'}), 200
    
@app.route('/accounts/upload', methods=['POST'])
def upload_accounts():
    if request.method != 'POST':
        return jsonify({'message': 'Error'}), 405

    upload_items(Accounts, 'items', 'username', db.session)
    return jsonify({'message': 'Success'}), 200

@app.route('/chats/upload', methods=['POST'])
def upload_chats():
    if request.method != 'POST':
        return jsonify({'message': 'Error'}), 405

    upload_items(Chats, 'items', 'messenger_ID', db.session)
    return jsonify({'message': 'Success'}), 200

@app.route('/get/chatnames', methods=['GET'])
def get_chat_names():
    chats = db.session.query(Chats.messenger_ID, Chats.name).all()
    print(chats)
    chat_data = [{"id": chat.messenger_ID, "name": chat.name} for chat in chats]
    return jsonify({"chats": chat_data})

@app.route('/get/accountnames', methods=['GET'])
def get_account_names():
    accounts = db.session.query(Accounts.username).all()
    account_data = [{"name": account.username} for account in accounts]
    return jsonify({"accounts": account_data})
