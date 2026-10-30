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
    document.getElementById('language-screen').classList.add('hidden');
    document.getElementById('main-content').classList.remove('hidden');

    document.querySelectorAll('#main-nav a').forEach(a => a.classList.remove('active'));
    const firstNav = document.querySelector('#main-nav a[href="#overview"]');
    if (firstNav) firstNav.classList.add('active');

    // Actualiza los botones fijos de cambio de idioma
    document.querySelectorAll('.lang-toggle').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    document.body.classList.add('loaded');
}

function scrollToSection(id) {
    const section = document.getElementById(id);
    if (!section) return;
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function setupObservers() {
    const revealItems = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('show');
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.2 });

    revealItems.forEach(el => revealObserver.observe(el));

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

function toggleBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;
    if (window.scrollY > 280) {
        btn.classList.add('show');
    } else {
        btn.classList.remove('show');
    }
}

function attachEvents() {
    const langButtons = document.querySelectorAll('[data-lang]');
    langButtons.forEach(btn => {
        btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
    });

    const projectButtons = document.querySelectorAll('#show-projects, #hero-projects');
    projectButtons.forEach(btn => {
        btn.addEventListener('click', () => scrollToSection('projects'));
    });

    const navLinks = document.querySelectorAll('#main-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            const target = link.getAttribute('href').replace('#', '');
            scrollToSection(target);
        });
    });

    const back = document.getElementById('back-to-top');
    if (back) {
        back.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    window.addEventListener('scroll', () => toggleBackToTop());
}

function initialize() {
    const savedLanguage = safeGetItem(LANG_KEY);
    if (savedLanguage === 'es' || savedLanguage === 'en') {
        setLanguage(savedLanguage);
    }

    setupObservers();
    attachEvents();
    toggleBackToTop();
}

document.addEventListener('DOMContentLoaded', initialize);