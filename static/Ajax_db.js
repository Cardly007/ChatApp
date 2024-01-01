        //fonction pou gerer les popup         
        function openPopup() {
            document.getElementById('groupPopup').style.display = 'block';
        }

        function closePopup() {
            document.getElementById('groupPopup').style.display = 'none';
        }
        

        function loadChatRooms() {
            fetch('/get_chat_rooms')  // Endpoint à implémenter dans Flask pour récupérer les salles de discussion
                .then(response => response.json())
                .then(chatRooms => {
                    // Effacer la liste des salles de discussion existante
                    const chatRoomList = document.getElementById('chat-room-list');
                    chatRoomList.innerHTML = '';
        
                    // Ajouter chaque salle de discussion à la liste
                    chatRooms.forEach(chatRoom => {
                        const listItem = document.createElement('li');
                        listItem.textContent = chatRoom.room_name;
        
                        // Ajouter un gestionnaire d'événements pour charger les messages de la salle de discussion au clic
                        listItem.addEventListener('click', function () {
                            loadMessages(chatRoom.id);
                        });
        
                        chatRoomList.appendChild(listItem);
                    });
                });
        }


        // Fonction pour charger les messages d'une salle de discussion spécifique
        function loadMessages(roomId) {
            fetch(`/get_messages/${roomId}`)
                .then(response => response.json())
                .then(messages => {
                    // Effacer la liste des messages existante
                    messageList.innerHTML = '';

                    // Ajouter chaque message à la liste
                    messages.forEach(message => {
                        const listItem = document.createElement('li');
                        listItem.textContent = `${message.user.username}: ${message.content}`;
                        messageList.appendChild(listItem);
                    });
                });
        }







        //bon code 
        document.addEventListener("DOMContentLoaded", function () {
            var sectionButtons = document.querySelectorAll('#barre button');
            var sectionContent = document.getElementById('sidebar');

            // Fonction pour afficher le contenu de la section sélectionnée
            function showSectionContent(sectionId) {
            // Cacher le contenu actuel avec transition
            sectionContent.classList.add('hidden');

            // Attente de la fin de l'animation d'opacité avant de mettre à jour le contenu
            setTimeout(function () {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE) {
                        if (xhr.status === 200) {
                            // Mettre à jour le contenu de la section avec la réponse du serveur
                            sectionContent.innerHTML = ''; // Effacer le contenu actuel
                            sectionContent.insertAdjacentHTML('beforeend', xhr.responseText);

                            // Ajuster la largeur du contenu en fonction de la largeur de la Sidebar
                            var sidebarWidth = document.getElementById('sidebar').offsetWidth;
                            sectionContent.style.width = (sidebarWidth - 0) + 'px';

                            // Définir la largeur de la div collectée sur 100%
                            var collectedDiv = sectionContent.querySelector('.collected-div');
                            if (collectedDiv) {
                                collectedDiv.style.width = '100%';
                            }

                            // Limiter la hauteur du contenu à 250px
                            sectionContent.style.maxHeight = '100%';

                            // Remplir verticalement la div Sidebar
                            sectionContent.style.height = '100%';

                            sectionContent.classList.remove('hidden'); // Afficher le contenu avec transition
                        } else {
                            console.error('Erreur lors de la récupération du contenu de la section');
                        }
                    }
                };
                xhr.open('GET', '/get_content/' + sectionId, true);
                xhr.send();
            }, 300); // Le délai ici (300ms) doit correspondre à la durée de la transition dans le CSS
        }


            // Ajouter un gestionnaire de clic à chaque bouton de section
            sectionButtons.forEach(function (button) {
                button.addEventListener('click', function () {
                    // Obtenir l'identifiant de la section à partir de l'attribut data-section-id
                    var sectionId = button.getAttribute('data-section-id');

                    // Mettre en surbrillance le bouton cliqué et désélectionner les autres
                    sectionButtons.forEach(function (btn) {
                        btn.classList.remove('selected');
                    });
                    button.classList.add('selected');

                    // Afficher le contenu de la section
                    showSectionContent(sectionId);
                });
            });
        });

        

        // //fonction d'ajout de bouton 
        // // Récupérer l'élément de la barre
        // const barre = document.getElementById('barre');

        // // Boucle pour créer 8 boutons
        // for (let i = 1; i <= 8; i++) {
        //     const a = document.createElement('a');
        //     a.href = `#`;
        //     a.textContent = `Utilisateur ${i}`;
        //     a.addEventListener('click', () => handleUserClick(i)); // Ajoutez un gestionnaire de clic avec l'ID de l'utilisateur

        //     // Ajouter le bouton à la barre
        //     barre.appendChild(a);
        // }

        // // Fonction de gestion du clic d'utilisateur (peut être modifiée selon vos besoins)
        // function handleUserClick(userId) {
        //     console.log(`Utilisateur cliqué avec l'ID : ${userId}`);
        // }        
        
        
        // fonction pour rechercher le clients dans la sidebarre
        const searchInput = document.getElementById('searchInput');
        const searchResultsList = document.getElementById('searchResults');
        const sidebar = document.getElementById('sidebar');

        // Liste des utilisateurs déjà présents dans la sidebar
        const addedUsers = [];


        function handleUserClick(userId) {
            // Vérifier si l'utilisateur est déjà dans la sidebar
            if (!addedUsers.includes(userId)) {
                // Utiliser l'ID du client pour obtenir son nom et sa photo
                fetch(`/get_user_details/${userId}`)
                    .then(response => response.json())
                    .then(data => {
                        if ('error' in data) {
                            console.error(data.error);
                        } else {
                            // Ajouter l'utilisateur à la sidebar seulement s'il n'est pas déjà présent
                            if (!addedUsers.includes(userId)) {
                                addClickableUserDiv(data.username, userId, data.photo,data.est_en_ligne);
                            }
                        }
                    })
                    .catch(error => console.error(error));
            }

            // Masquer la liste des résultats après avoir traité le clic
            searchResultsList.style.display = 'none';
        }

        
        function addClickableUserDiv(username, userId, userPhoto, estEnLigne) {
            // Vérifier si l'utilisateur est déjà dans la sidebar
            if (!addedUsers.includes(userId)) {
                // Créer une nouvelle div cliquable avec le nom et la photo du client
                const userDiv = document.createElement('div');
                userDiv.classList.add('clickable-user');
        
                // Ajouter la miniature de la photo à la div
                const userPhotoMiniature = document.createElement('img');
                userPhotoMiniature.src = userPhoto;
                userPhotoMiniature.alt = `${username} Photo`;
        
                // Appliquer des styles CSS pour la taille et la forme de la miniature
                userPhotoMiniature.style.maxWidth = '50px'; // Ajustez la taille selon vos besoins
                userPhotoMiniature.style.borderRadius = '50%'; // Forme de cercle
                userPhotoMiniature.style.marginRight = '8px'; // Marge à droite du texte
        
                userDiv.appendChild(userPhotoMiniature);
        
                // Ajouter le nom de l'utilisateur à la div
                const usernameSpan = document.createElement('span');
                usernameSpan.textContent = username;
                userDiv.appendChild(usernameSpan);
        
                // Ajouter un point lumineux à la fin de la div en fonction du statut en ligne
                const statusDot = document.createElement('div');
                statusDot.classList.add('status-dot');
                if (estEnLigne === true) {
                    // En ligne (vert)
                    statusDot.style.backgroundColor = 'green';
                } else if (estEnLigne === false) {
                    // Hors ligne (rouge)
                    statusDot.style.backgroundColor = 'red';
                } else {
                    // Statut inconnu (bleu)
                    statusDot.style.backgroundColor = 'blue';
                }
                userDiv.appendChild(statusDot);
        
                // Ajouter des classes pour styliser
                userDiv.classList.add('clickable-user');
                usernameSpan.classList.add('username-style');
        
                // Ajouter un gestionnaire d'événements pour gérer le clic sur la div
                userDiv.addEventListener('click', function () {
                    // Ajouter ici le code pour gérer le clic sur le nom du client dans la sidebar
                    alert(`Clic sur ${username}`);
                });
        
                // Ajouter la div à la sidebar
                sidebar.appendChild(userDiv);
        
                // Ajouter l'ID de l'utilisateur à la liste des utilisateurs ajoutés
                addedUsers.push(userId);
            }
        }
        
        
        
        document.addEventListener('DOMContentLoaded', function () {
            let searchTimer;
            
            searchInput.addEventListener('input', function () {
                clearTimeout(searchTimer);
        
                const query = searchInput.value.trim();
                if (query.length === 0) {
                    searchResultsList.innerHTML = '';
                    searchResultsList.style.display = 'none';
                    return;
                }
        
                searchTimer = setTimeout(() => {
                    fetch(`/search_users/${query}`)
                        .then(response => response.json())
                        .then(results => {
                            searchResultsList.innerHTML = results.map(user => {
                                const highlightedUsername = user.username.replace(new RegExp(query, 'ig'), match => `<span style="background-color: green">${match}</span>`);
                                return `<li data-user-id="${user.id}" data-user-photo="${user.photo}" onclick="handleUserClick(${user.id})">${user.id}: ${highlightedUsername}</li>`;
                            }).join('');                            
        
                            // Affichez la liste des résultats sous la barre de recherche
                            searchResultsList.style.display = 'block';
                        });
                }, 300);
            });


            // Ajouter un gestionnaire d'événements pour les boutons de chargement des groupes
            const loadGroupButtons = document.querySelectorAll('.load-group-button');
            loadGroupButtons.forEach(button => {
                button.addEventListener('click', function () {
                    const roomId = button.getAttribute('data-room-id');
                    loadMessages(roomId);
                });
            });

            // Ajouter un gestionnaire d'événements pour le formulaire de création de groupe
            const createGroupForm = document.getElementById('create-group-form');
            createGroupForm.addEventListener('submit', function (event) {
                event.preventDefault();

                // Récupérer les détails du nouveau groupe depuis le formulaire
                const groupName = document.getElementById('group-name-input').value;

                // Envoyer la demande de création de groupe au serveur
                fetch('/create_group', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `group_name=${encodeURIComponent(groupName)}`,
                })
                .then(response => response.json())
                .then(data => {
                    // Rafraîchir la liste des boutons de chargement des groupes
                    loadChatRooms();
                });
            });


            // Gérer l'envoi de nouveaux messages
            messageForm.addEventListener('submit', function (event) {
                event.preventDefault();

                const messageContent = messageInput.value;

                // Envoyer le message au serveur (vous pouvez utiliser fetch ou une bibliothèque comme Axios)
                fetch(`/send_messago/${roomId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message_content=${encodeURIComponent(messageContent)}`,
                })
                .then(response => response.json())
                .then(data => {
                    // Si le message est envoyé avec succès, rafraîchir la liste des messages
                    loadMessages(roomId);
                });

                // Effacer le champ de saisie après l'envoi
                messageInput.value = '';
            });

            
            loadChatRooms(); 
        });


        //theme sombre 
        function toggleTheme() {
            // Sélectionnez le body
            var body = document.body;
    
            // Ajoutez ou supprimez la classe dark-theme
            body.classList.toggle('dark-theme');
    
            // Vous pouvez également stocker le thème dans le stockage local pour le conserver après le rafraîchissement de la page
            if (body.classList.contains('dark-theme')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.setItem('theme', 'light');
            }
        }

        // Chargement initial du thème à partir du stockage local
        document.addEventListener('DOMContentLoaded', function () {
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-theme');
            }
        });
        