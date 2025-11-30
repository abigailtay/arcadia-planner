import React, { useState, useEffect } from "react";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import "react-big-calendar/lib/css/react-big-calendar.css";
import { SketchPicker } from "react-color";

// ---- Date and holiday helpers ----
function parseDueDateString(str) {
  const [year, month, day] = str.split("-");
  return new Date(year, month - 1, day, 12, 0);
}
function getMLKDay(year) {
  const d = new Date(year, 0, 1);
  let mondays = 0;
  while (mondays < 3) {
    if (d.getDay() === 1) mondays++;
    d.setDate(d.getDate() + 1);
  }
  return new Date(year, 0, d.getDate() - 1, 12, 0);
}
function getMemorialDay(year) {
  const d = new Date(year, 4, 31);
  while (d.getDay() !== 1) d.setDate(d.getDate() - 1);
  return new Date(year, 4, d.getDate(), 12, 0);
}
function getLaborDay(year) {
  const d = new Date(year, 8, 1);
  while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
  return new Date(year, 8, d.getDate(), 12, 0);
}
function getThanksgiving(year) {
  const d = new Date(year, 10, 1);
  let thursdays = 0;
  while (thursdays < 4) {
    if (d.getDay() === 4) thursdays++;
    d.setDate(d.getDate() + 1);
  }
  return new Date(year, 10, d.getDate() - 1, 12, 0);
}
function getUSHolidays(year) {
  return [
    { id: "newyear" + year, title: "New Year's Day", start: new Date(year, 0, 1, 12, 0), end: new Date(year, 0, 1, 12, 0), allDay: true, status: "Holiday", color: "#1976d2", category: "Holiday" },
    { id: "mlk" + year, title: "MLK Jr. Day", start: getMLKDay(year), end: getMLKDay(year), allDay: true, status: "Holiday", color: "#9e9e9e", category: "Holiday" },
    { id: "memorial" + year, title: "Memorial Day", start: getMemorialDay(year), end: getMemorialDay(year), allDay: true, status: "Holiday", color: "#d72660", category: "Holiday" },
    { id: "independence" + year, title: "Independence Day", start: new Date(year, 6, 4, 12, 0), end: new Date(year, 6, 4, 12, 0), allDay: true, status: "Holiday", color: "#ffd600", category: "Holiday" },
    { id: "labor" + year, title: "Labor Day", start: getLaborDay(year), end: getLaborDay(year), allDay: true, status: "Holiday", color: "#00897b", category: "Holiday" },
    { id: "veterans" + year, title: "Veterans Day", start: new Date(year, 10, 11, 12, 0), end: new Date(year, 10, 11, 12, 0), allDay: true, status: "Holiday", color: "#009688", category: "Holiday" },
    { id: "thanksgiving" + year, title: "Thanksgiving", start: getThanksgiving(year), end: getThanksgiving(year), allDay: true, status: "Holiday", color: "#ff9800", category: "Holiday" },
    { id: "christmas" + year, title: "Christmas", start: new Date(year, 11, 25, 12, 0), end: new Date(year, 11, 25, 12, 0), allDay: true, status: "Holiday", color: "#43a047", category: "Holiday" }
  ];
}

const CATEGORIES_STORAGE_KEY = "arcadia-categories";

const locales = {
  'en-US': require('date-fns/locale/en-US'),
};
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

function CalendarEvent({ event }) {
  return (
    <span title={event.title}>
      {event.title}
    </span>
  );
}

export default function Tasks({ tasks, setTasks, setActiveSection }) {
  // Always load localStorage categories if present
  const [categories, setCategories] = useState(() => {
    const saved = localStorage.getItem(CATEGORIES_STORAGE_KEY);
    return saved ? JSON.parse(saved) : [{ name: "General", color: "#3174ad" }];
  });
  const [category, setCategory] = useState("General");
  const [color, setColor] = useState("#3174ad");
  const [title, setTitle] = useState("");
  const [due, setDue] = useState(format(new Date(), "yyyy-MM-dd"));

  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryColor, setNewCategoryColor] = useState("#3174ad");
  const [showCategoryColorPicker, setShowCategoryColorPicker] = useState(false);

  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [rescheduleDate, setRescheduleDate] = useState("");
  const [calendarDate, setCalendarDate] = useState(new Date());

  // Persist categories on change
  useEffect(() => {
    localStorage.setItem(CATEGORIES_STORAGE_KEY, JSON.stringify(categories));
  }, [categories]);

  useEffect(() => {
    const cat = categories.find(c => c.name === category);
    if (cat) setColor(cat.color);
    else {
      setCategory("General");
      setColor(categories.find(c => c.name === "General")?.color || "#3174ad");
    }
  }, [category, categories]);

  // Holidays for visible year
  const holidayEvents = getUSHolidays(calendarDate.getFullYear());

  // Events for calendar + title prop for hover
  const events = [
    ...tasks.map(task => ({
      id: task.id,
      title: task.title,
      start: parseDueDateString(task.due),
      end: parseDueDateString(task.due),
      allDay: true,
      status: task.status,
      color: categories.find(c => c.name === task.category)?.color || "#3174ad",
      category: task.category
    })),
    ...holidayEvents
  ];

  function handleAddCategory() {
    if (!newCategoryName.trim() || categories.find(c => c.name === newCategoryName)) return;
    setCategories([...categories, { name: newCategoryName, color: newCategoryColor }]);
    setNewCategoryName("");
    setNewCategoryColor("#3174ad");
    setShowCategoryColorPicker(false);
  }

  function handleRemoveCategory(name) {
    if (name === "General") return; // protect General
    setCategories(prev =>
      prev.filter(c => c.name !== name)
    );
    // If currently selected category was removed, switch to General
    if (category === name) setCategory("General");
  }

  function handleAddTask() {
    if (!title.trim()) return;
    setTasks([
      ...tasks,
      {
        id: Date.now(),
        title,
        due,
        status: "Upcoming",
        color: categories.find(c => c.name === category)?.color || "#3174ad",
        category,
      },
    ]);
    setTitle("");
    setDue(format(new Date(), "yyyy-MM-dd"));
    setCategory(categories[0]?.name || "General");
  }

  function handleCompleteTask(id) {
    setTasks(tasks.filter(task => task.id !== id));
    setRescheduleDate("");
  }
  function handleRemoveTask(id) {
    setTasks(tasks.filter(task => task.id !== id));
    setRescheduleDate("");
  }
  function handleRescheduleTask(id) {
    if (!rescheduleDate) return;
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, due: rescheduleDate } : task
    ));
    setSelectedTaskId(null);
    setRescheduleDate("");
  }

  function eventPropGetter(event) {
    return {
      style: {
        backgroundColor: event.color || "#3174ad",
        borderRadius: "8px",
        opacity: 0.9,
        color: "#fff",
        border: event.status === "Holiday" ? "3px solid #fff" : "none"
      }
    };
  }

  const selectedTask = tasks.find(t => t.id === selectedTaskId);

  function CustomToolbar({ label, onNavigate }) {
    const [month, year] = label.split(" ");
    return (
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.6em", fontWeight: 700, marginBottom: 5
      }}>
        <button
          style={{ background: "#eee", border: "none", marginRight: 14, fontSize: "1.2em", borderRadius: 7, cursor: "pointer", padding: "7px 15px" }}
          onClick={() => onNavigate("PREV")}
        >‹</button>
        <span>
          <span style={{ fontWeight: 800 }}>{month}</span> <span style={{ fontWeight: 800 }}>{year}</span>
        </span>
        <button
          style={{ background: "#eee", border: "none", marginLeft: 14, fontSize: "1.2em", borderRadius: 7, cursor: "pointer", padding: "7px 15px" }}
          onClick={() => onNavigate("NEXT")}
        >›</button>
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100vw",
        background: "#ffe2ed",
        display: "flex",
        flexDirection: "column",
        alignItems: "center"
      }}
    >
      <h1 style={{
        color: "#6b21a8",
        fontSize: 42,
        fontWeight: 800,
        letterSpacing: "0.04em",
        marginBottom: 16 }}>
        Tasks Calendar
      </h1>
      <button
        style={{
          background: "linear-gradient(90deg,#d72660,#6b21a8)",
          color: "#fff", fontWeight: 700, fontSize: 18,
          border: "none", borderRadius: 12, padding: "10px 30px", marginBottom: "18px",
          boxShadow: "0 2px 8px #6b21a855", cursor: "pointer"
        }}
        onClick={() => setActiveSection("dashboard")}
      >
        Back to Dashboard
      </button>
      {/* New Category Form and List */}
      <div style={{
        background: "#fff",
        borderRadius: 12,
        padding: "14px 16px",
        boxShadow: "0 1.5px 8px #d7266033",
        marginBottom: "18px",
        display: "flex",
        alignItems: "center",
        gap: "14px",
        position: "relative"
      }}>
        <input
          type="text"
          value={newCategoryName}
          onChange={e => setNewCategoryName(e.target.value)}
          placeholder="New category name"
          style={{ padding: "6px 8px", borderRadius: 7, border: "1.5px solid #aaa", fontSize: 16, minWidth: "115px" }}
        />
        <button
          type="button"
          onClick={() => setShowCategoryColorPicker(!showCategoryColorPicker)}
          style={{
            background: newCategoryColor,
            border: "none", padding: "8px 12px",
            borderRadius: 8, color: "#fff", fontWeight: 700, cursor: "pointer"
          }}>
          Pick Category Color
        </button>
        {showCategoryColorPicker && (
          <div style={{ position: "absolute", zIndex: 99, left: "160px", top: "50px" }}>
            <SketchPicker color={newCategoryColor} onChange={c => setNewCategoryColor(c.hex)} />
          </div>
        )}
        <button
          type="button"
          onClick={handleAddCategory}
          style={{
            background: "linear-gradient(90deg,#6b21a8,#d72660)",
            color: "#fff",
            fontWeight: 700, fontSize: 16,
            border: "none", borderRadius: 10, padding: "8px 16px", cursor: "pointer"
          }}>
          Add Category
        </button>
        {/* Display existing categories (with remove if not General) */}
        <div style={{ marginLeft: 22, display: "flex", gap: 12 }}>
          {categories.map(cat => (
            <span key={cat.name} style={{ display: "flex", alignItems: "center" }}>
              <span style={{
                width: 18, height: 18, borderRadius: "50%",
                background: cat.color, display: "inline-block", marginRight: 6,
                border: "1.5px solid #ccc"
              }} />
              <span>{cat.name}</span>
              {cat.name !== "General" && (
                <button
                  onClick={() => handleRemoveCategory(cat.name)}
                  style={{
                    marginLeft: 6, padding: "0 8px", border: "none",
                    borderRadius: 6, background: "#d72660", color: "#fff",
                    fontSize: 13, fontWeight: 700, cursor: "pointer"
                  }}
                  title={`Remove category ${cat.name}`}
                >×</button>
              )}
            </span>
          ))}
        </div>
      </div>
      {/* Add Task Form */}
      <div style={{
        background: "#fff",
        borderRadius: 14,
        boxShadow: "0 2px 8px #d7266030",
        padding: 20,
        marginBottom: 22,
        display: "flex",
        alignItems: "center",
        gap: 18,
        position: "relative"
      }}>
        <input
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Task title..."
          style={{ padding: "8px 12px", borderRadius: 7, border: "1.5px solid #aaa", fontSize: 18, minWidth: "140px" }}
        />
        <input
          type="date"
          value={due}
          onChange={e => setDue(e.target.value)}
          style={{ fontSize: 17, padding: "6px 10px", borderRadius: 7, border: "1.5px solid #aaa" }}
        />
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          style={{ fontSize: 17, padding: "6px 10px", borderRadius: 7, border: "1.5px solid #aaa" }}
        >
          {categories.map(cat => (
            <option key={cat.name} value={cat.name}>{cat.name}</option>
          ))}
        </select>
        <div style={{
          width: "36px", height: "36px",
          borderRadius: "50%",
          background: color,
          border: "2px solid #eee", marginRight: "10px"
        }} />
        <button
          type="button"
          onClick={handleAddTask}
          style={{
            background: "linear-gradient(90deg,#6b21a8,#d72660)",
            color: "#fff", fontWeight: 700, fontSize: 18,
            border: "none", borderRadius: 12, padding: "10px 20px", cursor: "pointer"
          }}>
          Add Task
        </button>
      </div>
      {/* Calendar */}
      <div style={{ width: "900px", maxWidth: "95vw" }}>
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{
            height: 600, background: "#fff", borderRadius: "18px",
            boxShadow: "0 2px 18px #d7266030", padding: "10px"
          }}
          views={["month"]}
          eventPropGetter={eventPropGetter}
          onSelectEvent={event => {
            setSelectedTaskId(event.id);
            if (event.status !== "Holiday" && selectedTask) setRescheduleDate(selectedTask.due);
          }}
          toolbar={true}
          components={{
            event: CalendarEvent,
            toolbar: CustomToolbar,
          }}
          date={calendarDate}
          onNavigate={date => setCalendarDate(date)}
        />
      </div>
      {/* Task controls for selected task */}
      {selectedTaskId && selectedTask && selectedTask.status !== "Holiday" && (
        <div style={{
          marginTop: 24, background: "#fff", borderRadius: 10,
          boxShadow: "0 2px 8px #6b21a840", padding: 16, display: "flex", gap: 12, alignItems: "center"
        }}>
          <button
            style={{ background: "#43a047", color: "#fff", border: "none", borderRadius: 8, padding: "8px 16px", fontWeight: 700, cursor: "pointer" }}
            onClick={() => { handleCompleteTask(selectedTaskId); setSelectedTaskId(null); }}
          >Complete Task</button>
          <button
            style={{ background: "#d72660", color: "#fff", border: "none", borderRadius: 8, padding: "8px 16px", fontWeight: 700, cursor: "pointer" }}
            onClick={() => { handleRemoveTask(selectedTaskId); setSelectedTaskId(null); }}
          >Remove Task</button>
          <input
            type="date"
            value={rescheduleDate}
            onChange={e => setRescheduleDate(e.target.value)}
            style={{ fontSize: 17, padding: "6px 10px", borderRadius: 7, border: "1.5px solid #aaa" }}
          />
          <button
            style={{ background: "#6b21a8", color: "#fff", border: "none", borderRadius: 8, padding: "8px 16px", fontWeight: 700, cursor: "pointer" }}
            onClick={() => handleRescheduleTask(selectedTaskId)}
          >Reschedule</button>
          <button
            style={{ background: "#aaa", color: "#fff", border: "none", borderRadius: 8, padding: "8px 16px", fontWeight: 700, cursor: "pointer" }}
            onClick={() => { setSelectedTaskId(null); setRescheduleDate(""); }}
          >Cancel</button>
        </div>
      )}
      <div style={{ marginTop: "18px", fontSize: "16px", color: "#888", textAlign: "center" }}>
        US holidays auto-populate for any year.<br />
        Category choices are saved.<br />
        You can remove saved categories (except General).<br />
        Hover calendar tasks to see full task name.<br />
        Add tasks under any category.<br />
        Multiple events can exist per day.<br />
        Click a task in the calendar to complete, remove, or reschedule.
      </div>
    </div>
  );
}
