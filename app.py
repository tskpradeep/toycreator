# ... [Previous CSS and Layout remain the same] ...

    /* UPDATED SIDEBAR IN MODULAR WINDOW */
    <div class="ai-setup-sidebar" id="tool-list">
        <div class="ai-tool-item active" onclick="updateToolView(this, 'Gemini 3.1 Pro', 'Logic', 'Vibe Coding', 'Deep reasoning and agentic workflows.')">GEMINI 3.1 PRO</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'Gemini 3 Flash', 'Speed', 'Multimodal', 'Lightning fast PhD-level reasoning.')">GEMINI 3 FLASH</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'Luvia AI', 'Selection', 'MPN Text', 'Sourcing only.')">LUVIA AI</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'Flux.ai', 'Schematic', '.json / .net', 'Non-proprietary concept.')">FLUX.AI</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'KiCad', 'Analysis', '.kicad_sch', 'Local & Private.')">KICAD</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'Quilter', 'Layout', 'ODB++', 'Best for high-end CAM.')">QUILTER</div>
        <div class="ai-tool-item" onclick="updateToolView(this, 'nTop / Fusion', 'Enclosure', 'STEP / STL', 'Physics-verified.')">NTOP / FUSION</div>
    </div>

# ... [Rest of the dynamic update logic] ...
