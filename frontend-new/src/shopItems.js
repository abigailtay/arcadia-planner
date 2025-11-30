// src/shopItems.js
import beanie from "./assets/beanie.png";
import heartGlasses from "./assets/heartglasses.png";
import scarf from "./assets/scarf.png";

export const SHOP_ITEMS = [
  {
    id: "red_scarf",
    name: "Red Scarf",
    rarity: "Common",
    cost: 50,
    slot: "scarf",
    image: scarf,
  },
  {
    id: "cozy_hat",
    name: "Cozy Beanie",
    rarity: "Uncommon",
    cost: 80,
    slot: "hat",
    image: beanie,
  },
  {
    id: "heart_glasses",
    name: "Heart Glasses",
    rarity: "Rare",
    cost: 120,
    slot: "glasses",
    image: heartGlasses,
  },
];
