import React, { useState, useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

// ---------- MODAL ----------
function Modal({ open, onClose, children }) {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed", top: 0, left: 0, width: "100vw", height: "100vh",
      background: "#0003", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 999
    }}>
      <div style={{
        background: "#fff", borderRadius: 14, padding: 36, minWidth: 320,
        boxShadow: "0 6px 32px #0002", position: "relative"
      }}>
        <button onClick={onClose} style={{
          position: "absolute", top: 12, right: 16, fontSize: 21, color: "#d72660",
          background: "none", border: "none", cursor: "pointer", fontWeight: 800
        }}>&times;</button>
        {children}
      </div>
    </div>
  );
}

// ---------- PERSISTENT STATE ----------
function usePersistentState(key, defaultValue) {
  const [val, setVal] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : defaultValue;
  });
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(val));
  }, [key, val]);
  return [val, setVal];
}

// ---------- PIGGY BANK CARD ----------
function PiggyBankCard({ goal, onAdd, onWithdraw }) {
  const percent = goal.goal > 0
    ? Math.min(100, (goal.current / goal.goal) * 100)
    : 0;
  const roundedPercent = percent.toFixed(2);
  return (
    <div style={{
      background: "#fffdf6",
      borderRadius: 18,
      boxShadow: "0 2px 14px #ffd70033",
      padding: 28,
      width: 265,
      margin: 18,
      display: "inline-block"
    }}>
      <div style={{ display: "flex", alignItems: "center", marginBottom: 7 }}>
        <span role="img" aria-label="Piggy" style={{ fontSize: 44, marginRight: 7 }}>🐖</span>
        <div style={{ color: goal.color, fontWeight: 700, fontSize: 21, marginLeft: 5 }}>
          {goal.name}
        </div>
      </div>
      <div style={{ fontSize: 16, color: "#444" }}>
        ${goal.current} / ${goal.goal}
      </div>
      <div style={{
        width: "100%", height: 14, background: "#fffbe2",
        borderRadius: 9, margin: "12px 0", position: "relative"
      }}>
        <div style={{
          width: `${percent}%`, height: 14, background: goal.color,
          borderRadius: 9, transition: "width .5s"
        }} />
      </div>
      <div style={{ fontSize: 14, color: "#b350e0", marginBottom: 10 }}>
        {percent >= 100
          ? "Goal Reached!"
          : `${roundedPercent}% done`}
      </div>
      <div style={{ display: "flex", gap: 10 }}>
        <button onClick={() => onAdd(goal)} style={{
          background: "#d72660", color: "#fff", border: "none", borderRadius: 9,
          padding: "7px 16px", fontWeight: 700, cursor: "pointer"
        }}>
          Add
        </button>
        <button onClick={() => onWithdraw(goal)} style={{
          background: "#ffd700", color: "#b350e0", border: "none", borderRadius: 9,
          padding: "7px 16px", fontWeight: 700, cursor: "pointer"
        }}>
          Withdraw
        </button>
      </div>
    </div>
  );
}

// ---------- BILLS LIST ----------
function BillsList({ bills, onAddBill, onDeleteBill }) {
  return (
    <div style={{
      background: "#fff",
      borderRadius: 14,
      boxShadow: "0 1px 8px #ade0ff55",
      padding: 24,
      width: 340,
      minHeight: 125
    }}>
      <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 10, color: "#0378ed" }}>Upcoming Bills</div>
      {bills.length === 0 ? (
        <div style={{ color: "#34B233", fontWeight: 600, fontSize: 17, marginBottom: 8 }}>
          No upcoming bills! Yay!
        </div>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {bills.map(b => (
            <li key={b.id} style={{ marginBottom: 8, display: "flex", alignItems: "center" }}>
              <span>
                {b.name}: ${b.amount} due {b.due}
              </span>
              <button
                onClick={() => onDeleteBill(b.id)}
                style={{
                  marginLeft: 12,
                  background: "#ffd700",
                  color: "#d72660",
                  border: "none",
                  fontWeight: "700",
                  borderRadius: 8,
                  padding: "3px 10px",
                  fontSize: 15,
                  cursor: "pointer"
                }}
                title="Delete bill"
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
      <button onClick={onAddBill} style={{
        marginTop: 16, background: "#b350e0", color: "#fff", border: "none",
        borderRadius: 10, padding: "9px 26px", fontWeight: 700, cursor: "pointer"
      }}>Add Bill</button>
    </div>
  );
}

// ---------- CATEGORY LEGEND ----------
function CategoryLegend({ category, onEdit, onRemove, onAddSpending }) {
  const spendingArray = Array.isArray(category.spending) ? category.spending : [];
  const spent = spendingArray.reduce((a, s) => a + s.amount, 0);
  const overLimit = spent >= category.limit;
  return (
    <span style={{ marginRight: 28, display: "inline-flex", alignItems: "center" }}>
      <span style={{
        verticalAlign: "middle", display: "inline-block", width: 15, height: 15,
        background: overLimit ? "#d72660" : category.color, marginRight: 7, borderRadius: 7
      }} />
      <span style={{
        fontWeight: 700,
        color: overLimit ? "#d72660" : category.color,
        fontSize: 16, marginRight: 3
      }}>
        {category.name}
      </span>
      <span style={{ color: overLimit ? "#d72660" : "#777", fontSize: 15 }}>
        ${spent} spent / ${category.limit}
        {overLimit && <span> &nbsp; (limit!)</span>}
      </span>
      <button
        onClick={() => onAddSpending(category)}
        style={{
          background: "#5ddcbe",
          color: "#fff",
          border: "none",
          fontSize: 15,
          cursor: "pointer",
          fontWeight: "700",
          borderRadius: 6,
          marginLeft: 12,
          marginRight: 2,
          padding: "2px 8px"
        }}
        title="Add Spending"
      >+$</button>
      <button
        onClick={() => onEdit(category)}
        style={{
          background: "transparent",
          color: "#d72660",
          border: "none",
          fontSize: 17,
          cursor: "pointer",
          fontWeight: "700",
          marginLeft: 2,
          marginRight: 2
        }}
        title="Edit"
      >✎</button>
      <button
        onClick={() => onRemove(category)}
        style={{
          background: "transparent",
          color: "#d72660",
          border: "none",
          fontSize: 19,
          cursor: "pointer",
          fontWeight: 700
        }}
        title="Delete category"
      >🗑</button>
    </span>
  );
}

// ---------- CUSTOM TOOLTIP ----------
const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const { name, value } = payload[0].payload;
    return (
      <div style={{
        background: "#fff",
        border: "1.5px solid #ddd",
        padding: 8,
        borderRadius: 8,
        fontSize: 16,
        color: "#222"
      }}>
        <span style={{ fontWeight: 600 }}>{name}:</span> ${value}
      </div>
    );
  }
  return null;
};

// ---------- SPENDING PIE CHART ----------
function SpendingPieChart({
  income, categories,
  onSetIncome, onAddCategory, onEditCategory, onRemoveCategory,
  onAddSpending, onRemoveSpending
}) {
  const COLORS = ["#ffd700", "#d72660", "#b350e0", "#5ddcbe", "#6b21a8", "#abc6ea", "#f7931e"];
  const safeCategories = Array.isArray(categories) ? categories : [];

  const data = safeCategories.map((cat, i) => {
    const spendingArray = Array.isArray(cat.spending) ? cat.spending : [];
    const spent = spendingArray.reduce((a, s) => a + s.amount, 0);
    return {
      ...cat,
      spent,
      color: COLORS[i % COLORS.length]
    };
  });

  const sumSpent = data.reduce((acc, c) => acc + c.spent, 0);
  const unused = Math.max(0, (income || 0) - sumSpent);

  const pieSlices = [
    ...data
      .filter(d => d.spent > 0)
      .map(d => ({
        name: d.name,
        value: d.spent,
        color: d.color
      })),
    {
      name: "Unused",
      value: unused,
      color: "#e3e3e3"
    }
  ];

  const percentFn = amt => income > 0 ? (amt / income * 100).toFixed(2) : "0.00";

  return (
    <div style={{
      background: "#fff",
      borderRadius: 14,
      padding: 26,
      boxShadow: "0 1px 8px #ffd70033",
      width: 485,
      minHeight: 485,
      display: "flex",
      flexDirection: "column",
      alignItems: "center"
    }}>
      <div style={{ fontWeight: 700, fontSize: 22, color: "#f7931e", marginBottom: 4 }}>Spending Breakdown</div>
      <div style={{ fontSize: 16, marginBottom: 8, fontWeight: 700 }}>
        Monthly income:&nbsp;
        <span style={{
          color: "#37b246",
          borderBottom: "1.5px dashed #b350e0",
          cursor: "pointer"
        }}
          title="Click to edit"
          onClick={onSetIncome}
        >${income}</span>
      </div>
      <ResponsiveContainer width={460} height={260}>
        <PieChart>
          <Pie
            data={pieSlices}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={110}
            labelLine={false}
            label={({ name, value }) =>
              value > 0 && (name !== "Unused" || pieSlices.length === 1)
                ? `${name}: $${value}`
                : null
            }
          >
            {pieSlices.map((entry, index) => (
              <Cell key={entry.name} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ fontSize: 15, marginTop: 8, marginBottom: 4, color: "#888" }}>
        Total Spent: ${sumSpent} / ${income} ({percentFn(sumSpent)}% used)
      </div>
      <button
        onClick={onAddCategory}
        style={{
          marginTop: 12,
          background: "#ffb6e6",
          color: "#d72660",
          border: "none",
          borderRadius: 10,
          fontWeight: 700,
          padding: "8px 22px",
          fontSize: 16,
          cursor: "pointer"
        }}
      >Add Category</button>
      <div style={{
        display: "flex",
        flexWrap: "wrap",
        gap: 8,
        margin: "7px 0 0 0",
        justifyContent: "center"
      }}>
        {data.map(cat =>
          <CategoryLegend
            key={cat.name}
            category={cat}
            onEdit={onEditCategory}
            onRemove={onRemoveCategory}
            onAddSpending={onAddSpending}
          />
        )}
      </div>
      {/* Only show spending logs for categories with spending */}
      {data
        .filter(cat => Array.isArray(cat.spending) && cat.spending.length > 0)
        .map(cat =>
          <div key={cat.name} style={{
            background: "#f7f8fc",
            marginTop: 12,
            padding: "8px 18px 12px 18px",
            borderRadius: 10,
            minWidth: 340,
            maxWidth: 380,
            marginBottom: 7,
            border: cat.spent >= cat.limit ? "2px solid #d72660" : "1.5px solid #dedede"
          }}>
            <div style={{ fontWeight: 700, color: "#344" }}>
              {cat.name} Spending Log
            </div>
            <ul style={{ margin: 0, padding: 0, fontSize: 15 }}>
              {cat.spending.map((s, i) =>
                <li key={i} style={{
                  marginBottom: 2, display: "flex", alignItems: "baseline"
                }}>
                  <span style={{ marginRight: 9 }}>{s.description}</span>
                  <span style={{ color: "#d72660", fontWeight: 700, minWidth: 40 }}>${s.amount}</span>
                  <button onClick={() => onRemoveSpending(cat.name, i)}
                    style={{
                      background: "none", color: "#d72660", border: "none",
                      fontSize: 14, cursor: "pointer", marginLeft: 9
                    }}
                    title="Remove"
                  >🗑</button>
                </li>
              )}
            </ul>
          </div>
        )
      }
    </div>
  );
}

// ---------- MAIN COMPONENT ----------
export default function Budgets({ setActiveSection, onAddTaskFromBill }) {
  // State
  const [savingsGoals, setSavingsGoals] = usePersistentState('arcadia-savingsGoals', []);
  const [bills, setBills] = usePersistentState('arcadia-bills', []);
  const [categories, setCategories] = usePersistentState('arcadia-categories', []);
  const [monthlyIncome, setMonthlyIncome] = usePersistentState('arcadia-monthlyIncome', 0);

  const [openGoal, setOpenGoal] = useState(false);
  const [goalInput, setGoalInput] = useState({ name: "", goal: "" });
  const [openTransfer, setOpenTransfer] = useState(false);
  const [transferMode, setTransferMode] = useState("add");
  const [transferGoal, setTransferGoal] = useState(null);
  const [transferAmount, setTransferAmount] = useState("");
  const [openBill, setOpenBill] = useState(false);
  const [billInput, setBillInput] = useState({ name: "", amount: "", due: "" });
  const [openCategory, setOpenCategory] = useState(false);
  const [categoryInput, setCategoryInput] = useState({ name: "", limit: "" });
  const [openEditCat, setOpenEditCat] = useState(false);
  const [editCat, setEditCat] = useState({ name: "", limit: "" });
  const [openAddSpend, setOpenAddSpend] = useState(false);
  const [addSpendCat, setAddSpendCat] = useState({ name: "", description: "", amount: "" });
  const [openIncome, setOpenIncome] = useState(monthlyIncome === 0);
  const [incomeInput, setIncomeInput] = useState(monthlyIncome);

  // -------- HANDLERS ----------
  function handleFinalAddBill(e) {
    e.preventDefault();
    if (!billInput.name || !billInput.amount || !billInput.due || !(+billInput.amount > 0)) return;
    const bill = { id: Date.now(), name: billInput.name, amount: +billInput.amount, due: billInput.due, category: "Other" };
    setBills(bills => [...bills, bill]);
    setBillInput({ name: "", amount: "", due: "" });
    setOpenBill(false);
    if (typeof onAddTaskFromBill === "function") {
      onAddTaskFromBill({ title: `Pay: ${bill.name}`, due: bill.due, status: "Due", notes: `Bill for $${bill.amount}` });
    }
  }
  function handleFinalAddCategory(e) {
    e.preventDefault();
    if (!categoryInput.name || !(parseFloat(categoryInput.limit) > 0)) return;
    setCategories(cats => [...cats, {
      name: categoryInput.name,
      limit: parseFloat(categoryInput.limit),
      spending: []
    }]);
    setCategoryInput({ name: "", limit: "" });
    setOpenCategory(false);
  }
  function handleEditCategory(cat) {
    setEditCat({ name: cat.name, limit: cat.limit });
    setOpenEditCat(true);
  }
  function handleFinalEditCat(e) {
    e.preventDefault();
    if (!editCat.name || !(parseFloat(editCat.limit) > 0)) return;
    setCategories(cats =>
      cats.map(cat =>
        cat.name === editCat.name
          ? { ...cat, limit: parseFloat(editCat.limit), spending: Array.isArray(cat.spending) ? cat.spending : [] }
          : cat
      )
    );
    setOpenEditCat(false);
  }
  function handleRemoveCategory(cat) {
    setCategories(cats => cats.filter(c => c.name !== cat.name));
  }
  function handleAddSpending(cat) {
    setAddSpendCat({ name: cat.name, description: "", amount: "" });
    setOpenAddSpend(true);
  }
  function handleFinalAddSpend(e) {
    e.preventDefault();
    if (!addSpendCat.description || isNaN(parseFloat(addSpendCat.amount)) || !(parseFloat(addSpendCat.amount) > 0)) return;
    setCategories(cats =>
      cats.map(cat =>
        cat.name === addSpendCat.name
          ? { ...cat, spending: Array.isArray(cat.spending)
                ? [...cat.spending, { description: addSpendCat.description, amount: parseFloat(addSpendCat.amount) }]
                : [{ description: addSpendCat.description, amount: parseFloat(addSpendCat.amount) }]
            }
          : cat
      )
    );
    setOpenAddSpend(false);
  }
  function handleRemoveSpending(catName, idx) {
    setCategories(cats =>
      cats.map(cat =>
        cat.name === catName
          ? { ...cat, spending: Array.isArray(cat.spending) ? cat.spending.filter((_, i) => i !== idx) : [] }
          : cat
      )
    );
  }
  function handleFinalAddGoal(e) {
    e.preventDefault();
    if (!goalInput.name || !goalInput.goal || !(+goalInput.goal > 0)) return;
    const colorSet = ["#b350e0", "#ffd700", "#5ddcbe", "#f7931e", "#6b21a8", "#e871ef"];
    const nextColor = colorSet[savingsGoals.length % colorSet.length];
    const id = Date.now();
    setSavingsGoals(goals => [...goals, { id, name: goalInput.name, goal: +goalInput.goal, current: 0, color: nextColor }]);
    setGoalInput({ name: "", goal: "" });
    setOpenGoal(false);
  }
  function handleTransferSubmit(e) {
    e.preventDefault();
    if (!transferGoal || !(parseFloat(transferAmount) > 0)) return;
    setSavingsGoals(goals =>
      goals
        .map(g => {
          if (g.id !== transferGoal.id) return g;
          let updatedCurrent;
          if (transferMode === "add") {
            updatedCurrent = Math.min(g.current + parseFloat(transferAmount), g.goal);
          } else {
            updatedCurrent = Math.max(g.current - parseFloat(transferAmount), 0);
          }
          return { ...g, current: updatedCurrent };
        })
        .filter(g => g.current < g.goal)
    );
    setOpenTransfer(false);
  }
  function handleDeleteBill(billId) {
    setBills(bills => bills.filter(b => b.id !== billId));
  }
  function handleFinalSetIncome(e) {
    e.preventDefault();
    const val = Number(incomeInput);
    if (!(val > 0)) return;
    setMonthlyIncome(val);
    setOpenIncome(false);
  }

  // ---------- RENDER ----------
  return (
    <div style={{ background: "#fff8f6", minHeight: "100vh", paddingBottom: 110 }}>
      <div style={{
        width: "100%",
        display: "flex",
        justifyContent: "flex-end",
        alignItems: "center",
        position: "relative"
      }}>
        <button
          onClick={() => setActiveSection && setActiveSection("dashboard")}
          style={{
            margin: "36px 44px 18px 0",
            padding: "9px 30px",
            fontSize: "18px",
            fontWeight: 700,
            background: "#d72660",
            color: "#fff",
            border: "none",
            borderRadius: "12px",
            cursor: "pointer",
            boxShadow: "0 2px 12px #d7266040"
          }}>
          ← Back to Dashboard
        </button>
      </div>
      <div style={{
        display: "flex",
        flexWrap: "wrap",
        gap: 36,
        justifyContent: "center",
        marginTop: 2,
        marginBottom: 32
      }}>
        {savingsGoals
          .filter(goal => goal.current < goal.goal)
          .map(goal =>
            <PiggyBankCard
              key={goal.id}
              goal={goal}
              onAdd={g => setOpenTransfer(true) || setTransferGoal(g) || setTransferMode("add")}
              onWithdraw={g => setOpenTransfer(true) || setTransferGoal(g) || setTransferMode("withdraw")}
            />
        )}
        <button
          onClick={() => setOpenGoal(true)}
          style={{
            background: "#fff",
            borderRadius: 16,
            boxShadow: "0 2px 10px #abc6ea25",
            fontWeight: 700,
            color: "#b350e0",
            fontSize: 21,
            height: 180,
            width: 125,
            border: "3px dashed #b350e0",
            cursor: "pointer",
            margin: 18
          }}
        >+ Add<br />Goal</button>
      </div>
      <div style={{
        display: "flex",
        gap: 42,
        justifyContent: "center",
        marginBottom: 70,
        flexWrap: "wrap"
      }}>
        <BillsList bills={bills} onAddBill={() => setOpenBill(true)} onDeleteBill={handleDeleteBill} />
        <SpendingPieChart
          income={monthlyIncome}
          categories={categories}
          onSetIncome={() => setOpenIncome(true)}
          onAddCategory={() => setOpenCategory(true)}
          onEditCategory={handleEditCategory}
          onRemoveCategory={handleRemoveCategory}
          onAddSpending={handleAddSpending}
          onRemoveSpending={handleRemoveSpending}
        />
      </div>
      {/* Modals */}
      <Modal open={openGoal} onClose={() => setOpenGoal(false)}>
        <form onSubmit={handleFinalAddGoal}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#b350e0" }}>
            Add Savings Goal
          </div>
          <input type="text" placeholder="Goal Name"
            value={goalInput.name}
            onChange={e => setGoalInput(g => ({ ...g, name: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 12, width: "99%" }}
            required autoFocus />
          <input type="number" min={1} placeholder="Goal Amount"
            value={goalInput.goal}
            onChange={e => setGoalInput(g => ({ ...g, goal: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 20, width: "99%" }}
            required />
          <button type="submit" style={{
            fontSize: 17, background: "#ffd700", color: "#b350e0", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Add Goal</button>
        </form>
      </Modal>
      <Modal open={openTransfer} onClose={() => setOpenTransfer(false)}>
        <form onSubmit={handleTransferSubmit}>
          <div style={{
            fontWeight: 700, fontSize: 22, marginBottom: 18,
            color: transferMode === "add" ? "#37b246" : "#d72660"
          }}>
            {transferMode === "add" ? "Add Money" : "Withdraw Money"}
          </div>
          <div style={{
            fontWeight: 600, marginBottom: 12, fontSize: 17,
            color: transferGoal ? transferGoal.color : "#444"
          }}>
            {transferGoal ? transferGoal.name : ""}
          </div>
          <input
            type="number"
            min={1}
            placeholder="Amount"
            value={transferAmount}
            onChange={e => setTransferAmount(e.target.value)}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 16, width: "99%" }}
            required autoFocus
          />
          <button type="submit" style={{
            fontSize: 17,
            background: transferMode === "add" ? "#37b246" : "#d72660",
            color: "#fff", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>
            {transferMode === "add" ? "Add" : "Withdraw"}
          </button>
        </form>
      </Modal>
      <Modal open={openBill} onClose={() => setOpenBill(false)}>
        <form onSubmit={handleFinalAddBill}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#0378ed" }}>
            Add Bill
          </div>
          <input type="text" placeholder="Bill Name"
            value={billInput.name}
            onChange={e => setBillInput(b => ({ ...b, name: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 11, width: "99%" }}
            required autoFocus />
          <input type="number" min={1} placeholder="Amount"
            value={billInput.amount}
            onChange={e => setBillInput(b => ({ ...b, amount: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 11, width: "99%" }}
            required />
          <input type="date" placeholder="Due Date"
            value={billInput.due}
            onChange={e => setBillInput(b => ({ ...b, due: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 16, width: "99%" }}
            required />
          <button type="submit" style={{
            fontSize: 17, background: "#0378ed", color: "#fff", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Add Bill</button>
        </form>
      </Modal>
      {/* Add/Edit Category */}
      <Modal open={openCategory} onClose={() => setOpenCategory(false)}>
        <form onSubmit={handleFinalAddCategory}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#f7931e" }}>
            Add Spending Category
          </div>
          <input type="text" placeholder="Category Name"
            value={categoryInput.name}
            onChange={e => setCategoryInput(c => ({ ...c, name: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 15, width: "99%" }}
            required autoFocus />
          <input type="number" min={1} placeholder="Limit (Budget for Category)"
            value={categoryInput.limit}
            onChange={e => setCategoryInput(c => ({ ...c, limit: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 16, width: "99%" }}
            required />
          <button type="submit" style={{
            fontSize: 17, background: "#ffd700", color: "#b350e0", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Add Category</button>
        </form>
      </Modal>
      <Modal open={openEditCat} onClose={() => setOpenEditCat(false)}>
        <form onSubmit={handleFinalEditCat}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#d72660" }}>
            Edit Category
          </div>
          <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 9 }}>{editCat.name}</div>
          <input type="number" min={1} placeholder="Limit"
            value={editCat.limit}
            onChange={e => setEditCat(cat => ({ ...cat, limit: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 13px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 13, width: "99%" }}
            required />
          <button type="submit" style={{
            fontSize: 17, background: "#d72660", color: "#fff", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Save</button>
        </form>
      </Modal>
      {/* Add Spending */}
      <Modal open={openAddSpend} onClose={() => setOpenAddSpend(false)}>
        <form onSubmit={handleFinalAddSpend}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#5ddcbe" }}>
            Add Spending to {addSpendCat.name}
          </div>
          <input type="text" placeholder="Description"
            value={addSpendCat.description}
            onChange={e => setAddSpendCat(c => ({ ...c, description: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 13, width: "99%" }}
            required autoFocus />
          <input type="number" min={1} placeholder="Amount"
            value={addSpendCat.amount}
            onChange={e => setAddSpendCat(c => ({ ...c, amount: e.target.value }))}
            style={{ fontSize: 17, padding: "7px 13px", borderRadius: 8, border: "1.5px solid #d3bcff", marginBottom: 12, width: "99%" }}
            required />
          <button type="submit" style={{
            fontSize: 17, background: "#5ddcbe", color: "#fff", border: "none",
            borderRadius: 11, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Add Spending</button>
        </form>
      </Modal>
      {/* Income */}
      <Modal open={openIncome} onClose={() => setOpenIncome(false)}>
        <form onSubmit={handleFinalSetIncome}>
          <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 18, color: "#37b246" }}>
            Set Monthly Income
          </div>
          <input
            type="number"
            min={1}
            placeholder="Monthly Income"
            value={incomeInput}
            onChange={e => setIncomeInput(e.target.value)}
            style={{ fontSize: 18, padding: "9px 12px", borderRadius: 9, marginBottom: 16, width: "99%" }}
            required autoFocus
          />
          <button type="submit" style={{
            fontSize: 17, background: "#37b246", color: "#fff", border: "none",
            borderRadius: 12, padding: "10px 32px", fontWeight: 700, cursor: "pointer"
          }}>Set Income</button>
        </form>
      </Modal>
    </div>
  );
}
