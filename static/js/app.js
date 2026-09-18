// ==========================================================================
// AURA // Ultimate Cinematic Engine: 2-Role Dynamic Portal & Media Lightbox
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Scene Elements
    const sceneContainer = document.getElementById('sceneContainer');
    const ambientSpotlight = document.getElementById('ambientSpotlight');
    const anamorphicFlare = document.getElementById('anamorphicFlare');
    const giantBackdrop = document.getElementById('giantBackdrop');
    const giantWord = document.getElementById('giantWord');
    const foregroundContent = document.getElementById('foregroundContent');
    const touchHint = document.getElementById('touchHint');
    const typedTextEl = document.getElementById('typedText');
    const typingContainer = document.getElementById('typingContainer');

    // Dynamic Header Texts
    const headlineWord1 = document.getElementById('headlineWord1');
    const headlineWord2 = document.getElementById('headlineWord2');
    const topBadgeText = document.getElementById('topBadgeText');
    const specPill1 = document.getElementById('specPill1');
    const specPill2 = document.getElementById('specPill2');

    // Supernova & IMAX Elements
    const supernovaFlash = document.getElementById('supernovaFlash');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const fullscreenLabel = document.getElementById('fullscreenLabel');
    const igniteWrap = document.getElementById('igniteWrap');
    const supernovaBtn = document.getElementById('supernovaBtn');

    // VFX Canvas
    const canvas = document.getElementById('vfxCanvas');
    const ctx = canvas.getContext('2d');

    // Holographic Sheen
    const cardHoloSheen = document.getElementById('cardHoloSheen');

    // Sound Toggle
    const soundToggleBtn = document.getElementById('soundToggleBtn');
    const soundLabel = document.getElementById('soundLabel');
    let soundEnabled = true;

    // Chapter Journey & Staged Dots Elements
    const chapterStage = document.getElementById('chapterStage');
    const chapterCard = document.getElementById('chapterCard');
    const backdropDots = document.getElementById('backdropDots');
    const dotsContainer = document.getElementById('dotsContainer');
    const trackLineActive = document.getElementById('trackLineActive');
    const trackSparkRunner = document.getElementById('trackSparkRunner');
    let bDots = document.querySelectorAll('.b-dot');

    const cardStepBadge = document.getElementById('cardStepBadge');
    const cardStepCounter = document.getElementById('cardStepCounter');
    const cardStepTitle = document.getElementById('cardStepTitle');
    const cardStepBody = document.getElementById('cardStepBody');
    const nextStepBtn = document.getElementById('nextStepBtn');
    const prevStepBtn = document.getElementById('prevStepBtn');
    const nextBtnText = document.getElementById('nextBtnText');

    // Card Media Button Elements
    const cardMediaTriggerWrap = document.getElementById('cardMediaTriggerWrap');
    const cardMediaBtn = document.getElementById('cardMediaBtn');
    const cardMediaIcon = document.getElementById('cardMediaIcon');
    const cardMediaLabel = document.getElementById('cardMediaLabel');

    // Dedicated Below-Card Reply Elements for Viewer (Glory)
    const cardReplyTriggerWrap = document.getElementById('cardReplyTriggerWrap');
    const cardReplyBtn = document.getElementById('cardReplyBtn');
    const cardReplyBtnLabel = document.getElementById('cardReplyBtnLabel');

    // Auth & Header Control Elements
    const authControls = document.getElementById('authControls');
    const userChipName = document.getElementById('userChipName');
    const adminStudioBtn = document.getElementById('adminStudioBtn');
    const adminViewRepliesBtn = document.getElementById('adminViewRepliesBtn');
    const headerRepliesCount = document.getElementById('headerRepliesCount');
    const gloryReplyBtn = document.getElementById('gloryReplyBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    // Login Portal Modal Elements
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const loginUsername = document.getElementById('loginUsername');
    const loginPassword = document.getElementById('loginPassword');
    const loginErrorMsg = document.getElementById('loginErrorMsg');

    // Admin Studio Drawer Elements
    const adminDrawerBackdrop = document.getElementById('adminDrawerBackdrop');
    const adminDrawerCloseBtn = document.getElementById('adminDrawerCloseBtn');
    const studioTabBtns = document.querySelectorAll('.studio-tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const repliesBadgeCount = document.getElementById('repliesBadgeCount');

    // Studio Tab 1: Texts
    const adminTextsForm = document.getElementById('adminTextsForm');
    const adminHeadline1 = document.getElementById('adminHeadline1');
    const adminHeadline2 = document.getElementById('adminHeadline2');
    const adminGiantWord = document.getElementById('adminGiantWord');
    const adminTopBadge = document.getElementById('adminTopBadge');
    const adminTypingText = document.getElementById('adminTypingText');

    // Studio Tab 2: Chapters & Media
    const chapterSelectorBar = document.getElementById('chapterSelectorBar');
    const addChapterBtn = document.getElementById('addChapterBtn');
    const adminDeleteChapterBtn = document.getElementById('adminDeleteChapterBtn');
    const adminChapterForm = document.getElementById('adminChapterForm');
    const adminCurrentStepIndex = document.getElementById('adminCurrentStepIndex');
    const adminCardBadge = document.getElementById('adminCardBadge');
    const adminCardCounter = document.getElementById('adminCardCounter');
    const adminCardTitle = document.getElementById('adminCardTitle');
    const adminCardBody = document.getElementById('adminCardBody');
    const adminCardTheme = document.getElementById('adminCardTheme');
    const currentMediaText = document.getElementById('currentMediaText');
    const adminFileInput = document.getElementById('adminFileInput');
    const adminRemoveMediaBtn = document.getElementById('adminRemoveMediaBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const uploadProgressFill = document.getElementById('uploadProgressFill');

    // In-Editor Live Media Preview Elements
    const editorMediaPreviewWrap = document.getElementById('editorMediaPreviewWrap');
    const editorImagePreview = document.getElementById('editorImagePreview');
    const editorVideoPreview = document.getElementById('editorVideoPreview');
    const editorAudioPreview = document.getElementById('editorAudioPreview');
    const editorAudioPreviewBox = document.getElementById('editorAudioPreviewBox');

    // Studio Tab 3: Replies
    const adminRepliesList = document.getElementById('adminRepliesList');
    const refreshRepliesBtn = document.getElementById('refreshRepliesBtn');

    // Dedicated Admin Replies Modal Elements
    const adminRepliesModal = document.getElementById('adminRepliesModal');
    const adminRepliesModalCloseBtn = document.getElementById('adminRepliesModalCloseBtn');
    const modalRefreshRepliesBtn = document.getElementById('modalRefreshRepliesBtn');
    const richRepliesContainer = document.getElementById('richRepliesContainer');

    // Glory Reply Modal Elements
    const replyModal = document.getElementById('replyModal');
    const replyModalCloseBtn = document.getElementById('replyModalCloseBtn');
    const replyCardContextWrap = document.getElementById('replyCardContextWrap');
    const replyContextTag = document.getElementById('replyContextTag');
    const replyContextTitle = document.getElementById('replyContextTitle');
    const gloryChapterIndex = document.getElementById('gloryChapterIndex');
    const gloryChapterTitle = document.getElementById('gloryChapterTitle');
    const gloryReplyForm = document.getElementById('gloryReplyForm');
    const glorySenderName = document.getElementById('glorySenderName');
    const gloryMessageText = document.getElementById('gloryMessageText');

    // Media Lightbox Modal Elements
    const mediaModal = document.getElementById('mediaModal');
    const mediaModalCloseBtn = document.getElementById('mediaModalCloseBtn');
    const mediaBadgeLabel = document.getElementById('mediaBadgeLabel');
    const mediaTitleText = document.getElementById('mediaTitleText');
    const mediaPaneImage = document.getElementById('mediaPaneImage');
    const lightboxImage = document.getElementById('lightboxImage');
    const mediaPaneVideo = document.getElementById('mediaPaneVideo');
    const lightboxVideo = document.getElementById('lightboxVideo');
    const lightboxVideoSrc = document.getElementById('lightboxVideoSrc');
    const mediaPaneAudio = document.getElementById('mediaPaneAudio');
    const lightboxAudio = document.getElementById('lightboxAudio');
    const lightboxAudioTitle = document.getElementById('lightboxAudioTitle');

    // Toast Notification
    const auraToast = document.getElementById('auraToast');
    const toastMsg = document.getElementById('toastMsg');
    let toastTimeout = null;

    function showToast(text) {
        if (!auraToast || !toastMsg) return;
        toastMsg.textContent = text;
        auraToast.classList.add('toast-show');
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            auraToast.classList.remove('toast-show');
        }, 3200);
    }

    // Dynamic State
    let siteConfig = null;
    let MILESTONES = [];
    let currentStep = 0;
    let totalSteps = 4;
    let isTransitioning = false;
    let typewriterStarted = false;

    // Temporary editor upload state
    let tempMediaUrl = '';
    let tempMediaType = 'none';
    let tempMediaName = '';

    // Session State
    let currentUser = localStorage.getItem('aura_user') || null;
    let currentRole = localStorage.getItem('aura_role') || null;

    // ==========================================================================
    // 1. Cinematic Web Audio Synthesizer
    // ==========================================================================
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                audioCtx = new AudioContext();
            }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function playLaserWhoosh() {
        if (!soundEnabled) return;
        initAudio();
        if (!audioCtx) return;

        try {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            const filter = audioCtx.createBiquadFilter();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(450, now);
            osc.frequency.exponentialRampToValueAtTime(80, now + 0.38);

            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(1400, now);
            filter.frequency.exponentialRampToValueAtTime(180, now + 0.38);

            gain.gain.setValueAtTime(0.14, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);

            osc.connect(filter);
            filter.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(now);
            osc.stop(now + 0.38);
        } catch (_) {}
    }

    function playImpactThud(isFinale = false) {
        if (!soundEnabled) return;
        initAudio();
        if (!audioCtx) return;

        try {
            const now = audioCtx.currentTime;
            
            const sub = audioCtx.createOscillator();
            const subGain = audioCtx.createGain();
            sub.type = 'sine';
            sub.frequency.setValueAtTime(isFinale ? 140 : 110, now);
            sub.frequency.exponentialRampToValueAtTime(28, now + 0.55);
            subGain.gain.setValueAtTime(isFinale ? 0.35 : 0.22, now);
            subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
            sub.connect(subGain);
            subGain.connect(audioCtx.destination);
            sub.start(now);
            sub.stop(now + 0.55);

            const chimeFreqs = isFinale ? [523.25, 659.25, 783.99, 1046.5] : [587.33, 880];
            chimeFreqs.forEach((freq, i) => {
                const chime = audioCtx.createOscillator();
                const chimeGain = audioCtx.createGain();
                chime.type = 'triangle';
                chime.frequency.setValueAtTime(freq, now + (i * 0.04));
                chimeGain.gain.setValueAtTime(0.09, now + (i * 0.04));
                chimeGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.65);
                chime.connect(chimeGain);
                chimeGain.connect(audioCtx.destination);
                chime.start(now + (i * 0.04));
                chime.stop(now + 0.65);
            });
        } catch (_) {}
    }

    function playSupernovaFanfare() {
        if (!soundEnabled) return;
        initAudio();
        if (!audioCtx) return;

        try {
            const now = audioCtx.currentTime;
            const chords = [
                { f: 261.63, d: 0.0 },
                { f: 329.63, d: 0.08 },
                { f: 392.00, d: 0.16 },
                { f: 523.25, d: 0.24 },
                { f: 659.25, d: 0.32 },
                { f: 783.99, d: 0.40 },
                { f: 1046.50, d: 0.48 }
            ];

            chords.forEach(note => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(note.f, now + note.d);

                gain.gain.setValueAtTime(0.18, now + note.d);
                gain.gain.exponentialRampToValueAtTime(0.001, now + note.d + 1.2);

                osc.connect(gain);
                gain.connect(audioCtx.destination);

                osc.start(now + note.d);
                osc.stop(now + note.d + 1.2);
            });
        } catch (_) {}
    }

    // Sound toggle pill
    if (soundToggleBtn && soundLabel) {
        soundToggleBtn.addEventListener('click', () => {
            initAudio();
            soundEnabled = !soundEnabled;
            if (soundEnabled) {
                soundLabel.textContent = "AUDIO ON";
                soundToggleBtn.classList.remove('muted');
                playLaserWhoosh();
            } else {
                soundLabel.textContent = "MUTED";
                soundToggleBtn.classList.add('muted');
            }
        });
    }

    // ==========================================================================
    // 2. IMAX Fullscreen Mode Controller
    // ==========================================================================
    if (fullscreenBtn && fullscreenLabel) {
        fullscreenBtn.addEventListener('click', () => {
            initAudio();
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(() => {});
                fullscreenLabel.textContent = "EXIT IMAX";
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                    fullscreenLabel.textContent = "IMAX MODE";
                }
            }
        });

        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement) {
                fullscreenLabel.textContent = "IMAX MODE";
            } else {
                fullscreenLabel.textContent = "EXIT IMAX";
            }
        });
    }

    // ==========================================================================
    // 3. Cyber Title Scramble Decoder Effect
    // ==========================================================================
    const GLYPHS = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789//--++==<>';

    function decodeText(element, targetText, duration = 650) {
        if (!element) return;
        const totalLength = targetText.length;
        const startTime = performance.now();

        function updateDecoder(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const revealedChars = Math.floor(progress * totalLength);

            let output = '';
            for (let i = 0; i < totalLength; i++) {
                if (i < revealedChars) {
                    output += targetText[i];
                } else if (targetText[i] === ' ') {
                    output += ' ';
                } else {
                    output += GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
                }
            }

            element.textContent = output;

            if (progress < 1) {
                requestAnimationFrame(updateDecoder);
            } else {
                element.textContent = targetText;
            }
        }

        requestAnimationFrame(updateDecoder);
    }

    // ==========================================================================
    // 4. VFX Canvas: Floating Embers, Interactive Stardust Trails & Shockwaves
    // ==========================================================================
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    function resizeCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);

    class EmberParticle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * width;
            this.y = height + Math.random() * 50;
            this.size = Math.random() * 1.8 + 0.6;
            this.vx = (Math.random() - 0.5) * 0.45;
            this.vy = -(Math.random() * 0.65 + 0.25);
            this.alpha = Math.random() * 0.45 + 0.15;
            this.decay = Math.random() * 0.0015 + 0.0005;
            this.flickerSpeed = Math.random() * 0.03 + 0.01;
            this.color = Math.random() > 0.4 ? 'rgba(255, 42, 75,' : 'rgba(255, 215, 0,';
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.alpha -= this.decay;
            if (this.alpha <= 0 || this.y < -20) {
                this.reset();
            }
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `${this.color} ${this.alpha})`;
            ctx.shadowBlur = 6;
            ctx.shadowColor = `${this.color} 0.5)`;
            ctx.fill();
        }
    }

    const embers = Array.from({ length: 35 }, () => new EmberParticle());
    const stardustTrails = [];
    const burstParticles = [];
    const fireworks = [];

    function addStardust(x, y) {
        stardustTrails.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5 - 0.5,
            size: Math.random() * 2.2 + 0.8,
            alpha: 0.85,
            decay: Math.random() * 0.035 + 0.02,
            color: Math.random() > 0.4 ? 'rgba(255, 240, 200,' : 'rgba(255, 42, 75,'
        });
    }

    function triggerShockwave(x, y) {
        for (let i = 0; i < 35; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 4.5 + 1.2;
            burstParticles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size: Math.random() * 2.5 + 1,
                alpha: 1,
                decay: Math.random() * 0.025 + 0.012,
                color: Math.random() > 0.5 ? 'rgba(255, 42, 75,' : 'rgba(255, 255, 255,'
            });
        }
    }

    function launchCelebrationFireworks(count = 5) {
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                const ox = width * (0.2 + Math.random() * 0.6);
                const oy = height * (0.25 + Math.random() * 0.4);
                const hues = ['rgba(255, 215, 0,', 'rgba(255, 42, 75,', 'rgba(56, 189, 248,', 'rgba(168, 85, 247,'];
                const color = hues[Math.floor(Math.random() * hues.length)];

                for (let j = 0; j < 45; j++) {
                    const angle = Math.random() * Math.PI * 2;
                    const speed = Math.random() * 6 + 1.5;
                    fireworks.push({
                        x: ox,
                        y: oy,
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        gravity: 0.06,
                        size: Math.random() * 3 + 1,
                        alpha: 1,
                        decay: Math.random() * 0.015 + 0.008,
                        color: color
                    });
                }
            }, i * 250);
        }
    }

    function renderVfxLoop() {
        ctx.clearRect(0, 0, width, height);

        // 1. Embers
        embers.forEach(e => {
            e.update();
            e.draw();
        });

        // 2. Stardust trails
        for (let i = stardustTrails.length - 1; i >= 0; i--) {
            const s = stardustTrails[i];
            s.x += s.vx;
            s.y += s.vy;
            s.alpha -= s.decay;

            if (s.alpha <= 0) {
                stardustTrails.splice(i, 1);
                continue;
            }

            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            ctx.fillStyle = `${s.color} ${s.alpha})`;
            ctx.shadowBlur = 8;
            ctx.shadowColor = `${s.color} 0.8)`;
            ctx.fill();
        }

        // 3. Shockwave particles
        for (let i = burstParticles.length - 1; i >= 0; i--) {
            const p = burstParticles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vx *= 0.94;
            p.vy *= 0.94;
            p.alpha -= p.decay;

            if (p.alpha <= 0) {
                burstParticles.splice(i, 1);
                continue;
            }

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `${p.color} ${p.alpha})`;
            ctx.shadowBlur = 10;
            ctx.shadowColor = `${p.color} 0.8)`;
            ctx.fill();
        }

        // 4. Celebration Fireworks
        for (let i = fireworks.length - 1; i >= 0; i--) {
            const f = fireworks[i];
            f.x += f.vx;
            f.y += f.vy;
            f.vy += f.gravity;
            f.vx *= 0.97;
            f.alpha -= f.decay;

            if (f.alpha <= 0) {
                fireworks.splice(i, 1);
                continue;
            }

            ctx.beginPath();
            ctx.arc(f.x, f.y, f.size, 0, Math.PI * 2);
            ctx.fillStyle = `${f.color} ${f.alpha})`;
            ctx.shadowBlur = 12;
            ctx.shadowColor = `${f.color} 0.9)`;
            ctx.fill();
        }

        requestAnimationFrame(renderVfxLoop);
    }
    requestAnimationFrame(renderVfxLoop);

    // ==========================================================================
    // 5. Dynamic Content Synchronization & Authentication Pipeline
    // ==========================================================================
    async function fetchSiteContent() {
        try {
            const res = await fetch('/api/content');
            const data = await res.json();
            if (data.status === 'success') {
                siteConfig = data.config;
                MILESTONES = data.chapters;
                totalSteps = MILESTONES.length;

                // Apply config to DOM
                if (headlineWord1) headlineWord1.textContent = siteConfig.headline_word1 || 'HAPPY';
                if (headlineWord2) headlineWord2.textContent = siteConfig.headline_word2 || 'BIRTHDAY';
                if (giantWord) giantWord.textContent = siteConfig.giant_word || 'YASH';
                if (topBadgeText) topBadgeText.textContent = siteConfig.top_badge || 'NEXT LEVEL UI / UX';
                if (specPill1) specPill1.textContent = siteConfig.spec_pill1 || 'CINEMATIC EDITION';
                if (specPill2) specPill2.textContent = siteConfig.spec_pill2 || 'LEVEL 2026';
                if (typedTextEl) typedTextEl.setAttribute('data-text', siteConfig.typing_text || '');

                renderDots();
                populateStudioForm();
            }
        } catch (err) {
            console.error('Error fetching site content:', err);
        }
    }

    function renderDots() {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = '';
        MILESTONES.forEach((m, idx) => {
            const dot = document.createElement('span');
            dot.className = `b-dot ${idx === currentStep ? 'active' : ''}`;
            dot.setAttribute('data-step', idx);
            dot.innerHTML = `
                <span class="b-dot-num">${String(idx + 1).padStart(2, '0')}</span>
                <span class="b-dot-ripple"></span>
            `;
            dot.addEventListener('click', () => {
                if (idx !== currentStep && !isTransitioning) {
                    transitionToStep(idx);
                }
            });
            dotsContainer.appendChild(dot);
        });
        bDots = document.querySelectorAll('.b-dot');
    }

    function checkAuth() {
        if (currentUser && currentRole) {
            // Already logged in
            if (loginModal) loginModal.classList.add('portal-hidden');
            if (authControls) authControls.style.display = 'flex';
            if (userChipName) userChipName.textContent = currentUser.toUpperCase();

            if (currentRole === 'admin') {
                if (adminStudioBtn) adminStudioBtn.style.display = 'inline-flex';
                if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'inline-flex';
                if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
                if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
                fetchAndRenderRichReplies();
            } else {
                if (adminStudioBtn) adminStudioBtn.style.display = 'none';
                if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
                if (gloryReplyBtn) gloryReplyBtn.style.display = 'inline-flex';
                if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'flex';
            }

            startTypewriter();
        } else {
            // Show login portal
            if (loginModal) loginModal.classList.remove('portal-hidden');
            if (authControls) authControls.style.display = 'none';
            if (adminStudioBtn) adminStudioBtn.style.display = 'none';
            if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
            if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
            if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
        }
    }

    // Login Form Submit
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = loginUsername.value.trim();
            const password = loginPassword.value.trim();
            if (loginErrorMsg) loginErrorMsg.style.display = 'none';

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                if (res.ok) {
                    const data = await res.json();
                    currentUser = data.username;
                    currentRole = data.role;
                    localStorage.setItem('aura_user', currentUser);
                    localStorage.setItem('aura_role', currentRole);

                    // Fade out login modal
                    if (loginModal) loginModal.classList.add('portal-hidden');
                    if (authControls) authControls.style.display = 'flex';
                    if (userChipName) userChipName.textContent = currentUser.toUpperCase();

                    if (currentRole === 'admin') {
                        if (adminStudioBtn) adminStudioBtn.style.display = 'inline-flex';
                        if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'inline-flex';
                        if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
                        if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
                        fetchAndRenderRichReplies();
                        showToast(`Welcome back, Yash! Admin studio unlocked ✦`);
                    } else {
                        if (adminStudioBtn) adminStudioBtn.style.display = 'none';
                        if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
                        if (gloryReplyBtn) gloryReplyBtn.style.display = 'inline-flex';
                        if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'flex';
                        showToast(`Welcome, Glory! Cinematic portal unlocked ✦`);
                    }

                    initAudio();
                    playLaserWhoosh();
                    startTypewriter();
                } else {
                    const err = await res.json();
                    if (loginErrorMsg) {
                        loginErrorMsg.textContent = err.detail || 'Invalid credentials.';
                        loginErrorMsg.style.display = 'block';
                    }
                }
            } catch (err) {
                if (loginErrorMsg) {
                    loginErrorMsg.textContent = 'Network error. Please try again.';
                    loginErrorMsg.style.display = 'block';
                }
            }
        });
    }

    // Logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('aura_user');
            localStorage.removeItem('aura_role');
            currentUser = null;
            currentRole = null;
            if (loginModal) loginModal.classList.remove('portal-hidden');
            if (authControls) authControls.style.display = 'none';
            if (adminStudioBtn) adminStudioBtn.style.display = 'none';
            if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
            if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
            if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
            if (loginPassword) loginPassword.value = '';
            showToast('Session ended.');
        });
    }

    // ==========================================================================
    // 6. Text Typewriter Animation Engine
    // ==========================================================================
    function startTypewriter() {
        if (typewriterStarted) return;
        typewriterStarted = true;

        if (!typedTextEl) return;
        const fullMessage = typedTextEl.getAttribute('data-text') || typedTextEl.textContent.trim();
        typedTextEl.textContent = '';
        let index = 0;

        function typeNextLetter() {
            if (index < fullMessage.length) {
                const char = fullMessage.charAt(index);
                typedTextEl.textContent += char;
                index++;

                let charDelay = 30;
                if (char === '.' || char === '!' || char === '?') {
                    charDelay = 280;
                } else if (char === ',') {
                    charDelay = 160;
                } else if (char === ' ') {
                    charDelay = 35;
                } else {
                    charDelay = Math.random() * 20 + 20;
                }

                setTimeout(typeNextLetter, charDelay);
            } else {
                setTimeout(() => {
                    if (typingContainer) {
                        typingContainer.classList.add('typing-fade-out');
                    }

                    setTimeout(() => {
                        if (typingContainer) {
                            typingContainer.style.display = 'none';
                        }
                        revealChapterStage();
                    }, 600);
                }, 1600);
            }
        }

        setTimeout(typeNextLetter, 500);
    }

    // ==========================================================================
    // 7. Staged Chapter & Dot Transition Controller
    // ==========================================================================
    function revealChapterStage() {
        if (!chapterStage) return;

        chapterStage.classList.add('visible');
        initDotsPosition(0);
        applyTheme(0);
        updateCardContent(0, true);
        if (chapterCard) {
            chapterCard.classList.add('card-enter');
        }
    }

    function applyTheme(stepIndex) {
        const meta = MILESTONES[stepIndex];
        if (!meta) return;
        document.body.className = meta.theme || 'theme-crimson';
    }

    function initDotsPosition(stepIndex) {
        bDots = document.querySelectorAll('.b-dot');
        if (!bDots || bDots.length === 0) return;

        bDots.forEach((dot, idx) => {
            dot.classList.remove('active', 'completed', 'burst');
            if (idx === stepIndex) {
                dot.classList.add('active');
            } else if (idx < stepIndex) {
                dot.classList.add('completed');
            }
        });

        const activeDot = bDots[stepIndex];
        const firstDot = bDots[0];
        if (activeDot && firstDot && trackLineActive && trackSparkRunner && backdropDots) {
            const trackRect = backdropDots.getBoundingClientRect();
            const dotRect = activeDot.getBoundingClientRect();
            const firstRect = firstDot.getBoundingClientRect();

            const leftPos = dotRect.left - trackRect.left + (dotRect.width / 2);
            const firstLeft = firstRect.left - trackRect.left + (firstRect.width / 2);

            trackSparkRunner.style.left = `${leftPos}px`;
            trackLineActive.style.left = `${firstLeft}px`;
            trackLineActive.style.width = `${Math.max(0, leftPos - firstLeft)}px`;
        }
    }

    function updateCardContent(stepIndex, runDecoder = true) {
        const data = MILESTONES[stepIndex];
        if (!data) return;

        if (cardStepBadge) cardStepBadge.textContent = data.badge;
        if (cardStepCounter) cardStepCounter.textContent = data.counter;
        if (cardStepBody) cardStepBody.textContent = data.body;

        if (runDecoder && cardStepTitle) {
            decodeText(cardStepTitle, data.title, 550);
        } else if (cardStepTitle) {
            cardStepTitle.textContent = data.title;
        }

        // Configure Attached Media Button (Never auto-plays: click to trigger)
        const mediaType = (data.media_type || '').toLowerCase();
        if (cardMediaTriggerWrap) {
            if (mediaType && mediaType !== 'none' && data.media_url) {
                cardMediaTriggerWrap.style.display = 'flex';
                if (mediaType === 'image') {
                    if (cardMediaIcon) cardMediaIcon.textContent = '👁';
                    if (cardMediaLabel) cardMediaLabel.textContent = 'SHOW MEMORY IMAGE';
                } else if (mediaType === 'video') {
                    if (cardMediaIcon) cardMediaIcon.textContent = '🎬';
                    if (cardMediaLabel) cardMediaLabel.textContent = 'WATCH VIDEO';
                } else if (mediaType === 'audio') {
                    if (cardMediaIcon) cardMediaIcon.textContent = '▶';
                    if (cardMediaLabel) cardMediaLabel.textContent = 'PLAY AUDIO MESSAGE';
                }
            } else {
                cardMediaTriggerWrap.style.display = 'none';
            }
        }

        // Show/Hide Dedicated Below-Card Reply for Viewer (Glory)
        if (cardReplyTriggerWrap) {
            cardReplyTriggerWrap.style.display = currentRole === 'viewer' ? 'flex' : 'none';
        }

        if (prevStepBtn) {
            prevStepBtn.style.visibility = stepIndex === 0 ? 'hidden' : 'visible';
        }

        // Show/Hide Supernova Ignite Button on Finale
        if (igniteWrap) {
            igniteWrap.style.display = stepIndex === totalSteps - 1 ? 'flex' : 'none';
        }

        if (nextBtnText) {
            if (stepIndex === totalSteps - 1) {
                nextBtnText.textContent = "Start Over ↺";
            } else {
                nextBtnText.textContent = "Next Chapter";
            }
        }
    }

    // Media Button Trigger
    if (cardMediaBtn) {
        cardMediaBtn.addEventListener('click', () => {
            const data = MILESTONES[currentStep];
            if (!data || !data.media_url) return;
            openMediaModal(data);
        });
    }

    // Media Modal Controls
    function openMediaModal(data) {
        if (!mediaModal) return;
        const mediaType = (data.media_type || '').toLowerCase();

        // Reset visibility
        if (mediaPaneImage) mediaPaneImage.style.display = 'none';
        if (mediaPaneVideo) mediaPaneVideo.style.display = 'none';
        if (mediaPaneAudio) mediaPaneAudio.style.display = 'none';

        if (lightboxVideo) lightboxVideo.pause();
        if (lightboxAudio) lightboxAudio.pause();

        if (mediaTitleText) mediaTitleText.textContent = data.title || 'CHAPTER MEDIA';

        if (mediaType === 'image') {
            if (mediaBadgeLabel) mediaBadgeLabel.textContent = '// MEMORY PHOTOGRAPH';
            if (lightboxImage) lightboxImage.src = data.media_url;
            if (mediaPaneImage) mediaPaneImage.style.display = 'block';
        } else if (mediaType === 'video') {
            if (mediaBadgeLabel) mediaBadgeLabel.textContent = '// VIDEO HIGHLIGHT';
            if (lightboxVideoSrc) lightboxVideoSrc.src = data.media_url;
            if (lightboxVideo) {
                lightboxVideo.load();
            }
            if (mediaPaneVideo) mediaPaneVideo.style.display = 'block';
        } else if (mediaType === 'audio') {
            if (mediaBadgeLabel) mediaBadgeLabel.textContent = '// AUDIO RECORDING';
            if (lightboxAudio) lightboxAudio.src = data.media_url;
            if (lightboxAudioTitle) lightboxAudioTitle.textContent = data.media_name || 'Personal Audio Note';
            if (lightboxAudio) {
                lightboxAudio.load();
            }
            if (mediaPaneAudio) mediaPaneAudio.style.display = 'flex';
        }

        mediaModal.style.display = 'flex';
        playLaserWhoosh();
    }

    function closeMediaModal() {
        if (!mediaModal) return;
        mediaModal.style.display = 'none';
        if (lightboxVideo) lightboxVideo.pause();
        if (lightboxAudio) lightboxAudio.pause();
    }

    if (mediaModalCloseBtn) {
        mediaModalCloseBtn.addEventListener('click', closeMediaModal);
    }
    if (mediaModal) {
        mediaModal.addEventListener('click', (e) => {
            if (e.target === mediaModal) closeMediaModal();
        });
    }

    // Supernova Climax Celebration Button
    if (supernovaBtn) {
        supernovaBtn.addEventListener('click', () => {
            if (supernovaFlash) {
                supernovaFlash.classList.add('active');
                setTimeout(() => supernovaFlash.classList.remove('active'), 600);
            }

            if (giantWord) {
                giantWord.classList.add('blaze-gold');
            }

            if (sceneContainer) {
                sceneContainer.classList.add('impact-shake');
                setTimeout(() => sceneContainer.classList.remove('impact-shake'), 300);
            }

            launchCelebrationFireworks(6);
            playSupernovaFanfare();
        });
    }

    // STAGED TRANSITION
    function transitionToStep(targetIndex) {
        if (isTransitioning) return;
        isTransitioning = true;

        if (nextStepBtn) nextStepBtn.disabled = true;

        playLaserWhoosh();
        if (anamorphicFlare) {
            anamorphicFlare.classList.add('flare-burst');
            setTimeout(() => anamorphicFlare.classList.remove('flare-burst'), 500);
        }

        if (sceneContainer) {
            sceneContainer.classList.add('camera-warp');
            setTimeout(() => sceneContainer.classList.remove('camera-warp'), 650);
        }

        if (chapterCard) {
            chapterCard.classList.remove('card-enter');
            chapterCard.classList.add('card-exit');
        }

        if (backdropDots) {
            backdropDots.classList.add('dots-spotlight');
        }

        setTimeout(() => {
            animateDotChange(targetIndex, () => {
                setTimeout(() => {
                    currentStep = targetIndex;
                    applyTheme(currentStep);
                    updateCardContent(currentStep, true);

                    if (currentStep === totalSteps - 1) {
                        launchCelebrationFireworks(3);
                    } else if (giantWord) {
                        giantWord.classList.remove('blaze-gold');
                    }

                    if (backdropDots) {
                        backdropDots.classList.remove('dots-spotlight');
                    }

                    if (chapterCard) {
                        chapterCard.classList.remove('card-exit');
                        chapterCard.classList.add('card-enter');
                    }

                    isTransitioning = false;
                    if (nextStepBtn) nextStepBtn.disabled = false;
                }, 240);
            });
        }, 280);
    }

    function animateDotChange(targetIndex, onComplete) {
        bDots = document.querySelectorAll('.b-dot');
        const targetDot = bDots[targetIndex];
        const firstDot = bDots[0];

        if (!targetDot || !firstDot || !backdropDots) {
            onComplete();
            return;
        }

        const trackRect = backdropDots.getBoundingClientRect();
        const dotRect = targetDot.getBoundingClientRect();
        const firstRect = firstDot.getBoundingClientRect();

        const targetLeft = dotRect.left - trackRect.left + (dotRect.width / 2);
        const firstLeft = firstRect.left - trackRect.left + (firstRect.width / 2);

        if (trackSparkRunner) {
            trackSparkRunner.classList.add('spark-active');
            trackSparkRunner.style.left = `${targetLeft}px`;
        }

        if (trackLineActive) {
            trackLineActive.style.width = `${Math.max(0, targetLeft - firstLeft)}px`;
        }

        setTimeout(() => {
            const dotScreenX = dotRect.left + (dotRect.width / 2);
            const dotScreenY = dotRect.top + (dotRect.height / 2);
            triggerShockwave(dotScreenX, dotScreenY);

            if (sceneContainer) {
                sceneContainer.classList.add('impact-shake');
                setTimeout(() => sceneContainer.classList.remove('impact-shake'), 260);
            }

            playImpactThud(targetIndex === totalSteps - 1);

            bDots.forEach((dot, idx) => {
                dot.classList.remove('active', 'burst');
                if (idx < targetIndex) {
                    dot.classList.add('completed');
                } else if (idx === targetIndex) {
                    dot.classList.remove('completed');
                    dot.classList.add('active', 'burst');
                } else {
                    dot.classList.remove('completed');
                }
            });

            if (trackSparkRunner) {
                setTimeout(() => trackSparkRunner.classList.remove('spark-active'), 200);
            }

            setTimeout(() => {
                onComplete();
            }, 360);
        }, 450);
    }

    if (nextStepBtn) {
        nextStepBtn.addEventListener('click', () => {
            const nextIndex = (currentStep + 1) % totalSteps;
            transitionToStep(nextIndex);
        });
    }

    if (prevStepBtn) {
        prevStepBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                transitionToStep(currentStep - 1);
            }
        });
    }

    window.addEventListener('resize', () => {
        initDotsPosition(currentStep);
    });

    // ==========================================================================
    // 8. Admin Studio CMS Drawer Controller (Yash)
    // ==========================================================================
    function populateStudioForm() {
        if (!siteConfig) return;
        if (adminHeadline1) adminHeadline1.value = siteConfig.headline_word1 || 'HAPPY';
        if (adminHeadline2) adminHeadline2.value = siteConfig.headline_word2 || 'BIRTHDAY';
        if (adminGiantWord) adminGiantWord.value = siteConfig.giant_word || 'YASH';
        if (adminTopBadge) adminTopBadge.value = siteConfig.top_badge || 'NEXT LEVEL UI / UX';
        if (adminTypingText) adminTypingText.value = siteConfig.typing_text || '';

        renderStudioChapterButtons(0);
        loadChapterIntoStudio(0);
    }

    function renderStudioChapterButtons(activeIdx = 0) {
        if (!chapterSelectorBar) return;
        chapterSelectorBar.innerHTML = '';

        MILESTONES.forEach((chap, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `btn-chapter-sel ${idx === activeIdx ? 'active' : ''}`;
            btn.setAttribute('data-step', idx);
            btn.innerHTML = `<span class="sel-num">${String(idx + 1).padStart(2, '0')}</span> Card ${idx + 1}`;
            btn.addEventListener('click', () => {
                loadChapterIntoStudio(idx);
            });
            chapterSelectorBar.appendChild(btn);
        });

        if (addChapterBtn) {
            chapterSelectorBar.appendChild(addChapterBtn);
        }
    }

    function updateEditorMediaPreview(type, url, name) {
        if (!editorMediaPreviewWrap) return;

        // Reset all previews
        if (editorImagePreview) {
            editorImagePreview.src = '';
            editorImagePreview.style.display = 'none';
        }
        if (editorVideoPreview) {
            editorVideoPreview.src = '';
            editorVideoPreview.pause();
            editorVideoPreview.style.display = 'none';
        }
        if (editorAudioPreviewBox) {
            editorAudioPreviewBox.style.display = 'none';
        }
        if (editorAudioPreview) {
            editorAudioPreview.src = '';
            editorAudioPreview.pause();
        }

        const normType = (type || '').toLowerCase();
        if (normType === 'image' && url) {
            editorImagePreview.src = url;
            editorImagePreview.style.display = 'block';
            editorMediaPreviewWrap.style.display = 'block';
        } else if (normType === 'video' && url) {
            editorVideoPreview.src = url;
            editorVideoPreview.style.display = 'block';
            editorMediaPreviewWrap.style.display = 'block';
        } else if (normType === 'audio' && url) {
            editorAudioPreview.src = url;
            const titleEl = document.getElementById('editorAudioTitle');
            if (titleEl) titleEl.textContent = name || 'Audio Message Preview';
            editorAudioPreviewBox.style.display = 'flex';
            editorMediaPreviewWrap.style.display = 'block';
        } else {
            editorMediaPreviewWrap.style.display = 'none';
        }
    }

    function loadChapterIntoStudio(stepIdx) {
        const chap = MILESTONES[stepIdx];
        if (!chap) return;

        if (adminCurrentStepIndex) adminCurrentStepIndex.value = stepIdx;
        if (adminCardBadge) adminCardBadge.value = chap.badge || '';
        if (adminCardCounter) adminCardCounter.value = chap.counter || '';
        if (adminCardTitle) adminCardTitle.value = chap.title || '';
        if (adminCardBody) adminCardBody.value = chap.body || '';
        if (adminCardTheme) adminCardTheme.value = chap.theme || 'theme-crimson';

        // Load media attachment state
        tempMediaUrl = chap.media_url || '';
        tempMediaType = chap.media_type || 'none';
        tempMediaName = chap.media_name || '';

        if (tempMediaType !== 'none' && tempMediaUrl) {
            if (currentMediaText) currentMediaText.textContent = `Attached: [${tempMediaType.toUpperCase()}] ${tempMediaName || 'Media File'}`;
            if (adminRemoveMediaBtn) adminRemoveMediaBtn.style.display = 'inline-flex';
        } else {
            if (currentMediaText) currentMediaText.textContent = 'No media attached';
            if (adminRemoveMediaBtn) adminRemoveMediaBtn.style.display = 'none';
        }

        // Live visual preview
        updateEditorMediaPreview(tempMediaType, tempMediaUrl, tempMediaName);

        // Highlight active chapter button
        if (chapterSelectorBar) {
            const buttons = chapterSelectorBar.querySelectorAll('.btn-chapter-sel');
            buttons.forEach(btn => {
                btn.classList.toggle('active', parseInt(btn.dataset.step, 10) === stepIdx);
            });
        }

        // Delete button visibility safety check (always keep at least 1 card)
        if (adminDeleteChapterBtn) {
            adminDeleteChapterBtn.style.display = MILESTONES.length > 1 ? 'inline-flex' : 'none';
        }
    }

    // Add New Chapter Card
    if (addChapterBtn) {
        addChapterBtn.addEventListener('click', async () => {
            try {
                addChapterBtn.disabled = true;
                const res = await fetch('/api/admin/chapter/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await res.json();
                if (data.status === 'success') {
                    MILESTONES = data.chapters;
                    totalSteps = MILESTONES.length;
                    const newIdx = MILESTONES.length - 1;

                    renderDots();
                    renderStudioChapterButtons(newIdx);
                    loadChapterIntoStudio(newIdx);
                    showToast(`✨ Chapter Card 0${newIdx + 1} added!`);
                    playLaserWhoosh();
                } else {
                    showToast('Failed to add chapter card.');
                }
            } catch (err) {
                console.error(err);
                showToast('Network error adding card.');
            } finally {
                addChapterBtn.disabled = false;
            }
        });
    }

    // Delete Current Chapter Card
    if (adminDeleteChapterBtn) {
        adminDeleteChapterBtn.addEventListener('click', async () => {
            if (MILESTONES.length <= 1) {
                showToast('At least one chapter card must remain.');
                return;
            }
            const stepIdx = parseInt(adminCurrentStepIndex.value, 10);
            if (!confirm(`Are you sure you want to permanently delete Card 0${stepIdx + 1}?`)) {
                return;
            }

            try {
                adminDeleteChapterBtn.disabled = true;
                const res = await fetch(`/api/admin/chapter/${stepIdx}`, {
                    method: 'DELETE'
                });
                const data = await res.json();
                if (data.status === 'success') {
                    MILESTONES = data.chapters;
                    totalSteps = MILESTONES.length;

                    // If currently viewing deleted step or beyond, clamp it
                    if (currentStep >= totalSteps) {
                        currentStep = Math.max(0, totalSteps - 1);
                    }
                    applyTheme(currentStep);
                    updateCardContent(currentStep, false);

                    const nextStudioIdx = Math.min(stepIdx, MILESTONES.length - 1);
                    renderDots();
                    renderStudioChapterButtons(nextStudioIdx);
                    loadChapterIntoStudio(nextStudioIdx);
                    showToast(`Card 0${stepIdx + 1} deleted.`);
                } else {
                    showToast('Failed to delete chapter card.');
                }
            } catch (err) {
                console.error(err);
                showToast('Network error deleting card.');
            } finally {
                adminDeleteChapterBtn.disabled = false;
            }
        });
    }

    // File Upload Handler
    if (adminFileInput) {
        adminFileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            if (uploadProgress) uploadProgress.style.display = 'block';
            if (uploadProgressFill) uploadProgressFill.style.width = '40%';

            try {
                const res = await fetch('/api/admin/upload', {
                    method: 'POST',
                    body: formData
                });
                if (uploadProgressFill) uploadProgressFill.style.width = '100%';

                const data = await res.json();
                if (res.ok && data.status === 'success') {
                    tempMediaUrl = data.url;
                    tempMediaType = data.media_type;
                    tempMediaName = data.filename;

                    if (currentMediaText) currentMediaText.textContent = `Attached: [${data.media_type.toUpperCase()}] ${data.filename}`;
                    if (adminRemoveMediaBtn) adminRemoveMediaBtn.style.display = 'inline-flex';
                    updateEditorMediaPreview(tempMediaType, tempMediaUrl, tempMediaName);
                    showToast(`Media attached: ${data.filename} ✦`);
                } else {
                    const errorMsg = data.detail || 'Media upload failed. Ensure Supabase credentials are configured.';
                    showToast(errorMsg);
                }
            } catch (err) {
                console.error(err);
                showToast('Network error during media upload.');
            } finally {
                setTimeout(() => {
                    if (uploadProgress) uploadProgress.style.display = 'none';
                    if (uploadProgressFill) uploadProgressFill.style.width = '0%';
                }, 500);
            }
        });
    }

    // Detach Media
    if (adminRemoveMediaBtn) {
        adminRemoveMediaBtn.addEventListener('click', () => {
            tempMediaUrl = '';
            tempMediaType = 'none';
            tempMediaName = '';
            if (currentMediaText) currentMediaText.textContent = 'No media attached';
            adminRemoveMediaBtn.style.display = 'none';
            updateEditorMediaPreview('none', '', '');
            showToast('Media detached. Click Save to apply changes.');
        });
    }

    // Save Chapter Card
    if (adminChapterForm) {
        adminChapterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const stepIdx = parseInt(adminCurrentStepIndex.value, 10);
            const payload = {
                step_index: stepIdx,
                badge: adminCardBadge.value.trim(),
                counter: adminCardCounter.value.trim(),
                title: adminCardTitle.value.trim(),
                body: adminCardBody.value.trim(),
                theme: adminCardTheme.value,
                media_type: tempMediaType || 'none',
                media_url: tempMediaUrl || '',
                media_name: tempMediaName || ''
            };

            try {
                const res = await fetch('/api/admin/chapter', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (result.status === 'success') {
                    MILESTONES[stepIdx] = result.data;
                    if (currentStep === stepIdx) {
                        applyTheme(stepIdx);
                        updateCardContent(stepIdx, false);
                    }
                    showToast(`Card 0${stepIdx + 1} updated! ✦`);
                }
            } catch (err) {
                console.error(err);
                showToast('Failed to save chapter card.');
            }
        });
    }

    // Save Site Texts
    if (adminTextsForm) {
        adminTextsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                headline_word1: adminHeadline1.value.trim() || 'HAPPY',
                headline_word2: adminHeadline2.value.trim() || 'BIRTHDAY',
                giant_word: adminGiantWord.value.trim() || 'YASH',
                top_badge: adminTopBadge.value.trim() || 'NEXT LEVEL UI / UX',
                typing_text: adminTypingText.value.trim()
            };

            try {
                const res = await fetch('/api/admin/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (result.status === 'success') {
                    siteConfig = result.data;
                    if (headlineWord1) headlineWord1.textContent = siteConfig.headline_word1;
                    if (headlineWord2) headlineWord2.textContent = siteConfig.headline_word2;
                    if (giantWord) giantWord.textContent = siteConfig.giant_word;
                    if (topBadgeText) topBadgeText.textContent = siteConfig.top_badge;
                    if (typedTextEl) typedTextEl.setAttribute('data-text', siteConfig.typing_text);
                    showToast('Site texts saved successfully! ✦');
                }
            } catch (err) {
                console.error(err);
                showToast('Failed to update texts.');
            }
        });
    }

    // Studio Drawer Open/Close
    if (adminStudioBtn && adminDrawerBackdrop) {
        adminStudioBtn.addEventListener('click', () => {
            adminDrawerBackdrop.classList.add('drawer-open');
            fetchAndRenderRichReplies();
        });
    }

    if (adminDrawerCloseBtn && adminDrawerBackdrop) {
        adminDrawerCloseBtn.addEventListener('click', () => {
            adminDrawerBackdrop.classList.remove('drawer-open');
        });
    }

    if (adminDrawerBackdrop) {
        adminDrawerBackdrop.addEventListener('click', (e) => {
            if (e.target === adminDrawerBackdrop) {
                adminDrawerBackdrop.classList.remove('drawer-open');
            }
        });
    }

    // Studio Tab Switching
    studioTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;
            studioTabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const pane = document.getElementById(targetTab);
            if (pane) pane.classList.add('active');
        });
    });

    // ==========================================================================
    // 9. Dedicated Replies Modal & Rich Inbox Engine (Yash)
    // ==========================================================================
    async function fetchAndRenderRichReplies() {
        try {
            const res = await fetch('/api/admin/replies');
            const data = await res.json();
            if (data.status !== 'success') return;
            const replies = data.data || [];

            // Update badge counters
            if (headerRepliesCount) headerRepliesCount.textContent = replies.length;
            if (repliesBadgeCount) repliesBadgeCount.textContent = replies.length;

            // Render Studio Drawer simple list if present
            if (adminRepliesList) {
                if (replies.length === 0) {
                    adminRepliesList.innerHTML = '<div class="empty-replies">No messages received yet from Glory.</div>';
                } else {
                    adminRepliesList.innerHTML = '';
                    replies.forEach(r => {
                        const item = document.createElement('div');
                        item.className = 'reply-item-card';
                        const contextBadge = r.chapter_title ? `<span class="reply-context-badge">📍 Card 0${(r.chapter_index != null ? r.chapter_index + 1 : '')}: ${r.chapter_title}</span>` : '';
                        item.innerHTML = `
                            <div class="reply-item-meta">
                                <span class="reply-sender-name">💌 ${r.sender}</span>
                                <span class="reply-time">${r.created_at || 'Recent'}</span>
                            </div>
                            ${contextBadge}
                            <p class="reply-item-content">${r.message}</p>
                        `;
                        adminRepliesList.appendChild(item);
                    });
                }
            }

            // Render Dedicated Modal Rich Container with Uploaded Card Media
            if (richRepliesContainer) {
                if (replies.length === 0) {
                    richRepliesContainer.innerHTML = `
                        <div class="empty-replies" style="padding: 40px 20px; text-align: center; color: rgba(255,255,255,0.4);">
                            <div style="font-size: 32px; margin-bottom: 12px;">📭</div>
                            <p>No messages received yet from Glory.</p>
                        </div>
                    `;
                    return;
                }

                richRepliesContainer.innerHTML = '';
                replies.forEach(r => {
                    const card = document.createElement('div');
                    card.className = 'rich-reply-card';

                    // Attached card uploaded media preview
                    let mediaHtml = '';
                    const mediaType = (r.media_type || '').toLowerCase();
                    const mediaUrl = r.media_url || '';
                    const cardTitle = r.card_title || r.chapter_title || '';

                    if (r.chapter_index != null || cardTitle) {
                        let mediaContentHtml = '';
                        if (mediaType === 'image' && mediaUrl) {
                            mediaContentHtml = `
                                <div class="rich-reply-media-box">
                                    <div class="media-box-label">Attached Card Memory (Photo):</div>
                                    <img src="${mediaUrl}" class="rich-reply-thumb" alt="Memory Photo" onclick="window.open('${mediaUrl}', '_blank')" title="Click to view full photo">
                                </div>
                            `;
                        } else if (mediaType === 'video' && mediaUrl) {
                            mediaContentHtml = `
                                <div class="rich-reply-media-box">
                                    <div class="media-box-label">Attached Card Memory (Video):</div>
                                    <video src="${mediaUrl}" controls class="rich-reply-video" preload="metadata"></video>
                                </div>
                            `;
                        } else if (mediaType === 'audio' && mediaUrl) {
                            mediaContentHtml = `
                                <div class="rich-reply-media-box">
                                    <div class="media-box-label">Attached Card Memory (Audio): ${r.media_name || ''}</div>
                                    <audio src="${mediaUrl}" controls class="rich-reply-audio" preload="metadata"></audio>
                                </div>
                            `;
                        } else {
                            mediaContentHtml = `
                                <div class="rich-reply-media-box text-only-box">
                                    <span class="media-box-label">Card Story: "${cardTitle}"</span>
                                </div>
                            `;
                        }

                        mediaHtml = `
                            <div class="rich-reply-context-banner">
                                <span class="context-pill">📍 REPLIED TO CARD 0${r.chapter_index != null ? r.chapter_index + 1 : ''}</span>
                                <span class="context-title">${cardTitle}</span>
                            </div>
                            ${mediaContentHtml}
                        `;
                    }

                    card.innerHTML = `
                        <div class="rich-reply-header">
                            <div class="rich-reply-author">
                                <span class="reply-avatar">💌</span>
                                <div>
                                    <div class="author-name">${r.sender}</div>
                                    <div class="reply-timestamp">${r.created_at || 'Just now'}</div>
                                </div>
                            </div>
                        </div>
                        <div class="rich-reply-body">
                            "${r.message}"
                        </div>
                        ${mediaHtml}
                    `;
                    richRepliesContainer.appendChild(card);
                });
            }
        } catch (err) {
            console.error('Error fetching rich replies:', err);
        }
    }

    if (refreshRepliesBtn) {
        refreshRepliesBtn.addEventListener('click', () => {
            fetchAndRenderRichReplies();
            showToast('Inbox refreshed ✦');
        });
    }

    // Dedicated Admin View Replies Button & Modal
    if (adminViewRepliesBtn && adminRepliesModal) {
        adminViewRepliesBtn.addEventListener('click', () => {
            adminRepliesModal.style.display = 'flex';
            fetchAndRenderRichReplies();
        });
    }

    if (adminRepliesModalCloseBtn && adminRepliesModal) {
        adminRepliesModalCloseBtn.addEventListener('click', () => {
            adminRepliesModal.style.display = 'none';
        });
    }

    if (modalRefreshRepliesBtn) {
        modalRefreshRepliesBtn.addEventListener('click', () => {
            fetchAndRenderRichReplies();
            showToast('Replies updated ✦');
        });
    }

    if (adminRepliesModal) {
        adminRepliesModal.addEventListener('click', (e) => {
            if (e.target === adminRepliesModal) adminRepliesModal.style.display = 'none';
        });
    }

    // ==========================================================================
    // 10. Glory's Reply Modal Controller (Dedicated Below-Card + Header)
    // ==========================================================================
    // Triggered via Top Header
    if (gloryReplyBtn && replyModal) {
        gloryReplyBtn.addEventListener('click', () => {
            if (gloryChapterIndex) gloryChapterIndex.value = '';
            if (gloryChapterTitle) gloryChapterTitle.value = '';
            if (replyCardContextWrap) replyCardContextWrap.style.display = 'none';
            replyModal.style.display = 'flex';
            if (gloryMessageText) gloryMessageText.focus();
        });
    }

    // Triggered via Dedicated Button Below Current Chapter Card
    if (cardReplyBtn && replyModal) {
        cardReplyBtn.addEventListener('click', () => {
            const chap = MILESTONES[currentStep];
            if (gloryChapterIndex) gloryChapterIndex.value = currentStep;
            if (gloryChapterTitle) gloryChapterTitle.value = chap ? (chap.title || `Card 0${currentStep + 1}`) : `Card 0${currentStep + 1}`;

            if (replyCardContextWrap) replyCardContextWrap.style.display = 'flex';
            if (replyContextTag) replyContextTag.textContent = `Card 0${currentStep + 1}`;
            if (replyContextTitle) replyContextTitle.textContent = chap ? chap.title : '';

            replyModal.style.display = 'flex';
            if (gloryMessageText) gloryMessageText.focus();
        });
    }

    if (replyModalCloseBtn && replyModal) {
        replyModalCloseBtn.addEventListener('click', () => {
            replyModal.style.display = 'none';
        });
    }

    if (replyModal) {
        replyModal.addEventListener('click', (e) => {
            if (e.target === replyModal) replyModal.style.display = 'none';
        });
    }

    if (gloryReplyForm) {
        gloryReplyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const msg = gloryMessageText.value.trim();
            if (!msg) return;

            const payload = {
                sender: glorySenderName ? glorySenderName.value : (currentUser || 'Glory'),
                message: msg,
                chapter_index: gloryChapterIndex && gloryChapterIndex.value !== '' ? parseInt(gloryChapterIndex.value, 10) : null,
                chapter_title: gloryChapterTitle ? gloryChapterTitle.value : null
            };

            try {
                const res = await fetch('/api/viewer/reply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    gloryMessageText.value = '';
                    replyModal.style.display = 'none';
                    showToast('Message transmitted to Yash! ✦');
                    playSupernovaFanfare();
                }
            } catch (err) {
                console.error('Failed to submit reply:', err);
                showToast('Failed to send message.');
            }
        });
    }

    // ==========================================================================
    // 10. Viewport & Parallax Engine + Stardust Comet Trails
    // ==========================================================================
    let targetX = width / 2;
    let targetY = height / 2;
    let currentX = targetX;
    let currentY = targetY;
    let isTouching = false;
    let hasInteracted = false;

    function dismissHint() {
        if (!hasInteracted && touchHint) {
            hasInteracted = true;
            touchHint.style.opacity = '0';
            setTimeout(() => {
                touchHint.style.display = 'none';
            }, 600);
        }
    }

    window.addEventListener('mousemove', (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
        addStardust(e.clientX, e.clientY);
        dismissHint();
    });

    window.addEventListener('touchstart', (e) => {
        isTouching = true;
        dismissHint();
        initAudio();
        if (e.touches && e.touches[0]) {
            targetX = e.touches[0].clientX;
            targetY = e.touches[0].clientY;
            addStardust(e.touches[0].clientX, e.touches[0].clientY);
        }
        if (navigator.vibrate) {
            try { navigator.vibrate(8); } catch (_) {}
        }
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        if (e.touches && e.touches[0]) {
            targetX = e.touches[0].clientX;
            targetY = e.touches[0].clientY;
            addStardust(e.touches[0].clientX, e.touches[0].clientY);
        }
    }, { passive: true });

    window.addEventListener('touchend', () => {
        isTouching = false;
        setTimeout(() => {
            if (!isTouching) {
                targetX = width / 2;
                targetY = height / 2;
            }
        }, 1500);
    }, { passive: true });

    function render() {
        const lerpFactor = isTouching ? 0.14 : 0.08;
        currentX += (targetX - currentX) * lerpFactor;
        currentY += (targetY - currentY) * lerpFactor;

        if (ambientSpotlight) {
            const spotOffset = window.innerWidth <= 600 ? 190 : 320;
            ambientSpotlight.style.transform = `translate(${currentX - spotOffset}px, ${currentY - spotOffset}px)`;
        }

        const deltaX = (currentX - width / 2) / (width / 2);
        const deltaY = (currentY - height / 2) / (height / 2);

        if (cardHoloSheen) {
            const sheenX = ((currentX / width) * 100).toFixed(1);
            const sheenY = ((currentY / height) * 100).toFixed(1);
            cardHoloSheen.style.background = `radial-gradient(circle 350px at ${sheenX}% ${sheenY}%, rgba(255, 255, 255, 0.08), transparent 70%)`;
        }

        if (giantBackdrop) {
            const bgMaxX = window.innerWidth <= 600 ? 16 : 24;
            const bgMaxY = window.innerWidth <= 600 ? 12 : 18;
            const bgShiftX = -deltaX * bgMaxX;
            const bgShiftY = -deltaY * bgMaxY;
            giantBackdrop.style.transform = `translate(calc(-50% + ${bgShiftX}px), calc(-50% + ${bgShiftY}px))`;
        }

        if (foregroundContent) {
            const rotX = -deltaY * (window.innerWidth <= 600 ? 8 : 7);
            const rotY = deltaX * (window.innerWidth <= 600 ? 10 : 8);
            const fgShiftX = deltaX * (window.innerWidth <= 600 ? 10 : 14);
            const fgShiftY = deltaY * (window.innerWidth <= 600 ? 8 : 10);

            foregroundContent.style.transform = `translate(${fgShiftX}px, ${fgShiftY}px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(30px)`;
        }

        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', (e) => {
            if (!isTouching && e.gamma !== null && e.beta !== null) {
                const tiltX = Math.min(Math.max(e.gamma, -25), 25) / 25;
                const tiltY = Math.min(Math.max(e.beta - 45, -25), 25) / 25;

                targetX = (width / 2) + (tiltX * (width * 0.45));
                targetY = (height / 2) + (tiltY * (height * 0.45));
            }
        });
    }

    // ==========================================================================
    // 11. Initial Application Boot
    // ==========================================================================
    fetchSiteContent().then(() => {
        checkAuth();
    });
});
