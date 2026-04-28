/**
 * AP Calculus AB — Course Hub Main JS
 * Handles: navigation state, mobile menu, data loading (review page)
 */

(function () {
  "use strict";

  /* ── Navigation ─────────────────────────────────────────── */

  function initNav() {
    const toggle = document.querySelector(".nav-toggle");
    const links  = document.querySelector(".nav-links");
    if (toggle && links) {
      toggle.addEventListener("click", function () {
        const open = links.classList.toggle("open");
        toggle.setAttribute("aria-expanded", String(open));
      });
    }

    // Highlight the active nav link based on current page filename
    const current = window.location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-links a").forEach(function (a) {
      const href = a.getAttribute("href").split("/").pop();
      if (href === current) {
        a.classList.add("active");
        a.setAttribute("aria-current", "page");
      }
    });
  }

  /* ── Smooth scroll for in-page anchors ──────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        const target = document.querySelector(a.getAttribute("href"));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }

  /* ── Animated stat bars (units page) ────────────────────── */
  function initStatBars() {
    const bars = document.querySelectorAll(".stat-bar-fill[data-pct]");
    if (!bars.length) return;

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const bar = entry.target;
            bar.style.width = bar.dataset.pct + "%";
            observer.unobserve(bar);
          }
        });
      },
      { threshold: 0.2 }
    );
    bars.forEach(function (bar) {
      bar.style.width = "0%";
      observer.observe(bar);
    });
  }

  /* ── Review page: load JSON data ────────────────────────── */
  function initReviewPage() {
    const container = document.getElementById("review-data-container");
    if (!container) return;

    // Determine relative path from current page to site/data/
    const scriptPath  = document.querySelector('script[src*="main.js"]');
    const basePath    = scriptPath
      ? scriptPath.getAttribute("src").replace("assets/js/main.js", "")
      : "../";

    const dataUrl = basePath + "data/review-priorities.json";

    container.innerHTML =
      '<div class="loading-spinner"><div class="spinner"></div> Loading review data…</div>';

    fetch(dataUrl)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        renderReviewData(container, data);
      })
      .catch(function (err) {
        console.warn("Could not load review-priorities.json:", err.message);
        renderFallbackReview(container);
      });
  }

  function renderReviewData(container, data) {
    const priorities = ["High", "Medium", "Low"];
    const headerClass = { High: "priority-header--high", Medium: "priority-header--medium", Low: "priority-header--low" };
    const icons       = { High: "🔴", Medium: "🟡", Low: "🟢" };
    const labels      = { High: "High Priority", Medium: "Medium Priority", Low: "Maintenance / Low Priority" };

    let html = "";
    priorities.forEach(function (level) {
      const items = (data.skills || []).filter(function (s) {
        return s.review_priority === level;
      });
      if (!items.length) return;

      html += '<div class="priority-section">';
      html += '<div class="priority-section-header ' + headerClass[level] + '">';
      html += '<span style="font-size:1.1rem">' + icons[level] + '</span>';
      html += '<h3>' + labels[level] + '</h3>';
      html += '<span class="pcount">' + items.length + " skills</span>";
      html += "</div>";
      html += '<div class="priority-section-body">';
      items.forEach(function (item) {
        html += '<div class="priority-item">';
        html += '<div class="priority-item-unit">Unit ' + item.unit + "</div>";
        html += '<div class="priority-item-content">';
        html += '<div class="priority-item-skill">' + escHtml(item.skill) + "</div>";
        html += '<div class="priority-item-topic">' + escHtml(item.topic) + "</div>";
        html += "</div></div>";
      });
      html += "</div></div>";
    });

    container.innerHTML = html || '<p class="text-center" style="color:var(--gray-400)">No review data found.</p>';
  }

  function renderFallbackReview(container) {
    container.innerHTML =
      '<div class="info-banner">' +
      '<span class="info-banner-icon">ℹ️</span>' +
      '<span>Live data not yet generated. Run <code>python tools/export_site_data.py</code> to populate <code>site/data/review-priorities.json</code>, then reload this page. ' +
      "The starter priority table below is loaded from the static fallback.</span>" +
      "</div>" +
      document.getElementById("review-static-fallback").innerHTML;
  }

  /* ── Units page: load JSON data ─────────────────────────── */
  function initUnitsPage() {
    // Units page is fully static — no fetch needed.
    // This hook is available for future chart/badge injection.
    document.querySelectorAll(".unit-card").forEach(function (card, i) {
      // stagger entrance animation
      card.style.animationDelay = i * 0.04 + "s";
    });
  }

  /* ── Utility ─────────────────────────────────────────────── */
  function escHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ── Init ────────────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initSmoothScroll();
    initStatBars();
    initReviewPage();
    initUnitsPage();
  });
})();
