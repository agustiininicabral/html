const LANG_KEY = "portfolio_lang";
const translations = {
  es: {
    title: "Agustín Cabral — QA Automation, Data Analytics y tecnología",
    description: "Portfolio profesional de Agustín Cabral: QA Automation, análisis de datos, desarrollo y automatización."
  },
  en: {
    title: "Agustín Cabral — QA Automation, Data Analytics & Technology",
    description: "Agustín Cabral's professional portfolio: QA Automation, data analytics, software development and automation."
  }
};

function readLanguage() {
  try { return localStorage.getItem(LANG_KEY) === "en" ? "en" : "es"; }
  catch { return "es"; }
}

function saveLanguage(lang) {
  try { localStorage.setItem(LANG_KEY, lang); }
  catch (error) { console.warn("Language preference could not be saved.", error); }
}

function setLanguage(lang) {
  if (!["es", "en"].includes(lang)) return;
  saveLanguage(lang);
  document.documentElement.lang = lang === "es" ? "es-AR" : "en";
  document.querySelectorAll("[data-es][data-en]").forEach((element) => {
    element.textContent = element.getAttribute(`data-${lang}`);
  });
  document.title = translations[lang].title;
  const description = document.querySelector('meta[name="description"]');
  if (description) description.content = translations[lang].description;
  const ogLocale = document.querySelector('meta[property="og:locale"]');
  if (ogLocale) ogLocale.content = lang === "es" ? "es_AR" : "en_US";

  document.querySelectorAll(".lang-toggle").forEach((button) => {
    const active = button.dataset.lang === lang;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  const switcher = document.querySelector(".language-switcher");
  if (switcher) switcher.setAttribute("aria-label", lang === "es" ? "Selector de idioma" : "Language selector");

  const cvPath = lang === "en" ? "cv-en.html" : "cv.html";
  document.querySelectorAll('a[href="cv.html"], a[href="cv-en.html"]').forEach((link) => {
    link.href = cvPath;
  });
  const skip = document.querySelector(".skip-link");
  if (skip) skip.href = "#main";
  const backToTop = document.querySelector('a[href="#home"]');
  if (backToTop) backToTop.setAttribute("aria-label", lang === "es" ? "Volver al inicio" : "Back to top");
}

function setupNavigation() {
  const links = [...document.querySelectorAll(".nav-links a")];
  const sections = links.map((link) => document.querySelector(link.getAttribute("href"))).filter(Boolean);
  if (!("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((link) => link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`));
    });
  }, { rootMargin: "-28% 0px -58% 0px", threshold: 0 });
  sections.forEach((section) => observer.observe(section));
}

function setupScrollProgress() {
  const bar = document.getElementById("progress-bar");
  if (!bar) return;
  let ticking = false;
  const update = () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const value = total > 0 ? (window.scrollY / total) * 100 : 0;
    bar.style.width = `${Math.min(100, Math.max(0, value))}%`;
    ticking = false;
  };
  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
  update();
}

function initialize() {
  document.querySelectorAll(".lang-toggle").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.lang));
  });
  setLanguage(readLanguage());
  setupNavigation();
  setupScrollProgress();
}

document.addEventListener("DOMContentLoaded", initialize);