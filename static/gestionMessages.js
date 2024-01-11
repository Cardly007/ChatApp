// Initialiser la connexion WebSocket (ajouter https pour connexion crypté)
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Cette fonction empêche le formulaire de se soumettre lors de l'appui sur la touche "Entrée"
document.getElementById('message').addEventListener('keypress', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendMessage(current_user, pic);
        updateTypingIndicator();
    }
});
// Définir une fonction pour envoyer le fichier sélectionné
// Ajoutez la fonction displayMessage pour afficher les fichiers multimédias dans le chat
function displayMessage(data) {
    var messagesContainer = document.getElementById('messages-container');
    var messageDiv = document.createElement('div');
    var messageContent = document.createElement('div');
    var messageHeader = document.createElement('div');
    var messageTime = document.createElement('div');

    messageHeader.classList.add('message-header');
    messageContent.classList.add('message-content');
    messageTime.classList.add('message-time');

    // Créer la div pour la photo de l'utilisateur
    var userPhotoContainer = document.createElement('div');
    userPhotoContainer.classList.add('user-photo-container');

    // Afficher la photo de l'utilisateur en miniature si disponible
    if (data.photo) {
        var userPhotoElement = document.createElement('img');
        userPhotoElement.src = data.photo;
        userPhotoElement.alt = 'User Photo';
        userPhotoElement.classList.add('user-photo');
        userPhotoContainer.appendChild(userPhotoElement);
    }

    // Afficher le nom d'utilisateur
    var usernameElement = document.createElement('strong');
    usernameElement.textContent = data.username;

    // Afficher le message
    messageContent.textContent = data.message;

    // Afficher l'heure en bas de la div avec une petite police
    messageTime.textContent = data.time_stamp;

    // Ajouter les éléments au messageHeader
    messageHeader.appendChild(userPhotoContainer);
    messageHeader.appendChild(usernameElement);
    messageHeader.appendChild(messageContent);
    messageHeader.appendChild(messageTime);

    // Ajouter le messageHeader à messageDiv
    messageDiv.appendChild(messageHeader);

    // Appliquer la classe CSS en fonction de l'expéditeur du message
    if (data.username === current_user) {
        messageDiv.classList.add('message', 'sent');
    } else {
        messageDiv.classList.add('message', 'received');
    }

    // Ajouter le messageDiv à messagesContainer
    messagesContainer.appendChild(messageDiv);
}


// Intégrer la fonction displayImage pour afficher les images dans le chat
function displayImage(data) {
    var messagesContainer = document.getElementById('messages-container');
    var messageDiv = document.createElement('div');
    var messageHeader = document.createElement('div');
    //var usernameElement = document.createElement('span'); // Changer en span pour rester en ligne
    var usernameElement = document.createElement('strong');
    var imageElement = document.createElement('img');
    var timeElement = document.createElement('span'); // Ajouter un élément pour l'heure

    // Ajouter la classe pour le style de l'image
    messageDiv.classList.add('image-message');

    // Afficher le nom d'utilisateur au-dessus de l'image
    usernameElement.textContent = data.username;
    messageHeader.appendChild(usernameElement);

    // Configurer l'élément de l'image
    imageElement.src =  data.image_url;
    imageElement.style.maxWidth = '100%'; // Ajuster la largeur maximale de l'image pour l'affichage
    imageElement.style.maxHeight = 'auto'; // Ajuster la hauteur maximale de l'image pour l'affichage

    // probleme de siposition echange pour l'instant
    if (data.username === current_user) {
        messageDiv.classList.add('image-message', 'received');
    } else {
        messageDiv.classList.add('image-message', 'sent');
    }

    // Ajouter l'élément de l'image et le nom d'utilisateur au conteneur du message
    messageDiv.appendChild(messageHeader);
    messageDiv.appendChild(imageElement);

    // Ajouter l'heure au bas du message
    timeElement.classList.add('message-time');
    timeElement.textContent = data.time_stamp;
    messageDiv.appendChild(timeElement);

    // Ajouter le messageDiv au conteneur de messages
    messagesContainer.appendChild(messageDiv);
}

// Cette fonction envoie un message via WebSocket
function sendMessage(username, image) {
    var message = document.getElementById('message').value;
    // Envoyer le message via WebSocket
    socket.emit('message', { message: message, username: username, photo: image });

    document.getElementById('message').value = '';
}


// Cette fonction envoie une image via WebSocket
function sendImage() {
    var imageInput = document.getElementById('image-input');
    var image = imageInput.files[0];

    // Utiliser FileReader pour lire le contenu du fichier
    var reader = new FileReader();

    // Lorsque la lecture est terminée
    reader.onloadend = function() {
        // Récupérer les données encodées en base64
        var base64data = reader.result.split(',')[1];

        // Envoyer les données via WebSocket
        socket.emit('image', { image: base64data, type: image.type });
    };

    // Lire le fichier en tant que URL de données
    reader.readAsDataURL(image);
}

// Cette fonction empêche le formulaire de se soumettre lors de l'appui sur la touche "Entrée"
// Appeler la fonction sendMessage avec le nom d'utilisateur actuel
document.getElementById('send-button').addEventListener('click', function() {
    sendMessage(current_user, pic);
    updateTypingIndicator();
});

// Écouter les messages du serveur via WebSocket
socket.on('message', function(data) {
        displayMessage(data);
});

// Écouter les images du serveur via WebSocket
socket.on('image', function(data) {
    displayImage(data);
});




// implemetation de la fonction est en train d'ecrire


// // Détecter le début de la saisie
// document.getElementById('message').addEventListener('input', () => {
//     socket.emit('typing', {'username': current_user});
// });

// // Détecter la fin de la saisie
// document.getElementById('message').addEventListener('blur', () => {
//     // Émettre un événement pour indiquer que l'utilisateur a arrêté de taper
//     socket.emit('typing', {'username': ''});
// });

// // Gérer les événements de saisie côté client
// socket.on('typing', (data) => {
//     const typingIndicator = document.getElementById('typing-indicator');

//     if (data.username !== '') {
//         typingIndicator.textContent = data.username + ' est en train d\'écrire...';
//     } else {
//         typingIndicator.textContent = '';
//     }
// });

const typingIndicator = document.getElementById('typing-indicator');
const messageInput = document.getElementById('message');

// Détecter le début de la saisie
messageInput.addEventListener('input', () => {
    updateTypingIndicator();
});

// Détecter la fin de la saisie
messageInput.addEventListener('blur', () => {
    socket.emit('typing', {'username': ''});
    updateTypingIndicator();
});

function updateTypingIndicator() {
    const message = messageInput.value.trim();
    if (message !== '') {
        socket.emit('typing', {'username': current_user});
    } else {
        socket.emit('typing', {'username': ''});
    }
}

// Gérer les événements de saisie côté client
socket.on('typing', (data) => {
    if (data.username !== '' && data.username !== current_user) {
        typingIndicator.textContent = data.username + ' est en train d\'écrire...';
    } else {
        typingIndicator.textContent = '';
    }
});


