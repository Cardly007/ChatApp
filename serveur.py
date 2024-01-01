                                                    # Fichier du serveur Flask 


from flask import Flask, render_template, render_template_string,request, redirect, url_for, jsonify, session, send_from_directory, flash
from flask_socketio import SocketIO, send
from flask_login import current_user
from flask_wtf import FlaskForm
from time import localtime, strftime
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import os
import base64


# Configuration de l'application Flask
app = Flask(__name__)
app.secret_key = 'Real_Madrid_better_than_PSG'  # Assurez-vous d'avoir une clé secrète unique pour votre application
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")  # Ajoutez cors_allowed_origins si nécessaire

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitez la taille maximale du fichier (ici, 16 Mo)
app.config['UPLOAD_FOLDER'] = '/Users/cardly/Downloads/PROJET/upload'  #remplacez le par l'emplacement de votre fichier upload
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'clients.db')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


db = SQLAlchemy(app)
migrate = Migrate(app, db) # initialisation d'une instance de migration pour l'application Flask

'''
creation de la BD
flask db init  # Initialisez les migrations
flask db migrate -m "Initial migration."  # Créez une migration
flask db upgrade  # Appliquez la migration pour créer la base de données

'''


# mise en place d'une authentification administrateur pour pourvoir acceder au donne des clients 
# Configuration de Flask-BasicAuth
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'IMPOSSIBLE_IS_NOTHING'
basic_auth = BasicAuth(app)




# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Config des tables 
# Classe User pour Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    photo_profile = db.Column(db.String(255))  # Chemin ou lien vers la photo de profil
    bio = db.Column(db.Text)  # Champ pour la biographie de l'utilisateur



#exemple de modele de table 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Modèle SQLAlchemy pour stocker le code HTML des sections
class HtmlCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    icon_url = db.Column(db.String(255))

# Modèle SQLAlchemy pour stocker les messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salle_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_et_heure = db.Column(db.DateTime, default=datetime.utcnow)
    reponse_a = db.Column(db.Integer, db.ForeignKey('message.id'))  # Nouvelle colonne pour stocker l'ID du message auquel on répond

# Modèle SQLAlchemy pour stocker les fichiers associés aux messages
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    chemin_file = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)

# Modèle SQLAlchemy pour stocker les messages privés
class PrivateMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_et_heure = db.Column(db.DateTime, default=datetime.utcnow)

# Modèle SQLAlchemy pour stocker le statut en ligne
class OnlineStatus(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    Est_en_line = db.Column(db.Boolean, default=False)
    last_online_at = db.Column(db.DateTime)

online_status = db.relationship('OnlineStatus', backref='user', uselist=False)

# Mise à jour de la table des salles de discussion pour inclure une clé étrangère
class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat_room', lazy=True)




# interface admin 
admin = Admin(app, name='Admin', template_mode='bootstrap3')
# Ajoutez votre modèle à l'interface d'administration
admin.add_view(ModelView(HtmlCode, db.session))
admin.add_view(ModelView(Message, db.session))
admin.add_view(ModelView(File, db.session))
admin.add_view(ModelView(PrivateMessage, db.session))
admin.add_view(ModelView(OnlineStatus, db.session))
admin.add_view(ModelView(ChatRoom, db.session))
admin.add_view(ModelView(User, db.session))






# GESTION DE L'AUTHETIFICATION 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Définition du formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=80,)])
    submit = SubmitField('Se connecter')

# Définition du formulaire d'inscription
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirmer le mot de passe',validators=[InputRequired(), Length(min=8, max=80),EqualTo('password', message='Les mots de passe doivent correspondre')])
    submit = SubmitField('S\'inscrire')


# Route pour la page d'acceuil
@app.route('/')
def home():
    message = request.args.get('message') # Récupérer le message de la requête s'il y en a 
    if message:
        return render_template('h2.html', message=message)
    return render_template('h2.html')



# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            user_status = OnlineStatus.query.filter_by(user_id=user.id).first()
            if user_status:
                # Mettez à jour le statut en ligne de l'utilisateur
                user_status.Est_en_line = True
                db.session.commit()
            return redirect(url_for('index'))
        else:
            error_message = 'Identifiant ou mot de passe incorrect'
            return render_template('l2.html', form=login_form, error_message=error_message)
    return render_template('l2.html', form=login_form)

# Route où l'on est redirigé apres la connexion 
@app.route('/index')
@login_required
def index():
    sections = HtmlCode.query.all()
    chat_rooms = ChatRoom.query.all()
    return render_template('side2.html', username = current_user.username,sections=sections,user = current_user, chat_rooms=chat_rooms)

# Ajoutez cette nouvelle route à votre fichier app.py
@app.route('/get_content/<section_id>', methods=['GET'])
def get_content(section_id):
    section = HtmlCode.query.filter_by(section_id=section_id).first()
    if section:
        user = User.query.get(current_user.id)
        rendered_content = render_template_string(section.content, user=user)
        return rendered_content
    else:
        return 'Section non trouvée', 404





# Route pour la page de profil
@app.route('/profile', methods=['POST'])
def profile():
    try:
        # Récupération des données du formulaire
        email = request.form.get('email')
        bio = request.form.get('bio')
        # phone = request.form.get('telephone')
        photo_profile = request.files['photo_profile'] if 'photo_profile' in request.files else None

        # Enregistrement des données dans la base de données
        user = User.query.filter_by(username=current_user.username).first()  # Remplacez par l'utilisateur actuel
        user.email = email
        user.bio = bio
        # user.telephone = phone

        # Gestion de la photo de profil
        if photo_profile:
            # Sauvegarde de la photo dans le dossier 'static'
            photo_path = f'static/{photo_profile.filename}'
            photo_profile.save(photo_path)
            user.photo_profile = photo_path

        db.session.commit()
        flash('Profil mis à jour avec succès', 'success')
        return redirect(url_for('index'))
        # return get_content(3)

    except Exception as e:
        print(e)
        flash('Une erreur s\'est produite lors de la mise à jour du profil', 'danger')
        return redirect(url_for('index'))
        # return get_content(3)






#route pour aller vers la bue admininstrateur 
@app.route('/admin')
def admin():
    return redirect(url_for('admin.index'))

# Route pour la déconnexion de l'utilisateur
@app.route('/logout')
@login_required
def logout():
    # Mettez à jour le statut en ligne de l'utilisateur à False et l'heure de déconnexion
    user_status = OnlineStatus.query.filter_by(user_id=current_user.id).first()

    if user_status:
        user_status.Est_en_line = False
        user_status.last_online_at = datetime.utcnow()
        db.session.commit()

    logout_user()
    return redirect(url_for('home'))

# Route pour l'inscription de l'utilisateur   
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        
        # Créer un nouvel utilisateur
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Ajouter une photo de profil par défaut
        default_profile_path = 'static/default-avatar-profile-icon-social-600nw-1677509740.webp'
        new_user.photo_profile = default_profile_path
        db.session.commit()

        # Récupérer l'ID de l'utilisateur nouvellement créé
        user_id = new_user.id

        # Insérer l'ID dans la table OnlineStatus
        new_online_status = OnlineStatus(user_id=user_id)
        db.session.add(new_online_status)
        db.session.commit()

        return redirect(url_for('home', message='Nouvel utilisateur créé ! Connectez-vous maintenant'))  # Redirection vers la page d'accueil avec un message

    return render_template('r2.html', form=form) 
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
#         new_user = User(username=form.username.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('home', message='Nouvel utilisateur créé ! Connectez vous mmaintenant'))  # Redirection vers la page d'accueil avec un message
#     return render_template('r2.html', form=form)


# Route pour supprimer un client de la base de donnee 
@app.route('/delete_client/<int:user_id>', methods=['POST'])
def delete_client(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('clients'))




# Route pour la page clients securise avec un systeme d'authetification admin 
@app.route('/clients')
@basic_auth.required #  protégée par le décorateur @basic_auth.required, ce qui signifie que seuls les administrateurs  pourront accéder à cette page. 
def clients():
    username = request.authorization.username
    password = request.authorization.password

    if not check_credentials(username, password):
        return render_template('unauthorized.html'), 401

    all_users = User.query.all()
    return render_template('dataClient.html', users=all_users)


def check_credentials(username, password):
    if username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']:
        return True
    else:
        return False


#@basic_auth.error_handler  en cas de donne admin incorrect redirection vers une page d'erreur 
def unauthorized():
    return render_template('unauthorized.html'), 401






# GESTION DES MESSAGES 



# Dans la route send_message
@app.route('/send_message', methods=['POST'])
@login_required #  protégée par le décorateur @login_required, ce qui signifie que seuls les utilisateurs connectés pourront accéder à cette page. 
def send_message():
    if request.method == 'POST':
        message = request.json['message']

        username = current_user.username 
        full_message = f"{username}: {message}"  # Associe le message au nom de l'utilisateur
        #client_socket.sendall(full_message.encode())

        # Ajoutez la photo de profil de l'utilisateur
        user_photo = current_user.photo_profile

        socketio.emit('message', {'message': msg['message'], 'username': msg['username'], 'time_stamp': strftime('%I:%M%p', localtime())}, broadcast=True)

        return jsonify({'status': 'success'})

# Dans la fonction pour la gestion des message  
@socketio.on('message')
def handle_message(msg):
    print('Message:', str(msg))
    print('photo:', msg.get('photo'))  # Utilisez .get pour éviter KeyError si la clé est absente
    send({'message': msg['message'], 'username': msg['username'], 'photo': msg.get('photo'), 'time_stamp': strftime('%I:%M%p', localtime())}, broadcast=True)


@socketio.on('image')
def handle_image(image_data):

    image = image_data['image']  # Récupérez les données de l'image à partir de image_data
    username = current_user.username
    print(f'{username} a envoyé une image.')

     # Assurez-vous que le répertoire d'upload existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Par exemple, vous pouvez enregistrer l'image dans un répertoire spécifique avec un nom de fichier unique
    image_filename = f"{username}_{strftime('%Y%m%d%H%M%S', localtime())}.png"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

    with open(image_path, "wb") as image_file:
        image_file.write(base64.b64decode(image))


    image_url = url_for('uploaded_file', filename=image_filename)
    socketio.emit('image', {'image_url': image_url, 'username': username, 'time_stamp': strftime('%I:%M%p', localtime())})


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Gérer le téléchargement du fichier
@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected image'})

    if image and allowed_image(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('uploaded_file', filename=filename)
        return jsonify({'message': 'Image uploaded successfully', 'image_url': image_url})
    else:
        return jsonify({'error': 'Image type not allowed'})


# Route pour servir les images téléchargées
@app.route('/images/<filename>')
@login_required
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Vérifiez si l'extension du fichier est autorisée
def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

#Route pour la fonction de recherche des clients 
@app.route('/search_users/<search_query>')
def search_users(search_query):
    results = perform_user_search(search_query)
    return jsonify(results)

def perform_user_search(query):
    # Recherche dans la base de données avec SQLAlchemy
    users = User.query.filter((User.id.like(f'%{query}%')) | (User.username.ilike(f'%{query}%'))).all()
    
    # Convertit les résultats en un format JSON
    results = [{'id': user.id, 'username': user.username} for user in users]
    
    return results

# Endpoint pour obtenir le nom d'utilisateur
@app.route('/api/get-username')
def get_username():
    # Ajoutez ici la logique pour récupérer le nom d'utilisateur depuis la base de données
    # Remplacez 'john_doe' par le véritable nom d'utilisateur obtenu depuis la base de données
    username_from_database = current_user.username
    
    return jsonify({'username': username_from_database})

# route pour obtenir la photo dans le repertoir static
# @app.route('/static/<filename>')
# def serve_static(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ajoutez cette route pour obtenire les infos sur les utilisateurs 
@app.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if user:
        # Récupérer le statut en ligne de l'utilisateur
        user_status = OnlineStatus.query.filter_by(user_id=user.id).first()

        # Construire l'URL de la photo de l'utilisateur
        if user.photo_profile:
            photo_url = user.photo_profile 
        else:
            photo_url = None
        
        if user_status:
            est_en_ligne = user_status.Est_en_line
        else:
            est_en_ligne = None  # Utilisez None (ou null en JavaScript) pour indiquer l'absence de statut en ligne


        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'photo': photo_url,
            'est_en_ligne': est_en_ligne  # Ajouter le statut en ligne à la réponse JSON
        })
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404


'''
# Gestion des clients en ligne 
online_users = set()

@socketio.on('connect')
def handle_connect():
    online_users.add(current_user.username)
    print(f"Utilisateur connecté : {current_user.username}")
    update_online_users()

@socketio.on('disconnect')
def handle_disconnect():
    online_users.discard(current_user.username)
    print(f"Utilisateur déconnecté : {current_user.username}")
    update_online_users()

def update_online_users():
    # Émettez la liste des utilisateurs connectés à tous les clients
    socketio.emit('update_users', {'online_users': list(online_users)}, room=current_user.sid)
'''

# route manipulation de la base de donnees avec les messages chat


# Votre point de terminaison pour créer un nouveau groupe
@app.route('/create_group', methods=['POST'])
def create_group():
    try:
        group_name = request.form.get('group_name')

        # Vérifier si le groupe existe déjà
        existing_group = ChatRoom.query.filter_by(room_name=group_name).first()
        if existing_group:
            return jsonify({'error': 'Le groupe existe déjà.'}), 400

        # Créer le nouveau groupe
        new_group = ChatRoom(room_name=group_name)
        db.session.add(new_group)
        db.session.commit()

        return jsonify({'message': 'Nouveau groupe créé avec succès.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Votre point de terminaison pour obtenir la liste des groupes (utilisé pour rafraîchir les boutons de chargement des groupes)
@app.route('/get_chat_rooms', methods=['GET'])
def get_chat_rooms():
    try:
        chat_rooms = ChatRoom.query.all()
        data = [{'id': room.id, 'room_name': room.room_name} for room in chat_rooms]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# route pour envoyer les messges dans un groupe 
@app.route('/send_messago/<int:room_id>', methods=['POST'])
def send_messago(room_id):
    # Récupérer l'utilisateur actuel (vous devez gérer l'authentification)
    #current_user = get_current_user()  # Fonction à implémenter

    # Récupérer le contenu du message depuis la requête POST
    message_content = request.form.get('message_content')

    # Créer un nouveau message
    new_message = Message(salle_id=room_id, user_id=current_user.id, content=message_content)

    # Ajouter le message à la base de données
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('chat_room', room_id=room_id))


if __name__ == '__main__':
    socketio.run(app, debug=True)



