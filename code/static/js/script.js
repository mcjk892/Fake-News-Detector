document.addEventListener('DOMContentLoaded', () => {
    const newsInput = document.getElementById('newsInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const resetBtn = document.getElementById('resetBtn');
    const historyList = document.getElementById('historyList');
    const historyModal = document.getElementById('historyModal');
    const historyToggle = document.getElementById('historyToggle');
    const closeModal = document.getElementById('closeModal');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    
    // History Modal Logic
    historyToggle.addEventListener('click', () => {
        loadHistory();
        historyModal.classList.remove('hidden');
    });

    closeModal.addEventListener('click', () => {
        historyModal.classList.add('hidden');
    });

    window.addEventListener('click', (e) => {
        if (e.target === historyModal) historyModal.classList.add('hidden');
    });

    clearHistoryBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear your entire search history?')) {
            try {
                const response = await fetch('/history/delete', { method: 'POST' });
                if (response.ok) {
                    loadHistory();
                }
            } catch (err) {
                console.error('Failed to delete history', err);
            }
        }
    });
    
    // Result elements
    const verdictBadge = document.getElementById('verdictBadge');
    const explanation = document.getElementById('explanation');
    const rightAnswer = document.getElementById('rightAnswer');

    // Enter to Search
    newsInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            analyzeBtn.click();
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const input = newsInput.value.trim();
        if (!input) {
            alert('Please enter some text or a link to analyze.');
            return;
        }

        // Show loading state
        showSection('loading');
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            displayResult(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong during analysis. Please try again.');
            showSection('input');
        }
    });

    resetBtn.addEventListener('click', () => {
        newsInput.value = '';
        newsInput.focus();
        // Hide result and loading specifically
        loading.classList.add('hidden');
        result.classList.add('hidden');
        document.querySelector('.input-section').classList.remove('hidden');
    });

    async function loadHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();
            
            if (data.length === 0) return;

            historyList.innerHTML = '';
            data.forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                
                const text = document.createElement('span');
                text.className = 'history-text';
                text.textContent = item.input_text;
                
                const verdict = document.createElement('span');
                const vClass = item.verdict.toLowerCase().includes('true') ? 'true' : 
                              (item.verdict.toLowerCase().includes('false') ? 'false' : 'uncertain');
                verdict.className = `history-verdict ${vClass}`;
                verdict.textContent = item.verdict;
                
                div.appendChild(text);
                div.appendChild(verdict);
                
                // Allow clicking history item to re-search
                div.style.cursor = 'pointer';
                div.onclick = () => {
                    newsInput.value = item.input_text;
                    analyzeBtn.click();
                };
                
                historyList.appendChild(div);
            });
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    function showSection(section) {
        // Reset dynamic sections
        loading.classList.add('hidden');
        result.classList.add('hidden');

        if (section === 'loading') {
            loading.classList.remove('hidden');
        } else if (section === 'result') {
            result.classList.remove('hidden');
        }
    }

    function displayResult(data) {
        // Set verdict badge
        verdictBadge.textContent = data.verdict;
        verdictBadge.className = 'badge ' + data.verdict.toLowerCase();
        
        // Show explanation and truth
        explanation.textContent = data.explanation;
        rightAnswer.textContent = data.right_answer;

        showSection('result');
    }
});
