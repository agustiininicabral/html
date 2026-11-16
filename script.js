const LANG_KEY = "portfolio_lang";
const LANG_EXPIRY_KEY = "portfolio_lang_expires";
const LANG_TTL_MS = 3 * 60 * 60 * 1000;
const translations = {
  es: {
    title: "Agustín Cabral — QA Automation, Data Analytics y tecnología",
    description: "Portfolio de Agustín Cabral: análisis de datos, Business Intelligence, SQL, Power BI, QA Automation y desarrollo."
  },
  en: {
    title: "Agustín Cabral — QA Automation, Data Analytics & Technology",
    description: "Agustín Cabral's portfolio: data analytics, Business Intelligence, SQL, Power BI, QA Automation and software development."
  }
};

function readLanguagePreference() {
  try {
    const lang = localStorage.getItem(LANG_KEY);
    const expiresAt = Number(localStorage.getItem(LANG_EXPIRY_KEY));
    return (lang === "es" || lang === "en") && expiresAt > Date.now() ? lang : null;
  } catch (error) {
    console.warn("Language preference could not be read.", error);
    return null;
  }
}

function saveLanguage(lang) {
  try {
    localStorage.setItem(LANG_KEY, lang);
    localStorage.setItem(LANG_EXPIRY_KEY, String(Date.now() + LANG_TTL_MS));
  }
  catch (error) { console.warn("Language preference could not be saved.", error); }
}

function setLanguage(lang, persist = true) {
  if (!["es", "en"].includes(lang)) return;
  if (persist) saveLanguage(lang);
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
  const ogDescription = document.querySelector('meta[property="og:description"]');
  if (ogDescription) ogDescription.content = translations[lang].description;
  const backToTop = document.querySelector('a[href="#home"]');
  if (backToTop) backToTop.setAttribute("aria-label", lang === "es" ? "Volver al inicio" : "Back to top");
}

function setupLanguageGate(showGate) {
  const gate = document.getElementById("language-gate");
  if (!gate) return;
  if (!showGate) {
    document.documentElement.classList.remove("language-choice-required");
    return;
  }

  document.documentElement.classList.add("language-choice-required");
  gate.querySelectorAll(".language-choice").forEach((button) => {
    button.addEventListener("click", () => {
      const lang = button.dataset.lang;
      if (!["es", "en"].includes(lang)) return;
      setLanguage(lang);
      gate.close();
      document.documentElement.classList.remove("language-choice-required");
      const activeToggle = document.querySelector(`.lang-toggle[data-lang="${lang}"]`);
      if (activeToggle) activeToggle.focus();
    });
  });
  gate.addEventListener("cancel", (event) => event.preventDefault());
  gate.showModal();
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

function setupEmailCopy() {
  const button = document.querySelector("[data-copy-email]");
  const status = document.getElementById("copy-email-status");
  if (!button || !status) return;
  if (!navigator.clipboard?.writeText) {
    button.hidden = true;
    return;
  }
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copyEmail);
      status.textContent = document.documentElement.lang === "en" ? "Email copied" : "Correo copiado";
    } catch (error) {
      status.textContent = document.documentElement.lang === "en" ? "Copy unavailable. Use the email link." : "No se pudo copiar. Usá el enlace de correo.";
    }
  });
}

function initialize() {
  document.querySelectorAll(".lang-toggle").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.lang));
  });
  const savedLanguage = readLanguagePreference();
  setLanguage(savedLanguage || "es", false);
  setupLanguageGate(!savedLanguage);
  setupNavigation();
  setupScrollProgress();
  setupEmailCopy();
}

document.addEventListener("DOMContentLoaded", initialize);