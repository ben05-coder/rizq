import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText,
  Lightbulb,
  CheckCircle2,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Copy,
  Check
} from "lucide-react";

export default function ResultCard({ digest }) {
  const [expandedSections, setExpandedSections] = useState({
    summary: true,
    highlights: true,
    insights: true,
    actions: true,
    questions: true
  });
  const [copied, setCopied] = useState(false);

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const copyToClipboard = () => {
    const text = `
Summary: ${digest.summary}

Highlights:
${digest.highlights.map((h, i) => `${i + 1}. ${h}`).join('\n')}

Insights:
${digest.insights.map((ins, i) => `${i + 1}. ${ins}`).join('\n')}

Action Items:
${digest.action_items.map((a, i) => `${i + 1}. ${a}`).join('\n')}

Questions:
${digest.questions.map((q, i) => `${i + 1}. ${q}`).join('\n')}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const Section = ({ title, items, icon: Icon, color, section }) => (
    <motion.div
      className={`card-section ${color}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div
        className="section-header"
        onClick={() => toggleSection(section)}
      >
        <div className="section-title">
          <Icon size={20} />
          <h3>{title}</h3>
          <span className="item-count">{items?.length || 0}</span>
        </div>
        {expandedSections[section] ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </div>

      <AnimatePresence>
        {expandedSections[section] && (
          <motion.div
            className="section-content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {typeof items === 'string' ? (
              <p className="summary-text">{items}</p>
            ) : (
              <ul>
                {items?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );

  return (
    <motion.div
      className="result-card"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="card-header">
        <h2>Digest Result</h2>
        <button
          className="copy-button"
          onClick={copyToClipboard}
          title="Copy to clipboard"
        >
          {copied ? <Check size={18} /> : <Copy size={18} />}
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>

      <div className="card-body">
        <Section
          title="Summary"
          items={digest.summary}
          icon={FileText}
          color="blue"
          section="summary"
        />

        <Section
          title="Highlights"
          items={digest.highlights}
          icon={Lightbulb}
          color="yellow"
          section="highlights"
        />

        <Section
          title="Insights"
          items={digest.insights}
          icon={Lightbulb}
          color="green"
          section="insights"
        />

        <Section
          title="Action Items"
          items={digest.action_items}
          icon={CheckCircle2}
          color="orange"
          section="actions"
        />

        <Section
          title="Questions"
          items={digest.questions}
          icon={HelpCircle}
          color="purple"
          section="questions"
        />
      </div>
    </motion.div>
  );
}
