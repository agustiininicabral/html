const LANG_KEY = 'portfolio_lang';

function safeSetItem(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (error) {
        console.warn('No se pudo guardar en localStorage:', error);
    }
}

function safeGetItem(key) {
    try {
        return localStorage.getItem(key);
    } catch (error) {
        return null;
    }
}

function translateAll(lang) {
    document.querySelectorAll(`[data-${lang}]`).forEach(el => {
        el.textContent = el.getAttribute(`data-${lang}`) || el.textContent;
    });
}

function setLanguage(lang) {
    if (!['es', 'en'].includes(lang)) return;
    safeSetItem(LANG_KEY, lang);
    document.documentElement.lang = lang;
    translateAll(lang);

    document.querySelectorAll('#main-nav a').forEach(a => a.classList.remove('active'));
    const firstNav = document.querySelector('#main-nav a[href="#overview"]');
    if (firstNav) firstNav.classList.add('active');

    // Actualiza los botones fijos de cambio de idioma
    document.querySelectorAll('.lang-toggle').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    const languageSwitcher = document.querySelector('.language-switcher');
    if (languageSwitcher) {
        languageSwitcher.setAttribute('aria-label', lang === 'es' ? 'Selector de idioma' : 'Language selector');
    }

    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        backToTop.setAttribute('aria-label', lang === 'es' ? 'Volver arriba' : 'Back to top');
    }

    document.body.classList.add('loaded');
}

function setupObservers() {
    const revealItems = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
        revealItems.forEach(el => el.classList.add('show'));
        return;
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
        revealItems.forEach(el => el.classList.add('show'));
    } else {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('show');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.12 });

        revealItems.forEach(el => revealObserver.observe(el));
    }

    const sections = document.querySelectorAll('main section');
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const link = document.querySelector(`#main-nav a[href="#${entry.target.id}"]`);
            if (!link) return;
            if (entry.isIntersecting) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }, { threshold: 0.45 });

    sections.forEach(section => sectionObserver.observe(section));
}

function updateScrollUI() {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollableHeight > 0 ? (window.scrollY / scrollableHeight) * 100 : 0;
    const progressBar = document.getElementById('scroll-progress-bar');
    const btn = document.getElementById('back-to-top');
    if (progressBar) progressBar.style.width = `${progress}%`;
    if (btn) btn.classList.toggle('show', window.scrollY > 420);
}

function attachEvents() {
    const langButtons = document.querySelectorAll('[data-lang]');
    langButtons.forEach(btn => {
        btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
    });

    const back = document.getElementById('back-to-top');
    if (back) {
        back.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    window.addEventListener('scroll', updateScrollUI, { passive: true });
}

function initialize() {
    document.documentElement.classList.add('js-motion');
    const savedLanguage = safeGetItem(LANG_KEY);
    setLanguage(savedLanguage === 'en' ? 'en' : 'es');

    const hero = document.getElementById('hero');
    if (hero) hero.classList.add('show');

    setupObservers();
    attachEvents();
    updateScrollUI();
}

document.addEventListener('DOMContentLoaded', initialize);