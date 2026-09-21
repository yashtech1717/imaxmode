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
    const dotsPrevBtn = document.getElementById('dotsPrevBtn');
    const dotsNextBtn = document.getElementById('dotsNextBtn');
    const dotsPageIndicator = document.getElementById('dotsPageIndicator');
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
    const cardFeedbackBtn = document.getElementById('cardFeedbackBtn');

    // Auth & Header Control Elements
    const authControls = document.getElementById('authControls');
    const userChipName = document.getElementById('userChipName');
    const adminStudioBtn = document.getElementById('adminStudioBtn');
    const adminViewRepliesBtn = document.getElementById('adminViewRepliesBtn');
    const adminLoginLogsBtn = document.getElementById('adminLoginLogsBtn');
    const adminFeedbackBtn = document.getElementById('adminFeedbackBtn');
    const headerRepliesCount = document.getElementById('headerRepliesCount');
    const gloryReplyBtn = document.getElementById('gloryReplyBtn');
    const gloryFeedbackBtn = document.getElementById('gloryFeedbackBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    // Login Portal Modal Elements
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const loginUsername = document.getElementById('loginUsername');
    const loginPassword = document.getElementById('loginPassword');
    const loginErrorMsg = document.getElementById('loginErrorMsg');
    const pwdToggleBtn = document.getElementById('pwdToggleBtn');
    const eyeOpenIcon = document.getElementById('eyeOpenIcon');
    const eyeSlashIcon = document.getElementById('eyeSlashIcon');

    // Admin Studio Drawer Elements
    const adminDrawerBackdrop = document.getElementById('adminDrawerBackdrop');
    const adminDrawerCloseBtn = document.getElementById('adminDrawerCloseBtn');
    const studioTabBtns = document.querySelectorAll('.studio-tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const repliesBadgeCount = document.getElementById('repliesBadgeCount');
    const logsBadgeCount = document.getElementById('logsBadgeCount');

    // Studio Tab 1: Texts
    const adminTextsForm = document.getElementById('adminTextsForm');
    const adminHeadline1 = document.getElementById('adminHeadline1');
    const adminHeadline2 = document.getElementById('adminHeadline2');
    const adminGiantWord = document.getElementById('adminGiantWord');
    const adminTopBadge = document.getElementById('adminTopBadge');
    const adminTypingText = document.getElementById('adminTypingText');

    // Studio Tab 2: Chapters & Media
    const chapterSelectorBar = document.getElementById('chapterSelectorBar');
    const studioPrevPageBtn = document.getElementById('studioPrevPageBtn');
    const studioNextPageBtn = document.getElementById('studioNextPageBtn');
    const studioPageIndicator = document.getElementById('studioPageIndicator');
    const addChapterBtn = document.getElementById('addChapterBtn');
    const adminDeleteChapterBtn = document.getElementById('adminDeleteChapterBtn');
    const reorderCurrentBadge = document.getElementById('reorderCurrentBadge');
    const adminCardTargetPosition = document.getElementById('adminCardTargetPosition');
    const btnMoveCardEarlier = document.getElementById('btnMoveCardEarlier');
    const btnMoveCardLater = document.getElementById('btnMoveCardLater');
    const btnApplyCardReorder = document.getElementById('btnApplyCardReorder');
    const adminChapterForm = document.getElementById('adminChapterForm');
    const adminCurrentStepIndex = document.getElementById('adminCurrentStepIndex');
    const adminCardBadge = document.getElementById('adminCardBadge');
    const adminCardCounter = document.getElementById('adminCardCounter');
    const adminCardTitle = document.getElementById('adminCardTitle');
    const adminCardBody = document.getElementById('adminCardBody');
    const adminCardTheme = document.getElementById('adminCardTheme');
    const themeSwatchesGrid = document.getElementById('themeSwatchesGrid');
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

    // Studio Tab 4: Login Logs
    const drawerLoginLogsList = document.getElementById('drawerLoginLogsList');
    const refreshDrawerLogsBtn = document.getElementById('refreshDrawerLogsBtn');

    // Studio Tab 5: Feedback & Ratings
    const feedbackBadgeCount = document.getElementById('feedbackBadgeCount');
    const refreshDrawerFeedbackBtn = document.getElementById('refreshDrawerFeedbackBtn');
    const drawerActiveQuestionText = document.getElementById('drawerActiveQuestionText');
    const adminNewQuestionForm = document.getElementById('adminNewQuestionForm');
    const adminNewQuestionInput = document.getElementById('adminNewQuestionInput');
    const adminPublishQuestionBtn = document.getElementById('adminPublishQuestionBtn');
    const drawerAvgRating = document.getElementById('drawerAvgRating');
    const drawerTotalFeedbackCount = document.getElementById('drawerTotalFeedbackCount');
    const drawerFeedbackList = document.getElementById('drawerFeedbackList');

    // Dedicated Admin Replies Modal Elements
    const adminRepliesModal = document.getElementById('adminRepliesModal');
    const adminRepliesModalCloseBtn = document.getElementById('adminRepliesModalCloseBtn');
    const modalRefreshRepliesBtn = document.getElementById('modalRefreshRepliesBtn');
    const richRepliesContainer = document.getElementById('richRepliesContainer');
    const repliesCountPill = document.getElementById('repliesCountPill');

    // Dedicated Admin Login Logs Modal Elements
    const adminLogsModal = document.getElementById('adminLogsModal');
    const adminLogsModalCloseBtn = document.getElementById('adminLogsModalCloseBtn');
    const modalRefreshLogsBtn = document.getElementById('modalRefreshLogsBtn');
    const loginLogsContainer = document.getElementById('loginLogsContainer');
    const logsCountPill = document.getElementById('logsCountPill');

    // Dedicated Admin Feedback Modal Elements
    const adminFeedbackModal = document.getElementById('adminFeedbackModal');
    const adminFeedbackModalCloseBtn = document.getElementById('adminFeedbackModalCloseBtn');
    const modalRefreshFeedbackBtn = document.getElementById('modalRefreshFeedbackBtn');
    const adminFeedbackCountPill = document.getElementById('adminFeedbackCountPill');
    const adminModalAvgRating = document.getElementById('adminModalAvgRating');
    const adminModalTotalCount = document.getElementById('adminModalTotalCount');
    const adminModalFiveStarCount = document.getElementById('adminModalFiveStarCount');
    const adminModalActiveQuestionText = document.getElementById('adminModalActiveQuestionText');
    const adminFeedbackListContainer = document.getElementById('adminFeedbackListContainer');

    // Glory Feedback Modal Elements
    const feedbackModal = document.getElementById('feedbackModal');
    const feedbackModalCloseBtn = document.getElementById('feedbackModalCloseBtn');
    const viewerFeedbackQuestionText = document.getElementById('viewerFeedbackQuestionText');
    const gloryFeedbackForm = document.getElementById('gloryFeedbackForm');
    const feedbackQuestionId = document.getElementById('feedbackQuestionId');
    const selectedStarRating = document.getElementById('selectedStarRating');
    const starRatingGroup = document.getElementById('starRatingGroup');
    const ratingDescriptorText = document.getElementById('ratingDescriptorText');
    const feedbackCommentInput = document.getElementById('feedbackCommentInput');
    const feedbackSubmitBtn = document.getElementById('feedbackSubmitBtn');
    const feedbackSubmitBtnLabel = document.getElementById('feedbackSubmitBtnLabel');

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
    const videoPreloadOverlay = document.getElementById('videoPreloadOverlay');
    const videoPreloadBar = document.getElementById('videoPreloadBar');
    const videoPreloadPct = document.getElementById('videoPreloadPct');
    const videoPreloadBytes = document.getElementById('videoPreloadBytes');
    const videoSkipPreloadBtn = document.getElementById('videoSkipPreloadBtn');
    const videoTapToPlay = document.getElementById('videoTapToPlay');
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
    // 2. IMAX Theatrical Immersion & Audio Synthesizer Engine
    // ==========================================================================
    let isImaxActive = false;

    function playImaxBoom() {
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (!AudioContextClass) return;
            if (!audioCtx) audioCtx = new AudioContextClass();
            if (audioCtx.state === 'suspended') audioCtx.resume();

            const now = audioCtx.currentTime;

            // Deep Theatrical Sub-Bass Oscillator (75Hz -> 26Hz exponential sweep)
            const subOsc = audioCtx.createOscillator();
            const subGain = audioCtx.createGain();
            subOsc.type = 'sine';
            subOsc.frequency.setValueAtTime(75, now);
            subOsc.frequency.exponentialRampToValueAtTime(26, now + 1.8);

            subGain.gain.setValueAtTime(0.001, now);
            subGain.gain.linearRampToValueAtTime(0.85, now + 0.15);
            subGain.gain.exponentialRampToValueAtTime(0.0001, now + 2.8);

            // Harmonic Cinema Tone (140Hz -> 52Hz)
            const harmOsc = audioCtx.createOscillator();
            const harmGain = audioCtx.createGain();
            harmOsc.type = 'triangle';
            harmOsc.frequency.setValueAtTime(140, now);
            harmOsc.frequency.exponentialRampToValueAtTime(52, now + 1.6);

            harmGain.gain.setValueAtTime(0.001, now);
            harmGain.gain.linearRampToValueAtTime(0.35, now + 0.12);
            harmGain.gain.exponentialRampToValueAtTime(0.0001, now + 2.2);

            subOsc.connect(subGain);
            harmOsc.connect(harmGain);
            subGain.connect(audioCtx.destination);
            harmGain.connect(audioCtx.destination);

            subOsc.start(now);
            harmOsc.start(now);
            subOsc.stop(now + 2.9);
            harmOsc.stop(now + 2.3);
        } catch (err) {
            console.warn('IMAX Audio Boom error:', err);
        }
    }

    function toggleImaxMode() {
        isImaxActive = !isImaxActive;
        document.body.classList.toggle('imax-active', isImaxActive);

        if (isImaxActive) {
            if (fullscreenLabel) fullscreenLabel.textContent = "EXIT IMAX";
            playImaxBoom();
            triggerAnamorphicLaserSweep();
            showToast('IMAX THEATRICAL IMMERSION ENGAGED ✦');
            if (navigator.vibrate) try { navigator.vibrate(25); } catch (_) {}
            // Attempt native fullscreen where supported
            if (document.documentElement.requestFullscreen && !document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(() => {});
            }
        } else {
            if (fullscreenLabel) fullscreenLabel.textContent = "IMAX MODE";
            showToast('IMAX IMMERSION STANDBY');
            if (document.exitFullscreen && document.fullscreenElement) {
                document.exitFullscreen().catch(() => {});
            }
        }
    }

    if (fullscreenBtn && fullscreenLabel) {
        fullscreenBtn.addEventListener('click', () => {
            initAudio();
            toggleImaxMode();
        });

        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement && isImaxActive) {
                isImaxActive = false;
                document.body.classList.remove('imax-active');
                if (fullscreenLabel) fullscreenLabel.textContent = "IMAX MODE";
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

        function safeChar(ch) {
            if (ch === '&') return '&amp;';
            if (ch === '<') return '&lt;';
            if (ch === '>') return '&gt;';
            if (ch === '"') return '&quot;';
            if (ch === "'") return '&#039;';
            return ch;
        }

        function updateDecoder(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const revealedChars = Math.floor(progress * totalLength);

            let html = '';
            for (let i = 0; i < totalLength; i++) {
                if (i < revealedChars) {
                    html += `<span class="dec-char-done">${safeChar(targetText[i])}</span>`;
                } else if (targetText[i] === ' ') {
                    html += ' ';
                } else if (i === revealedChars) {
                    const sparkChar = GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
                    html += `<span class="dec-char-spark">${sparkChar}</span>`;
                } else {
                    const scrambleChar = GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
                    html += `<span class="dec-char-scramble">${scrambleChar}</span>`;
                }
            }

            element.innerHTML = html;

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

    const THEME_EMBER_PALETTES = {
        'theme-crimson': ['rgba(255, 42, 75,', 'rgba(255, 120, 140,', 'rgba(255, 215, 0,'],
        'theme-gold': ['rgba(255, 215, 0,', 'rgba(255, 180, 50,', 'rgba(255, 245, 160,'],
        'theme-cyan': ['rgba(0, 242, 254,', 'rgba(56, 189, 248,', 'rgba(147, 197, 253,'],
        'theme-aurora': ['rgba(168, 85, 247,', 'rgba(236, 72, 153,', 'rgba(192, 132, 252,'],
        'theme-emerald': ['rgba(16, 185, 129,', 'rgba(52, 211, 153,', 'rgba(110, 231, 183,'],
        'theme-amber': ['rgba(249, 115, 22,', 'rgba(251, 146, 60,', 'rgba(255, 215, 0,'],
        'theme-rose': ['rgba(244, 63, 94,', 'rgba(251, 113, 133,', 'rgba(253, 164, 175,'],
        'theme-ice': ['rgba(56, 189, 248,', 'rgba(186, 230, 253,', 'rgba(224, 242, 254,'],
        'theme-violet': ['rgba(139, 92, 246,', 'rgba(196, 181, 253,', 'rgba(167, 139, 250,'],
        'theme-silver': ['rgba(226, 232, 240,', 'rgba(255, 255, 255,', 'rgba(203, 213, 225,'],
        'theme-lime': ['rgba(132, 204, 22,', 'rgba(190, 242, 100,', 'rgba(217, 249, 157,'],
        'theme-magenta': ['rgba(217, 70, 239,', 'rgba(244, 114, 182,', 'rgba(251, 207, 232,'],
        'theme-sunset': ['rgba(255, 87, 34,', 'rgba(251, 146, 60,', 'rgba(254, 215, 170,'],
        'theme-teal': ['rgba(20, 184, 166,', 'rgba(45, 212, 191,', 'rgba(153, 246, 228,'],
        'theme-indigo': ['rgba(99, 102, 241,', 'rgba(165, 180, 252,', 'rgba(199, 210, 254,'],
        'theme-coral': ['rgba(251, 113, 133,', 'rgba(253, 164, 175,', 'rgba(254, 205, 211,'],
        'theme-mint': ['rgba(45, 212, 191,', 'rgba(94, 234, 212,', 'rgba(204, 251, 241,'],
        'theme-copper': ['rgba(217, 119, 6,', 'rgba(245, 158, 11,', 'rgba(253, 230, 138,']
    };
    let currentThemeEmberPalette = THEME_EMBER_PALETTES['theme-crimson'];

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
            const palette = currentThemeEmberPalette || THEME_EMBER_PALETTES['theme-crimson'];
            this.color = palette[Math.floor(Math.random() * palette.length)];
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
    const anamorphicBeams = [];

    function triggerAnamorphicLaserSweep(posY) {
        const y = posY != null ? posY : height * (0.35 + Math.random() * 0.3);
        anamorphicBeams.push({
            y: y,
            alpha: 1.0,
            height: Math.random() * 2.5 + 3,
            decay: 0.022,
            color: Math.random() > 0.4 ? 'rgba(245, 158, 11,' : 'rgba(56, 189, 248,'
        });
    }

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

        // 5. Anamorphic Laser Flare Sweeps
        for (let i = anamorphicBeams.length - 1; i >= 0; i--) {
            const b = anamorphicBeams[i];
            b.alpha -= b.decay;
            if (b.alpha <= 0) {
                anamorphicBeams.splice(i, 1);
                continue;
            }

            const grad = ctx.createLinearGradient(0, b.y, width, b.y);
            grad.addColorStop(0, 'rgba(0, 0, 0, 0)');
            grad.addColorStop(0.2, `${b.color} ${b.alpha * 0.4})`);
            grad.addColorStop(0.5, `rgba(255, 255, 255, ${b.alpha * 0.95})`);
            grad.addColorStop(0.8, `${b.color} ${b.alpha * 0.4})`);
            grad.addColorStop(1, 'rgba(0, 0, 0, 0)');

            ctx.save();
            ctx.fillStyle = grad;
            ctx.shadowBlur = 20;
            ctx.shadowColor = `${b.color} ${b.alpha})`;
            ctx.fillRect(0, b.y - b.height / 2, width, b.height);
            ctx.restore();
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

                // Pre-download initial chapter videos silently in background
                if (MILESTONES[0] && (MILESTONES[0].media_type || '').toLowerCase() === 'video' && MILESTONES[0].media_url) {
                    ensureVideoFullyLoaded(MILESTONES[0].media_url);
                }
                if (MILESTONES[1] && (MILESTONES[1].media_type || '').toLowerCase() === 'video' && MILESTONES[1].media_url) {
                    ensureVideoFullyLoaded(MILESTONES[1].media_url);
                }
            }
        } catch (err) {
            console.error('Error fetching site content:', err);
        }
    }

    const DOTS_PER_PAGE = 4;

    function renderDots() {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = '';
        const totalMilestones = MILESTONES.length;
        if (totalMilestones === 0) return;

        const totalPages = Math.ceil(totalMilestones / DOTS_PER_PAGE);
        const currentPage = Math.floor(currentStep / DOTS_PER_PAGE);
        const startIdx = currentPage * DOTS_PER_PAGE;
        const endIdx = Math.min(startIdx + DOTS_PER_PAGE, totalMilestones);

        for (let idx = startIdx; idx < endIdx; idx++) {
            const dot = document.createElement('span');
            dot.className = `b-dot ${idx === currentStep ? 'active' : (idx < currentStep ? 'completed' : '')}`;
            dot.setAttribute('data-step', idx);
            dot.innerHTML = `
                <span class="b-dot-num">${String(idx + 1).padStart(2, '0')}</span>
                <span class="b-dot-ripple"></span>
            `;
            dot.addEventListener('click', () => {
                if (idx !== currentStep && !isTransitioning) {
                    transitionToStep(idx);
                } else if (idx === currentStep && !isTransitioning) {
                    // If user clicks the 4th dot (last dot of window) when active, advance to next 4 dots!
                    if (idx === endIdx - 1 && endIdx < totalMilestones) {
                        transitionToStep(endIdx);
                    }
                }
            });
            dotsContainer.appendChild(dot);
        }
        bDots = document.querySelectorAll('.b-dot');

        // Toggle pagination navigation and page indicator
        if (totalMilestones > DOTS_PER_PAGE) {
            if (dotsPrevBtn) {
                dotsPrevBtn.style.display = 'inline-flex';
                dotsPrevBtn.style.opacity = currentPage > 0 ? '1' : '0.25';
                dotsPrevBtn.style.pointerEvents = currentPage > 0 ? 'auto' : 'none';
            }
            if (dotsNextBtn) {
                dotsNextBtn.style.display = 'inline-flex';
                dotsNextBtn.style.opacity = currentPage < totalPages - 1 ? '1' : '0.25';
                dotsNextBtn.style.pointerEvents = currentPage < totalPages - 1 ? 'auto' : 'none';
            }
            if (dotsPageIndicator) {
                dotsPageIndicator.style.display = 'block';
                const startNum = String(startIdx + 1).padStart(2, '0');
                const endNum = String(endIdx).padStart(2, '0');
                const totalNum = String(totalMilestones).padStart(2, '0');
                dotsPageIndicator.textContent = `PAGE ${currentPage + 1} OF ${totalPages} • ${startNum} – ${endNum} OF ${totalNum}`;
            }
        } else {
            if (dotsPrevBtn) dotsPrevBtn.style.display = 'none';
            if (dotsNextBtn) dotsNextBtn.style.display = 'none';
            if (dotsPageIndicator) dotsPageIndicator.style.display = 'none';
        }
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
                if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'inline-flex';
                if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'inline-flex';
                if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
                if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'none';
                if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
                fetchAndRenderRichReplies();
                fetchAndRenderLoginLogs();
                fetchAndRenderAdminFeedback();
            } else {
                if (adminStudioBtn) adminStudioBtn.style.display = 'none';
                if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
                if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'none';
                if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'none';
                if (gloryReplyBtn) gloryReplyBtn.style.display = 'inline-flex';
                if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'inline-flex';
                if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'flex';
                if (cardFeedbackBtn) cardFeedbackBtn.style.display = 'inline-flex';
            }

            startTypewriter();
        } else {
            // Show login portal
            if (loginModal) loginModal.classList.remove('portal-hidden');
            if (authControls) authControls.style.display = 'none';
            if (adminStudioBtn) adminStudioBtn.style.display = 'none';
            if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
            if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'none';
            if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'none';
            if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
            if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'none';
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
                        if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'inline-flex';
                        if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'inline-flex';
                        if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
                        if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'none';
                        if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
                        fetchAndRenderRichReplies();
                        fetchAndRenderLoginLogs();
                        fetchAndRenderAdminFeedback();
                        showToast(`Welcome back, Yash! Admin studio unlocked ✦`);
                    } else {
                        if (adminStudioBtn) adminStudioBtn.style.display = 'none';
                        if (adminViewRepliesBtn) adminViewRepliesBtn.style.display = 'none';
                        if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'none';
                        if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'none';
                        if (gloryReplyBtn) gloryReplyBtn.style.display = 'inline-flex';
                        if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'inline-flex';
                        if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'flex';
                        if (cardFeedbackBtn) cardFeedbackBtn.style.display = 'inline-flex';
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

    // Password Visibility Toggle
    if (pwdToggleBtn && loginPassword) {
        pwdToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const isPassword = loginPassword.type === 'password';
            loginPassword.type = isPassword ? 'text' : 'password';
            if (eyeOpenIcon) eyeOpenIcon.style.display = isPassword ? 'none' : 'block';
            if (eyeSlashIcon) eyeSlashIcon.style.display = isPassword ? 'block' : 'none';
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
            if (adminLoginLogsBtn) adminLoginLogsBtn.style.display = 'none';
            if (adminFeedbackBtn) adminFeedbackBtn.style.display = 'none';
            if (gloryReplyBtn) gloryReplyBtn.style.display = 'none';
            if (gloryFeedbackBtn) gloryFeedbackBtn.style.display = 'none';
            if (cardReplyTriggerWrap) cardReplyTriggerWrap.style.display = 'none';
            if (loginPassword) {
                loginPassword.value = '';
                loginPassword.type = 'password';
            }
            if (eyeOpenIcon) eyeOpenIcon.style.display = 'block';
            if (eyeSlashIcon) eyeSlashIcon.style.display = 'none';
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

    function applyTheme(stepIndexOrTheme) {
        let themeName = 'theme-crimson';
        if (typeof stepIndexOrTheme === 'number') {
            const meta = MILESTONES[stepIndexOrTheme];
            if (meta && meta.theme) themeName = meta.theme;
        } else if (typeof stepIndexOrTheme === 'string' && stepIndexOrTheme) {
            themeName = stepIndexOrTheme;
        }
        document.body.className = themeName;
        currentThemeEmberPalette = THEME_EMBER_PALETTES[themeName] || THEME_EMBER_PALETTES['theme-crimson'];
        if (typeof embers !== 'undefined' && Array.isArray(embers)) {
            embers.forEach(e => {
                const palette = currentThemeEmberPalette;
                e.color = palette[Math.floor(Math.random() * palette.length)];
            });
        }
    }

    function initDotsPosition(stepIndex) {
        if (!MILESTONES || MILESTONES.length === 0) return;
        const currentPage = Math.floor(stepIndex / DOTS_PER_PAGE);
        const currentRenderedFirst = bDots && bDots[0] ? parseInt(bDots[0].getAttribute('data-step'), 10) : 0;
        const currentRenderedPage = Math.floor(currentRenderedFirst / DOTS_PER_PAGE);

        if (currentRenderedPage !== currentPage) {
            renderDots();
        } else {
            bDots = document.querySelectorAll('.b-dot');
        }

        if (!bDots || bDots.length === 0) return;

        const startIdx = currentPage * DOTS_PER_PAGE;
        bDots.forEach((dot, rIdx) => {
            const realIdx = startIdx + rIdx;
            dot.classList.remove('active', 'completed', 'burst');
            if (realIdx === stepIndex) {
                dot.classList.add('active');
            } else if (realIdx < stepIndex) {
                dot.classList.add('completed');
            }
        });

        const relativeIndex = stepIndex - startIdx;
        const activeDot = bDots[relativeIndex] || bDots[0];
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

        // Intelligent Full Video Preloader:
        // Silently pre-downloads 100% of the video bytes into local RAM before playing,
        // so when played it NEVER buffers, stutters, or drops out!
        if (mediaType === 'video' && data.media_url) {
            ensureVideoFullyLoaded(data.media_url);
        }
        const nextData = MILESTONES[stepIndex + 1];
        if (nextData && (nextData.media_type || '').toLowerCase() === 'video' && nextData.media_url) {
            ensureVideoFullyLoaded(nextData.media_url);
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

    // ==========================================================================
    // Video Full Preload & Blob Cache Engine (Ensures 100% complete load before play)
    // ==========================================================================
    const videoCache = new Map();

    function formatVideoBytes(bytes) {
        if (!bytes || isNaN(bytes)) return '0 MB';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    async function ensureVideoFullyLoaded(url, progressCallback) {
        if (!url || typeof url !== 'string' || !url.startsWith('http')) return url;

        if (videoCache.has(url)) {
            const entry = videoCache.get(url);
            if (entry.status === 'ready') {
                if (progressCallback) progressCallback(100, entry.total, entry.total);
                return entry.blobUrl;
            }
            if (entry.status === 'loading') {
                if (progressCallback) entry.listeners.push(progressCallback);
                return entry.promise;
            }
        }

        const listeners = [];
        if (progressCallback) listeners.push(progressCallback);

        const entry = {
            blobUrl: null,
            blob: null,
            status: 'loading',
            progress: 0,
            loaded: 0,
            total: 0,
            listeners,
            promise: null
        };

        const loadPromise = (async () => {
            try {
                const res = await fetch(url, { mode: 'cors' });
                if (!res.ok) throw new Error(`HTTP error ${res.status}`);

                const len = res.headers.get('content-length');
                const total = len ? parseInt(len, 10) : 0;
                entry.total = total;

                if (!res.body || !total) {
                    const blob = await res.blob();
                    const blobUrl = URL.createObjectURL(blob);
                    entry.blob = blob;
                    entry.blobUrl = blobUrl;
                    entry.status = 'ready';
                    entry.progress = 100;
                    entry.listeners.forEach(cb => cb(100, blob.size, blob.size));
                    return blobUrl;
                }

                const reader = res.body.getReader();
                let received = 0;
                const chunks = [];

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    chunks.push(value);
                    received += value.length;
                    entry.loaded = received;
                    const pct = Math.min(99, Math.round((received / total) * 100));
                    entry.progress = pct;
                    entry.listeners.forEach(cb => cb(pct, received, total));
                }

                const blob = new Blob(chunks, { type: res.headers.get('content-type') || 'video/mp4' });
                const blobUrl = URL.createObjectURL(blob);
                entry.blob = blob;
                entry.blobUrl = blobUrl;
                entry.status = 'ready';
                entry.progress = 100;
                entry.listeners.forEach(cb => cb(100, received, total));
                return blobUrl;
            } catch (err) {
                console.warn('Full preload via fetch failed; falling back to direct stream:', err);
                entry.status = 'error';
                return url;
            }
        })();

        entry.promise = loadPromise;
        videoCache.set(url, entry);
        return loadPromise;
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
        if (videoTapToPlay) videoTapToPlay.style.display = 'none';

        if (lightboxVideo) lightboxVideo.pause();
        if (lightboxAudio) lightboxAudio.pause();

        if (mediaTitleText) mediaTitleText.textContent = data.title || 'CHAPTER MEDIA';

        if (mediaType === 'image') {
            if (mediaBadgeLabel) mediaBadgeLabel.textContent = '// MEMORY PHOTOGRAPH';
            if (lightboxImage) lightboxImage.src = data.media_url;
            if (mediaPaneImage) mediaPaneImage.style.display = 'block';
        } else if (mediaType === 'video') {
            if (mediaBadgeLabel) mediaBadgeLabel.textContent = '// VIDEO HIGHLIGHT';
            if (mediaPaneVideo) mediaPaneVideo.style.display = 'block';

            const videoUrl = data.media_url;
            const cached = videoCache.get(videoUrl);

            function showTapToPlayPrompt() {
                if (videoTapToPlay) videoTapToPlay.style.display = 'flex';
            }

            function startPlaying(src) {
                if (!lightboxVideo) return;
                if (videoPreloadOverlay) videoPreloadOverlay.style.display = 'none';
                if (lightboxVideo.src !== src) {
                    lightboxVideo.src = src;
                    if (lightboxVideoSrc) lightboxVideoSrc.src = src;
                    lightboxVideo.load();
                }
                const playPromise = lightboxVideo.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        if (videoTapToPlay) videoTapToPlay.style.display = 'none';
                    }).catch(() => {
                        // Unmuted autoplay blocked by browser policy: show glowing Tap To Play button
                        showTapToPlayPrompt();
                    });
                }
            }

            if (cached && cached.status === 'ready' && cached.blobUrl) {
                // 100% PRE-LOADED IN RAM! Play immediately with ZERO loading!
                if (videoPreloadOverlay) videoPreloadOverlay.style.display = 'none';
                startPlaying(cached.blobUrl);
            } else {
                // Video is downloading: show full preload progress
                if (videoPreloadOverlay) videoPreloadOverlay.style.display = 'flex';
                if (videoPreloadBar) videoPreloadBar.style.width = '0%';
                if (videoPreloadPct) videoPreloadPct.textContent = '0%';
                if (videoPreloadBytes) videoPreloadBytes.textContent = 'Buffering 100% into memory for zero loading...';

                // Skip button allows playing progressively immediately if user prefers
                if (videoSkipPreloadBtn) {
                    videoSkipPreloadBtn.onclick = () => {
                        startPlaying(videoUrl);
                    };
                }

                ensureVideoFullyLoaded(videoUrl, (pct, loaded, total) => {
                    if (videoPreloadBar) videoPreloadBar.style.width = `${pct}%`;
                    if (videoPreloadPct) videoPreloadPct.textContent = `${pct}%`;
                    if (videoPreloadBytes) {
                        videoPreloadBytes.textContent = `${formatVideoBytes(loaded)} / ${formatVideoBytes(total)}`;
                    }
                }).then(srcToPlay => {
                    startPlaying(srcToPlay || videoUrl);
                });
            }
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
        if (lightboxVideo) {
            lightboxVideo.pause();
        }
        if (lightboxAudio) lightboxAudio.pause();
        if (videoPreloadOverlay) videoPreloadOverlay.style.display = 'none';
        if (videoTapToPlay) videoTapToPlay.style.display = 'none';
    }

    if (videoTapToPlay) {
        videoTapToPlay.addEventListener('click', () => {
            if (videoTapToPlay) videoTapToPlay.style.display = 'none';
            if (lightboxVideo) {
                lightboxVideo.play();
            }
        });
    }

    if (lightboxVideo) {
        lightboxVideo.addEventListener('playing', () => {
            if (videoTapToPlay) videoTapToPlay.style.display = 'none';
            if (videoPreloadOverlay) videoPreloadOverlay.style.display = 'none';
        });
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
        const currentRenderedFirst = bDots && bDots[0] ? parseInt(bDots[0].getAttribute('data-step'), 10) : 0;
        const currentWindowPage = Math.floor(currentRenderedFirst / DOTS_PER_PAGE);
        const targetWindowPage = Math.floor(targetIndex / DOTS_PER_PAGE);

        if (targetWindowPage !== currentWindowPage) {
            currentStep = targetIndex;
            renderDots();
            if (dotsContainer) {
                dotsContainer.classList.add('dots-page-transition');
                setTimeout(() => dotsContainer.classList.remove('dots-page-transition'), 360);
            }
        }

        bDots = document.querySelectorAll('.b-dot');
        const startIdx = targetWindowPage * DOTS_PER_PAGE;
        const relativeIndex = targetIndex - startIdx;
        const targetDot = bDots[relativeIndex] || bDots[0];
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

            bDots.forEach((dot, rIdx) => {
                const realIdx = startIdx + rIdx;
                dot.classList.remove('active', 'burst');
                if (realIdx < targetIndex) {
                    dot.classList.add('completed');
                } else if (realIdx === targetIndex) {
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

    // Touch Swipe Navigation for Mobile Devices (Swipe left for Next, Swipe right for Prev)
    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;

    const swipeTarget = document.getElementById('cardOuter') || document.getElementById('chapterStage');
    if (swipeTarget) {
        swipeTarget.addEventListener('touchstart', (e) => {
            if (e.touches && e.touches[0]) {
                touchStartX = e.touches[0].clientX;
                touchStartY = e.touches[0].clientY;
                touchStartTime = Date.now();
            }
        }, { passive: true });

        swipeTarget.addEventListener('touchend', (e) => {
            if (!e.changedTouches || !e.changedTouches[0] || isTransitioning) return;
            const deltaX = e.changedTouches[0].clientX - touchStartX;
            const deltaY = e.changedTouches[0].clientY - touchStartY;
            const elapsedTime = Date.now() - touchStartTime;

            // Must be quick (< 500ms), horizontal (|deltaX| > 45px), and primarily horizontal
            if (elapsedTime < 500 && Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY) * 1.25) {
                if (deltaX < 0) {
                    // Swipe Left -> Next Chapter
                    if (nextStepBtn && !nextStepBtn.disabled) {
                        if (navigator.vibrate) try { navigator.vibrate(14); } catch (_) {}
                        nextStepBtn.click();
                    }
                } else if (deltaX > 0) {
                    // Swipe Right -> Previous Chapter
                    if (currentStep > 0 && prevStepBtn && !prevStepBtn.disabled) {
                        if (navigator.vibrate) try { navigator.vibrate(14); } catch (_) {}
                        prevStepBtn.click();
                    }
                }
            }
        }, { passive: true });
    }

    if (dotsPrevBtn) {
        dotsPrevBtn.addEventListener('click', () => {
            if (isTransitioning) return;
            const currentWindowPage = Math.floor(currentStep / DOTS_PER_PAGE);
            if (currentWindowPage > 0) {
                const targetStep = (currentWindowPage - 1) * DOTS_PER_PAGE;
                transitionToStep(targetStep);
            }
        });
    }

    if (dotsNextBtn) {
        dotsNextBtn.addEventListener('click', () => {
            if (isTransitioning) return;
            const currentWindowPage = Math.floor(currentStep / DOTS_PER_PAGE);
            const totalPages = Math.ceil(MILESTONES.length / DOTS_PER_PAGE);
            if (currentWindowPage < totalPages - 1) {
                const targetStep = (currentWindowPage + 1) * DOTS_PER_PAGE;
                transitionToStep(targetStep);
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

    const STUDIO_CHAPS_PER_PAGE = 4;
    let studioChapterPage = 0;

    function renderStudioChapterButtons(activeIdx = 0) {
        if (!chapterSelectorBar) return;
        chapterSelectorBar.innerHTML = '';

        const totalMilestones = MILESTONES.length;
        if (totalMilestones === 0) return;

        studioChapterPage = Math.floor(activeIdx / STUDIO_CHAPS_PER_PAGE);
        const totalPages = Math.max(1, Math.ceil(totalMilestones / STUDIO_CHAPS_PER_PAGE));
        const startIdx = studioChapterPage * STUDIO_CHAPS_PER_PAGE;
        const endIdx = Math.min(startIdx + STUDIO_CHAPS_PER_PAGE, totalMilestones);

        for (let idx = startIdx; idx < endIdx; idx++) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `btn-chapter-sel ${idx === activeIdx ? 'active' : ''}`;
            btn.setAttribute('data-step', idx);
            btn.innerHTML = `<span class="sel-num">${String(idx + 1).padStart(2, '0')}</span> Card ${idx + 1}`;
            btn.addEventListener('click', () => {
                loadChapterIntoStudio(idx);
            });
            chapterSelectorBar.appendChild(btn);
        }

        // Toggle Studio Pagination Controls
        if (studioPrevPageBtn) {
            studioPrevPageBtn.disabled = (studioChapterPage <= 0);
            studioPrevPageBtn.style.opacity = studioChapterPage > 0 ? '1' : '0.25';
            studioPrevPageBtn.style.pointerEvents = studioChapterPage > 0 ? 'auto' : 'none';
        }
        if (studioNextPageBtn) {
            studioNextPageBtn.disabled = (studioChapterPage >= totalPages - 1);
            studioNextPageBtn.style.opacity = studioChapterPage < totalPages - 1 ? '1' : '0.25';
            studioNextPageBtn.style.pointerEvents = studioChapterPage < totalPages - 1 ? 'auto' : 'none';
        }
        if (studioPageIndicator) {
            const startNum = String(startIdx + 1).padStart(2, '0');
            const endNum = String(endIdx).padStart(2, '0');
            const totalNum = String(totalMilestones).padStart(2, '0');
            studioPageIndicator.textContent = `CARDS ${startNum} – ${endNum} OF ${totalNum} • PAGE ${studioChapterPage + 1} OF ${totalPages}`;
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
        if (adminCardTheme) {
            const currentTheme = chap.theme || 'theme-crimson';
            adminCardTheme.value = currentTheme;
            if (themeSwatchesGrid) {
                themeSwatchesGrid.querySelectorAll('.theme-swatch-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.theme === currentTheme);
                });
            }
        }

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

        // Highlight active chapter button (or re-render page if out of current window)
        const activePage = Math.floor(stepIdx / STUDIO_CHAPS_PER_PAGE);
        if (activePage !== studioChapterPage) {
            renderStudioChapterButtons(stepIdx);
        } else if (chapterSelectorBar) {
            const buttons = chapterSelectorBar.querySelectorAll('.btn-chapter-sel');
            buttons.forEach(btn => {
                btn.classList.toggle('active', parseInt(btn.dataset.step, 10) === stepIdx);
            });
        }

        // Update Reorder Panel
        if (reorderCurrentBadge) {
            reorderCurrentBadge.textContent = `CURRENT: POSITION ${String(stepIdx + 1).padStart(2, '0')}`;
        }
        if (btnMoveCardEarlier) {
            btnMoveCardEarlier.disabled = (stepIdx <= 0);
        }
        if (btnMoveCardLater) {
            btnMoveCardLater.disabled = (stepIdx >= MILESTONES.length - 1);
        }
        if (adminCardTargetPosition) {
            adminCardTargetPosition.innerHTML = '';
            MILESTONES.forEach((chapItem, cIdx) => {
                const opt = document.createElement('option');
                opt.value = cIdx;
                const posStr = String(cIdx + 1).padStart(2, '0');
                const titleStr = (chapItem.title || 'UNTITLED').substring(0, 18);
                opt.textContent = `Position ${posStr} (${titleStr})${cIdx === stepIdx ? ' [Current]' : ''}`;
                adminCardTargetPosition.appendChild(opt);
            });
            adminCardTargetPosition.value = stepIdx;
        }

        // Delete button visibility safety check (always keep at least 1 card)
        if (adminDeleteChapterBtn) {
            adminDeleteChapterBtn.style.display = MILESTONES.length > 1 ? 'inline-flex' : 'none';
        }
    }

    if (studioPrevPageBtn) {
        studioPrevPageBtn.addEventListener('click', () => {
            if (studioChapterPage > 0) {
                const targetIdx = (studioChapterPage - 1) * STUDIO_CHAPS_PER_PAGE;
                renderStudioChapterButtons(targetIdx);
                loadChapterIntoStudio(targetIdx);
            }
        });
    }

    if (studioNextPageBtn) {
        studioNextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(MILESTONES.length / STUDIO_CHAPS_PER_PAGE);
            if (studioChapterPage < totalPages - 1) {
                const targetIdx = (studioChapterPage + 1) * STUDIO_CHAPS_PER_PAGE;
                renderStudioChapterButtons(targetIdx);
                loadChapterIntoStudio(targetIdx);
            }
        });
    }

    async function executeChapterReorder(fromIdx, toIdx) {
        if (fromIdx === toIdx || fromIdx < 0 || toIdx < 0) return;
        if (fromIdx >= MILESTONES.length || toIdx >= MILESTONES.length) return;

        try {
            if (btnApplyCardReorder) btnApplyCardReorder.disabled = true;
            if (btnMoveCardEarlier) btnMoveCardEarlier.disabled = true;
            if (btnMoveCardLater) btnMoveCardLater.disabled = true;

            const res = await fetch('/api/admin/chapter/reorder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ from_index: fromIdx, to_index: toIdx })
            });
            const data = await res.json();
            if (data.status === 'success') {
                MILESTONES = data.chapters;
                totalSteps = MILESTONES.length;

                // Sync Studio and Main Canvas
                renderStudioChapterButtons(toIdx);
                loadChapterIntoStudio(toIdx);
                currentStep = toIdx;
                applyTheme(currentStep);
                updateCardContent(currentStep, false);
                renderDots();

                showToast(`✨ Card moved to Position ${String(toIdx + 1).padStart(2, '0')}!`);
                playLaserWhoosh();
            } else {
                showToast(data.message || 'Failed to reorder card.');
            }
        } catch (err) {
            console.error('Error reordering chapters:', err);
            showToast('Network error reordering card.');
        } finally {
            if (btnApplyCardReorder) btnApplyCardReorder.disabled = false;
            if (btnMoveCardEarlier) btnMoveCardEarlier.disabled = (toIdx <= 0);
            if (btnMoveCardLater) btnMoveCardLater.disabled = (toIdx >= MILESTONES.length - 1);
        }
    }

    if (btnMoveCardEarlier) {
        btnMoveCardEarlier.addEventListener('click', () => {
            const currentIdx = parseInt(adminCurrentStepIndex.value, 10);
            if (currentIdx > 0) {
                executeChapterReorder(currentIdx, currentIdx - 1);
            }
        });
    }

    if (btnMoveCardLater) {
        btnMoveCardLater.addEventListener('click', () => {
            const currentIdx = parseInt(adminCurrentStepIndex.value, 10);
            if (currentIdx < MILESTONES.length - 1) {
                executeChapterReorder(currentIdx, currentIdx + 1);
            }
        });
    }

    if (btnApplyCardReorder) {
        btnApplyCardReorder.addEventListener('click', () => {
            const currentIdx = parseInt(adminCurrentStepIndex.value, 10);
            const targetIdx = parseInt(adminCardTargetPosition.value, 10);
            if (currentIdx === targetIdx) {
                showToast(`Card is already at Position ${String(targetIdx + 1).padStart(2, '0')}.`);
                return;
            }
            executeChapterReorder(currentIdx, targetIdx);
        });
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

    // Theme Swatches Grid & Select Synchronization
    if (themeSwatchesGrid && adminCardTheme) {
        themeSwatchesGrid.addEventListener('click', (e) => {
            const btn = e.target.closest('.theme-swatch-btn');
            if (!btn) return;
            const chosenTheme = btn.dataset.theme;
            adminCardTheme.value = chosenTheme;
            themeSwatchesGrid.querySelectorAll('.theme-swatch-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyTheme(chosenTheme);
        });

        adminCardTheme.addEventListener('change', () => {
            const chosenTheme = adminCardTheme.value;
            themeSwatchesGrid.querySelectorAll('.theme-swatch-btn').forEach(b => {
                b.classList.toggle('active', b.dataset.theme === chosenTheme);
            });
            applyTheme(chosenTheme);
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

            if (targetTab === 'tabLogs') {
                fetchAndRenderLoginLogs();
            } else if (targetTab === 'tabReplies') {
                fetchAndRenderRichReplies();
            } else if (targetTab === 'tabFeedback') {
                fetchAndRenderAdminFeedback();
            }
        });
    });

    // Helper: HTML Escaping
    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(text).replace(/[&<>"']/g, m => map[m]);
    }

    // Helper: Friendly timestamp
    function formatTransmissionTime(dateStr) {
        if (!dateStr) return 'Recent Transmission';
        try {
            const d = new Date(dateStr);
            if (isNaN(d.getTime())) return dateStr;
            const now = new Date();
            const diffSec = Math.floor((now - d) / 1000);
            if (diffSec < 60) return 'Just now';
            if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
            if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
            return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        } catch (e) {
            return dateStr;
        }
    }

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
            if (repliesCountPill) {
                repliesCountPill.textContent = `${replies.length} TRANSMISSION${replies.length === 1 ? '' : 'S'}`;
            }

            // Render Studio Drawer simple list if present
            if (adminRepliesList) {
                if (replies.length === 0) {
                    adminRepliesList.innerHTML = '<div class="empty-replies">No messages received yet from Glory.</div>';
                } else {
                    adminRepliesList.innerHTML = '';
                    replies.forEach(r => {
                        const item = document.createElement('div');
                        item.className = 'reply-item-card';
                        const cardTitle = r.card_title || r.chapter_title || '';
                        const contextBadge = cardTitle ? `<span class="reply-context-badge">📍 Card 0${(r.chapter_index != null ? r.chapter_index + 1 : '')}: ${escapeHtml(cardTitle)}</span>` : '';
                        item.innerHTML = `
                            <div class="reply-item-meta">
                                <span class="reply-sender-name">💌 ${escapeHtml(r.sender || 'Glory')}</span>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span class="reply-time">${formatTransmissionTime(r.created_at)}</span>
                                    <button type="button" class="btn-delete-reply" style="padding: 2px 7px; font-size: 0.58rem;" data-reply-id="${r.id}">✕</button>
                                </div>
                            </div>
                            ${contextBadge}
                            <div style="margin-top: 8px; padding: 10px 14px; background: rgba(255,255,255,0.05); border-left: 3px solid var(--accent-color); border-radius: 8px;">
                                <p class="reply-item-content" style="font-size: 0.94rem; font-weight: 500; color: #ffffff; line-height: 1.55;">“${escapeHtml(r.message)}”</p>
                            </div>
                        `;
                        const delBtn = item.querySelector('.btn-delete-reply');
                        if (delBtn) {
                            delBtn.addEventListener('click', async () => {
                                if (!confirm('Delete this transmission?')) return;
                                try {
                                    await fetch(`/api/admin/reply/${r.id}`, { method: 'DELETE' });
                                    showToast('Transmission deleted ✦');
                                    fetchAndRenderRichReplies();
                                } catch (_) {}
                            });
                        }
                        adminRepliesList.appendChild(item);
                    });
                }
            }

            // Render Dedicated Modal Rich Container
            if (richRepliesContainer) {
                if (replies.length === 0) {
                    richRepliesContainer.innerHTML = `
                        <div class="empty-replies" style="padding: 48px 20px; text-align: center;">
                            <div class="radar-scan-box">
                                <div class="radar-sweep"></div>
                                <span class="radar-icon">📡</span>
                            </div>
                            <h4 style="font-family: var(--font-display); letter-spacing: 0.12em; color: #ffffff; margin-bottom: 6px;">NO TRANSMISSIONS YET</h4>
                            <p class="radar-text">INBOX READY // AWAITING SECURE MESSAGES FROM GLORY</p>
                        </div>
                    `;
                    return;
                }

                richRepliesContainer.innerHTML = '';
                replies.forEach((r, idx) => {
                    const card = document.createElement('div');
                    card.className = 'rich-reply-card';

                    const senderName = r.sender || 'Glory';
                    const senderInitial = senderName.charAt(0).toUpperCase();
                    const cardTitle = r.card_title || r.chapter_title || '';
                    const timeStr = formatTransmissionTime(r.created_at);

                    let contextHtml = '';
                    if (r.chapter_index != null || cardTitle) {
                        const cardNum = r.chapter_index != null ? `0${r.chapter_index + 1}` : '';
                        contextHtml = `
                            <div class="reply-context-ribbon">
                                <span>📍 Sent regarding Chapter ${cardNum}${cardTitle ? ' – ' + escapeHtml(cardTitle) : ''}</span>
                            </div>
                        `;
                    }

                    card.innerHTML = `
                        <div class="reply-card-header">
                            <div class="reply-author-cluster">
                                <div class="reply-avatar-monogram">${senderInitial}</div>
                                <div class="reply-author-meta">
                                    <div class="author-title-row">
                                        <span class="reply-author-name">${escapeHtml(senderName)}</span>
                                        <span class="reply-verified-badge">VERIFIED TRANSMISSION</span>
                                    </div>
                                    <span class="reply-timestamp">⏱ ${escapeHtml(timeStr)}</span>
                                </div>
                            </div>
                            <div class="reply-header-actions">
                                <button type="button" class="btn-copy-reply" title="Copy transmission text" data-reply-id="${r.id || idx}">
                                    <span>📋 COPY</span>
                                </button>
                                <button type="button" class="btn-delete-reply" title="Delete transmission" data-reply-id="${r.id}">
                                    <span>🗑 DELETE</span>
                                </button>
                            </div>
                        </div>

                        <!-- Glory's Direct Transmission Spotlight -->
                        <div class="reply-quote-box">
                            <div class="reply-quote-tag">
                                <span>💌 MESSAGE FROM ${escapeHtml(senderName.toUpperCase())}:</span>
                            </div>
                            <div class="reply-quote-text"><span class="reply-quote-mark">“</span>${escapeHtml(r.message)}<span class="reply-quote-mark">”</span></div>
                        </div>

                        ${contextHtml}
                    `;

                    // Wire copy button
                    const copyBtn = card.querySelector('.btn-copy-reply');
                    if (copyBtn) {
                        copyBtn.addEventListener('click', async () => {
                            try {
                                await navigator.clipboard.writeText(r.message);
                                copyBtn.innerHTML = '<span>✓ COPIED</span>';
                                showToast('Transmission copied to clipboard! ✦');
                                setTimeout(() => {
                                    copyBtn.innerHTML = '<span>📋 COPY</span>';
                                }, 2000);
                            } catch (e) {
                                showToast('Message: ' + r.message.substring(0, 40) + '...');
                            }
                        });
                    }

                    // Wire delete button
                    const delBtn = card.querySelector('.btn-delete-reply');
                    if (delBtn) {
                        delBtn.addEventListener('click', async () => {
                            if (!confirm('Delete this transmission from Glory?')) return;
                            try {
                                const delRes = await fetch(`/api/admin/reply/${r.id}`, { method: 'DELETE' });
                                const delData = await delRes.json();
                                if (delData.status === 'success') {
                                    showToast('Transmission deleted ✦');
                                    fetchAndRenderRichReplies();
                                }
                            } catch (e) {
                                showToast('Failed to delete transmission.');
                            }
                        });
                    }

                    richRepliesContainer.appendChild(card);
                });
            }
        } catch (err) {
            console.error('Error fetching rich replies:', err);
        }
    }

    const modalClearRepliesBtn = document.getElementById('modalClearRepliesBtn');
    const drawerClearRepliesBtn = document.getElementById('drawerClearRepliesBtn');

    async function handleClearAllReplies() {
        if (!confirm('Are you sure you want to permanently clear ALL replies and wishes from Glory?')) return;
        try {
            const res = await fetch('/api/admin/replies/clear', { method: 'DELETE' });
            const data = await res.json();
            if (data.status === 'success') {
                showToast('All replies cleared ✦');
                fetchAndRenderRichReplies();
            }
        } catch (e) {
            showToast('Failed to clear replies.');
        }
    }

    if (modalClearRepliesBtn) modalClearRepliesBtn.addEventListener('click', handleClearAllReplies);
    if (drawerClearRepliesBtn) drawerClearRepliesBtn.addEventListener('click', handleClearAllReplies);

    const modalClearLogsBtn = document.getElementById('modalClearLogsBtn');
    const drawerClearLogsBtn = document.getElementById('drawerClearLogsBtn');

    async function handleClearAllLogs() {
        if (!confirm('Are you sure you want to permanently clear all login access history?')) return;
        try {
            const res = await fetch('/api/admin/login-logs', { method: 'DELETE' });
            const data = await res.json();
            if (data.status === 'success') {
                showToast('Login audit logs cleared ✦');
                fetchAndRenderLoginLogs();
            }
        } catch (e) {
            showToast('Failed to clear login logs.');
        }
    }

    if (modalClearLogsBtn) modalClearLogsBtn.addEventListener('click', handleClearAllLogs);
    if (drawerClearLogsBtn) drawerClearLogsBtn.addEventListener('click', handleClearAllLogs);

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
    // 9.5 Dedicated Admin Login Activity & Audit Engine (Yash)
    // ==========================================================================
    function formatLogDateTime(isoStr) {
        if (!isoStr) return { dateStr: 'Unknown Date', timeStr: 'Unknown Time', relativeStr: '' };
        try {
            const d = new Date(isoStr);
            if (isNaN(d.getTime())) return { dateStr: isoStr, timeStr: '', relativeStr: '' };
            const dateStr = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
            const timeStr = d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const now = new Date();
            const diffSec = Math.floor((now - d) / 1000);
            let relativeStr = 'Just now';
            if (diffSec >= 60 && diffSec < 3600) relativeStr = `${Math.floor(diffSec / 60)}m ago`;
            else if (diffSec >= 3600 && diffSec < 86400) relativeStr = `${Math.floor(diffSec / 3600)}h ago`;
            else if (diffSec >= 86400) relativeStr = `${Math.floor(diffSec / 86400)}d ago`;
            return { dateStr, timeStr, relativeStr };
        } catch (e) {
            return { dateStr: isoStr, timeStr: '', relativeStr: '' };
        }
    }

    function parseDeviceSummary(ua) {
        if (!ua) return 'Web Client';
        if (/iphone/i.test(ua)) return 'Apple iPhone';
        if (/ipad/i.test(ua)) return 'Apple iPad';
        if (/android/i.test(ua)) return 'Android Device';
        if (/macintosh|mac os x/i.test(ua)) return 'macOS Workstation';
        if (/windows/i.test(ua)) return 'Windows PC';
        if (/linux/i.test(ua)) return 'Linux System';
        return 'Web Browser';
    }

    async function fetchAndRenderLoginLogs() {
        try {
            const res = await fetch('/api/admin/login-logs');
            const data = await res.json();
            if (data.status !== 'success') return;
            const logs = data.data || [];

            // Update badge counters
            if (logsBadgeCount) logsBadgeCount.textContent = logs.length;
            if (logsCountPill) {
                logsCountPill.textContent = `${logs.length} SESSION${logs.length === 1 ? '' : 'S'}`;
            }

            // Render Studio Drawer simple list
            if (drawerLoginLogsList) {
                if (logs.length === 0) {
                    drawerLoginLogsList.innerHTML = '<div class="empty-replies">No login sessions recorded yet.</div>';
                } else {
                    drawerLoginLogsList.innerHTML = '';
                    logs.forEach(log => {
                        const item = document.createElement('div');
                        item.className = 'reply-item-card';
                        const { dateStr, timeStr, relativeStr } = formatLogDateTime(log.created_at);
                        const device = parseDeviceSummary(log.user_agent);
                        const ip = log.ip_address || '127.0.0.1';
                        const roleClass = (log.role || 'viewer').toLowerCase() === 'admin' ? 'admin' : 'viewer';

                        item.innerHTML = `
                            <div class="reply-item-meta">
                                <span class="reply-sender-name">🔒 ${escapeHtml(log.username)}</span>
                                <span class="log-role-pill ${roleClass}">${escapeHtml((log.role || 'viewer').toUpperCase())}</span>
                                <span class="reply-time" style="margin-left: auto;">${escapeHtml(relativeStr)}</span>
                            </div>
                            <div style="font-family: var(--font-tech); font-size: 0.72rem; color: rgba(255, 255, 255, 0.75); margin-top: 6px;">
                                📅 ${escapeHtml(dateStr)} • ⏰ ${escapeHtml(timeStr)}
                            </div>
                            <div style="font-family: var(--font-tech); font-size: 0.65rem; color: #38bdf8; margin-top: 4px; display: flex; gap: 8px; flex-wrap: wrap;">
                                <span>🌐 ${escapeHtml(ip)}</span>
                                <span>💻 ${escapeHtml(device)}</span>
                            </div>
                        `;
                        drawerLoginLogsList.appendChild(item);
                    });
                }
            }

            // Render Dedicated Cinematic Modal
            if (loginLogsContainer) {
                if (logs.length === 0) {
                    loginLogsContainer.innerHTML = `
                        <div class="empty-replies">
                            <div class="radar-scan-box">
                                <div class="radar-sweep"></div>
                                <span class="radar-icon">🔒</span>
                            </div>
                            <p class="radar-text">NO LOGIN SESSIONS RECORDED YET</p>
                        </div>
                    `;
                } else {
                    loginLogsContainer.innerHTML = '';
                    logs.forEach(log => {
                        const card = document.createElement('div');
                        card.className = 'log-audit-card';
                        const roleClass = (log.role || 'viewer').toLowerCase() === 'admin' ? 'admin' : 'viewer';
                        const avatarInitial = (log.username || '?').charAt(0).toUpperCase();
                        const { dateStr, timeStr, relativeStr } = formatLogDateTime(log.created_at);
                        const device = parseDeviceSummary(log.user_agent);
                        const ip = log.ip_address || '127.0.0.1';

                        card.innerHTML = `
                            <div class="log-user-info">
                                <div class="log-user-avatar ${roleClass}">${avatarInitial}</div>
                                <div class="log-user-details">
                                    <div class="log-name-row">
                                        <span class="log-username">${escapeHtml(log.username)}</span>
                                        <span class="log-role-pill ${roleClass}">${escapeHtml((log.role || 'viewer').toUpperCase())}</span>
                                    </div>
                                    <div class="log-meta-row">
                                        <span class="log-time-exact">📅 ${escapeHtml(dateStr)} • ⏰ ${escapeHtml(timeStr)} (${escapeHtml(relativeStr)})</span>
                                        <span class="log-ip-pill">🌐 ${escapeHtml(ip)}</span>
                                        <span class="log-agent-pill" title="${escapeHtml(log.user_agent || '')}">💻 ${escapeHtml(device)}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="log-status-badge">
                                <span class="log-status-dot"></span>
                                <span>AUTHENTICATED</span>
                            </div>
                        `;
                        loginLogsContainer.appendChild(card);
                    });
                }
            }
        } catch (err) {
            console.error('Error fetching login logs:', err);
        }
    }

    if (refreshDrawerLogsBtn) {
        refreshDrawerLogsBtn.addEventListener('click', () => {
            fetchAndRenderLoginLogs();
            showToast('Access logs refreshed ✦');
        });
    }

    if (adminLoginLogsBtn && adminLogsModal) {
        adminLoginLogsBtn.addEventListener('click', () => {
            adminLogsModal.style.display = 'flex';
            fetchAndRenderLoginLogs();
        });
    }

    if (adminLogsModalCloseBtn && adminLogsModal) {
        adminLogsModalCloseBtn.addEventListener('click', () => {
            adminLogsModal.style.display = 'none';
        });
    }

    if (modalRefreshLogsBtn) {
        modalRefreshLogsBtn.addEventListener('click', () => {
            fetchAndRenderLoginLogs();
            showToast('Access logs refreshed ✦');
        });
    }

    if (adminLogsModal) {
        adminLogsModal.addEventListener('click', (e) => {
            if (e.target === adminLogsModal) adminLogsModal.style.display = 'none';
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
    // 10.5 5-Star Feedback Question & Review Engine (Viewer & Admin)
    // ==========================================================================
    let currentSelectedRating = 0;
    const STAR_DESCRIPTIONS = {
        0: 'Select stars to rate (1 to 5)',
        1: '★ 1 / 5 – Needs Improvement',
        2: '★ 2 / 5 – Nice Effort',
        3: '★ 3 / 5 – Loved The Journey!',
        4: '★ 4 / 5 – Extraordinary & Heartfelt!',
        5: '★ 5 / 5 – Absolute Cinematic Masterpiece! ★'
    };

    const starBtns = starRatingGroup ? starRatingGroup.querySelectorAll('.star-btn') : [];

    function highlightStars(count) {
        starBtns.forEach((btn, idx) => {
            const val = idx + 1;
            btn.classList.toggle('hovered', val <= count);
        });
    }

    function setStarRating(count) {
        currentSelectedRating = count;
        if (selectedStarRating) selectedStarRating.value = count;

        starBtns.forEach((btn, idx) => {
            const val = idx + 1;
            btn.classList.toggle('active', val <= count);
            btn.classList.remove('hovered');
        });

        if (ratingDescriptorText) {
            ratingDescriptorText.textContent = STAR_DESCRIPTIONS[count] || STAR_DESCRIPTIONS[0];
            ratingDescriptorText.classList.toggle('active', count > 0);
        }

        if (feedbackSubmitBtn) {
            feedbackSubmitBtn.disabled = (count === 0);
        }
        if (feedbackSubmitBtnLabel) {
            feedbackSubmitBtnLabel.textContent = count > 0 ? `TRANSMIT FEEDBACK (★ ${count}/5)` : 'SELECT RATING';
        }
    }

    starBtns.forEach((btn, idx) => {
        const starVal = idx + 1;
        btn.addEventListener('mouseenter', () => {
            highlightStars(starVal);
            if (ratingDescriptorText) {
                ratingDescriptorText.textContent = STAR_DESCRIPTIONS[starVal];
            }
        });

        btn.addEventListener('mouseleave', () => {
            highlightStars(currentSelectedRating);
            if (ratingDescriptorText) {
                ratingDescriptorText.textContent = STAR_DESCRIPTIONS[currentSelectedRating];
            }
        });

        btn.addEventListener('click', () => {
            setStarRating(starVal);
        });
    });

    async function openFeedbackModal() {
        if (!feedbackModal) return;
        setStarRating(0);
        if (feedbackCommentInput) feedbackCommentInput.value = '';

        try {
            const res = await fetch('/api/feedback/active-question');
            const data = await res.json();
            if (data.status === 'success' && data.data) {
                if (viewerFeedbackQuestionText) {
                    viewerFeedbackQuestionText.textContent = data.data.question;
                }
                if (feedbackQuestionId) {
                    feedbackQuestionId.value = data.data.id || 1;
                }
            }
        } catch (err) {
            console.error('Error fetching active feedback question:', err);
        }

        feedbackModal.style.display = 'flex';
    }

    if (gloryFeedbackBtn) {
        gloryFeedbackBtn.addEventListener('click', openFeedbackModal);
    }
    if (cardFeedbackBtn) {
        cardFeedbackBtn.addEventListener('click', openFeedbackModal);
    }

    if (feedbackModalCloseBtn && feedbackModal) {
        feedbackModalCloseBtn.addEventListener('click', () => {
            feedbackModal.style.display = 'none';
        });
    }

    if (feedbackModal) {
        feedbackModal.addEventListener('click', (e) => {
            if (e.target === feedbackModal) feedbackModal.style.display = 'none';
        });
    }

    if (gloryFeedbackForm) {
        gloryFeedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (currentSelectedRating < 1 || currentSelectedRating > 5) {
                showToast('Please tap on the stars to select your rating (1-5) ✦');
                return;
            }

            const qId = feedbackQuestionId ? parseInt(feedbackQuestionId.value, 10) : null;
            const qText = viewerFeedbackQuestionText ? viewerFeedbackQuestionText.textContent.trim() : '';
            const comment = feedbackCommentInput ? feedbackCommentInput.value.trim() : '';
            const sender = currentUser || 'Glory';

            try {
                if (feedbackSubmitBtn) feedbackSubmitBtn.disabled = true;
                const res = await fetch('/api/feedback/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question_id: qId,
                        question_text: qText,
                        rating: currentSelectedRating,
                        sender: sender,
                        comment: comment
                    })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    feedbackModal.style.display = 'none';
                    showToast(`Thank you, Glory! Your ${currentSelectedRating}-star rating was sent to Yash! ✦`);
                    playSupernovaFanfare();
                    fetchAndRenderAdminFeedback();
                } else {
                    showToast('Failed to submit feedback.');
                }
            } catch (err) {
                console.error('Feedback submit error:', err);
                showToast('Network error submitting feedback.');
            } finally {
                if (feedbackSubmitBtn) feedbackSubmitBtn.disabled = false;
            }
        });
    }

    // Admin Question Creator Form
    if (adminNewQuestionForm) {
        adminNewQuestionForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const question = adminNewQuestionInput ? adminNewQuestionInput.value.trim() : '';
            if (!question) return;

            try {
                if (adminPublishQuestionBtn) adminPublishQuestionBtn.disabled = true;
                const res = await fetch('/api/admin/feedback/question', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    if (adminNewQuestionInput) adminNewQuestionInput.value = '';
                    showToast('New question published for Glory! ✦');
                    fetchAndRenderAdminFeedback();
                } else {
                    showToast('Failed to publish question.');
                }
            } catch (err) {
                console.error('Error publishing question:', err);
                showToast('Network error publishing question.');
            } finally {
                if (adminPublishQuestionBtn) adminPublishQuestionBtn.disabled = false;
            }
        });
    }

    // Admin Feedback & Ratings Engine (Yash)
    function renderStarDisplay(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            stars += (i <= rating) ? '★' : '☆';
        }
        return stars;
    }

    async function fetchAndRenderAdminFeedback() {
        try {
            const res = await fetch('/api/admin/feedback');
            const data = await res.json();
            if (data.status !== 'success') return;

            const activeQ = data.active_question || {};
            const stats = data.stats || { total_count: 0, average_rating: 0.0, breakdown: {} };
            const responses = data.responses || [];

            // Update Active Question
            if (drawerActiveQuestionText) {
                drawerActiveQuestionText.textContent = activeQ.question || 'How would you rate this experience?';
            }
            if (adminModalActiveQuestionText) {
                adminModalActiveQuestionText.textContent = activeQ.question || 'How would you rate this experience?';
            }

            // Update Stats
            const avgStr = `${stats.average_rating || 0.0} ★`;
            const countNum = stats.total_count || 0;
            const fiveStars = (stats.breakdown && stats.breakdown[5]) ? stats.breakdown[5] : 0;

            if (drawerAvgRating) drawerAvgRating.textContent = avgStr;
            if (drawerTotalFeedbackCount) drawerTotalFeedbackCount.textContent = countNum;
            if (feedbackBadgeCount) feedbackBadgeCount.textContent = countNum;

            if (adminModalAvgRating) adminModalAvgRating.textContent = avgStr;
            if (adminModalTotalCount) adminModalTotalCount.textContent = countNum;
            if (adminModalFiveStarCount) adminModalFiveStarCount.textContent = fiveStars;
            if (adminFeedbackCountPill) {
                adminFeedbackCountPill.textContent = `${countNum} REVIEW${countNum === 1 ? '' : 'S'}`;
            }

            // Render Drawer List
            if (drawerFeedbackList) {
                if (responses.length === 0) {
                    drawerFeedbackList.innerHTML = '<div class="empty-replies">No feedback submissions received yet from Glory.</div>';
                } else {
                    drawerFeedbackList.innerHTML = '';
                    responses.forEach(f => {
                        const item = document.createElement('div');
                        item.className = 'reply-item-card';
                        const timeStr = formatTransmissionTime(f.created_at);
                        const starStr = renderStarDisplay(f.rating);

                        item.innerHTML = `
                            <div class="reply-item-meta">
                                <span class="reply-sender-name">★ ${escapeHtml(f.sender)} (${f.rating}/5)</span>
                                <span class="reply-time">${escapeHtml(timeStr)}</span>
                            </div>
                            <div style="color: #ffd700; font-size: 0.95rem; margin-top: 3px; letter-spacing: 2px;">
                                ${starStr}
                            </div>
                            <div style="font-family: var(--font-tech); font-size: 0.7rem; color: rgba(255,255,255,0.6); margin-top: 5px;">
                                💬 ${escapeHtml(f.question_text || '')}
                            </div>
                            ${f.comment ? `<div style="font-family: var(--font-heading); font-size: 0.8rem; color: #fff; margin-top: 6px; font-style: italic;">"${escapeHtml(f.comment)}"</div>` : ''}
                        `;
                        drawerFeedbackList.appendChild(item);
                    });
                }
            }

            // Render Dedicated Admin Modal Container
            if (adminFeedbackListContainer) {
                if (responses.length === 0) {
                    adminFeedbackListContainer.innerHTML = `
                        <div class="empty-replies">
                            <div class="radar-scan-box">
                                <div class="radar-sweep"></div>
                                <span class="radar-icon">★</span>
                            </div>
                            <p class="radar-text">NO VIEWER FEEDBACK RECORDED YET</p>
                        </div>
                    `;
                } else {
                    adminFeedbackListContainer.innerHTML = '';
                    responses.forEach(f => {
                        const card = document.createElement('div');
                        card.className = 'feedback-review-card';
                        const timeStr = formatLogDateTime(f.created_at);
                        const starStr = renderStarDisplay(f.rating);

                        card.innerHTML = `
                            <div class="feedback-card-header">
                                <div class="feedback-card-user">
                                    <div class="log-user-avatar viewer">${(f.sender || 'G').charAt(0).toUpperCase()}</div>
                                    <div>
                                        <span class="log-username">${escapeHtml(f.sender)}</span>
                                        <div class="log-meta-row" style="margin-top: 2px;">
                                            <span>📅 ${escapeHtml(timeStr.dateStr)} • ⏰ ${escapeHtml(timeStr.timeStr)}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="feedback-card-stars">${starStr} <span style="font-family: var(--font-tech); font-size: 0.8rem; color: #fbbf24; margin-left: 4px;">(${f.rating}/5)</span></div>
                            </div>
                            <div class="feedback-card-question">
                                <strong>QUESTION:</strong> ${escapeHtml(f.question_text || '')}
                            </div>
                            ${f.comment ? `<div class="feedback-card-comment">"${escapeHtml(f.comment)}"</div>` : ''}
                        `;
                        adminFeedbackListContainer.appendChild(card);
                    });
                }
            }
        } catch (err) {
            console.error('Error fetching admin feedback:', err);
        }
    }

    if (adminFeedbackBtn && adminFeedbackModal) {
        adminFeedbackBtn.addEventListener('click', () => {
            adminFeedbackModal.style.display = 'flex';
            fetchAndRenderAdminFeedback();
        });
    }

    if (adminFeedbackModalCloseBtn && adminFeedbackModal) {
        adminFeedbackModalCloseBtn.addEventListener('click', () => {
            adminFeedbackModal.style.display = 'none';
        });
    }

    if (modalRefreshFeedbackBtn) {
        modalRefreshFeedbackBtn.addEventListener('click', () => {
            fetchAndRenderAdminFeedback();
            showToast('Feedback ratings refreshed ✦');
        });
    }

    if (refreshDrawerFeedbackBtn) {
        refreshDrawerFeedbackBtn.addEventListener('click', () => {
            fetchAndRenderAdminFeedback();
            showToast('Feedback ratings refreshed ✦');
        });
    }

    if (adminFeedbackModal) {
        adminFeedbackModal.addEventListener('click', (e) => {
            if (e.target === adminFeedbackModal) adminFeedbackModal.style.display = 'none';
        });
    }

    // ==========================================================================
    // 11. Viewport & Parallax Engine + Stardust Comet Trails
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
