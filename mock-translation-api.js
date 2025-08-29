/**
 * This is a mock/simulation of a real-time transcription and translation service.
 * In a real application, this module would be replaced with actual API calls to
 * services like Google Cloud Speech-to-Text and Google Translate API.
 *
 * This mock simulates receiving audio data and periodically emitting a translated subtitle.
 */
class MockTranslationService {
  constructor() {
    this.intervalId = null;
    this.subtitleCallback = null;

    this.mockSentences = [
      { en: "Hello and welcome to the live broadcast.", pt: "Olá e bem-vindo à transmissão ao vivo." },
      { en: "In today's news, we have some interesting developments.", pt: "Nas notícias de hoje, temos alguns desenvolvimentos interessantes." },
      { en: "The weather forecast shows clear skies for the weekend.", pt: "A previsão do tempo mostra céu claro para o fim de semana." },
      { en: "Our top story tonight is about the new technology.", pt: "Nossa principal história esta noite é sobre a nova tecnologia." },
      { en: "And now for a look at sports.", pt: "E agora, vamos ver os esportes." },
    ];
    this.currentIndex = 0;
  }

  // The renderer calls this function to register a callback.
  // The callback will be invoked with a new subtitle when it's "ready".
  onSubtitle(callback) {
    this.subtitleCallback = callback;
  }

  // This simulates the start of the audio stream processing.
  start() {
    if (this.intervalId) {
      this.stop();
    }

    this.intervalId = setInterval(() => {
      if (this.subtitleCallback) {
        // "Transcribe" and "Translate"
        const sentence = this.mockSentences[this.currentIndex];
        this.subtitleCallback(sentence.pt); // Send the Portuguese sentence

        this.currentIndex = (this.currentIndex + 1) % this.mockSentences.length;
      }
    }, 5000); // Emit a new subtitle every 5 seconds.
  }

  // This simulates the end of the audio stream processing.
  stop() {
    clearInterval(this.intervalId);
    this.intervalId = null;
    this.currentIndex = 0;
  }
}

// Export a single instance of the service
module.exports = new MockTranslationService();
