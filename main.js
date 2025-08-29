const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const parser = require('iptv-playlist-parser');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      // It's recommended to keep contextIsolation true and nodeIntegration false.
      // We will use the preload script to expose necessary Node.js APIs securely.
      contextIsolation: true,
      nodeIntegration: false,
    }
  });

  mainWindow.loadFile('index.html');

  // Parse the M3U file and send it to the renderer process
  mainWindow.webContents.on('did-finish-load', () => {
    const playlistPath = path.join(__dirname, 'assets', 'playlist.m3u');
    const playlistContent = fs.readFileSync(playlistPath, 'utf8');
    const result = parser.parse(playlistContent);

    // Group channels by group-title
    const categories = result.items.reduce((acc, channel) => {
      const groupTitle = channel.group.title;
      if (!acc[groupTitle]) {
        acc[groupTitle] = [];
      }
      acc[groupTitle].push(channel);
      return acc;
    }, {});

    mainWindow.webContents.send('playlist-parsed', categories);
  });


  // Open the DevTools for debugging.
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
