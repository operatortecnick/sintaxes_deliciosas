// Browser functionality for Sintaxes Deliciosas
class SintaxesBrowser {
    constructor() {
        this.history = ['sintaxes://home'];
        this.currentIndex = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateNavigationButtons();
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('backBtn').addEventListener('click', () => this.goBack());
        document.getElementById('forwardBtn').addEventListener('click', () => this.goForward());
        document.getElementById('refreshBtn').addEventListener('click', () => this.refresh());
        document.getElementById('homeBtn').addEventListener('click', () => this.goHome());
        
        // URL input and go button
        document.getElementById('urlInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.navigate();
        });
        document.getElementById('goBtn').addEventListener('click', () => this.navigate());

        // Menu button
        document.getElementById('menuBtn').addEventListener('click', () => this.showMenu());
    }

    navigate() {
        const url = document.getElementById('urlInput').value.trim();
        if (!url) return;

        this.setStatus('Carregando...');
        this.showProgress();

        // Add to history
        this.currentIndex++;
        this.history = this.history.slice(0, this.currentIndex);
        this.history.push(url);
        this.updateNavigationButtons();

        // Process the URL
        setTimeout(() => {
            this.processUrl(url);
            this.hideProgress();
            this.setStatus('Pronto');
        }, 500);
    }

    processUrl(url) {
        const content = document.getElementById('webContent');
        
        if (url === 'sintaxes://home' || url === 'home') {
            this.loadHomePage();
        } else if (url.startsWith('code:')) {
            this.analyzeCode(url.substring(5));
        } else if (url.startsWith('example:')) {
            this.loadExample(url.substring(8));
        } else if (this.isValidUrl(url)) {
            this.loadExternalUrl(url);
        } else {
            // Treat as code to analyze
            this.analyzeCode(url);
        }
    }

    loadHomePage() {
        const content = document.getElementById('webContent');
        content.innerHTML = `
            <div class="welcome-page">
                <h1>🍯 Bem-vindo ao Navegador Sintaxes Deliciosas</h1>
                <p>Corretor supremo de programas, funções, aprimoramentos e sintaxes no geral</p>
                
                <div class="features">
                    <div class="feature-card">
                        <h3>📝 Análise de Código</h3>
                        <p>Cole seu código na barra de endereço com o prefixo "code:" para análise automática</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔍 Verificação de Sintaxe</h3>
                        <p>Detecta erros de sintaxe em múltiplas linguagens de programação</p>
                    </div>
                    <div class="feature-card">
                        <h3>✨ Sugestões de Melhoria</h3>
                        <p>Receba sugestões inteligentes para melhorar seu código</p>
                    </div>
                </div>

                <div class="quick-actions">
                    <h3>Ações Rápidas:</h3>
                    <button class="action-btn" onclick="loadExample('python')">Exemplo Python</button>
                    <button class="action-btn" onclick="loadExample('javascript')">Exemplo JavaScript</button>
                    <button class="action-btn" onclick="loadExample('html')">Exemplo HTML</button>
                </div>
            </div>
        `;
    }

    analyzeCode(code) {
        const content = document.getElementById('webContent');
        const language = this.detectLanguage(code);
        const issues = this.findIssues(code, language);
        const highlightedCode = this.highlightSyntax(code, language);

        content.innerHTML = `
            <div class="code-analysis">
                <h2>🔍 Análise de Código - ${language.toUpperCase()}</h2>
                
                <div class="code-container">
                    <div class="code-header">Código Original</div>
                    <div class="code-content">${highlightedCode}</div>
                </div>

                <div class="analysis-results">
                    <div class="analysis-header">Resultados da Análise (${issues.length} problema(s) encontrado(s))</div>
                    <div class="analysis-content">
                        ${issues.length === 0 ? 
                            '<p style="color: #28a745; font-weight: 600;">✅ Código parece estar em boa forma!</p>' :
                            issues.map(issue => `
                                <div class="issue ${issue.type}">
                                    <div class="issue-type">${this.getIssueIcon(issue.type)} ${issue.type.toUpperCase()}</div>
                                    <div class="issue-message">${issue.message}</div>
                                </div>
                            `).join('')
                        }
                    </div>
                </div>

                <div class="quick-actions">
                    <button class="action-btn" onclick="browser.goHome()">🏠 Voltar ao Início</button>
                    <button class="action-btn" onclick="browser.copyAnalysis()">📋 Copiar Análise</button>
                </div>
            </div>
        `;
    }

    detectLanguage(code) {
        // Simple language detection based on syntax patterns
        if (code.includes('def ') || code.includes('import ') || code.includes('print(')) return 'python';
        if (code.includes('function') || code.includes('const ') || code.includes('let ')) return 'javascript';
        if (code.includes('<html>') || code.includes('<!DOCTYPE')) return 'html';
        if (code.includes('#include') || code.includes('int main')) return 'c';
        if (code.includes('public class') || code.includes('System.out')) return 'java';
        if (code.includes('<?php') || code.includes('echo ')) return 'php';
        return 'text';
    }

    findIssues(code, language) {
        const issues = [];

        // Common syntax issues
        if (code.includes('    ') && code.includes('\t')) {
            issues.push({
                type: 'warning',
                message: 'Mistura de espaços e tabs para indentação detectada'
            });
        }

        if (code.split('\n').some(line => line.length > 100)) {
            issues.push({
                type: 'info',
                message: 'Algumas linhas são muito longas (>100 caracteres)'
            });
        }

        // Language-specific checks
        if (language === 'python') {
            if (!code.includes('def ') && code.length > 50) {
                issues.push({
                    type: 'info',
                    message: 'Considere organizar o código em funções'
                });
            }
            if (code.includes('print ')) {
                issues.push({
                    type: 'error',
                    message: 'Sintaxe print() incorreta - use print() ao invés de print'
                });
            }
        }

        if (language === 'javascript') {
            if (code.includes('var ')) {
                issues.push({
                    type: 'warning',
                    message: 'Considere usar let ou const ao invés de var'
                });
            }
            if (code.includes('==') && !code.includes('===')) {
                issues.push({
                    type: 'warning',
                    message: 'Use === para comparação estrita'
                });
            }
        }

        // Check for missing semicolons in JS-like languages
        if (['javascript', 'java', 'c'].includes(language)) {
            const lines = code.split('\n');
            lines.forEach((line, index) => {
                const trimmed = line.trim();
                if (trimmed && 
                    !trimmed.endsWith(';') && 
                    !trimmed.endsWith('{') && 
                    !trimmed.endsWith('}') &&
                    !trimmed.startsWith('//') &&
                    !trimmed.startsWith('/*') &&
                    !trimmed.includes('if ') &&
                    !trimmed.includes('for ') &&
                    !trimmed.includes('while ')) {
                    issues.push({
                        type: 'error',
                        message: `Linha ${index + 1}: Possível ponto e vírgula ausente`
                    });
                }
            });
        }

        return issues;
    }

    highlightSyntax(code, language) {
        let highlighted = code;
        
        // Basic syntax highlighting
        const keywords = {
            python: ['def', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 'class', 'return', 'try', 'except'],
            javascript: ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'class'],
            java: ['public', 'private', 'class', 'int', 'String', 'void', 'if', 'else', 'for', 'while', 'return'],
            c: ['int', 'char', 'float', 'double', 'if', 'else', 'for', 'while', 'return', 'include']
        };

        if (keywords[language]) {
            keywords[language].forEach(keyword => {
                const regex = new RegExp(`\\b${keyword}\\b`, 'g');
                highlighted = highlighted.replace(regex, `<span class="keyword">${keyword}</span>`);
            });
        }

        // Highlight strings
        highlighted = highlighted.replace(/(["'])([^"']*)\1/g, '<span class="string">$1$2$1</span>');
        
        // Highlight comments
        highlighted = highlighted.replace(/(\/\/.*$|#.*$)/gm, '<span class="comment">$1</span>');
        highlighted = highlighted.replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="comment">$1</span>');
        
        // Highlight numbers
        highlighted = highlighted.replace(/\b\d+\b/g, '<span class="number">$&</span>');

        return highlighted;
    }

    getIssueIcon(type) {
        switch(type) {
            case 'error': return '❌';
            case 'warning': return '⚠️';
            case 'info': return 'ℹ️';
            default: return '•';
        }
    }

    loadExample(type) {
        const examples = {
            python: `def calcular_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calcular_fibonacci(n-1) + calcular_fibonacci(n-2)

# Exemplo com problema de indentação
for i in range(10):
print(calcular_fibonacci(i))  # Indentação incorreta`,

            javascript: `function calcularFibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return calcularFibonacci(n-1) + calcularFibonacci(n-2);
    }
}

// Exemplo com problemas
var resultado = calcularFibonacci(10)  // Faltando ponto e vírgula
if (resultado == 55) {  // Deveria usar ===
    console.log("Correto!");
}`,

            html: `<!DOCTYPE html>
<html>
<head>
    <title>Exemplo HTML</title>
</head>
<body>
    <h1>Olá Mundo!</h1>
    <p>Este é um exemplo de HTML básico.</p>
    <div class="container">
        <button onclick="alert('Clicou!')">Clique aqui</button>
    </div>
</body>
</html>`
        };

        document.getElementById('urlInput').value = `code:${examples[type]}`;
        this.navigate();
    }

    loadExternalUrl(url) {
        const content = document.getElementById('webContent');
        content.innerHTML = `
            <div class="welcome-page">
                <h2>🌐 Navegação Externa</h2>
                <p>Este navegador é especializado em análise de código e sintaxe.</p>
                <p>Para navegar em sites externos, use um navegador web tradicional.</p>
                <p><strong>URL solicitada:</strong> ${url}</p>
                
                <div class="quick-actions">
                    <button class="action-btn" onclick="browser.goHome()">🏠 Voltar ao Início</button>
                </div>
            </div>
        `;
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    goBack() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            document.getElementById('urlInput').value = this.history[this.currentIndex];
            this.processUrl(this.history[this.currentIndex]);
            this.updateNavigationButtons();
        }
    }

    goForward() {
        if (this.currentIndex < this.history.length - 1) {
            this.currentIndex++;
            document.getElementById('urlInput').value = this.history[this.currentIndex];
            this.processUrl(this.history[this.currentIndex]);
            this.updateNavigationButtons();
        }
    }

    refresh() {
        this.processUrl(this.history[this.currentIndex]);
    }

    goHome() {
        document.getElementById('urlInput').value = 'sintaxes://home';
        this.navigate();
    }

    updateNavigationButtons() {
        document.getElementById('backBtn').disabled = this.currentIndex <= 0;
        document.getElementById('forwardBtn').disabled = this.currentIndex >= this.history.length - 1;
    }

    setStatus(text) {
        document.getElementById('statusText').textContent = text;
    }

    showProgress() {
        document.getElementById('progressBar').classList.add('loading');
    }

    hideProgress() {
        document.getElementById('progressBar').classList.remove('loading');
    }

    showMenu() {
        alert('🍯 Sintaxes Deliciosas Browser v1.0\n\nFuncionalidades:\n• Análise de código\n• Verificação de sintaxe\n• Sugestões de melhoria\n\nDicas:\n• Use "code:" antes do código\n• Experimente os exemplos\n• Cole código diretamente na barra');
    }

    copyAnalysis() {
        // Simple copy functionality
        const analysisText = document.querySelector('.analysis-content').textContent;
        navigator.clipboard.writeText(analysisText).then(() => {
            alert('Análise copiada para a área de transferência!');
        }).catch(() => {
            alert('Não foi possível copiar. Selecione e copie manualmente.');
        });
    }
}

// Global functions for onclick handlers
function loadExample(type) {
    browser.loadExample(type);
}

// Initialize browser when page loads
let browser;
document.addEventListener('DOMContentLoaded', () => {
    browser = new SintaxesBrowser();
});