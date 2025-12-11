import { motion } from "framer-motion";
import { Search, FileText, Sparkles, Copy, Check } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function SearchResults({ searchData }) {
  const [copied, setCopied] = useState(false);

  const copyAnswer = () => {
    navigator.clipboard.writeText(searchData.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getRelevanceColor = (score) => {
    if (!score) return "gray";
    if (score > 0.8) return "green";
    if (score > 0.6) return "yellow";
    return "orange";
  };

  const getRelevanceLabel = (score) => {
    if (!score) return "N/A";
    if (score > 0.8) return "Highly Relevant";
    if (score > 0.6) return "Relevant";
    return "Somewhat Relevant";
  };

  return (
    <motion.div
      className="search-results"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Query Display */}
      <div className="search-query">
        <Search size={20} />
        <span>{searchData.query}</span>
      </div>

      {/* Answer Section */}
      <motion.div
        className="answer-card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3, delay: 0.1 }}
      >
        <div className="answer-header">
          <div className="header-left">
            <Sparkles size={20} />
            <h3>Answer</h3>
          </div>
          <button
            className="icon-button"
            onClick={copyAnswer}
            title="Copy answer"
          >
            {copied ? <Check size={18} /> : <Copy size={18} />}
          </button>
        </div>
        <div className="answer-content">
          <ReactMarkdown>{searchData.answer}</ReactMarkdown>
        </div>
      </motion.div>

      {/* Sources Section */}
      {searchData.sources && searchData.sources.length > 0 && (
        <div className="sources-section">
          <div className="sources-header">
            <FileText size={20} />
            <h3>Sources</h3>
            <span className="source-count">{searchData.sources.length}</span>
          </div>

          <div className="sources-list">
            {searchData.sources.map((source, index) => (
              <motion.div
                key={source.id}
                className="source-card"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2, delay: 0.2 + index * 0.1 }}
              >
                <div className="source-header">
                  <span className="source-number">#{index + 1}</span>
                  {source.relevance_score && (
                    <span
                      className={`relevance-badge ${getRelevanceColor(source.relevance_score)}`}
                    >
                      {getRelevanceLabel(source.relevance_score)}
                    </span>
                  )}
                </div>
                <div className="source-snippet">
                  <p>{source.snippet}</p>
                </div>
                <div className="source-footer">
                  <span className="source-id">{source.id.substring(0, 8)}...</span>
                  {source.relevance_score && (
                    <span className="score-value">
                      {(source.relevance_score * 100).toFixed(1)}%
                    </span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}
