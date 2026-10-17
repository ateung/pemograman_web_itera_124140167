const STORAGE_KEY = "sela_agenda_v1";
const WEATHER_URL = "https://api.open-meteo.com/v1/forecast?latitude=-5.36&longitude=105.31&current_weather=true";
const PRIORITY_LABELS = { high: "Mendesak", medium: "Penting", normal: "Santai" };
const WEATHER_LABELS = new Map([
  [0, ["Cerah", "☀"]],
  [1, ["Cerah berawan", "🌤"]],
  [2, ["Berawan", "⛅"]],
  [3, ["Mendung", "☁"]],
  [45, ["Berkabut", "☁"]],
  [48, ["Berkabut", "☁"]],
  [51, ["Gerimis", "☂"]],
  [53, ["Gerimis", "☂"]],
  [55, ["Gerimis", "☂"]],
  [61, ["Hujan ringan", "☂"]],
  [63, ["Hujan", "☂"]],
  [65, ["Hujan lebat", "☂"]],
  [80, ["Hujan lokal", "☂"]],
  [81, ["Hujan lokal", "☂"]],
  [82, ["Hujan lebat", "☂"]],
  [95, ["Badai petir", "ϟ"]],
  [96, ["Badai petir", "ϟ"]],
  [99, ["Badai petir", "ϟ"]],
]);

const buatId = () => globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
const tanggalLokal = (date = new Date()) => {
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
};
const tambahHari = (jumlah) => {
  const date = new Date();
  date.setDate(date.getDate() + jumlah);
  return tanggalLokal(date);
};
const escapeHTML = (value = "") =>
  String(value).replace(/[&<>"']/g, (karakter) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[karakter]);

class TaskItem {
  constructor({
    id = buatId(),
    title,
    course = "",
    dueDate = "",
    priority = "normal",
    notes = "",
    completed = false,
    createdAt = new Date().toISOString(),
  }) {
    this.id = typeof id === "string" ? id : buatId();
    this.title = title.trim();
    this.course = course.trim();
    this.dueDate = typeof dueDate === "string" && /^\d{4}-\d{2}-\d{2}$/.test(dueDate) ? dueDate : "";
    this.priority = Object.prototype.hasOwnProperty.call(PRIORITY_LABELS, priority) ? priority : "normal";
    this.notes = notes.trim();
    this.completed = completed === true;
    this.createdAt = createdAt;
  }

  static from(data) {
    if (!data || typeof data !== "object") return null;
    const { id, title, course, dueDate, priority, notes, completed, createdAt } = data;
    if (typeof title !== "string" || title.trim().length < 3) return null;
    if (course !== undefined && typeof course !== "string") return null;
    if (notes !== undefined && typeof notes !== "string") return null;
    return new TaskItem({ id, title, course, dueDate, priority, notes, completed, createdAt });
  }
}

class DashboardApp {
  constructor() {
    this.tasks = this.loadTasks();
    this.filter = "all";
    this.query = "";
    this.editingId = null;

    this.form = document.getElementById("task-form");
    this.taskList = document.getElementById("task-list");
    this.emptyState = document.getElementById("empty-state");
    this.titleInput = document.getElementById("task-title");
    this.feedback = document.getElementById("form-feedback");
    this.searchInput = document.getElementById("search-input");
    this.saveButton = document.getElementById("save-task-button");
    this.cancelButton = document.getElementById("cancel-edit-button");

    this.bindEvents();
    this.render();
    this.loadWeather();
  }

  loadTasks() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === null) {
        const starterTasks = [
          new TaskItem({ title: "Baca materi JavaScript ES6+", course: "PAW", dueDate: tambahHari(0), priority: "high", notes: "Fokus ke arrow function dan template literals." }),
          new TaskItem({ title: "Rangkum catatan kuliah minggu ini", course: "Catatan pribadi", dueDate: tambahHari(1), priority: "medium" }),
          new TaskItem({ title: "Rapikan folder dan file praktikum", course: "Produktivitas", dueDate: tambahHari(3), priority: "normal" }),
        ];
        this.writeTasks(starterTasks);
        return starterTasks;
      }

      const parsed = JSON.parse(saved);
      return Array.isArray(parsed)
        ? parsed.map((item) => TaskItem.from(item)).filter(Boolean)
        : [];
    } catch (error) {
      console.error("Agenda Sela tidak dapat dimuat:", error);
      return [];
    }
  }

  writeTasks(tasks = this.tasks) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
      return true;
    } catch (error) {
      console.error("Agenda Sela tidak dapat disimpan:", error);
      if (this.feedback) this.showFeedback("Penyimpanan browser tidak tersedia. Agenda hanya tersimpan sementara.");
      return false;
    }
  }

  bindEvents() {
    this.form.addEventListener("submit", (event) => this.handleSubmit(event));
    this.cancelButton.addEventListener("click", () => this.cancelEdit());
    this.searchInput.addEventListener("input", ({ target }) => {
      this.query = target.value.trim().toLocaleLowerCase("id-ID");
      this.renderTasks();
    });

    document.querySelectorAll("[data-filter]").forEach((button) => {
      button.addEventListener("click", () => {
        this.filter = button.dataset.filter;
        document.querySelectorAll("[data-filter]").forEach((filterButton) => {
          const isActive = filterButton === button;
          filterButton.classList.toggle("is-active", isActive);
          filterButton.setAttribute("aria-pressed", String(isActive));
        });
        this.renderTasks();
      });
    });

    this.taskList.addEventListener("click", (event) => {
      const actionButton = event.target.closest("[data-action]");
      if (!actionButton) return;
      const { action, id } = actionButton.dataset;
      if (action === "toggle") this.toggleTask(id);
      if (action === "edit") this.editTask(id);
      if (action === "delete") this.deleteTask(id);
    });

    document.getElementById("empty-add-button").addEventListener("click", () => {
      this.titleInput.focus();
      document.getElementById("task-form").scrollIntoView({ behavior: "smooth", block: "center" });
    });
    document.getElementById("refresh-weather").addEventListener("click", () => this.loadWeather());
  }

  handleSubmit(event) {
    event.preventDefault();
    if (!this.form.reportValidity()) return;

    const formData = new FormData(this.form);
    const { title, course, dueDate, priority, notes } = Object.fromEntries(formData.entries());
    const values = { title, course, dueDate, priority, notes };

    if (this.editingId) {
      this.tasks = this.tasks.map((task) =>
        task.id === this.editingId ? new TaskItem({ ...task, ...values }) : task
      );
      this.showFeedback("Perubahan agenda berhasil disimpan.", true);
    } else {
      this.tasks = [new TaskItem(values), ...this.tasks];
      this.showFeedback("Agenda baru berhasil ditambahkan.", true);
    }

    this.writeTasks();
    this.cancelEdit(false);
    this.render();
  }

  toggleTask(id) {
    this.tasks = this.tasks.map((task) =>
      task.id === id ? new TaskItem({ ...task, completed: !task.completed }) : task
    );
    this.writeTasks();
    this.render();
  }

  editTask(id) {
    const task = this.tasks.find((item) => item.id === id);
    if (!task) return;

    this.editingId = id;
    this.form.elements.title.value = task.title;
    this.form.elements.course.value = task.course;
    this.form.elements.dueDate.value = task.dueDate;
    this.form.elements.priority.value = task.priority;
    this.form.elements.notes.value = task.notes;
    document.getElementById("editor-title").textContent = "Ubah agenda";
    this.saveButton.innerHTML = "<span aria-hidden=\"true\">✓</span> Simpan perubahan";
    this.cancelButton.hidden = false;
    this.showFeedback("Mode edit aktif. Perbarui detail agenda di bawah.");
    document.getElementById("task-form").scrollIntoView({ behavior: "smooth", block: "center" });
    this.titleInput.focus({ preventScroll: true });
  }

  cancelEdit(clearFeedback = true) {
    this.editingId = null;
    this.form.reset();
    document.getElementById("editor-title").textContent = "Agenda baru";
    this.saveButton.innerHTML = "<span aria-hidden=\"true\">＋</span> Simpan agenda";
    this.cancelButton.hidden = true;
    if (clearFeedback) this.showFeedback("");
  }

  deleteTask(id) {
    const task = this.tasks.find((item) => item.id === id);
    if (!task || !window.confirm(`Hapus agenda “${task.title}”?`)) return;
    this.tasks = this.tasks.filter((item) => item.id !== id);
    if (this.editingId === id) this.cancelEdit();
    this.writeTasks();
    this.render();
  }

  showFeedback(message, isSuccess = false) {
    this.feedback.textContent = message;
    this.feedback.classList.toggle("success", isSuccess);
  }

  visibleTasks() {
    return this.tasks
      .filter((task) => {
        const matchesFilter = this.filter === "all"
          || (this.filter === "open" && !task.completed)
          || (this.filter === "done" && task.completed);
        const searchable = `${task.title} ${task.course} ${task.notes}`.toLocaleLowerCase("id-ID");
        return matchesFilter && searchable.includes(this.query);
      })
      .sort((first, second) => {
        if (first.completed !== second.completed) return Number(first.completed) - Number(second.completed);
        if (!first.dueDate) return second.dueDate ? 1 : 0;
        if (!second.dueDate) return -1;
        return first.dueDate.localeCompare(second.dueDate);
      });
  }

  render() {
    const total = this.tasks.length;
    const done = this.tasks.filter(({ completed }) => completed).length;
    const open = total - done;
    document.getElementById("stat-total").textContent = total;
    document.getElementById("stat-open").textContent = open;
    document.getElementById("stat-done").textContent = done;
    document.getElementById("filter-all-count").textContent = total;
    document.getElementById("filter-open-count").textContent = open;
    document.getElementById("filter-done-count").textContent = done;
    this.renderTasks();
  }

  renderTasks() {
    const tasks = this.visibleTasks();
    const hasAnyTask = this.tasks.length > 0;
    const hasQuery = this.query.length > 0;
    this.taskList.innerHTML = tasks.map((task) => this.renderTask(task)).join("");
    this.taskList.hidden = tasks.length === 0;
    this.emptyState.hidden = tasks.length > 0;

    if (tasks.length === 0) {
      const isFiltered = hasAnyTask && (hasQuery || this.filter !== "all");
      document.getElementById("empty-title").textContent = isFiltered ? "Belum ada yang cocok" : "Ruangmu masih kosong";
      document.getElementById("empty-description").textContent = isFiltered
        ? "Coba kata kunci atau filter yang berbeda."
        : "Tambahkan agenda pertama dan mulai atur ritme belajarmu.";
      document.getElementById("empty-add-button").hidden = isFiltered;
    }
  }

  renderTask(task) {
    const due = task.dueDate ? new Date(`${task.dueDate}T00:00:00`) : null;
    const today = new Date(`${tanggalLokal()}T00:00:00`);
    const isOverdue = due && due < today && !task.completed;
    const dueLabel = due ? this.formatDueDate(task.dueDate) : "Tanpa tenggat";
    const priorityClass = `priority-${task.priority}`;
    const dueClass = isOverdue ? "date-overdue" : "";
    const note = task.notes ? `<p class="task-description">${escapeHTML(task.notes)}</p>` : "";
    const course = task.course ? `<span class="meta-chip">▧ ${escapeHTML(task.course)}</span>` : "";
    const dueChip = `<span class="meta-chip ${dueClass}">${isOverdue ? "! " : "◷ "}${escapeHTML(dueLabel)}</span>`;

    return `
      <article class="task-card ${task.completed ? "is-complete" : ""}">
        <button class="task-check" type="button" data-action="toggle" data-id="${escapeHTML(task.id)}" aria-label="${task.completed ? "Tandai belum selesai" : "Tandai selesai"}: ${escapeHTML(task.title)}" aria-pressed="${task.completed}">✓</button>
        <div class="task-content">
          <h3 class="task-title">${escapeHTML(task.title)}</h3>
          ${note}
          <div class="task-meta">
            ${course}
            ${dueChip}
            <span class="meta-chip ${priorityClass}">${escapeHTML(PRIORITY_LABELS[task.priority])}</span>
          </div>
        </div>
        <div class="task-actions">
          <button class="task-action" type="button" data-action="edit" data-id="${escapeHTML(task.id)}" aria-label="Ubah ${escapeHTML(task.title)}" title="Ubah agenda">✎</button>
          <button class="task-action delete" type="button" data-action="delete" data-id="${escapeHTML(task.id)}" aria-label="Hapus ${escapeHTML(task.title)}" title="Hapus agenda">×</button>
        </div>
      </article>`;
  }

  formatDueDate(dateString) {
    const date = new Date(`${dateString}T00:00:00`);
    const delta = Math.round((date - new Date(`${tanggalLokal()}T00:00:00`)) / 86_400_000);
    let label = new Intl.DateTimeFormat("id-ID", { day: "numeric", month: "short" }).format(date);
    if (delta === 0) label = "Hari ini";
    else if (delta === 1) label = "Besok";
    else if (delta === -1) label = "Kemarin";
    return label;
  }

  async loadWeather() {
    const value = document.getElementById("weather-value");
    const detail = document.getElementById("weather-detail");
    const symbol = document.getElementById("weather-symbol");
    value.textContent = "Mengambil cuaca…";
    detail.textContent = "Lampung Selatan";

    try {
      const response = await fetch(WEATHER_URL);
      if (!response.ok) throw new Error(`Cuaca tidak tersedia (${response.status})`);
      const { current_weather: currentWeather } = await response.json();
      if (!currentWeather) throw new Error("Data cuaca tidak ditemukan");
      const [condition, icon] = WEATHER_LABELS.get(currentWeather.weathercode) ?? ["Cuaca berubah", "☁"];
      symbol.textContent = icon;
      value.textContent = `${Math.round(currentWeather.temperature)}°C · ${condition}`;
      detail.textContent = "Lampung Selatan · terkini";
    } catch (error) {
      console.warn("Widget cuaca tidak dapat dimuat:", error);
      symbol.textContent = "☁";
      value.textContent = "Cuaca belum tersedia";
      detail.textContent = "Agenda tetap bisa dikelola offline";
    }
  }
}

const tampilkanTanggalHariIni = () => {
  const hariIni = new Intl.DateTimeFormat("id-ID", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date());
  document.getElementById("today-label").textContent = hariIni;
};

tampilkanTanggalHariIni();
new DashboardApp();
