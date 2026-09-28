const task = document.getElementById("task");
const input = document.getElementById("input-text");
const inputLabel = document.getElementById("input-label");
const submitBtn = document.getElementById("submit-btn");
const buttonLabel = document.getElementById("button-label");
const result = document.getElementById("result");
const status = document.getElementById("status");
const copyBtn = document.getElementById("copy-btn");
const levelField = document.getElementById("level-field");
const weeksField = document.getElementById("weeks-field");
const level = document.getElementById("level");
const weeks = document.getElementById("weeks");
const weeksValue = document.getElementById("weeks-value");

const taskConfig = {
  qa: {
    label: "Your question",
    placeholder: "Example: Which is the largest ocean?",
    button: "Ask EduGenie",
    endpoint: "/qa",
    body: value => ({ text: value })
  },
  explain: {
    label: "Concept to explain",
    placeholder: "Example: Explain the Pythagoras theorem simply.",
    button: "Explain Concept",
    endpoint: "/explain",
    body: value => ({ topic: value })
  },
  quiz: {
    label: "Topic or passage for the quiz",
    placeholder: "Paste a lesson, paragraph, or topic here.",
    button: "Generate Quiz",
    endpoint: "/quiz",
    body: value => ({ text: value })
  },
  summarize: {
    label: "Text to summarize",
    placeholder: "Paste your educational passage here.",
    button: "Summarize",
    endpoint: "/summarize",
    body: value => ({ text: value })
  },
  learn: {
    label: "Topic to learn",
    placeholder: "Example: SQL",
    button: "Build Learning Path",
    endpoint: "/learn/recommendations",
    body: value => ({
      topic: value,
      level: level.value,
      weeks: Number(weeks.value)
    })
  }
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderMarkdownish(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

function renderQuiz(data) {
  return `
    <div class="quiz">
      <h3>${escapeHtml(data.title)}</h3>
      ${data.questions.map((q, index) => `
        <article class="quiz-question">
          <h4>${index + 1}. ${escapeHtml(q.question)}</h4>
          <div class="options">
            ${q.options.map(option => `
              <button class="option" type="button"
                data-correct="${option === q.correct_answer}"
                data-explanation="${escapeHtml(q.explanation)}">
                ${escapeHtml(option)}
              </button>
            `).join("")}
          </div>
          <div class="quiz-feedback" hidden></div>
        </article>
      `).join("")}
    </div>
  `;
}

function renderLearningPath(data) {
  return `
    <div>
      <div class="learning-meta">
        <span>${escapeHtml(data.learner_level)}</span>
        <span>${escapeHtml(data.duration)}</span>
      </div>
      <h3>${escapeHtml(data.topic)}</h3>
      ${data.steps.map((step, index) => `
        <article class="path-step">
          <h4>Stage ${index + 1}: ${escapeHtml(step.stage)}</h4>
          <p><strong>Estimated time:</strong> ${escapeHtml(step.estimated_time)}</p>
          <p><strong>Topics</strong></p>
          <ul>${step.topics.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
          <p><strong>Resources</strong></p>
          <ul>${step.resources.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
          <p><strong>Practice</strong></p>
          <ul>${step.practice.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
        </article>
      `).join("")}
    </div>
  `;
}

function renderResponse(data) {
  if (task.value === "quiz") return renderQuiz(data);
  if (task.value === "learn") return renderLearningPath(data);
  const value = data.answer || data.explanation || data.summary || JSON.stringify(data, null, 2);
  return `<div class="text-result">${renderMarkdownish(value)}</div>`;
}

function updateTask() {
  const config = taskConfig[task.value];
  inputLabel.textContent = config.label;
  input.placeholder = config.placeholder;
  buttonLabel.textContent = config.button;

  const isLearn = task.value === "learn";
  levelField.hidden = !isLearn;
  weeksField.hidden = !isLearn;
}

weeks.addEventListener("input", () => {
  weeksValue.textContent = weeks.value;
});

task.addEventListener("change", updateTask);

submitBtn.addEventListener("click", async () => {
  const value = input.value.trim();
  if (!value) {
    status.textContent = "Please enter something to work with.";
    status.className = "status error";
    return;
  }

  const config = taskConfig[task.value];
  submitBtn.disabled = true;
  copyBtn.hidden = true;
  status.textContent = "EduGenie is thinking…";
  status.className = "status loading";
  result.innerHTML = "";

  try {
    const response = await fetch(config.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config.body(value))
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "The request failed.");
    }

    result.innerHTML = renderResponse(data);
    status.textContent = "Completed";
    status.className = "status success";
    copyBtn.hidden = false;
    attachQuizHandlers();
  } catch (error) {
    status.textContent = error.message;
    status.className = "status error";
    result.innerHTML = `<p class="muted">Try again or check the server configuration.</p>`;
  } finally {
    submitBtn.disabled = false;
  }
});

function attachQuizHandlers() {
  document.querySelectorAll(".option").forEach(option => {
    option.addEventListener("click", () => {
      const question = option.closest(".quiz-question");
      const feedback = question.querySelector(".quiz-feedback");
      const correct = option.dataset.correct === "true";

      question.querySelectorAll(".option").forEach(btn => {
        btn.disabled = true;
      });

      feedback.hidden = false;
      feedback.textContent = correct
        ? `Correct! ${option.dataset.explanation}`
        : `Not quite. ${option.dataset.explanation}`;
      feedback.className = correct
        ? "quiz-feedback correct"
        : "quiz-feedback incorrect";
    });
  });
}

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(result.innerText);
  copyBtn.textContent = "Copied";
  setTimeout(() => copyBtn.textContent = "Copy", 1200);
});

updateTask();
