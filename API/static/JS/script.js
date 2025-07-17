// Configuración de formaciones con jugadores ordenados por posición
const formations = {
  "4-4-2": [
    // Portero
    {
      id: 1,
      position: "GK",
      type: "goalkeeper",
      x: 50,
      y: 80,
    },

    // Defensores (ordenados de izquierda a derecha)
    {
      id: 2,
      position: "LB",
      type: "defender",
      x: 15,
      y: 75,
    },
    {
      id: 3,
      position: "CB",
      type: "defender",
      x: 35,
      y: 75,
    },
    {
      id: 4,
      position: "CB",
      type: "defender",
      x: 65,
      y: 75,
    },
    {
      id: 5,
      position: "RB",
      type: "defender",
      x: 85,
      y: 75,
    },

    // Mediocampistas (ordenados de izquierda a derecha)
    {
      id: 6,
      position: "LM",
      type: "midfielder",
      x: 15,
      y: 50,
    },
    {
      id: 7,
      position: "CM",
      type: "midfielder",
      x: 35,
      y: 50,
    },
    {
      id: 8,
      position: "CM",
      type: "midfielder",
      x: 65,
      y: 50,
    },
    {
      id: 9,
      position: "RM",
      type: "midfielder",
      x: 85,
      y: 50,
    },

    // Delanteros (ordenados de izquierda a derecha)
    {
      id: 10,
      position: "ST",
      type: "forward",
      x: 35,
      y: 25,
    },
    {
      id: 11,
      position: "ST",
      type: "forward",
      x: 65,
      y: 25,
    },
  ],

  "4-3-3": [
    // Portero
    {
      id: 1,
      position: "GK",
      type: "goalkeeper",
      x: 50,
      y: 80,
    },

    // Defensores
    {
      id: 2,
      position: "LB",
      type: "defender",
      x: 15,
      y: 75,
    },
    {
      id: 3,
      position: "CB",
      type: "defender",
      x: 35,
      y: 75,
    },
    {
      id: 4,
      position: "CB",
      type: "defender",
      x: 65,
      y: 75,
    },
    {
      id: 5,
      position: "RB",
      type: "defender",
      x: 85,
      y: 75,
    },

    // Mediocampistas
    {
      id: 6,
      position: "CDM",
      type: "midfielder",
      x: 50,
      y: 60,
    },
    {
      id: 7,
      position: "CM",
      type: "midfielder",
      x: 30,
      y: 45,
    },
    {
      id: 8,
      position: "CM",
      type: "midfielder",
      x: 70,
      y: 45,
    },

    // Delanteros
    {
      id: 9,
      position: "LW",
      type: "forward",
      x: 15,
      y: 25,
    },
    {
      id: 10,
      position: "ST",
      type: "forward",
      x: 50,
      y: 20,
    },
    {
      id: 11,
      position: "RW",
      type: "forward",
      x: 85,
      y: 25,
    },
  ],

  "4-2-3-1": [
    // Portero
    {
      id: 1,
      position: "GK",
      type: "goalkeeper",
      x: 50,
      y: 80,
    },

    // Defensores
    {
      id: 2,
      position: "LB",
      type: "defender",
      x: 15,
      y: 75,
    },
    {
      id: 3,
      position: "CB",
      type: "defender",
      x: 35,
      y: 75,
    },
    {
      id: 4,
      position: "CB",
      type: "defender",
      x: 65,
      y: 75,
    },
    {
      id: 5,
      position: "RB",
      type: "defender",
      x: 85,
      y: 75,
    },

    // Mediocampistas defensivos
    {
      id: 6,
      position: "CDM",
      type: "midfielder",
      x: 35,
      y: 60,
    },
    {
      id: 7,
      position: "CDM",
      type: "midfielder",
      x: 65,
      y: 60,
    },

    // Mediocampistas ofensivos
    {
      id: 8,
      position: "LM",
      type: "midfielder",
      x: 15,
      y: 40,
    },
    {
      id: 9,
      position: "CAM",
      type: "midfielder",
      x: 50,
      y: 35,
    },
    {
      id: 10,
      position: "RM",
      type: "midfielder",
      x: 85,
      y: 40,
    },

    // Delantero
    {
      id: 11,
      position: "ST",
      type: "forward",
      x: 50,
      y: 20,
    },
  ],
};

// Variables globales
let currentFormation = "4-4-2";
let players = [...formations["4-4-2"]];
let selectedPlayer = null;

// Elementos del DOM
const field = document.getElementById("field");
const formationTitle = document.getElementById("formation-title");
const playersGrid = document.getElementById("players-grid");
const instruction = document.getElementById("instruction");
const formationButtons = document.querySelectorAll(".btn");

function init() {
  setupEventListeners();
  renderPlayers();
  renderPlayersInfo();
  loadBestPlayers("4-4-2"); 
}

// Configurar Eventos 
function setupEventListeners() {
  // Botones de formación
  formationButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const formation = e.target.dataset.formation;
      changeFormation(formation);
    });
  });

  // Click en el campo
  field.addEventListener("click", handleFieldClick);
}

// Renderizar jugadores en el campo
function renderPlayers() {
  // Limpiar jugadores existentes
  const existingPlayers = field.querySelectorAll(".player, .player-label");
  existingPlayers.forEach((el) => el.remove());

  // Crear nuevos jugadores
  players.forEach((player) => {
    // Crear elemento del jugador
    const playerElement = document.createElement("div");
    playerElement.className = `player ${player.type}`;
    playerElement.dataset.playerId = player.id;
    playerElement.textContent = player.id;
    playerElement.style.left = `${player.x}%`;
    playerElement.style.top = `${player.y}%`;

    // Crear etiqueta del jugador
    const labelElement = document.createElement("div");
    labelElement.className = "player-label";
    labelElement.textContent = player.name;
    labelElement.style.left = `${player.x}%`;
    labelElement.style.top = `${player.y + 8}%`;

    // Event listener para seleccionar jugador
    playerElement.addEventListener("click", (e) => {
      e.stopPropagation();
      selectPlayer(player.id);
    });

    // Añadir al campo
    field.appendChild(playerElement);
    field.appendChild(labelElement);
  });
}

// Cambiar formación
function changeFormation(formation) {
  currentFormation = formation;
  players = [...formations[formation]];
  selectedPlayer = null;

  // Actualizar botones activos
  formationButtons.forEach((btn) => {
    btn.classList.remove("active");
    if (btn.dataset.formation === formation) {
      btn.classList.add("active");
    }
  });

  // Actualizar UI
  formationTitle.textContent = `Formación Actual: ${formation}`;
  instruction.textContent =
    "Haz clic en un jugador para seleccionarlo y luego en el campo para moverlo";

  renderPlayers();
  renderPlayersInfo();
  loadBestPlayers(formation);
}

// Seleccionar jugador
function selectPlayer(playerId) {
  selectedPlayer = selectedPlayer === playerId ? null : playerId;

  // Actualizar clases visuales
  const playerElements = field.querySelectorAll(".player");
  playerElements.forEach((el) => {
    el.classList.remove("selected");
    if (
      selectedPlayer &&
      Number.parseInt(el.dataset.playerId) === selectedPlayer
    ) {
      el.classList.add("selected");
    }
  });

  // Actualizar instrucciones
  if (selectedPlayer) {
    const player = players.find((p) => p.id === selectedPlayer);
    instruction.textContent = `Jugador seleccionado: ${player.name}. Haz clic en el campo para moverlo.`;
  } else {
    instruction.textContent =
      "Haz clic en un jugador para seleccionarlo y luego en el campo para moverlo";
  }

  renderPlayersInfo();
}
async function loadBestPlayers(formation) {
  try {
    const res = await fetch(`/mejor_11/${formation}`);
    const data = await res.json();

    if (data.error) {
      console.error("Error al cargar mejor 11:", data.error);
      return;
    }

    // Rellenar los nombres reales
    data.forEach((player, index) => {
      if (players[index]) {
        players[index].name = player.name;
      }
    });

    renderPlayers();
    renderPlayersInfo();
  } catch (err) {
    console.error("Error al conectar con el servidor:", err);
  }
}

// Manejar click en el campo
function handleFieldClick(e) {
  if (!selectedPlayer) return;

  const rect = field.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;

  // Limitar movimiento dentro del campo
  const clampedX = Math.max(5, Math.min(95, x));
  const clampedY = Math.max(10, Math.min(95, y));

  // Actualizar posición del jugador
  const playerIndex = players.findIndex((p) => p.id === selectedPlayer);
  if (playerIndex !== -1) {
    players[playerIndex].x = clampedX;
    players[playerIndex].y = clampedY;
  }

  // Deseleccionar jugador
  selectedPlayer = null;
  instruction.textContent =
    "Haz clic en un jugador para seleccionarlo y luego en el campo para moverlo";

  // Re-renderizar
  renderPlayers();
  renderPlayersInfo();
}

// Renderizar información de jugadores
function renderPlayersInfo() {
  playersGrid.innerHTML = "";

  players.forEach((player) => {
    const playerInfo = document.createElement("div");
    playerInfo.className = "player-info";
    if (selectedPlayer === player.id) {
      playerInfo.classList.add("selected");
    }

    playerInfo.innerHTML = `
            <span class="player-number">#${player.id}</span> 
            ${player.name} (${player.position})
        `;

    playersGrid.appendChild(playerInfo);
  });
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", init);
