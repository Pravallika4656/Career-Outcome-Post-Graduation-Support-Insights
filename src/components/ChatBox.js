import React, { useState } from "react";
import "./../styles/ChatBox.css";
import axios from "axios";

const ChatBox = () => {
  const [activeTab, setActiveTab] = useState("parent");

  // Chat states
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  // Parent Insight States
  const [major, setMajor] = useState("");
  const [academicStrength, setAcademicStrength] = useState("");
  const [interestArea, setInterestArea] = useState("");

  // ✅ NEW STATES
  const [investment, setInvestment] = useState("");
  const [placement, setPlacement] = useState("");

  const [insight, setInsight] = useState("");
  const [loadingInsights, setLoadingInsights] = useState(false);

  // ✅ ✅ BACKEND URL (Render)
  const API_BASE = "https://career-outcome-post-graduation-support.onrender.com";

  // ✅ Chatbot Message Sender
  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    const msg = input;
    setInput("");

    try {
      const response = await axios.post(`${API_BASE}/api/chat`, {
        message: msg,
      });

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: response.data.reply },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Server error. Try again." },
      ]);
    }
  };

  // ✅ Parent Insight Generator
  const getParentInsights = async () => {
    setLoadingInsights(true);

    try {
      const response = await axios.post(`${API_BASE}/api/parent_insights`, {
        major,
        academic_strength: academicStrength,
        interest_area: interestArea,
        investment,
        placement,
      });

      setInsight(response.data.insight);
    } catch {
      setInsight("❗ Error generating insights.");
    }

    setLoadingInsights(false);
  };

  return (
    <div className="page-container">
      {/* ✅ TOP NAV BUTTONS */}
      <div className="tab-buttons">
        <button
          className={activeTab === "parent" ? "tab active" : "tab"}
          onClick={() => setActiveTab("parent")}
        >
          Parent Insights
        </button>

        <button
          className={activeTab === "chat" ? "tab active" : "tab"}
          onClick={() => setActiveTab("chat")}
        >
          Chatbot
        </button>
      </div>

      {/* ✅ PARENT INSIGHT PANEL */}
      {activeTab === "parent" && (
        <div className="parent-box">
          <h2>🎓 Career Outcomes & Parent Insights</h2>

          <input
            placeholder="Student Major (e.g., Computer Science)"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
          />

          <input
            placeholder="Academic Strength (Average / Good / Excellent)"
            value={academicStrength}
            onChange={(e) => setAcademicStrength(e.target.value)}
          />

          <input
            placeholder="Interest Area (Tech / Research / Business etc.)"
            value={interestArea}
            onChange={(e) => setInterestArea(e.target.value)}
          />

          {/* ✅ NEW INPUTS */}
          <input
            type="number"
            placeholder="Total Course Investment (₹)"
            value={investment}
            onChange={(e) => setInvestment(e.target.value)}
          />

          <input
            type="number"
            placeholder="Placement Percentage (%)"
            value={placement}
            onChange={(e) => setPlacement(e.target.value)}
          />

          <button className="main-btn" onClick={getParentInsights}>
            {loadingInsights ? "Analyzing..." : "Generate Parent Insights"}
          </button>

          {insight && <div className="insight-box">{insight}</div>}
        </div>
      )}

      {/* ✅ CHATBOT PANEL */}
      {activeTab === "chat" && (
        <div className="chat-section">
          <h2>💬 Student Career Q&A Chatbot</h2>

          <div className="chat-box">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="input-area">
            <input
              type="text"
              value={input}
              placeholder="Ask your career question..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button className="send-btn" onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
