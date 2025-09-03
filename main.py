from fasthtml.common import *
# MonsterUI shadows fasthtml components with the same name
from monsterui.all import *
# If you don't want shadowing behavior, you use import monsterui.core as ... style instead

# Get frankenui and tailwind headers via CDN using Theme.blue.headers()
_hdrs = Theme.blue.headers()

# fast_app is shadowed by MonsterUI to make it default to no Pico, and add body classes
# needed for frankenui theme styling
app, rt = fast_app(hdrs=_hdrs)


def TimerCard():
    return Card(
        Div(
            Div(
                H1("Two-Phase Bird Timer"),
                ThemePicker(color=False, radii=False, shadows=False, font=False, mode=True, cls="ml-auto"),
                cls="flex items-center justify-between"
            ),
            H4("Set phase durations and press Start.", cls="text-muted-foreground mb-2"),
            cls="space-y-2"
        ),
        Grid(
            # Controls
            Div(
                Div(
                    LabelInput("First phase seconds", id="phase1", type="number", value="60", min="1"),
                    LabelInput("Second phase seconds", id="phase2", type="number", value="15", min="1"),
                    Div(
                        Button("Start", id="startBtn", cls=(ButtonT.primary, "mr-2")),
                        Button("Pause", id="pauseBtn", cls=(ButtonT.secondary, "mr-2"), disabled=True),
                        Button("Reset", id="resetBtn", cls=ButtonT.secondary),
                        cls="flex items-center"
                    ),
                    cls="space-y-3"
                ),
                cls="p-2"
            ),
            # Display
            Div(
                Div(
                    H2("00:00", id="timerDisplay", cls="font-mono text-5xl"),
                    H4("Phase: none", id="phaseLabel", cls="text-muted-foreground"),
                    cls="text-center space-y-1"
                ),
                Div(
                    Img(
                        src="https://cdn.pixabay.com/photo/2025/05/04/18/04/robin-9578746_1280.jpg",
                        alt="Bird",
                        id="imgPhase1",
                        cls="rounded-lg border hidden"
                    ),
                    Img(
                        src="https://cdn.pixabay.com/photo/2025/04/17/08/33/ring-necked-parakeet-9539733_1280.jpg",
                        alt="Parakeet",
                        id="imgPhase2",
                        cls="rounded-lg border hidden"
                    ),
                    cls="mt-4 flex justify-center gap-4"
                ),
                cls="p-2"
            ),
            cols_lg=2
        ),
        # --- Audio Section ---
        Div(
            Grid(
                Div(
                    H4("INTRO", cls="text-md font-medium mb-2"),
                    Audio(controls=True, preload="auto", src="/music/INTRO.mp3", id="introAudio", cls="w-full"),
                    P("Stop & start manually.", cls="text-sm text-muted-foreground mt-2"),
                    cls="p-3 border rounded-lg"
                ),
                Div(
                    H4("OUTRO", cls="text-md font-medium mb-2"),
                    Audio(controls=True, preload="auto", src="/music/OUTRO.mp3", id="outroAudio", cls="w-full"),
                    P("Stop & start manually.", cls="text-sm text-muted-foreground mt-2"),
                    cls="p-3 border rounded-lg"
                ),
                cols_lg=2,
                cls="gap-4"
            ),
            cls="mt-6 p-4 border-t"
        ),

        # Test sound buttons
        Div(
            H3("Test Sounds", cls="text-lg font-semibold mb-3"),
            Div(
                Button("🐦 Test Bird Chirp", id="testBirdBtn", cls=(ButtonT.secondary, "mr-3")),
                Button("🦜 Test Parakeet Call", id="testParakeetBtn", cls=ButtonT.secondary),
                cls="flex gap-3"
            ),
            cls="mt-6 p-4 border-t"
        ),

        # Inline script: timer logic, Web Audio, and dark mode toggle
        Script("""
        (() => {
          // --- DOM Elements ---
          const display = document.getElementById('timerDisplay');
          const phaseLabel = document.getElementById('phaseLabel');
          const startBtn = document.getElementById('startBtn');
          const pauseBtn = document.getElementById('pauseBtn');
          const resetBtn = document.getElementById('resetBtn');
          const img1 = document.getElementById('imgPhase1');
          const img2 = document.getElementById('imgPhase2');
          const phase1Input = document.getElementById('phase1');
          const phase2Input = document.getElementById('phase2');
          const testBirdBtn = document.getElementById('testBirdBtn');
          const testParakeetBtn = document.getElementById('testParakeetBtn');

          // --- State Variables ---
          let intervalId = null;
          let startEpochMs = null;
          let phase1Ms = 60000;
          let phase2Ms = 15000;
          let phase1Fired = false;
          let isPaused = false;
          let pausedElapsedMs = 0;

          const fmt = (ms) => {
            const total = Math.max(0, Math.floor(ms / 1000));
            const m = String(Math.floor(total / 60)).padStart(2, '0');
            const s = String(total % 60).padStart(2, '0');
            return `${m}:${s}`;
          };

          const showPhase = (phase) => {
            if (phase === 1) {
              phaseLabel.textContent = 'Phase: bird';
              img1.classList.remove('hidden');
              img2.classList.add('hidden');
            } else if (phase === 2) {
              phaseLabel.textContent = 'Phase: parakeet';
              img2.classList.remove('hidden');
              img1.classList.add('hidden');
            } else {
              phaseLabel.textContent = 'Phase: none';
              img1.classList.add('hidden');
              img2.classList.add('hidden');
            }
          };

          // --- Web Audio (Full implementation from previous steps) ---
          let audioCtx = null;
          const ensureAudio = () => { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); };
          const chirp = () => { ensureAudio(); const now = audioCtx.currentTime; const o1 = audioCtx.createOscillator(); const g1 = audioCtx.createGain(); o1.type = 'triangle'; o1.frequency.setValueAtTime(1800, now); o1.frequency.exponentialRampToValueAtTime(2600, now + 0.12); g1.gain.setValueAtTime(0, now); g1.gain.linearRampToValueAtTime(0.4, now + 0.02); g1.gain.exponentialRampToValueAtTime(0.0001, now + 0.25); o1.connect(g1).connect(audioCtx.destination); o1.start(now); o1.stop(now + 0.28); const o2 = audioCtx.createOscillator(); const g2 = audioCtx.createGain(); o2.type = 'triangle'; o2.frequency.setValueAtTime(1900, now + 0.35); o2.frequency.exponentialRampToValueAtTime(2700, now + 0.47); g2.gain.setValueAtTime(0, now + 0.35); g2.gain.linearRampToValueAtTime(0.4, now + 0.37); g2.gain.exponentialRampToValueAtTime(0.0001, now + 0.60); o2.connect(g2).connect(audioCtx.destination); o2.start(now + 0.35); o2.stop(now + 0.63); };
          const parakeetCall = () => { ensureAudio(); const now = audioCtx.currentTime; const duration = 2.2; const osc1 = audioCtx.createOscillator(); osc1.type = 'sine'; const osc2 = audioCtx.createOscillator(); osc2.type = 'triangle'; const filter = audioCtx.createBiquadFilter(); filter.type = 'bandpass'; filter.Q.value = 8; filter.frequency.value = 1200; const waveShaper = audioCtx.createWaveShaper(); const n_samples = 256; const curve = new Float32Array(n_samples); for (let i = 0; i < n_samples; ++i) { const x = (i * 2) / n_samples - 1; curve[i] = Math.tanh(x * 2); } waveShaper.curve = curve; waveShaper.oversample = '2x'; const gain = audioCtx.createGain(); const lfo = audioCtx.createOscillator(); lfo.type = 'sine'; lfo.frequency.value = 6; const lfoGain = audioCtx.createGain(); lfoGain.gain.value = 80; osc1.frequency.setValueAtTime(1000, now); osc1.frequency.exponentialRampToValueAtTime(1800, now + 0.3); osc1.frequency.exponentialRampToValueAtTime(1200, now + 0.8); osc1.frequency.exponentialRampToValueAtTime(2000, now + 1.2); osc1.frequency.exponentialRampToValueAtTime(1100, now + 1.8); osc1.frequency.exponentialRampToValueAtTime(1600, now + duration); osc2.frequency.setValueAtTime(1200, now); osc2.frequency.exponentialRampToValueAtTime(2000, now + 0.4); osc2.frequency.exponentialRampToValueAtTime(1400, now + 0.9); osc2.frequency.exponentialRampToValueAtTime(2200, now + 1.3); osc2.frequency.exponentialRampToValueAtTime(1300, now + 1.9); osc2.frequency.exponentialRampToValueAtTime(1800, now + duration); lfo.connect(lfoGain); lfoGain.connect(osc1.frequency); osc1.connect(filter); osc2.connect(filter); filter.connect(waveShaper); waveShaper.connect(gain); gain.connect(audioCtx.destination); gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(0.7, now + 0.05); gain.gain.linearRampToValueAtTime(0.5, now + 0.4); gain.gain.linearRampToValueAtTime(0.8, now + 0.8); gain.gain.linearRampToValueAtTime(0.4, now + 1.3); gain.gain.linearRampToValueAtTime(0.9, now + 1.7); gain.gain.exponentialRampToValueAtTime(0.0001, now + duration); lfo.start(now); osc1.start(now); osc2.start(now); lfo.stop(now + duration); osc1.stop(now + duration); osc2.stop(now + duration); };

          // --- Timer Logic Functions ---
          const runTimer = () => {
            intervalId = setInterval(() => {
              const elapsed = Date.now() - startEpochMs;
              display.textContent = fmt(elapsed);
              if (!phase1Fired && elapsed >= phase1Ms) {
                phase1Fired = true;
                showPhase(1);
                chirp();
              }
              if (elapsed >= (phase1Ms + phase2Ms)) {
                showPhase(2);
                parakeetCall();
                stop();
              }
            }, 100);
          };

          const start = () => {
            startBtn.disabled = true;
            pauseBtn.disabled = false;
            resetBtn.disabled = true;
            phase1Input.disabled = true;
            phase2Input.disabled = true;

            const p1 = Math.max(1, parseInt(phase1Input.value || '60', 10));
            const p2 = Math.max(1, parseInt(phase2Input.value || '15', 10));
            phase1Ms = p1 * 1000;
            phase2Ms = p2 * 1000;

            phase1Fired = false;
            isPaused = false;
            pausedElapsedMs = 0;
            pauseBtn.textContent = 'Pause';
            showPhase(null);
            display.textContent = '00:00';
            startEpochMs = Date.now();
            runTimer();
          };

          const togglePause = () => {
            if (!startEpochMs) return;
            isPaused = !isPaused;
            if (isPaused) {
              clearInterval(intervalId);
              intervalId = null;
              pausedElapsedMs = Date.now() - startEpochMs;
              pauseBtn.textContent = 'Resume';
              resetBtn.disabled = false;
            } else {
              startEpochMs = Date.now() - pausedElapsedMs;
              runTimer();
              pauseBtn.textContent = 'Pause';
              resetBtn.disabled = true;
            }
          };

          const stop = () => {
            if (intervalId) {
              clearInterval(intervalId);
              intervalId = null;
            }
            startBtn.disabled = false;
            pauseBtn.disabled = true;
            resetBtn.disabled = false;
            phase1Input.disabled = false;
            phase2Input.disabled = false;
            isPaused = false;
            pauseBtn.textContent = 'Pause';
          };

          const reset = () => {
            stop();
            startEpochMs = null;
            pausedElapsedMs = 0;
            display.textContent = '00:00';
            showPhase(null);
          };

          // --- Event Listeners ---
          startBtn.addEventListener('click', (e) => { e.preventDefault(); start(); });
          pauseBtn.addEventListener('click', (e) => { e.preventDefault(); togglePause(); });
          resetBtn.addEventListener('click', (e) => { e.preventDefault(); reset(); });
          testBirdBtn.addEventListener('click', (e) => { e.preventDefault(); chirp(); });
          testParakeetBtn.addEventListener('click', (e) => { e.preventDefault(); parakeetCall(); });
        })();
        """),
        cls="max-w-3xl mx-auto"
    )


@rt
def index():
    return Titled(
        Container(
            TimerCard(),
            cls="py-6"
        )
    )

@rt("/music/<path:filename>")
def serve_music(filename):
    """Serve music files from the music directory"""
    from pathlib import Path
    from fasthtml.common import FileResponse
    music_path = Path("music") / filename
    if not music_path.is_file(): return "File not found", 404
    if music_path.resolve().parent != Path("music").resolve(): return "Forbidden", 403
    return FileResponse(music_path)

serve()
