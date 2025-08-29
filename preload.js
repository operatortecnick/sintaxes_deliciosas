const { contextBridge, ipcRenderer } = require('electron');
const mockTranslationService = require('./mock-translation-api');

// Expose a safe, limited API to the renderer process.
contextBridge.exposeInMainWorld('api', {
  // Allows the renderer to receive data from the main process.
  onPlaylistParsed: (callback) => ipcRenderer.on('playlist-parsed', (event, ...args) => callback(...args)),

  // Expose the mock translation service methods
  subtitles: {
    on: (callback) => mockTranslationService.onSubtitle(callback),
    start: () => mockTranslationService.start(),
    stop: () => mockTranslationService.stop(),
  }
});
