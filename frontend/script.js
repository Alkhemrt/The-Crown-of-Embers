
let currentEvent = 'intro_event';
let currentPostBattle = null;


async function loadEvent(name) {
  currentEvent = name;
  try {
    const response = await fetch(`http://127.0.0.1:8000/event?name=${name}`);
    const data = await response.json();
    displayStory(data.text);
    displayOptions(data.options);
    updateEventTitle(data.title || name);
    updateFooter(data.footer || "The crown is gone. The night does not end...");
  } catch (error) {
    displayStory("Error loading event.");
    console.error("Error loading event:", error);
  }
}


function displayStory(text) {
  document.getElementById('story-panel').textContent = text;
}

function displayOptions(options) {
  const optionsPanel = document.getElementById('options-panel');
  optionsPanel.innerHTML = '';

  options.forEach(option => {
    const button = document.createElement('button');
    button.textContent = option;
    button.onclick = () => chooseOption(option);
    optionsPanel.appendChild(button);
  });
}

async function chooseOption(option) {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/choose?name=${encodeURIComponent(currentEvent)}&option=${encodeURIComponent(option)}`
    );
    const data = await response.json();

    if (data.battle) {
      await fetch(`http://127.0.0.1:8000/battle/start?enemy_file=${encodeURIComponent(data.enemy_file)}`);
      currentPostBattle = {
        event: data.return_event,
        choice: data.post_battle_choice
      };
      await doBattleTurn();
      return;
    }

    // Normal flow
    if (data.next_event) {
      currentEvent = data.next_event;
      await loadEvent(currentEvent);
      return;
    }

    displayStory(data.text);
    if (data.options) displayOptions(data.options);
    if (data.title) updateEventTitle(data.title);
    if (data.footer) updateFooter(data.footer);
    await updatePlayerUI();

  } catch (error) {
    displayStory("Error processing choice.");
    console.error("Error processing choice:", error);
  }
}





function updateEventTitle(titleText) {
  const borderWidth = 92;
  const padTitle = titleText.toUpperCase().padStart(
    Math.floor((borderWidth + titleText.length) / 2),
    " "
  ).padEnd(borderWidth, " ");
  document.getElementById('event-title').textContent = `+${padTitle}+`;
}

function updateFooter(footerText) {
  document.getElementById('footer-msg').textContent = footerText;
}

async function updatePlayerUI() {
  try {
    const res = await fetch("http://127.0.0.1:8000/player");
    const data = await res.json();

    document.getElementById("stats-panel").textContent =
      `HP : ${data.hp}\nXP : ${data.xp}\nLVL: ${data.level}\nGold: ${data.gold}\nDMG : ${data.damage}`;



    const panel = document.getElementById("inventory-panel");
    panel.innerHTML = "";

    if (data.inventory.length === 0) {
      panel.textContent = "(Empty)";
    } else {
      const tooltip = document.getElementById("tooltip");

      data.inventory.forEach(item => {
        const btn = document.createElement("button");
        btn.textContent = item.name + (item.name === data.equipped ? " [E]" : "");
        if (item.name === data.equipped) {
          btn.classList.add("equipped");
        }

        btn.onclick = async () => {
          await fetch(`http://127.0.0.1:8000/equip?name=${encodeURIComponent(item.name)}`, {
            method: "POST"
          });
          await updatePlayerUI();
        };

        let hoverTimeout;
        btn.addEventListener("mouseenter", (e) => {
          hoverTimeout = setTimeout(() => {
            tooltip.textContent = item.description;
            const rect = btn.getBoundingClientRect();
            tooltip.style.left = `${rect.right + 5}px`;
            tooltip.style.top = `${rect.top}px`;
            tooltip.style.opacity = 1;
          }, 300);
        });

        btn.addEventListener("mouseleave", () => {
          clearTimeout(hoverTimeout);
          tooltip.style.opacity = 0;
        });

        panel.appendChild(btn);
        panel.appendChild(document.createElement("br"));
      });
    }

  } catch (err) {
    console.error("Error loading player data", err);
  }
}

async function doBattleTurn(action = "attack") {
  const res = await fetch(`http://127.0.0.1:8000/battle/step?action=${action}`);
  const data = await res.json();

  displayStory(data.log.join("\n"));
  const optionsPanel = document.getElementById("options-panel");
  optionsPanel.innerHTML = "";

  if (data.outcome === "win") {
    const btn = document.createElement("button");
    btn.textContent = "Continue";
    btn.onclick = async () => {
      const res = await fetch(
        `http://127.0.0.1:8000/choose?name=${encodeURIComponent(currentPostBattle.event)}&option=${encodeURIComponent(currentPostBattle.choice)}`
      );
      const result = await res.json();
      displayStory(result.text);
      displayOptions(result.options);
      updateEventTitle(result.title);
      updateFooter(result.footer);
      await updatePlayerUI();
    };
    optionsPanel.appendChild(btn);
  } else if (data.outcome === "lose") {
    const btn = document.createElement("button");
    btn.textContent = "You Died";
    btn.disabled = true;
    optionsPanel.appendChild(btn);
  } else {
    const attackBtn = document.createElement("button");
    attackBtn.textContent = "Attack";
    attackBtn.onclick = () => doBattleTurn("attack");

    const defendBtn = document.createElement("button");
    defendBtn.textContent = "Defend";
    defendBtn.onclick = () => doBattleTurn("defend");

    optionsPanel.appendChild(attackBtn);
    optionsPanel.appendChild(defendBtn);
  }

  await updatePlayerUI();
}



window.onload = () => {
  loadEvent("intro_event");
  updatePlayerUI();
};