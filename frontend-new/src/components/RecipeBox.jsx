import React, { useState } from "react";
import WoodenBoxOpenAnimation from './WoodenBoxOpenAnimation';

// Modal component
function Modal({ open, onClose, children }) {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed", top: 0, left: 0, width: "100vw", height: "100vh",
      background: "#0003", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 9999
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

function decimalToFraction(num) {
  if (Number.isInteger(num)) return num;
  const fractionMap = { 0.25: '¼', 0.5: '½', 0.75: '¾', 0.33: '⅓', 0.67: '⅔', 0.2: '⅕', 0.4: '⅖', 0.6: '⅗', 0.8: '⅘' };
  const int = Math.floor(num);
  const dec = Math.round((num - int) * 100) / 100;
  const frac = fractionMap[dec] || dec.toFixed(2);
  return int ? `${int}${frac}` : frac;
}

const CATEGORY_OPTIONS = [
  "Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"
];

const DEFAULT_STICKERS = [
  { id: "heart", label: "Healthy", icon: "❤️", meaning: "Low sodium, diabetic friendly, low calorie" },
  { id: "star", label: "Popular", icon: "⭐", meaning: "Fan favorite" },
  { id: "bolt", label: "High Protein", icon: "⚡", meaning: "High protein" }
];

export default function RecipeBox({ onBackToDashboard }) {
  const [animationFinished, setAnimationFinished] = useState(false);
  const [recipes, setRecipes] = useState([]);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [showAddRecipe, setShowAddRecipe] = useState(false);
  const [showAddRecipeUrl, setShowAddRecipeUrl] = useState(false);

  const [newRecipe, setNewRecipe] = useState({
    title: "",
    category: "Other",
    ingredients: [],
    steps: [""],
    sourceUrl: "",
    stickers: []
  });

  function handleAddIngredient() {
    setNewRecipe(r => ({
      ...r,
      ingredients: [...r.ingredients, { name: "", amount: "", unit: "" }]
    }));
  }

  function handleChangeIngredient(index, field, value) {
    setNewRecipe(r => ({
      ...r,
      ingredients: r.ingredients.map((ing, i) =>
        i === index ? { ...ing, [field]: value } : ing
      )
    }));
  }

  function handleAddStep() {
    setNewRecipe(r => ({
      ...r,
      steps: [...r.steps, ""]
    }));
  }

  function handleChangeStep(index, value) {
    setNewRecipe(r => ({
      ...r,
      steps: r.steps.map((s, i) => i === index ? value : s)
    }));
  }

  function handleToggleSticker(id) {
    setNewRecipe(r => ({
      ...r,
      stickers: r.stickers.includes(id)
        ? r.stickers.filter(s => s !== id)
        : [...r.stickers, id]
    }));
  }

  function handleSaveRecipe(e) {
    e.preventDefault();
    if (!newRecipe.title.trim()) return;
    setRecipes(rs => [
      ...rs,
      {
        ...newRecipe,
        id: Date.now() + Math.random()
      }
    ]);
    setShowAddRecipe(false);
    setNewRecipe({
      title: "",
      category: "Other",
      ingredients: [],
      steps: [""],
      sourceUrl: "",
      stickers: []
    });
  }

  function handleAddRecipeFromUrl(url) {
    setNewRecipe({
      ...newRecipe,
      title: "Fetched Recipe Title",
      category: "Other",
      ingredients: [{ name: "Egg", amount: 2, unit: "" }],
      steps: ["Fetched step 1", "Fetched step 2"],
      sourceUrl: url,
      stickers: []
    });
    setShowAddRecipeUrl(false);
    setShowAddRecipe(true);
  }

  const filteredRecipes = recipes.filter(r =>
    r.title.toLowerCase().includes(search.toLowerCase()) &&
    (categoryFilter === "All" || r.category === categoryFilter)
  );

  return (
    <div
      style={{
        background: "#f0e5cd",
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        overflowY: "auto",
        zIndex: 1000
      }}
    >
      <div style={{ minHeight: "100vh", minWidth: "100vw", position: "relative", zIndex: 1 }}>
        {!animationFinished && (
          <div style={{ textAlign: "center" }}>
            <WoodenBoxOpenAnimation onEnded={() => setAnimationFinished(true)} />
          </div>
        )}
        {animationFinished && (
          <>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 30 }}>
              <button
                onClick={onBackToDashboard}
                style={{
                  background: "#d93b00", color: "#fff", border: "none",
                  borderRadius: 10, padding: "10px 26px", fontWeight: 700,
                  fontSize: 18, boxShadow: "0 2px 10px #d7266025", cursor: "pointer"
                }}
              >← Back to Dashboard</button>
              <div>
                <button
                  onClick={() => setShowAddRecipe(true)}
                  style={{
                    background: "#f9c993", color: "#6b2d09", border: "none",
                    borderRadius: 10, padding: "10px 26px", fontWeight: 700,
                    fontSize: 16, marginRight: 12, cursor: "pointer"
                  }}
                >+ Add Recipe</button>
                <button
                  onClick={() => setShowAddRecipeUrl(true)}
                  style={{
                    background: "#6b4f2a", color: "#fff", border: "none",
                    borderRadius: 10, padding: "10px 22px", fontWeight: 700,
                    fontSize: 15, cursor: "pointer"
                  }}
                >Add From URL</button>
              </div>
            </div>
            {/* Search & Filter Bar */}
            <div style={{ display: "flex", gap: 16, marginBottom: 26 }}>
              <input
                type="text"
                placeholder="Search recipes..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                style={{ fontSize: 17, padding: "8px 13px", borderRadius: 9, width: 260 }}
                autoFocus
              />
              <select value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}
                style={{ fontSize: 17, padding: "7px 12px", borderRadius: 8 }}>
                <option value="All">All</option>
                {CATEGORY_OPTIONS.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
            {/* Recipe Card Grid */}
            <div style={{ display: "flex", flexWrap: "wrap", gap: 20 }}>
              {filteredRecipes.length === 0 && (
                <div style={{ color: "#a77", fontWeight: 500, fontSize: 18 }}>
                  No recipes found.
                </div>
              )}
              {filteredRecipes.map(recipe => (
                <div key={recipe.id} style={{
                  background: "#fffbe5", borderRadius: 17, boxShadow: "0 2px 10px #dac38b33",
                  padding: "22px 28px", width: 320, marginBottom: 11, position: "relative"
                }}>
                  <div style={{ fontSize: 21, fontWeight: 700, color: "#904d16", marginBottom: 7 }}>
                    {recipe.title}
                  </div>
                  <div style={{ fontSize: 16, marginBottom: 7, color: "#734", fontWeight: 600 }}>
                    {recipe.category}
                  </div>
                  <div style={{ marginBottom: 7, color: "#626262" }}>
                    Ingredients:
                    <ul style={{ margin: 0, paddingLeft: 16 }}>
                      {recipe.ingredients.map((ing, i) =>
                        <li key={i}>
                          {ing.name}: {decimalToFraction(ing.amount)} {ing.unit}
                        </li>
                      )}
                    </ul>
                  </div>
                  <div style={{ marginBottom: 7, color: "#464", fontSize: 15 }}>
                    Steps:
                    <ol style={{ margin: 0, paddingLeft: 17 }}>
                      {recipe.steps.map((s, i) =>
                        <li key={i}>{s}</li>
                      )}
                    </ol>
                  </div>
                  {recipe.stickers.length > 0 && (
                    <div style={{ position: "absolute", top: 8, right: 8 }}>
                      {recipe.stickers.map(st =>
                        <span key={st} title={DEFAULT_STICKERS.find(d => d.id === st)?.meaning}
                          style={{ fontSize: 22, marginRight: 7 }}>
                          {DEFAULT_STICKERS.find(d => d.id === st)?.icon}
                        </span>
                      )}
                    </div>
                  )}
                  {recipe.sourceUrl && (
                    <div style={{ fontSize: 14, color: "#27b", marginTop: 7 }}>
                      Source: <a href={recipe.sourceUrl} target="_blank" rel="noopener noreferrer">{recipe.sourceUrl}</a>
                    </div>
                  )}
                </div>
              ))}
            </div>
            {/* Add Recipe Modal */}
            {showAddRecipe && (
              <Modal open={showAddRecipe} onClose={() => setShowAddRecipe(false)}>
                <form onSubmit={handleSaveRecipe}>
                  <div style={{ fontWeight: 700, fontSize: 20, color: "#6b2d09", marginBottom: 15 }}>
                    Add Recipe
                  </div>
                  <input type="text" placeholder="Title"
                    value={newRecipe.title}
                    onChange={e => setNewRecipe(r => ({ ...r, title: e.target.value }))}
                    style={{ fontSize: 16, padding: "7px 12px", borderRadius: 9, marginBottom: 12, width: "99%" }}
                    required autoFocus />
                  <select value={newRecipe.category}
                    onChange={e => setNewRecipe(r => ({ ...r, category: e.target.value }))}
                    style={{ fontSize: 16, padding: "7px 12px", borderRadius: 9, marginBottom: 12, width: "99%" }}>
                    {CATEGORY_OPTIONS.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 6 }}>Ingredients</div>
                    {newRecipe.ingredients.map((ing, i) =>
                      <div key={i} style={{ display: "flex", gap: 6, marginBottom: 5 }}>
                        <input type="text" placeholder="Name"
                          value={ing.name} onChange={e => handleChangeIngredient(i, "name", e.target.value)}
                          style={{ fontSize: 15, borderRadius: 7, padding: "5px 10px", width: 110 }} required />
                        <input type="number" min={0} step={0.01} placeholder="Amount"
                          value={ing.amount} onChange={e => handleChangeIngredient(i, "amount", e.target.value)}
                          style={{ fontSize: 15, borderRadius: 7, padding: "5px 10px", width: 58 }} required />
                        <input type="text" placeholder="Unit"
                          value={ing.unit} onChange={e => handleChangeIngredient(i, "unit", e.target.value)}
                          style={{ fontSize: 15, borderRadius: 7, padding: "5px 10px", width: 62 }} />
                      </div>
                    )}
                    <button type="button" onClick={handleAddIngredient}
                      style={{
                        background: "#ffb6e6", color: "#fff", border: "none", borderRadius: 9,
                        padding: "7px 19px", cursor: "pointer", fontWeight: 700
                      }}>Add Ingredient</button>
                  </div>
                  <div style={{ marginBottom: 14 }}>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 6 }}>Steps</div>
                    {newRecipe.steps.map((s, i) => (
                      <div key={i} style={{ marginBottom: 5 }}>
                        <input type="text" value={s} placeholder={`Step ${i + 1}`}
                          onChange={e => handleChangeStep(i, e.target.value)}
                          style={{ fontSize: 15, borderRadius: 7, padding: "5px 10px", width: "97%" }} required />
                      </div>
                    ))}
                    <button type="button" onClick={handleAddStep}
                      style={{
                        background: "#4b3315", color: "#fff", border: "none", borderRadius: 9,
                        padding: "7px 19px", cursor: "pointer", fontWeight: 700
                      }}>Add Step</button>
                  </div>
                  <div style={{ marginBottom: 13 }}>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 6 }}>Attach Custom Stickers</div>
                    {DEFAULT_STICKERS.map(st => (
                      <label key={st.id} style={{ marginRight: 12, fontSize: 16, cursor: "pointer" }}>
                        <input type="checkbox"
                          checked={newRecipe.stickers.includes(st.id)}
                          onChange={() => handleToggleSticker(st.id)}
                          style={{ marginRight: 5 }}
                        /> {st.icon} {st.label}
                      </label>
                    ))}
                  </div>
                  <button type="submit" style={{
                    marginTop: 8, fontSize: 17, background: "#f6c87b", color: "#7b5200",
                    border: "none", borderRadius: 11, padding: "9px 32px", fontWeight: 700,
                    cursor: "pointer"
                  }}>Save Recipe</button>
                </form>
              </Modal>
            )}
            {/* Add Recipe By URL Modal */}
            {showAddRecipeUrl && (
              <Modal open={showAddRecipeUrl} onClose={() => setShowAddRecipeUrl(false)}>
                <form onSubmit={e => {
                  e.preventDefault();
                  if (!newRecipe.sourceUrl) return;
                  handleAddRecipeFromUrl(newRecipe.sourceUrl);
                }}>
                  <div style={{ fontWeight: 700, fontSize: 20, color: "#6b2d09", marginBottom: 12 }}>
                    Add Recipe From URL
                  </div>
                  <input
                    type="text"
                    placeholder="Recipe Page URL"
                    value={newRecipe.sourceUrl}
                    onChange={e => setNewRecipe(r => ({ ...r, sourceUrl: e.target.value }))}
                    style={{ fontSize: 15, borderRadius: 7, padding: "7px 11px", marginBottom: 17, width: "99%" }}
                    required autoFocus
                  />
                  <button type="submit" style={{
                    fontSize: 16, background: "#4b3315", color: "#fff", border: "none",
                    borderRadius: 11, padding: "9px 32px", fontWeight: 700, cursor: "pointer"
                  }}>
                    Fetch Recipe
                  </button>
                </form>
              </Modal>
            )}
          </>
        )}
      </div>
    </div>
  );
}
