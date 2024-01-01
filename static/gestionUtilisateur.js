        //const current_user = `{{ username }}`; // Déclarer une variable pour stocker le nom d'utilisateur actuel



// Récupérer l'historique des messages depuis le local storage
const messageHistory = JSON.parse(localStorage.getItem('messageHistory')) || [];


// Fonction pour se déconnecter
function logout() {
    // Supprimer le nom d'utilisateur du stockage local
    localStorage.removeItem('username');

    window.location.href = '/logout'; // Mettez à jour avec l'URL correcte de déconnexion
}


// Barre lateral 
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const chatContainer = document.getElementById('chat-container');
    const barre = document.getElementById('barre');

    if (sidebar.style.width === '250px') {
        // Si la barre latérale est ouverte, rétracter le contenu principal
        sidebar.style.width = '0';
        barre.style.width = '0';
        chatContainer.style.marginLeft = '0';
    } else {
        // Si la barre latérale est fermée, agrandir le contenu principal
        sidebar.style.width = '250px';
        barre.style.width = '100px';
        chatContainer.style.marginLeft = '350px';
    }
}
