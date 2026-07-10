const storageKey = "mtc-daily-assistant-v01";

const elements = {
  todayLabel: document.querySelector("#todayLabel"),
  clockLabel: document.querySelector("#clockLabel"),
  startDayBtn: document.querySelector("#startDayBtn"),
  mainFocus: document.querySelector("#mainFocus"),
  checkCalendar: document.querySelector("#checkCalendar"),
  checkJournal: document.querySelector("#checkJournal"),
  checkFollowups: document.querySelector("#checkFollowups"),
  checkCloseoff: document.querySelector("#checkCloseoff"),
  followupInput: document.querySelector("#followupInput"),
  addFollowupBtn: document.querySelector("#addFollowupBtn"),
  followupList: document.querySelector("#followupList"),
  workingNote: document.querySelector("#workingNote"),
  clearNoteBtn: document.querySelector("#clearNoteBtn"),
  closeOffBtn: document.querySelector("#closeOffBtn"),
  journalOutput: document.querySelector("#journalOutput"),
  copyJournalBtn: document.querySelector("#copyJournalBtn"),
  resetDayBtn: document.querySelector("#resetDayBtn"),
  statusMessage: document.querySelector("#statusMessage")
};

let state = {
  dateStarted: "",
  mainFocus: "",
  checks: {
    calendar: false,
    journal: false,
    followups: false,
    closeoff: false
  },
  followups: [],
  workingNote: "",
  journalOutput: ""
};

function formatDate(date) {
  return new Intl.DateTimeFormat("en-AU", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric"
  }).format(date);
}

function formatTime(date) {
  return new Intl.DateTimeFormat("en-AU", {
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

function updateClock() {
  const now = new Date();
  elements.todayLabel.textContent = formatDate(now);
  elements.clockLabel.textContent = formatTime(now);
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function loadState() {
  const saved = localStorage.getItem(storageKey);
  if (!saved) return;
  try {
    state = { ...state, ...JSON.parse(saved) };
  } catch {
    localStorage.removeItem(storageKey);
  }
}

function showStatus(message) {
  elements.statusMessage.textContent = message;
  window.clearTimeout(showStatus.timer);
  showStatus.timer = window.setTimeout(() => {
    elements.statusMessage.textContent = "";
  }, 2500);
}

function syncInputs() {
  elements.mainFocus.value = state.mainFocus;
  elements.checkCalendar.checked = state.checks.calendar;
  elements.checkJournal.checked = state.checks.journal;
  elements.checkFollowups.checked = state.checks.followups;
  elements.checkCloseoff.checked = state.checks.closeoff;
  elements.workingNote.value = state.workingNote;
  elements.journalOutput.value = state.journalOutput;
  renderFollowups();
}

function renderFollowups() {
  elements.followupList.innerHTML = "";

  if (state.followups.length === 0) {
    const empty = document.createElement("li");
    empty.className = "followup-item";
    empty.innerHTML = "<span></span><span>No follow-ups added yet.</span><span></span>";
    elements.followupList.append(empty);
    return;
  }

  state.followups.forEach((item) => {
    const li = document.createElement("li");
    li.className = `followup-item${item.done ? " done" : ""}`;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = item.done;
    checkbox.addEventListener("change", () => {
      item.done = checkbox.checked;
      saveState();
      renderFollowups();
    });

    const text = document.createElement("span");
    text.textContent = item.text;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "small-button";
    remove.textContent = "Remove";
    remove.addEventListener("click", () => {
      state.followups = state.followups.filter((followup) => followup.id !== item.id);
      saveState();
      renderFollowups();
    });

    li.append(checkbox, text, remove);
    elements.followupList.append(li);
  });
}

function addFollowup() {
  const text = elements.followupInput.value.trim();
  if (!text) return;

  state.followups.push({
    id: crypto.randomUUID(),
    text,
    done: false
  });
  elements.followupInput.value = "";
  saveState();
  renderFollowups();
}

function startDay() {
  state.dateStarted = new Date().toISOString();
  if (!state.mainFocus) {
    state.mainFocus = "Review yesterday, choose top follow-ups, and save close-off notes during the day.";
  }
  state.checks.calendar = true;
  state.checks.journal = true;
  saveState();
  syncInputs();
  showStatus("Day started.");
}

function buildJournalEntry() {
  const now = new Date();
  const activeFollowups = state.followups.filter((item) => !item.done).map((item) => `- [ ] ${item.text}`);
  const completedFollowups = state.followups.filter((item) => item.done).map((item) => `- [x] ${item.text}`);

  const lines = [
    `## Close-Off Checkpoint`,
    ``,
    `Timestamp: ${formatDate(now)} ${formatTime(now)} Sydney time`,
    ``,
    `### Main Focus`,
    state.mainFocus || "Not recorded.",
    ``,
    `### Working Note`,
    state.workingNote.trim() || "No working note recorded.",
    ``,
    `### Open Follow-Ups`,
    activeFollowups.length ? activeFollowups.join("\n") : "No open follow-ups recorded.",
    ``,
    `### Completed Follow-Ups`,
    completedFollowups.length ? completedFollowups.join("\n") : "No completed follow-ups recorded.",
    ``,
    `### Start-Day Checks`,
    `- Calendar / teaching day checked: ${state.checks.calendar ? "Yes" : "No"}`,
    `- Yesterday's journal reviewed: ${state.checks.journal ? "Yes" : "No"}`,
    `- Top follow-ups picked: ${state.checks.followups ? "Yes" : "No"}`,
    `- Close-off completed before switching tasks: ${state.checks.closeoff ? "Yes" : "No"}`
  ];

  state.journalOutput = lines.join("\n");
  elements.journalOutput.value = state.journalOutput;
  saveState();
  showStatus("Journal entry created.");
}

function resetDay() {
  const confirmed = window.confirm("Reset today's assistant page? This only clears this browser page, not your MTC files.");
  if (!confirmed) return;

  state = {
    dateStarted: "",
    mainFocus: "",
    checks: {
      calendar: false,
      journal: false,
      followups: false,
      closeoff: false
    },
    followups: [],
    workingNote: "",
    journalOutput: ""
  };
  saveState();
  syncInputs();
  showStatus("Day reset.");
}

function bindEvents() {
  elements.startDayBtn.addEventListener("click", startDay);
  elements.addFollowupBtn.addEventListener("click", addFollowup);
  elements.followupInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") addFollowup();
  });

  elements.mainFocus.addEventListener("input", () => {
    state.mainFocus = elements.mainFocus.value;
    saveState();
  });
  elements.workingNote.addEventListener("input", () => {
    state.workingNote = elements.workingNote.value;
    saveState();
  });

  elements.checkCalendar.addEventListener("change", () => {
    state.checks.calendar = elements.checkCalendar.checked;
    saveState();
  });
  elements.checkJournal.addEventListener("change", () => {
    state.checks.journal = elements.checkJournal.checked;
    saveState();
  });
  elements.checkFollowups.addEventListener("change", () => {
    state.checks.followups = elements.checkFollowups.checked;
    saveState();
  });
  elements.checkCloseoff.addEventListener("change", () => {
    state.checks.closeoff = elements.checkCloseoff.checked;
    saveState();
  });

  elements.clearNoteBtn.addEventListener("click", () => {
    elements.workingNote.value = "";
    state.workingNote = "";
    saveState();
  });
  elements.closeOffBtn.addEventListener("click", buildJournalEntry);
  elements.copyJournalBtn.addEventListener("click", async () => {
    if (!state.journalOutput) buildJournalEntry();
    await navigator.clipboard.writeText(state.journalOutput);
    showStatus("Journal text copied.");
  });
  elements.resetDayBtn.addEventListener("click", resetDay);
}

loadState();
updateClock();
syncInputs();
bindEvents();
window.setInterval(updateClock, 30000);
