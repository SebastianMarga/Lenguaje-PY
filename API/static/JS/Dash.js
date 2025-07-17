document.addEventListener("DOMContentLoaded", () => {
  try {
    const navItems = document.querySelectorAll(".nav-item");

    const currentPath = window.location.pathname;

    navItems.forEach((item) => {
      const link = item.querySelector("a");

      // Si la ruta del enlace es igual a la ruta actual del navegador
      if (link && link.getAttribute("href") === currentPath) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });
  } catch (error) {
    console.error("Error al establecer pestaña activa:", error);
  }
});

// Animar estadísticas numéricas
function animateStats() {
  const statNumbers = document.querySelectorAll(".stat-number");

  statNumbers.forEach((stat) => {
    const finalValue = stat.textContent;
    const isPercentage = finalValue.includes("%");
    const isNumber = !isNaN(parseFloat(finalValue.replace(/[^\d.-]/g, "")));

    if (isNumber && !isPercentage) {
      const numericValue = parseFloat(finalValue.replace(/[^\d.-]/g, ""));
      animateNumber(stat, 0, numericValue, finalValue);
    }
  });
}

function animateNumber(element, start, end, originalText) {
  const duration = 2000;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const current = Math.floor(start + (end - start) * progress);

    element.textContent = originalText.includes(",")
      ? current.toLocaleString()
      : current.toString();

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = originalText;
    }
  }

  requestAnimationFrame(update);
}

// Actualización simulada de datos en tiempo real
function updateRealTimeData() {
  document.querySelectorAll(".stat-number").forEach((stat) => {
    const raw = stat.textContent.replace(/,/g, "");
    const num = parseInt(raw);
    if (!isNaN(num)) {
      const variation = Math.floor(Math.random() * 10) - 5;
      stat.textContent = Math.max(0, num + variation).toLocaleString();
    }
  });
}

// Responsive sidebar (modo móvil)
function handleResponsive() {
  const sidebar = document.querySelector(".sidebar");

  if (window.innerWidth <= 768 && !document.querySelector(".mobile-menu-btn")) {
    const btn = document.createElement("button");
    btn.className = "mobile-menu-btn";
    btn.innerHTML = '<i class="fas fa-bars"></i>';
    btn.style.cssText = `
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 1001;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.75rem;
        cursor: pointer;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      `;

    btn.addEventListener("click", () => {
      sidebar?.classList.toggle("open");
    });

    document.body.appendChild(btn);
  }
}

// Tooltips
function createTooltips() {
  document.querySelectorAll("[title]").forEach((el) => {
    el.addEventListener("mouseenter", function () {
      const tooltip = document.createElement("div");
      tooltip.className = "tooltip";
      tooltip.textContent = this.getAttribute("title");
      tooltip.style.cssText = `
          position: absolute;
          background: #1e293b;
          color: white;
          padding: 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.875rem;
          z-index: 1000;
          pointer-events: none;
          white-space: nowrap;
        `;

      document.body.appendChild(tooltip);

      const rect = this.getBoundingClientRect();
      tooltip.style.left = rect.left + "px";
      tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + "px";

      this.setAttribute("data-original-title", tooltip.textContent);
      this.removeAttribute("title");
    });

    el.addEventListener("mouseleave", function () {
      const tooltip = document.querySelector(".tooltip");
      if (tooltip) tooltip.remove();

      const originalTitle = this.getAttribute("data-original-title");
      if (originalTitle) {
        this.setAttribute("title", originalTitle);
        this.removeAttribute("data-original-title");
      }
    });
  });
}

// Inicializar funciones útiles
animateStats();
handleResponsive();
createTooltips();

setInterval(updateRealTimeData, 30000);
window.addEventListener("resize", handleResponsive);

// Cerrar sidebar móvil si se hace clic fuera
document.addEventListener("click", (e) => {
  const sidebar = document.querySelector(".sidebar");
  const menuBtn = document.querySelector(".mobile-menu-btn");

  if (
    window.innerWidth <= 768 &&
    sidebar?.classList.contains("open") &&
    !sidebar.contains(e.target) &&
    !menuBtn?.contains(e.target)
  ) {
    sidebar.classList.remove("open");
  }
});

console.log("Dashboard funcional sin SPA");
