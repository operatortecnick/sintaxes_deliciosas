const appContainer = document.getElementById('app-container');
let fullPlaylist = {};
let currentView = 'categories'; // Can be 'categories', 'channels', or 'player'
let previousView = 'categories';
let currentCategory = '';

// --- Navigation ---
function navigateTo(view, data) {
  // Stop the subtitle service if we're navigating away from the player
  if (currentView === 'player' && view !== 'player') {
    window.api.subtitles.stop();
  }

  previousView = currentView;
  currentView = view;
  appContainer.innerHTML = ''; // Clear the container

  const backButton = document.createElement('button');
  backButton.textContent = '<< Voltar';
  backButton.className = 'back-button';
  backButton.onclick = () => {
    if (currentView === 'player') {
      navigateTo('channels', currentCategory);
    } else if (currentView === 'channels') {
      navigateTo('categories', fullPlaylist);
    }
  };

  if (view !== 'categories') {
    appContainer.appendChild(backButton);
  }

  switch (view) {
    case 'categories':
      renderCategories(data);
      break;
    case 'channels':
      currentCategory = data;
      renderChannels(data);
      break;
    case 'player':
      renderPlayer(data);
      break;
  }
}

// --- Render Functions ---

function renderCategories(categories) {
  const categoriesList = document.createElement('ul');
  for (const categoryName in categories) {
    const listItem = document.createElement('li');
    listItem.textContent = `${categoryName} (${categories[categoryName].length} canais)`;
    listItem.onclick = () => navigateTo('channels', categoryName);
    categoriesList.appendChild(listItem);
  }
  appContainer.appendChild(categoriesList);
}

function renderChannels(categoryName) {
  const channels = fullPlaylist[categoryName];
  const channelsList = document.createElement('ul');
  channels.forEach(channel => {
    const listItem = document.createElement('li');
    listItem.textContent = channel.name;
    listItem.onclick = () => navigateTo('player', channel);
    channelsList.appendChild(listItem);
  });
  appContainer.appendChild(channelsList);
}

function renderPlayer(channel) {
  const videoContainer = document.createElement('div');
  videoContainer.className = 'video-container';

  const video = document.createElement('video');
  video.id = 'video-player';
  video.controls = true;
  video.autoplay = true;

  const subtitleContainer = document.createElement('div');
  subtitleContainer.className = 'subtitle-container';

  videoContainer.appendChild(video);
  videoContainer.appendChild(subtitleContainer);
  appContainer.appendChild(videoContainer);

  // Start the subtitle service
  window.api.subtitles.start();
  window.api.subtitles.on((subtitle) => {
    subtitleContainer.textContent = subtitle;
  });

  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(channel.url);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function () {
      video.play();
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = channel.url;
    video.addEventListener('loadedmetadata', function () {
      video.play();
    });
  }
}


// --- Initial Load ---
window.api.onPlaylistParsed((categories) => {
  console.log('Playlist data received from main process:', categories);
  fullPlaylist = categories;
  navigateTo('categories', fullPlaylist);
});
