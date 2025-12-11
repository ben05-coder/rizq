import { useState } from "react";
import "./index.css";
import ResultCard from "./components/ResultCard";
import TranscriptCard from "./components/TranscriptCard";
import SearchResults from "./components/SearchResults";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ingestData, setIngestData] = useState(null);
  const [searchData, setSearchData] = useState(null);
  const [error, setError] = useState(null);

  async function handleUpload() {
    if (!file) return;

    setLoading(true);
    setError(null);
    setIngestData(null);
    setSearchData(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/ingest", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        throw new Error(`Upload failed: ${res.statusText}`);
      }

      const data = await res.json();

      if (data.success) {
        setIngestData(data.data);
      } else {
        throw new Error(data.message || "Upload failed");
      }
    } catch (err) {
      setError(err.message);
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch(e) {
    e.preventDefault();
    const query = e.target.query.value.trim();

    if (!query) return;

    setLoading(true);
    setError(null);
    setIngestData(null);
    setSearchData(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        throw new Error(`Search failed: ${res.statusText}`);
      }

      const data = await res.json();

      if (data.success) {
        setSearchData(data.data);
      } else {
        throw new Error(data.message || "Search failed");
      }
    } catch (err) {
      setError(err.message);
      console.error("Search error:", err);
    } finally {
      setLoading(false);
      e.target.reset();
    }
  }

  return (
    <div className="container">
      <h1>Rizq Memory Engine — LOCAL</h1>

      <div className="upload-section">
        <input
          id="fileInput"
          type="file"
          accept="audio/*"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ display: "none" }}
        />

        <div
          className="upload-box"
          onClick={() => document.getElementById("fileInput").click()}
        >
          {file ? file.name : "Click to choose an audio file"}
        </div>

        <button onClick={handleUpload} disabled={loading || !file}>
          {loading ? "Processing..." : "Upload & Process"}
        </button>
      </div>

      <form className="search-box" onSubmit={handleSearch}>
        <input
          type="text"
          name="query"
          placeholder="Ask a question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Ask"}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="error-message" style={{
          padding: "16px",
          background: "#fee",
          border: "1px solid #fcc",
          borderRadius: "10px",
          color: "#c00",
          marginBottom: "24px"
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading">
          <div style={{ fontSize: "18px" }}>Processing...</div>
        </div>
      )}

      {/* Ingest Results */}
      {ingestData && !loading && (
        <>
          <TranscriptCard
            transcript={ingestData.transcript}
            metadata={ingestData.metadata}
          />
          <ResultCard digest={ingestData.digest} />
        </>
      )}

      {/* Search Results */}
      {searchData && !loading && (
        <SearchResults searchData={searchData} />
      )}
    </div>
  );
}

export default App;
