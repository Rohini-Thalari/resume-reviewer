# 📄 AI Resume Reviewer

> Upload your resume and get instant AI-powered feedback, scoring, and actionable suggestions to land your next job.

---

## 📌 Overview

**AI Resume Reviewer** is an intelligent web application that analyzes resumes using the **Anthropic Claude API**. Simply upload your resume (PDF or text), and the AI will evaluate it across multiple dimensions — structure, content, clarity, ATS compatibility, and more — returning detailed feedback with a score and improvement tips.

Whether you're a fresh graduate or an experienced professional, this tool helps you craft a resume that stands out.

---

## ✨ Features

- 📤 **Resume Upload** — supports PDF and plain text formats
- 🤖 **AI-Powered Analysis** — Claude reads and evaluates your resume intelligently
- 📊 **Resume Score** — get an overall score out of 100
- 🔍 **Section-by-Section Feedback** — detailed review of Summary, Skills, Experience, Education, and more
- ✅ **ATS Compatibility Check** — identifies keywords and formatting issues that may block automated screening
- 💡 **Actionable Suggestions** — specific, prioritized improvements you can make right away
- 🎯 **Job Role Targeting** *(optional)* — tailor feedback to a specific job title or description

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| HTML / CSS / JavaScript | Frontend UI |
| Anthropic Claude API (`claude-sonnet-4`) | Resume analysis & feedback generation |
| PDF.js / FileReader API | Resume file parsing |
| Fetch API | API communication |

---

## 🚀 Getting Started

### Prerequisites

- An [Anthropic API key](https://console.anthropic.com/)
- A modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohini-Thalari/resume-reviewer.git
   cd resume-reviewer
   ```

2. **Open the app**
   ```bash
   # Serve locally using any static server
   npx serve .
   # or
   python -m http.server 3000
   ```

3. **Configure your API key**
   - Add your Anthropic API key to the config or environment setup in the project.

---

## 🧪 How to Use

1. Open the app in your browser
2. Upload your resume as a **PDF** or paste the text directly
3. *(Optional)* Enter a target **job title or job description** for tailored feedback
4. Click **"Analyze Resume"**
5. Review your **score**, **section-by-section feedback**, and **suggestions**
6. Make improvements and re-upload to track your progress

---

## 📸 Sample Output

```
Overall Score: 78 / 100

✅ Strengths:
  - Clear work experience section with measurable achievements
  - Good use of action verbs

⚠️ Areas to Improve:
  - Summary section is too generic — personalize it for the target role
  - Missing key skills: Python, REST APIs (based on target JD)
  - Education section lacks relevant coursework or GPA

📋 ATS Check:
  - ✅ Standard section headers detected
  - ⚠️ Avoid tables/columns — some ATS parsers cannot read them
  - ⚠️ Add more industry-relevant keywords

💡 Top 3 Suggestions:
  1. Rewrite your summary to highlight your unique value proposition
  2. Add a dedicated Skills section with role-relevant technologies
  3. Quantify achievements with numbers (e.g., "increased sales by 30%")
```

---

## 🔍 Review Criteria

| Category | What's Evaluated |
|---|---|
| **Structure** | Sections present, logical order, formatting |
| **Content Quality** | Clarity, specificity, use of action verbs |
| **ATS Compatibility** | Keywords, formatting, header names |
| **Impact** | Quantified achievements, results-oriented language |
| **Relevance** | Alignment with target role (if provided) |
| **Grammar & Tone** | Professional language, spelling, consistency |

---

## 📁 Project Structure

```
resume-reviewer/
├── index.html          # Main application UI
├── style.css           # Styling
├── app.js              # Core logic — file parsing & API calls
├── utils.js            # Helper functions
└── README.md           # Project documentation
```

---

## 🔐 API Usage

This project calls the Anthropic Claude API to analyze resume content:

```javascript
const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1500,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: { type: "base64", media_type: "application/pdf", data: base64Resume }
          },
          {
            type: "text",
            text: "Analyze this resume and provide a score, section feedback, ATS check, and improvement suggestions. Return as JSON."
          }
        ]
      }
    ]
  })
});
```

---

## ⚠️ Limitations

- Works best with **text-based PDFs** (scanned/image PDFs may not parse correctly)
- Feedback quality improves when a **target job role** is provided
- API usage is subject to [Anthropic's rate limits](https://docs.anthropic.com)

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Rohini Thalari**
- GitHub: [@Rohini-Thalari](https://github.com/Rohini-Thalari)

---

> Built with ❤️ using Claude AI — because every resume deserves a second opinion.
