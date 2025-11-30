import React, { useEffect, useRef } from "react";

export default function WoodenBoxAnimation({ onEnded }) {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current && onEnded) {
      videoRef.current.onended = onEnded;
    }
  }, [onEnded]);

  return (
    <div style={{ width: 350, margin: "60px auto", textAlign: "center", position: "relative" }}>
      <video
        ref={videoRef}
        src="/RecipeBook.mp4"  // <-- This only works if RecipeBook.mp4 is in public/
        width="100%"
        autoPlay
        muted
        playsInline
        style={{
          borderRadius: 20,
          boxShadow: "0 8px 40px #0002",
          background: "#e4c7a3"
        }}
      />
      <div style={{
        fontWeight: 700, fontSize: 20, color: "#7d5521", marginTop: 18
      }}>
        Opening the recipe box...
      </div>
    </div>
  );
}
