import { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, Download, Copy, Check } from "lucide-react";

export default function FlashcardGrid({ flashcardsData }) {
  const [flippedCards, setFlippedCards] = useState(new Set());
  const [copied, setCopied] = useState(false);

  const toggleFlip = (index) => {
    setFlippedCards((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  const flipAll = () => {
    if (flippedCards.size === flashcardsData.flashcards.length) {
      setFlippedCards(new Set());
    } else {
      setFlippedCards(
        new Set(Array.from({ length: flashcardsData.flashcards.length }, (_, i) => i))
      );
    }
  };

  const exportToAnki = () => {
    // Create CSV format for Anki import
    let csv = "";
    flashcardsData.flashcards.forEach((card) => {
      // Escape quotes and add to CSV
      const front = card.front.replace(/"/g, '""');
      const back = card.back.replace(/"/g, '""');
      csv += `"${front}","${back}"\n`;
    });

    // Create download
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "rizq-flashcards.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyAllText = () => {
    const text = flashcardsData.flashcards
      .map((card, i) => `${i + 1}. Q: ${card.front}\n   A: ${card.back}`)
      .join("\n\n");

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!flashcardsData || flashcardsData.count === 0) {
    return null;
  }

  return (
    <motion.div
      className="flashcard-section"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flashcard-header">
        <div className="header-left">
          <BookOpen size={24} />
          <div>
            <h2>Flashcards</h2>
            <span className="flashcard-count">{flashcardsData.count} cards generated</span>
          </div>
        </div>
        <div className="flashcard-actions">
          <button className="icon-button" onClick={flipAll} title="Flip all cards">
            {flippedCards.size === flashcardsData.flashcards.length ? "Reset All" : "Flip All"}
          </button>
          <button className="icon-button" onClick={copyAllText} title="Copy all">
            {copied ? <Check size={18} /> : <Copy size={18} />}
            {copied ? "Copied!" : "Copy"}
          </button>
          <button className="icon-button" onClick={exportToAnki} title="Export to Anki">
            <Download size={18} />
            Export
          </button>
        </div>
      </div>

      <div className="flashcard-grid">
        {flashcardsData.flashcards.map((card, index) => (
          <motion.div
            key={index}
            className="flashcard-container"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2, delay: index * 0.05 }}
          >
            <div
              className={`flashcard ${flippedCards.has(index) ? "flipped" : ""}`}
              onClick={() => toggleFlip(index)}
            >
              <div className="flashcard-inner">
                <div className="flashcard-front">
                  <div className="card-number">#{index + 1}</div>
                  <div className="card-content">
                    <p>{card.front}</p>
                  </div>
                  <div className="card-hint">Click to reveal</div>
                </div>
                <div className="flashcard-back">
                  <div className="card-number">#{index + 1}</div>
                  <div className="card-content">
                    <p>{card.back}</p>
                  </div>
                  <div className="card-hint">Click to flip</div>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="flashcard-footer">
        <p>
          💡 <strong>Tip:</strong> Click any card to flip it. Export to Anki for spaced repetition studying!
        </p>
      </div>
    </motion.div>
  );
}
