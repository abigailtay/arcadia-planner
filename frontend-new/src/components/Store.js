// src/components/Store.js
import React, { useState } from "react";
import { SHOP_ITEMS } from "../shopItems";
import "./Store.css"; // we'll create this next
import avatarBase from "../assets/Pink Cartoon Character Wave.png"; // already correct

function Store({ onBackToDashboard }) { // NEW: accept back prop
  const [glitter, setGlitter] = useState(150);
  const [ownedItems, setOwnedItems] = useState([]);
  const [equipped, setEquipped] = useState({
    hat: null,
    glasses: null,
    scarf: null,
  });
  const [popup, setPopup] = useState(null);

  const handlePurchase = async (item) => {
    const isOwned = ownedItems.includes(item.id);
    const canAfford = glitter >= item.cost;
    if (isOwned || !canAfford) return;

    try {
      // TODO: replace with real API call to /store/purchase
      // await fetch("/store/purchase", { ... });

      // fake success for now:
      setGlitter((prev) => prev - item.cost);
      setOwnedItems((prev) => [...prev, item.id]);
      setEquipped((prev) => ({ ...prev, [item.slot]: item.id }));
      setPopup(`You got: ${item.name}!`);

      setTimeout(() => setPopup(null), 2000);
    } catch (err) {
      console.error("Purchase failed", err);
      // show error toast here if you use a toast lib
    }
  };

  const getItemById = (id) => SHOP_ITEMS.find((it) => it.id === id);

  return (
    <div className="store-page">
      {/* Top bar */}
      <div className="store-topbar">
        <div className="store-left-top">
          <div className="store-glitter">Glitter: {glitter}</div>

          {/* Avatar directly under glitter */}
          <div className={`avatar-container ${popup ? "avatar-bounce" : ""}`}>
            {/* USE real avatar image instead of placeholder */}
            <img src={avatarBase} alt="Avatar" className="avatar-base" />

            {/* Hat */}
            {equipped.hat && (
              <img
                src={getItemById(equipped.hat).image}
                alt="Hat"
                className="avatar-hat"
              />
            )}

            {/* Glasses */}
            {equipped.glasses && (
              <img
                src={getItemById(equipped.glasses).image}
                alt="Glasses"
                className="avatar-glasses"
              />
            )}

            {/* Scarf */}
            {equipped.scarf && (
              <img
                src={getItemById(equipped.scarf).image}
                alt="Scarf"
                className="avatar-scarf"
              />
            )}

            {popup && <div className="avatar-popup">{popup}</div>}
          </div>

          {/* Owned items under avatar */}
          <div className="owned-list">
            <h3>Owned items</h3>
            {ownedItems.length === 0 && (
              <p className="owned-empty">You don’t own anything yet.</p>
            )}
            {ownedItems.map((id) => {
              const item = getItemById(id);
              if (!item) return null;
              return (
                <div key={id} className="owned-row">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="owned-icon"
                  />
                  <div className="owned-info">
                    <span className="owned-name">{item.name}</span>
                    <span
                      className={`rarity-tag rarity-${item.rarity.toLowerCase()}`}
                    >
                      {item.rarity}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right side of top bar */}
        <div className="store-top-right">
          <div className="store-title">Dino Dress-Up Shop</div>
          {onBackToDashboard && (
            <button
              className="store-back-button"
              onClick={onBackToDashboard}
            >
              ← Back to Dashboard
            </button>
          )}
        </div>
      </div>

      <div className="store-main">
        {/* Right: item grid */}
        <div className="store-right">
          <div className="item-grid">
            {SHOP_ITEMS.map((item) => {
              const isOwned = ownedItems.includes(item.id);
              const canAfford = glitter >= item.cost;

              let buttonLabel = "Buy";
              let disabled = false;
              let title = "";

              if (isOwned) {
                buttonLabel = "Owned";
                disabled = true;
              } else if (!canAfford) {
                disabled = true;
                title = "Not enough glitter";
              }

              return (
                <div key={item.id} className="item-card">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="item-image"
                  />
                  <div className="item-name">{item.name}</div>
                  <div className="item-meta">
                    <span
                      className={`rarity-tag rarity-${item.rarity.toLowerCase()}`}
                    >
                      {item.rarity}
                    </span>
                    <span className="item-cost">✨ {item.cost}</span>
                  </div>
                  <button
                    className="item-buy-button"
                    disabled={disabled}
                    title={title}
                    onClick={() => handlePurchase(item)}
                  >
                    {buttonLabel}
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Store;
