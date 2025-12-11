import { useState } from "react";
import { motion } from "framer-motion";
import { FileAudio, Copy, Check, ChevronDown, ChevronUp } from "lucide-react";

export default function TranscriptCard({ transcript, metadata }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(transcript.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatDuration = (seconds) => {
    if (!seconds) return "N/A";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <motion.div
      className="transcript-card"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="card-header">
        <div className="header-left">
          <FileAudio size={24} />
          <div>
            <h2>Transcript</h2>
            {metadata?.filename && (
              <span className="filename">{metadata.filename}</span>
            )}
          </div>
        </div>
        <div className="header-right">
          <span className="word-count">{transcript.word_count} words</span>
          {transcript.duration && (
            <span className="duration">{formatDuration(transcript.duration)}</span>
          )}
          <button
            className="icon-button"
            onClick={() => setIsExpanded(!isExpanded)}
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
          </button>
          <button
            className="icon-button"
            onClick={copyToClipboard}
            title="Copy transcript"
          >
            {copied ? <Check size={18} /> : <Copy size={18} />}
          </button>
        </div>
      </div>

      {isExpanded && (
        <motion.div
          className="transcript-content"
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          <p>{transcript.text}</p>
        </motion.div>
      )}

      {metadata?.created_at && (
        <div className="card-footer">
          <span className="timestamp">
            {new Date(metadata.created_at).toLocaleString()}
          </span>
        </div>
      )}
    </motion.div>
  );
}
