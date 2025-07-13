// Navegación del Dashboard
document.addEventListener("DOMContentLoaded", () => {
  // Elementos del DOM
  const navLinks = document.querySelectorAll(".nav-link")
  const contentSections = document.querySelectorAll(".content-section")
  const navItems = document.querySelectorAll(".nav-item")

  // Función para cambiar de sección
  function switchSection(targetSection) {
    // Ocultar todas las secciones
    contentSections.forEach((section) => {
      section.classList.remove("active")
    })

    // Remover clase active de todos los nav items
    navItems.forEach((item) => {
      item.classList.remove("active")
    })

    // Mostrar la sección seleccionada
    const targetElement = document.getElementById(targetSection)
    if (targetElement) {
      targetElement.classList.add("active")
    }

    // Agregar clase active al nav item correspondiente
    const activeNavLink = document.querySelector(`[data-section="${targetSection}"]`)
    if (activeNavLink) {
      activeNavLink.closest(".nav-item").classList.add("active")
    }

    // Scroll al top del contenido
    document.querySelector(".main-content").scrollTop = 0
  }

  // Event listeners para los enlaces de navegación
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()
      const targetSection = this.getAttribute("data-section")
      switchSection(targetSection)
    })
  })

  // Animaciones para las tarjetas de estadísticas
  function animateStats() {
    const statNumbers = document.querySelectorAll(".stat-number")

    statNumbers.forEach((stat) => {
      const finalValue = stat.textContent
      const isPercentage = finalValue.includes("%")
      const isNumber = !isNaN(Number.parseFloat(finalValue.replace(/[^\d.-]/g, "")))

      if (isNumber && !isPercentage) {
        const numericValue = Number.parseFloat(finalValue.replace(/[^\d.-]/g, ""))
        animateNumber(stat, 0, numericValue, finalValue)
      }
    })
  }

  // Función para animar números
  function animateNumber(element, start, end, originalText) {
    const duration = 2000
    const startTime = performance.now()

    function updateNumber(currentTime) {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)

      const current = Math.floor(start + (end - start) * progress)

      if (originalText.includes(",")) {
        element.textContent = current.toLocaleString()
      } else {
        element.textContent = current.toString()
      }

      if (progress < 1) {
        requestAnimationFrame(updateNumber)
      } else {
        element.textContent = originalText
      }
    }

    requestAnimationFrame(updateNumber)
  }

  // Función para actualizar datos en tiempo real (simulado)
  function updateRealTimeData() {
    const statNumbers = document.querySelectorAll(".stat-number")

    statNumbers.forEach((stat) => {
      const currentValue = stat.textContent
      if (currentValue.includes(",")) {
        const numValue = Number.parseInt(currentValue.replace(/,/g, ""))
        const variation = Math.floor(Math.random() * 10) - 5 // -5 a +5
        const newValue = Math.max(0, numValue + variation)
        stat.textContent = newValue.toLocaleString()
      }
    })
  }

  // Función para manejar el responsive del sidebar
  function handleResponsive() {
    const sidebar = document.querySelector(".sidebar")
    const mainContent = document.querySelector(".main-content")

    if (window.innerWidth <= 768) {
      // Crear botón de menú móvil si no existe
      if (!document.querySelector(".mobile-menu-btn")) {
        const menuBtn = document.createElement("button")
        menuBtn.className = "mobile-menu-btn"
        menuBtn.innerHTML = '<i class="fas fa-bars"></i>'
        menuBtn.style.cssText = `
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
                `

        menuBtn.addEventListener("click", () => {
          sidebar.classList.toggle("open")
        })

        document.body.appendChild(menuBtn)
      }
    }
  }

  // Función para crear tooltips
  function createTooltips() {
    const elements = document.querySelectorAll("[title]")

    elements.forEach((element) => {
      element.addEventListener("mouseenter", function (e) {
        const tooltip = document.createElement("div")
        tooltip.className = "tooltip"
        tooltip.textContent = this.getAttribute("title")
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
                `

        document.body.appendChild(tooltip)

        const rect = this.getBoundingClientRect()
        tooltip.style.left = rect.left + "px"
        tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + "px"

        this.removeAttribute("title")
        this.setAttribute("data-original-title", tooltip.textContent)
      })

      element.addEventListener("mouseleave", function () {
        const tooltip = document.querySelector(".tooltip")
        if (tooltip) {
          tooltip.remove()
        }

        const originalTitle = this.getAttribute("data-original-title")
        if (originalTitle) {
          this.setAttribute("title", originalTitle)
          this.removeAttribute("data-original-title")
        }
      })
    })
  }

  // Inicializar funciones
  animateStats()
  handleResponsive()
  createTooltips()

  // Actualizar datos cada 30 segundos (simulado)
  setInterval(updateRealTimeData, 30000)

  // Manejar cambios de tamaño de ventana
  window.addEventListener("resize", handleResponsive)

  // Cerrar sidebar en móvil al hacer click fuera
  document.addEventListener("click", (e) => {
    const sidebar = document.querySelector(".sidebar")
    const menuBtn = document.querySelector(".mobile-menu-btn")

    if (
      window.innerWidth <= 768 &&
      sidebar.classList.contains("open") &&
      !sidebar.contains(e.target) &&
      !menuBtn.contains(e.target)
    ) {
      sidebar.classList.remove("open")
    }
  })

  console.log("Dashboard inicializado correctamente")
})
