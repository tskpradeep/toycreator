<script>
    // 1. Maintain the Triple Split Layout
    Split(['#left-stack', '#right-stack'], { sizes: [70, 30], gutterSize: 4 });
    Split(['#cad-pane', '#cmd-pane'], { direction: 'vertical', sizes: [80, 20], gutterSize: 4 });
    Split(['#ai-output', '#ai-input'], { direction: 'vertical', sizes: [50, 50], gutterSize: 4 });

    // 2. Generate the UI Grids (Side and Footer)
    for(let i=0; i<100; i++) document.getElementById('side-strip').innerHTML += '<div class="btn-cell"></div>';
    for(let i=0; i<18; i++) document.getElementById('foot-palette').innerHTML += '<div class="btn-cell"></div>';

    // 3. AI-SET Configuration Logic
    function toggleAISet(show) {
        document.getElementById('ai-modular-setup').style.display = show ? 'flex' : 'none';
    }

    // Capture Gemini Settings
    function saveData() {
        const apiKey = document.querySelector('#ai-modular-setup .ai-input').value;
        const selectedVersion = document.getElementById('version-select').value;
        
        if(apiKey) {
            localStorage.setItem('gemini_api_key', apiKey);
            localStorage.setItem('gemini_version', selectedVersion);
            document.getElementById('terminal-out').innerHTML += `\\n> GOOGLE GEMINI: CONFIGURATION SAVED [${selectedVersion.toUpperCase()}]`;
            document.getElementById('terminal-out').innerHTML += "\\n> SYSTEM: READY FOR CIRCUIT PROMPTS";
        } else {
            document.getElementById('terminal-out').innerHTML += "\\n> ERROR: NO API KEY PROVIDED";
        }
        toggleAISet(false);
    }

    function updateToolView(el, name, cat, func, note) {
        document.querySelectorAll('.ai-tool-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('tool-name').innerText = name;
        document.getElementById('function-select').value = func;
        document.getElementById('tool-desc').innerText = note;
        
        const versionBox = document.getElementById('version-container');
        versionBox.style.display = (name === 'Google Gemini') ? 'block' : 'none';
    }

    // 4. Menu & Input Logic
    function toggleMenu(el) {
        event.stopPropagation();
        const isActive = el.classList.contains('active');
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
        if(!isActive) el.classList.add('active');
    }

    window.onclick = function() {
        document.querySelectorAll('.dropup').forEach(d => d.classList.remove('active'));
    };

    // User Prompt Execution
    const promptInput = document.getElementById('user-prompt');
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const text = promptInput.value.trim();
            if(text !== "") {
                document.getElementById('ai-chat').innerHTML += "<br><br><span style='color:#800080'>[USER]:</span> " + text;
                document.getElementById('terminal-out').innerHTML += "\\n> GEMINI DISPATCH: " + text.toUpperCase();
                promptInput.value = "";
                
                // Placeholder for next step: Real API Call
                setTimeout(() => {
                   document.getElementById('terminal-out').innerHTML += "\\n> GEMINI: PROCESSING ARCHITECTURE...";
                }, 500);
            }
        }
    });
</script>
