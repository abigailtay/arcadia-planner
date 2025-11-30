import React, { useState } from "react";
import { HexColorPicker } from "react-colorful";

const ICONS = [
  "📚", "🏃‍♂️", "🏋️", "📝", "🎸", "🧹", "🦷", "🥗", "🧘", "🎮"
];

const XP_PER_COMPLETION = 10;
const MAX_TOTAL_XP = 100;

function getBestStreak(arr) {
  let best = 0, curr = 0;
  for (const v of arr) {
    if (v) {
      curr++;
      if (curr > best) best = curr;
    } else {
      curr = 0;
    }
  }
  return best;
}

const DinoMascot = () => (
  <div
    style={{
      width: 80,
      height: 80,
      borderRadius: "50%",
      background: "#ffb6e6",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      boxShadow: "0 2px 16px #c56aef55",
      marginRight: 24
    }}
  >
    <span
      role="img"
      aria-label="Pink Dino"
      style={{ fontSize: 48, transition: "transform .2s" }}
    >
      🦕
    </span>
  </div>
);

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function HabitStars({ daysChecked, color }) {
  const safeDays =
    Array.isArray(daysChecked) && daysChecked.length === 7
      ? daysChecked
      : Array(7).fill(false);
  return (
    <div style={{ display: "flex", gap: 8, margin: "0 0 9px 0" }}>
      {safeDays.map((checked, dayIdx) => (
        <span
          key={dayIdx}
          style={{
            fontSize: 27,
            color: checked ? color : "#e3e3e3",
            filter: checked ? "drop-shadow(0 2px 9px #f7a5e280)" : "none",
            userSelect: "none",
            transition: "color .3s"
          }}
          title={WEEKDAYS[dayIdx]}
        >
          ★
        </span>
      ))}
    </div>
  );
}

function HabitCard({ habit, onCompleteToday, onDelete }) {
  const today = new Date().getDay();
  const completedToday = habit.daysChecked[today];
  const bestStreak = getBestStreak(habit.daysChecked);
  const totalComplete = habit.daysChecked.filter(Boolean).length;
  return (
    <div
      style={{
        borderRadius: 16,
        background: "#f7f7fd",
        boxShadow: "0 1px 8px #fa89e622",
        padding: "19px 20px 15px 20px",
        marginBottom: 18,
        borderLeft: `10px solid ${habit.color}`,
        position: "relative"
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: 7,
          gap: 12
        }}
      >
        <span style={{ fontSize: 33 }}>{habit.icon}</span>
        <span
          style={{ fontWeight: 700, fontSize: 19, color: habit.color }}
        >
          {habit.name}
        </span>
      </div>
      <HabitStars daysChecked={habit.daysChecked} color={habit.color} />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginTop: 5,
          marginBottom: 2
        }}
      >
        <button
          disabled={completedToday}
          onClick={onCompleteToday}
          style={{
            fontSize: 16,
            fontWeight: 700,
            padding: "7px 18px",
            borderRadius: 10,
            background: completedToday ? "#e8e8e8" : "#d72660",
            color: completedToday ? "#aaa" : "#fff",
            border: "none",
            cursor: completedToday ? "default" : "pointer"
          }}
        >
          {completedToday ? "Completed" : "Complete"}
        </button>
        <button
          onClick={onDelete}
          style={{
            fontSize: 15,
            fontWeight: 700,
            padding: "7px 16px",
            borderRadius: 10,
            background: "#ffb6e6",
            color: "#d72660",
            border: "none",
            cursor: "pointer",
            marginLeft: 3
          }}
        >
          Delete
        </button>
        <span style={{ fontSize: 15, color: "#888", marginLeft: 8 }}>
          Done: {totalComplete}/7 &nbsp;|&nbsp; Best: {bestStreak}
        </span>
      </div>
    </div>
  );
}

function ProgressBar({ value, max, level }) {
  const percent = Math.min(100, Math.round((value / max) * 100));
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 10,
        marginLeft: 12,
        width: 235
      }}
    >
      <div
        style={{
          height: 13,
          width: 120,
          background: "#ece8ff",
          borderRadius: 7,
          overflow: "hidden",
          border: "1.5px solid #eee"
        }}
      >
        <div
          style={{
            width: percent + "%",
            height: 13,
            background: "#b350e0",
            transition: "width 0.4s",
            borderRadius: 7
          }}
        />
      </div>
      <span style={{ fontSize: 13, color: "#777", minWidth: 78 }}>
        Level {level} &nbsp; {value} / {max} XP
      </span>
    </div>
  );
}

// Encouragement Popup
function MascotPopup({ message, onClose }) {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        background: "rgba(255,182,230,0.38)",
        zIndex: 200,
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "26px 32px 20px 32px",
          borderRadius: 23,
          border: "4px solid #b350e0",
          boxShadow: "0 8px 36px #b350e032",
          textAlign: "center"
        }}
      >
        <div style={{ fontSize: 60, marginBottom: 4 }}>🦕</div>
        <div
          style={{
            fontWeight: 700,
            fontSize: 22,
            color: "#d72660",
            margin: "17px 0"
          }}
        >
          {message}
        </div>
        <button
          onClick={onClose}
          style={{
            fontSize: 17,
            background: "#d72660",
            color: "#fff",
            border: "none",
            borderRadius: 13,
            padding: "9px 36px",
            fontWeight: 700,
            cursor: "pointer"
          }}
        >
          Keep Going!
        </button>
      </div>
    </div>
  );
}

// Footer Controls
function FooterControls({ onAddHabit, onViewAnalytics }) {
  return (
    <div
      style={{
        position: "fixed",
        left: 0,
        bottom: 0,
        width: "100vw",
        zIndex: 100,
        background: "#fceaff",
        borderTop: "1.5px solid #e6bae4",
        padding: "16px 0",
        display: "flex",
        justifyContent: "center",
        gap: 24,
        boxShadow: "0 -3px 18px #eac4ed30"
      }}
    >
      <button
        onClick={onAddHabit}
        style={{
          fontWeight: 800,
          fontSize: 18,
          color: "#fff",
          background: "#d72660",
          padding: "10px 30px",
          border: "none",
          borderRadius: 16,
          cursor: "pointer",
          marginRight: 10
        }}
      >
        New Habit
      </button>
      <button
        onClick={onViewAnalytics}
        style={{
          fontWeight: 800,
          fontSize: 18,
          color: "#d72660",
          background: "#fff",
          padding: "10px 28px",
          border: "2px solid #d72660",
          borderRadius: 16,
          cursor: "pointer"
        }}
      >
        View Analytics
      </button>
    </div>
  );
}

// Analytics Modal
function AnalyticsModal({ onClose, habits }) {
  const allStreaks = habits.map(h => getBestStreak(h.daysChecked || []));
  const maxStreak = allStreaks.length ? Math.max(...allStreaks) : 0;
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        background: "#fff9",
        zIndex: 201,
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }}
    >
      <div
        style={{
          background: "#fff",
          borderRadius: 16,
          padding: 34,
          minWidth: 320,
          border: "2px solid #b350e0",
          boxShadow: "0 8px 32px #b350e033"
        }}
      >
        <div
          style={{
            fontWeight: 700,
            fontSize: 22,
            color: "#9245b3",
            marginBottom: 14
          }}
        >
          Detailed Analytics
        </div>
        <div style={{ fontSize: 18, color: "#d72660", marginBottom: 8 }}>
          Longest Streak: <strong>{maxStreak}</strong>
        </div>
        <div style={{ fontSize: 16, color: "#b350e0", marginBottom: 10 }}>
          Habits Tracked: <strong>{habits.length}</strong>
        </div>
        <button
          onClick={onClose}
          style={{
            marginTop: 18,
            fontWeight: 700,
            fontSize: 15,
            color: "#fff",
            background: "#d72660",
            border: "none",
            borderRadius: 10,
            padding: "7px 28px",
            cursor: "pointer"
          }}
        >
          Close
        </button>
      </div>
    </div>
  );
}

export default function Habits({ habits = [], setHabits, setActiveSection }) {
  const [showModal, setShowModal] = useState(false);
  const [formName, setFormName] = useState("");
  const [formIcon, setFormIcon] = useState(ICONS[0]);
  const [formColor, setFormColor] = useState("#ffb6e6");
  const [level, setLevel] = useState(1);
  const [totalXP, setTotalXP] = useState(0);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");

  const safeHabits = habits.map(h => ({
    ...h,
    daysChecked:
      Array.isArray(h.daysChecked) && h.daysChecked.length === 7
        ? h.daysChecked
        : Array(7).fill(false)
  }));

  const weekTotalCompletions = safeHabits
    .map(h => h.daysChecked.filter(Boolean).length)
    .reduce((a, b) => a + b, 0);

  const bestStreakAllTime = Math.max(
    ...safeHabits.map(h => getBestStreak(h.daysChecked)),
    0
  );

  function handleCompleteToday(habitIdx) {
    const today = new Date().getDay();
    setHabits(prev =>
      prev.map((h, i) => {
        if (i !== habitIdx) return h;
        const checked =
          Array.isArray(h.daysChecked) && h.daysChecked.length === 7
            ? [...h.daysChecked]
            : Array(7).fill(false);
        checked[today] = true;
        return { ...h, daysChecked: checked };
      })
    );
    setTotalXP(prev => {
      const nextXP = prev + XP_PER_COMPLETION;
      if (nextXP >= MAX_TOTAL_XP) {
        setLevel(l => l + 1);
        setPopupMessage("Level Up! You're now Level " + (level + 1) + " 🦕");
        return nextXP - MAX_TOTAL_XP;
      }
      return nextXP;
    });
  }

  function handleDeleteHabit(habitIdx) {
    setHabits(prev => prev.filter((_, i) => i !== habitIdx));
  }

  function handleCreateHabit(e) {
    e.preventDefault();
    if (!formName.trim()) return;
    const newHabit = {
      name: formName.trim(),
      icon: formIcon,
      color: formColor,
      daysChecked: Array(7).fill(false)
    };
    setHabits(prevHabits => [...prevHabits, newHabit]);
    setShowModal(false);
    setFormName("");
    setFormIcon(ICONS[0]);
    setFormColor("#ffb6e6");
  }

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: 18,
        boxShadow: "0 2px 24px #c56aef22",
        margin: "32px auto",
        padding: "40px 48px 64px 48px",
        maxWidth: 600,
        minHeight: 360,
        position: "relative"
      }}
    >
      {popupMessage && (
        <MascotPopup
          message={popupMessage}
          onClose={() => setPopupMessage("")}
        />
      )}

      {showAnalytics && (
        <AnalyticsModal
          onClose={() => setShowAnalytics(false)}
          habits={safeHabits}
        />
      )}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: 10,
          justifyContent: "flex-start",
          gap: 22
        }}
      >
        <DinoMascot />
        <div>
          <div
            style={{ fontWeight: 700, fontSize: 26, color: "#d72660" }}
          >
            Habits
          </div>
        </div>
        <button
          style={{
            marginLeft: "auto",
            padding: "9px 18px",
            borderRadius: 12,
            border: "none",
            background: "#d72660",
            color: "#fff",
            fontWeight: 700,
            fontSize: 16,
            cursor: "pointer"
          }}
          onClick={() => setActiveSection("dashboard")}
        >
          ← Back to Dashboard
        </button>
      </div>

      <div
        style={{
          margin: "8px 0 15px 0",
          display: "flex",
          alignItems: "center",
          gap: 18,
          justifyContent: "center"
        }}
      >
        <span
          style={{
            fontSize: 16,
            color: "#888",
            whiteSpace: "nowrap"
          }}
        >
          Total Completions: {weekTotalCompletions}
        </span>
        <span
          style={{
            fontSize: 16,
            color: "#993",
            whiteSpace: "nowrap"
          }}
        >
          Best Streak: {bestStreakAllTime}
        </span>
        <ProgressBar value={totalXP} max={MAX_TOTAL_XP} level={level} />
      </div>

      {safeHabits.length === 0 ? (
        <div
          style={{
            marginTop: 24,
            color: "#888",
            fontSize: 18,
            textAlign: "center"
          }}
        >
          No habits yet!
          <br />
          Click “New Habit” to get started.
        </div>
      ) : (
        <div>
          {safeHabits.map((habit, idx) => (
            <HabitCard
              key={idx}
              habit={habit}
              onCompleteToday={() => handleCompleteToday(idx)}
              onDelete={() => handleDeleteHabit(idx)}
            />
          ))}
        </div>
      )}

      {showModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            zIndex: 2000,
            background: "#1114",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            pointerEvents: "none"
          }}
        >
          <div
            style={{
              maxHeight: "80vh",
              width: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              pointerEvents: "auto",
              overflowY: "auto",
              padding: "20px 0"
            }}
          >
            <form
              style={{
                background: "#fff",
                borderRadius: 18,
                boxShadow: "0 8px 32px #c56aef36",
                padding: "38px 36px 32px 36px",
                minWidth: 360,
                maxWidth: 380,
                display: "flex",
                flexDirection: "column",
                gap: 18,
                alignItems: "center"
              }}
              onSubmit={handleCreateHabit}
            >
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 700,
                  marginBottom: 18,
                  color: "#d72660"
                }}
              >
                Create New Habit
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 14,
                  marginBottom: 4
                }}
              >
                <span
                  style={{
                    fontSize: 34,
                    background: formColor,
                    borderRadius: "50%",
                    padding: 8
                  }}
                >
                  {formIcon}
                </span>
                <span
                  style={{
                    fontSize: 20,
                    fontWeight: 700,
                    color: formColor
                  }}
                >
                  {formName || "Your habit name"}
                </span>
              </div>
              <input
                type="text"
                value={formName}
                onChange={e => setFormName(e.target.value)}
                placeholder="Habit Name"
                style={{
                  fontSize: 18,
                  padding: "8px 14px",
                  borderRadius: 8,
                  border: "1px solid #eee",
                  outline: "none",
                  width: "100%"
                }}
                autoFocus
                required
                maxLength={26}
              />
              <div style={{ width: "100%", margin: "8px 0 12px 0" }}>
                <div
                  style={{
                    fontSize: 15,
                    marginBottom: 4,
                    color: "#555"
                  }}
                >
                  Select Icon:
                </div>
                <div
                  style={{
                    display: "flex",
                    gap: 10,
                    flexWrap: "wrap"
                  }}
                >
                  {ICONS.map(icon => (
                    <label
                      key={icon}
                      style={{
                        cursor: "pointer",
                        padding: "0 6px",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center"
                      }}
                    >
                      <input
                        type="radio"
                        name="habit-icon"
                        value={icon}
                        checked={formIcon === icon}
                        onChange={() => setFormIcon(icon)}
                        style={{ display: "none" }}
                      />
                      <span
                        style={{
                          fontSize: 25,
                          borderRadius: "9px",
                          padding: 5,
                          background:
                            formIcon === icon ? "#ffb6e6" : "#f2f2fb",
                          border:
                            formIcon === icon
                              ? "2px solid #d72660"
                              : "1.5px solid #ccc"
                        }}
                      >
                        {icon}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
              <div style={{ width: "100%", marginBottom: 10 }}>
                <div
                  style={{
                    fontSize: 15,
                    marginBottom: 4,
                    color: "#555"
                  }}
                >
                  Select Color:
                </div>
                <HexColorPicker color={formColor} onChange={setFormColor} />
                <div
                  style={{
                    marginTop: 6,
                    fontSize: 13,
                    color: "#888",
                    textAlign: "center"
                  }}
                >
                  {formColor}
                </div>
              </div>
              <div style={{ display: "flex", gap: "18px", marginTop: 18 }}>
                <button
                  type="submit"
                  style={{
                    fontSize: 17,
                    fontWeight: 700,
                    background: "#d72660",
                    color: "#fff",
                    border: "none",
                    borderRadius: 12,
                    padding: "9px 32px",
                    cursor: "pointer"
                  }}
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  style={{
                    fontSize: 17,
                    fontWeight: 700,
                    background: "#f2f2fb",
                    color: "#d72660",
                    border: "none",
                    borderRadius: 12,
                    padding: "9px 32px",
                    cursor: "pointer"
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <FooterControls
        onAddHabit={() => setShowModal(true)}
        onViewAnalytics={() => setShowAnalytics(true)}
      />
    </div>
  );
}
