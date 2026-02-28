import { useEffect, useRef, useState, useCallback } from 'react';
import './index.css';

// Matrix rain background
function MatrixBackground() {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animId;
    const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; };
    resize();
    window.addEventListener('resize', resize);
    const cols = Math.floor(canvas.width / 18);
    const drops = Array(cols).fill(1);
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    function draw() {
      ctx.fillStyle = 'rgba(5, 5, 16, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#00f5ff';
      ctx.font = '14px Share Tech Mono, monospace';
      drops.forEach((y, i) => {
        ctx.fillText(chars[Math.floor(Math.random() * chars.length)], i * 18, y * 18);
        if (y * 18 > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      });
      animId = requestAnimationFrame(draw);
    }
    draw();
    return () => { cancelAnimationFrame(animId); window.removeEventListener('resize', resize); };
  }, []);
  return <canvas id="matrix-canvas" ref={canvasRef} />;
}

// Animated circular confidence ring
function ConfidenceRing({ percent, isAi }) {
  const r = 45;
  const circ = 2 * Math.PI * r;
  const offset = circ - (percent / 100) * circ;
  return (
    <div className="ring-wrap">
      <svg className="ring-svg" width="110" height="110" viewBox="0 0 110 110">
        <circle className="ring-bg" cx="55" cy="55" r={r} />
        <circle className="ring-fill" cx="55" cy="55" r={r}
          strokeDasharray={circ} strokeDashoffset={offset} />
      </svg>
      <div className="ring-label">
        <span className="ring-percent">{percent}%</span>
        <span className="ring-sub">CONFIDENCE</span>
      </div>
    </div>
  );
}

// Scanning progress states
const STEPS = [
  '[ 1/4 ] Decoding base64 audio stream...',
  '[ 2/4 ] Extracting Wav2Vec2 embeddings...',
  '[ 3/4 ] Running neural classifier...',
  '[ 4/4 ] Generating verdict...',
];

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
const API_KEY = import.meta.env.VITE_API_KEY || 'HACKATHON_SECRET_KEY_123';

const STORAGE_KEY = 'voiceguard_stats';
function loadStats() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { total: 0, ai: 0, human: 0 }; }
  catch { return { total: 0, ai: 0, human: 0 }; }
}
function saveStats(s) { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); }

export default function App() {
  const [file, setFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stepIdx, setStepIdx] = useState(0);
  const [result, setResult] = useState(null);   // { isAi, confidence, message }
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(loadStats);
  const fileInputRef = useRef(null);

  // handle file selection
  const handleFile = useCallback((f) => {
    if (!f || !f.type.startsWith('audio/')) { setError('⚠ Invalid file — please upload an audio file.'); return; }
    setFile(f);
    setResult(null);
    setError(null);
    setAudioUrl(URL.createObjectURL(f));
  }, []);

  const onDrop = (e) => { e.preventDefault(); setIsDragging(false); handleFile(e.dataTransfer.files[0]); };
  const onDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const onDragLeave = () => setIsDragging(false);

  // convert file → base64
  const toBase64 = (f) => new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = () => res(r.result.split(',')[1]);
    r.onerror = rej;
    r.readAsDataURL(f);
  });

  // fake progress animation while real call runs
  const runFakeProgress = () => {
    let p = 0; let s = 0;
    return new Promise((resolve) => {
      const iv = setInterval(() => {
        p = Math.min(p + Math.random() * 12, 92);
        setProgress(Math.round(p));
        const newStep = Math.floor((p / 100) * STEPS.length);
        if (newStep !== s) { s = newStep; setStepIdx(s); }
        if (p >= 92) { clearInterval(iv); resolve(); }
      }, 350);
    });
  };

  const analyze = async () => {
    if (!file) return;
    setError(null);
    setResult(null);
    setScanning(true);
    setProgress(0);
    setStepIdx(0);

    try {
      const [base64] = await Promise.all([toBase64(file), runFakeProgress()]);
      const ext = file.name.split('.').pop().toLowerCase() || 'mp3';

      const resp = await fetch(`${API_URL}/detect-audio/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-api-key': API_KEY },
        body: JSON.stringify({ audio_base64: base64, audio_format: ext, language: 'en' }),
      });

      setProgress(100);
      setStepIdx(STEPS.length);

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        if (resp.status === 401) throw new Error('⛔ Authentication failed — check your API key.');
        throw new Error(err.detail || `API Error ${resp.status}`);
      }

      const data = await resp.json();
      const newResult = {
        isAi: data.is_ai_generated,
        confidence: Math.round((data.confidence_score || 0) * 100),
        message: data.message || '',
      };
      setResult(newResult);

      const newStats = {
        total: stats.total + 1,
        ai: stats.ai + (newResult.isAi ? 1 : 0),
        human: stats.human + (!newResult.isAi ? 1 : 0),
      };
      setStats(newStats);
      saveStats(newStats);
    } catch (e) {
      setError(e.message || '⚠ Could not reach the detection server.');
    } finally {
      setTimeout(() => setScanning(false), 400);
    }
  };

  return (
    <>
      <MatrixBackground />
      <div className="app">
        {/* HEADER */}
        <header className="header">
          <h1 className="logo">VoiceGuard AI<span className="version-badge">v2.0</span></h1>
          <p className="subtitle">Neural Deepfake Detection System</p>
          <div className="api-status"><span className="status-dot" />API: ONLINE</div>
        </header>

        {/* STATS BAR */}
        <div className="stats-bar">
          {[
            { label: 'Analyses Run', val: stats.total, color: 'var(--cyan)' },
            { label: 'AI Detected', val: stats.ai, color: 'var(--red)' },
            { label: 'Human Verified', val: stats.human, color: 'var(--green)' },
          ].map(({ label, val, color }) => (
            <div key={label} className="stat-card glass">
              <span className="stat-value" style={{ color }}>{val}</span>
              <span className="stat-label">{label}</span>
            </div>
          ))}
        </div>

        {/* DETECTION PANEL */}
        <div className="detection-panel glass">
          <div className="panel-title">Audio Analysis Terminal</div>

          {/* UPLOAD ZONE */}
          <div
            className={`upload-zone${isDragging ? ' drag-over' : ''}`}
            onClick={() => fileInputRef.current?.click()}
            onDrop={onDrop} onDragOver={onDragOver} onDragLeave={onDragLeave}
          >
            <span className="waveform-icon">🎙</span>
            <p className="upload-text-main">Drop Audio File or Click to Upload</p>
            <p className="upload-text-sub">Analyze any voice recording for deepfake detection</p>
            <div className="format-badges">
              {['MP3', 'WAV', 'M4A', 'OGG', 'FLAC'].map(f => (
                <span key={f} className="format-badge">{f}</span>
              ))}
            </div>
            <input ref={fileInputRef} type="file" accept="audio/*" style={{ display: 'none' }}
              onChange={e => handleFile(e.target.files[0])} />
          </div>

          {/* FILE INFO */}
          {file && (
            <div className="file-info">
              <span className="file-info-icon">📁</span>
              <span className="file-name">{file.name}</span>
              <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
            </div>
          )}

          {/* AUDIO PLAYER */}
          {audioUrl && <audio className="audio-player" controls src={audioUrl} />}

          {/* ERROR */}
          {error && <div className="error-panel">⚠ {error}</div>}

          {/* SCANNING STATE */}
          {scanning && (
            <div className="scanning-state">
              <div className="scanning-label">
                <span>⬡ SCANNING AUDIO SIGNATURE...</span>
                <span>{progress}%</span>
              </div>
              <div className="progress-track"><div className="progress-bar" style={{ width: `${progress}%` }} /></div>
              <div className="scanning-steps">
                {STEPS.map((s, i) => (
                  <span key={i} className={`step ${i < stepIdx ? 'done' : i === stepIdx ? 'active' : ''}`}>
                    {i < stepIdx ? '✓' : i === stepIdx ? '▶' : '○'} {s}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* ANALYZE BUTTON */}
          <button className="analyze-btn" onClick={analyze} disabled={!file || scanning}>
            {scanning ? '⬡ ANALYZING...' : '▶ ANALYZE VOICE'}
          </button>
        </div>

        {/* RESULTS */}
        {result && (
          <div className={`result-panel glass ${result.isAi ? 'ai' : 'human'}`}>
            <div className="panel-title">{result.isAi ? 'Threat Assessment' : 'Authenticity Report'}</div>
            <div className="result-header">
              <span className="result-icon">{result.isAi ? '🚨' : '🛡'}</span>
              <p className="result-verdict">{result.isAi ? 'SYNTHETIC VOICE DETECTED' : 'AUTHENTIC HUMAN VOICE'}</p>
            </div>

            <div className="confidence-section">
              <ConfidenceRing percent={result.confidence} isAi={result.isAi} />
              <div className="confidence-details">
                <p className="detail-label">{result.isAi ? 'AI Probability' : 'Human Probability'}</p>
                <div className="detail-bar-track">
                  <div className="detail-bar-fill" style={{ width: `${result.confidence}%` }} />
                </div>
                <p className="detail-label">Confidence Level</p>
                <div className="detail-bar-track">
                  <div className="detail-bar-fill" style={{ width: `${result.confidence}%` }} />
                </div>
              </div>
            </div>

            <div className="result-message">» {result.message}</div>
            <div className="result-footer-tag">
              {result.isAi ? '⚠ DEEPFAKE SIGNATURES IDENTIFIED' : '✓ BIOMETRIC AUTHENTICITY CONFIRMED'}
            </div>
          </div>
        )}

        {/* HOW IT WORKS */}
        <div className="how-section">
          <div className="panel-title">How It Works</div>
          <div className="how-grid">
            {[
              { icon: '🎙', title: 'Upload Audio', desc: 'Drop any voice recording — MP3, WAV, M4A, OGG supported' },
              { icon: '🧠', title: 'Neural Analysis', desc: "Meta's Wav2Vec2 extracts 1024 vocal feature embeddings" },
              { icon: '🔐', title: 'Instant Verdict', desc: 'MLP classifier delivers real-time deepfake detection result' },
            ].map(({ icon, title, desc }) => (
              <div key={title} className="how-card glass">
                <span className="how-icon">{icon}</span>
                <p className="how-title">{title}</p>
                <p className="how-desc">{desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* FOOTER */}
        <footer className="footer">
          Powered by Wav2Vec2 Neural Network &nbsp;·&nbsp; Built for AI Transparency &nbsp;·&nbsp; VoiceGuard AI v2.0
        </footer>
      </div>
    </>
  );
}
