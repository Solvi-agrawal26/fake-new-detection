/**
 * Veritas AI - Fake News Detector Client Logic
 * Handles client validation, asynchronous prediction, micro-animations,
 * dark mode toggling, sample filling, and dynamic result rendering.
 */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------------------
    // DOM Element References
    // -------------------------------------------------------------------------
    const newsInput = document.getElementById("newsInput");
    const checkBtn = document.getElementById("checkBtn");
    const clearBtn = document.getElementById("clearBtn");
    const pasteBtn = document.getElementById("pasteBtn");
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const loadRealSampleBtn = document.getElementById("loadRealSampleBtn");
    const loadFakeSampleBtn = document.getElementById("loadFakeSampleBtn");

    // Counters & Validation Elements
    const wordCountEl = document.getElementById("wordCount");
    const charCountEl = document.getElementById("charCount");
    const readingTimeEl = document.getElementById("readingTime");
    const wordProgressBar = document.getElementById("wordProgressBar");
    const errorMessageEl = document.getElementById("errorMessage");
    const errorTextEl = document.getElementById("errorText");

    // Button state elements
    const btnSpinner = document.getElementById("btnSpinner");
    const btnIcon = document.getElementById("btnIcon");
    const btnText = document.getElementById("btnText");

    // Result Card Elements
    const resultCard = document.getElementById("resultCard");
    const resultCardContainer = document.getElementById("resultCardContainer");
    const verdictBadge = document.getElementById("verdictBadge");
    const verdictIcon = document.getElementById("verdictIcon");
    const verdictLabel = document.getElementById("verdictLabel");
    const verdictSubtext = document.getElementById("verdictSubtext");
    const confidenceValue = document.getElementById("confidenceValue");
    const confidenceExplanation = document.getElementById("confidenceExplanation");
    const realProbText = document.getElementById("realProbText");
    const fakeProbText = document.getElementById("fakeProbText");
    const probRealBar = document.getElementById("probRealBar");
    const probFakeBar = document.getElementById("probFakeBar");
    const resWordCount = document.getElementById("resWordCount");
    const resCharCount = document.getElementById("resCharCount");
    const copyResultBtn = document.getElementById("copyResultBtn");
    const copyResultText = document.getElementById("copyResultText");

    // Limits
    const MIN_WORDS = 20;
    const MAX_CHARS = 5000;

    // -------------------------------------------------------------------------
    // Sample News Articles for Instant Testing
    // -------------------------------------------------------------------------
    const samples = {
        real: "WASHINGTON (Reuters) - The Federal Reserve maintained its benchmark interest rate target on Wednesday, citing meaningful progress in slowing inflation toward its 2 percent annual target. Federal Reserve Chair Jerome Powell stated in a press briefing that economic growth remains resilient and labor market conditions continue to normalize. Policymakers noted that while wage increases have moderated, consumer spending and business investment continue to support domestic economic output. Financial markets reacted calmly to the monetary policy announcement, with treasury yields stabilizing across major bond maturities.",
        fake: "SHOCKING PROOF: Secret underground alien base discovered beneath Denver International Airport runway by whistleblowers! Leaked classified documents claim that high-ranking world leaders regularly meet with reptilian overlords during scheduled runway maintenance. Government spokespeople refused to answer questions, confirming what truth seekers have known for decades: the Illuminati controls commercial air travel and is preparing an apocalyptic underground bunker for the global elite. Share this post immediately before social media censors delete it forever!"
    };

    // -------------------------------------------------------------------------
    // Theme Management (Dark / Light Mode)
    // -------------------------------------------------------------------------
    const savedTheme = localStorage.getItem("veritas_theme") || "dark";
    if (savedTheme === "light") {
        document.body.classList.remove("dark-theme");
    } else {
        document.body.classList.add("dark-theme");
    }

    themeToggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark-theme");
        const currentTheme = document.body.classList.contains("dark-theme") ? "dark" : "light";
        localStorage.setItem("veritas_theme", currentTheme);
    });

    // -------------------------------------------------------------------------
    // Utility Helpers
    // -------------------------------------------------------------------------
    function countWords(text) {
        const trimmed = text.trim();
        if (!trimmed) return 0;
        return trimmed.split(/\s+/).filter(w => w.length > 0).length;
    }

    function calculateReadingTime(words) {
        if (words === 0) return "0 sec read";
        const wpm = 200;
        const minutes = Math.floor(words / wpm);
        const seconds = Math.floor((words % wpm) / (wpm / 60));
        if (minutes > 0) {
            return `~${minutes} min ${seconds > 0 ? seconds + 's' : ''} read`;
        }
        return `~${Math.max(seconds, 5)} sec read`;
    }

    function showError(message) {
        errorTextEl.textContent = message;
        errorMessageEl.style.display = "flex";
        errorMessageEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function clearError() {
        errorMessageEl.style.display = "none";
        errorTextEl.textContent = "";
    }

    // -------------------------------------------------------------------------
    // Input Stats & Live Validation
    // -------------------------------------------------------------------------
    function updateInputStats() {
        const text = newsInput.value;
        const words = countWords(text);
        const chars = text.length;

        // Update counts
        wordCountEl.textContent = words.toLocaleString();
        charCountEl.textContent = chars.toLocaleString();
        readingTimeEl.textContent = calculateReadingTime(words);

        // Progress bar toward MIN_WORDS
        const progressPct = Math.min(100, Math.round((words / MIN_WORDS) * 100));
        wordProgressBar.style.width = `${progressPct}%`;

        if (words >= MIN_WORDS) {
            wordProgressBar.classList.add("ready");
            wordCountEl.parentElement.style.color = "var(--real-color)";
        } else {
            wordProgressBar.classList.remove("ready");
            wordCountEl.parentElement.style.color = "";
        }

        // Warn if approaching or exceeding MAX_CHARS
        if (chars > MAX_CHARS) {
            charCountEl.parentElement.style.color = "var(--fake-color)";
        } else if (chars > MAX_CHARS - 300) {
            charCountEl.parentElement.style.color = "var(--warning-color)";
        } else {
            charCountEl.parentElement.style.color = "";
        }

        // Auto-clear error if user fixed the issue
        if (words >= MIN_WORDS && chars <= MAX_CHARS && errorMessageEl.style.display === "flex") {
            clearError();
        }
    }

    // Event listeners for live typing
    newsInput.addEventListener("input", updateInputStats);
    newsInput.addEventListener("paste", () => setTimeout(updateInputStats, 10));

    // -------------------------------------------------------------------------
    // Quick Sample Buttons
    // -------------------------------------------------------------------------
    loadRealSampleBtn.addEventListener("click", () => {
        newsInput.value = samples.real;
        updateInputStats();
        clearError();
        newsInput.focus();
    });

    loadFakeSampleBtn.addEventListener("click", () => {
        newsInput.value = samples.fake;
        updateInputStats();
        clearError();
        newsInput.focus();
    });

    // -------------------------------------------------------------------------
    // Clipboard Paste Helper
    // -------------------------------------------------------------------------
    pasteBtn.addEventListener("click", async () => {
        try {
            if (navigator.clipboard && navigator.clipboard.readText) {
                const clipText = await navigator.clipboard.readText();
                if (clipText) {
                    newsInput.value = clipText;
                    updateInputStats();
                    clearError();
                    newsInput.focus();
                } else {
                    showError("Clipboard is empty.");
                }
            } else {
                showError("Clipboard access not supported in this browser. Please use Ctrl+V / Cmd+V.");
            }
        } catch (err) {
            showError("Could not access clipboard. Please paste manually using Ctrl+V / Cmd+V.");
        }
    });

    // -------------------------------------------------------------------------
    // Clear Button
    // -------------------------------------------------------------------------
    clearBtn.addEventListener("click", () => {
        newsInput.value = "";
        updateInputStats();
        clearError();
        resultCard.style.display = "none";
        newsInput.focus();
    });

    // -------------------------------------------------------------------------
    // Animate Number Count-up Helper
    // -------------------------------------------------------------------------
    function animateValue(element, start, end, duration = 800) {
        const startTime = performance.now();
        const startVal = parseFloat(start) || 0;
        const endVal = parseFloat(end) || 0;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = startVal + (endVal - startVal) * ease;
            element.textContent = current.toFixed(1);

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = endVal.toFixed(1);
            }
        }

        requestAnimationFrame(update);
    }

    // -------------------------------------------------------------------------
    // Render Prediction Results
    // -------------------------------------------------------------------------
    function renderResult(data) {
        const isReal = data.label === "REAL";
        const confidence = parseFloat(data.confidence) || 0;
        const realProb = data.probabilities ? parseFloat(data.probabilities.real) : (isReal ? confidence : 100 - confidence);
        const fakeProb = data.probabilities ? parseFloat(data.probabilities.fake) : (isReal ? 100 - confidence : confidence);

        // Update card container classes
        resultCardContainer.className = "result-card";
        resultCardContainer.classList.add(isReal ? "state-real" : "state-fake");

        // Verdict Badge & Icon
        if (isReal) {
            verdictLabel.textContent = "VERIFIED REAL";
            verdictIcon.innerHTML = `
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="m9 12 2 2 4-4"/>
                </svg>`;
            verdictSubtext.textContent = "High probability of factual journalistic content";
            confidenceExplanation.textContent =
                "Our machine learning model detected strong stylistic markers of credible journalism, such as neutral attribution, corroborative phrasing, and standard press structure.";
        } else {
            verdictLabel.textContent = "LIKELY FAKE";
            verdictIcon.innerHTML = `
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>`;
            verdictSubtext.textContent = "Potential misinformation or sensationalized claims";
            confidenceExplanation.textContent =
                "Our machine learning model identified statistical patterns often associated with fabricated news, such as sensational hyperbole, urgency triggers, or conspiratorial phrasing.";
        }

        // Animate confidence number
        animateValue(confidenceValue, 0, confidence);

        // Update probability labels & animated bars
        realProbText.textContent = `${realProb.toFixed(1)}%`;
        fakeProbText.textContent = `${fakeProb.toFixed(1)}%`;

        probRealBar.style.width = "0%";
        probFakeBar.style.width = "0%";
        setTimeout(() => {
            probRealBar.style.width = `${realProb}%`;
            probFakeBar.style.width = `${fakeProb}%`;
        }, 50);

        // Update metrics
        resWordCount.textContent = (data.stats && data.stats.word_count) ? data.stats.word_count : countWords(newsInput.value);
        resCharCount.textContent = (data.stats && data.stats.character_count) ? data.stats.character_count : newsInput.value.length;

        // Show card and scroll into view smoothly
        resultCard.style.display = "block";
        resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // -------------------------------------------------------------------------
    // Copy Results Report
    // -------------------------------------------------------------------------
    copyResultBtn.addEventListener("click", async () => {
        const textSample = newsInput.value.slice(0, 140).trim();
        const verdict = verdictLabel.textContent;
        const conf = confidenceValue.textContent;
        const realP = realProbText.textContent;
        const fakeP = fakeProbText.textContent;

        const report = [
            "--- VERITAS AI NEWS VERIFICATION REPORT ---",
            `Verdict: ${verdict}`,
            `Confidence Score: ${conf}%`,
            `Probability Breakdown: Real (${realP}) | Fake (${fakeP})`,
            `Excerpt: "${textSample}..."`,
            "Timestamp: " + new Date().toUTCString(),
            "Notice: Prediction generated by ML TF-IDF Classifier. Not a guarantee of truth."
        ].join("\n");

        try {
            await navigator.clipboard.writeText(report);
            copyResultText.textContent = "Copied!";
            setTimeout(() => {
                copyResultText.textContent = "Copy Report";
            }, 2000);
        } catch (err) {
            console.error("Copy failed", err);
        }
    });

    // -------------------------------------------------------------------------
    // Main Prediction Handler (Fetch API)
    // -------------------------------------------------------------------------
    async function handlePredict() {
        clearError();
        const rawText = newsInput.value;
        const trimmed = rawText.trim();

        // 1. Client-Side Validation
        if (!trimmed) {
            showError("Please enter or paste the news headline or article body to analyze.");
            newsInput.focus();
            return;
        }

        const words = countWords(trimmed);
        if (words < MIN_WORDS) {
            showError(`Text is too short (${words} words). Please provide at least ${MIN_WORDS} words so the model can evaluate sufficient linguistic tokens.`);
            newsInput.focus();
            return;
        }

        if (rawText.length > MAX_CHARS) {
            showError(`Text exceeds maximum allowed length of ${MAX_CHARS.toLocaleString()} characters (currently ${rawText.length.toLocaleString()}). Please shorten your article.`);
            newsInput.focus();
            return;
        }

        // 2. Set UI Loading State
        checkBtn.disabled = true;
        clearBtn.disabled = true;
        btnSpinner.style.display = "inline-block";
        btnIcon.style.display = "none";
        btnText.textContent = "Analyzing Content...";

        try {
            // 3. Asynchronous HTTP POST Request
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ text: rawText })
            });

            const data = await response.json();

            if (!response.ok) {
                // Server returned 400 or 500 error JSON
                const message = data.error || `Server error (${response.status}). Please try again.`;
                showError(message);
                return;
            }

            // 4. Render Dynamic Result
            renderResult(data);

        } catch (err) {
            console.error("Prediction network error:", err);
            showError("Network error: Unable to reach the classification server. Please ensure the Flask backend is running.");
        } finally {
            // 5. Reset UI Loading State
            checkBtn.disabled = false;
            clearBtn.disabled = false;
            btnSpinner.style.display = "none";
            btnIcon.style.display = "inline-block";
            btnText.textContent = "Check News Authenticity";
        }
    }

    // Trigger on Check button click
    checkBtn.addEventListener("click", handlePredict);

    // Allow keyboard shortcut: Ctrl+Enter / Cmd+Enter inside textarea
    newsInput.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            handlePredict();
        }
    });

    // Initialize stats on page load
    updateInputStats();
});
