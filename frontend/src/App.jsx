
import { useState } from 'react'
import './App.css'

const navItems = [
  { label: 'Dashboard', icon: '⌂' },
  { label: 'Roadmap', icon: '◇' },
  { label: 'Learn & Practise', icon: '▤' },
  { label: 'AI Assistant', icon: '✳' },
  { label: 'My Progress', icon: '↗' },
]

const dailyPlan = [
  { time: '10 min', title: 'Review', description: 'Recall what you already know', number: '01' },
  { time: '25 min', title: 'Learn', description: 'Understand one new concept', number: '02' },
  { time: '20 min', title: 'Practise', description: 'Solve a question yourself', number: '03' },
  { time: '5 min', title: 'Reflect', description: 'Note what to revise next', number: '04' },
]

const phases = [
  { title: 'Programming foundations', detail: 'Variables, conditions, loops, functions, arrays and strings', tag: 'START HERE' },
  { title: 'Developer tools', detail: 'Git, debugging and working with your development environment', tag: 'ALONGSIDE' },
  { title: 'Problem solving and DSA', detail: 'Searching, sorting, complexity and common data structures', tag: 'NEXT' },
  { title: 'Core computer science', detail: 'OOP, DBMS, SQL, operating systems and networks', tag: 'CORE' },
  { title: 'Build a practical project', detail: 'Apply concepts and explain your own implementation', tag: 'BUILD' },
  { title: 'Advanced problem solving', detail: 'More DSA patterns and role-specific technical practice', tag: 'GROW' },
  { title: 'Aptitude and interviews', detail: 'Reasoning, communication and technical interview practice', tag: 'PRACTISE' },
  { title: 'Placement readiness', detail: 'Resume, portfolio, job descriptions and application preparation', tag: 'PREPARE' },
]

const pilotLessons = [
  {
    id: 1,
    title: 'Problem-solving basics',
    time: '15 min',
    level: 'Beginner',
    summary: 'Turn a problem statement into clear, ordered steps.',
    objective: 'Identify the input, output and steps needed to solve a simple problem.',
    explanation: 'Before writing code, make sure you understand what the problem asks. Identify the information you receive (input), the result you must produce (output), and the rules connecting them. Then write the steps in order and test them with a small example.',
    example: 'Problem: Calculate the total cost of 3 notebooks at ₹20 each.\n\nInput: quantity = 3, price = 20\nStep 1: Multiply quantity by price.\nStep 2: Display the result.\n\nPseudocode:\nINPUT quantity\nINPUT price\ntotal = quantity * price\nOUTPUT total\n\nOutput: 60',
    checkpoint: 'For a program that calculates the area of a rectangle, identify its two inputs and its output.',
  },
  {
    id: 2,
    title: 'Variables and data types',
    time: '20 min',
    level: 'Beginner',
    summary: 'Store information using appropriate types.',
    objective: 'Explain variables and distinguish common data types.',
    explanation: 'A variable is a named place to store a value that a program can use. A data type describes the kind of value. Common types include integers (whole numbers), decimals, strings (text) and booleans (true or false). Exact syntax can differ between Java, C++ and Python.',
    example: 'Illustrative examples:\n\nage = 20           // whole number\nprice = 49.50      // decimal value\nname = "Asha"      // text\nis_ready = true    // true or false\n\nThink about the kind of value each variable needs to hold. These examples illustrate concepts; syntax varies by language.',
    checkpoint: 'Which data type is most suitable for storing a student’s name: an integer, a string, or a boolean?',
  },
  {
    id: 3,
    title: 'Input, output and operators',
    time: '20 min',
    level: 'Beginner',
    summary: 'Accept values, calculate results and display them.',
    objective: 'Use arithmetic operators and follow the order of operations.',
    explanation: 'Input provides information to a program, and output displays a result. Arithmetic operators include + (addition), - (subtraction), * (multiplication) and / (division). Comparison operators compare values; logical operators combine conditions. Parentheses can make the intended order of calculations clear.',
    example: 'Given:\nquantity = 3\nprice = 20\n delivery_fee = 5\n\ntotal = quantity * price + delivery_fee\nOUTPUT total\n\nCalculation: 3 * 20 + 5 = 65\nOutput: 65\n\nMultiplication is evaluated before addition.',
    checkpoint: 'What is the result of 4 + 3 * 2? What would the result be if the expression were (4 + 3) * 2?',
  },
]

const upcomingLessons = [
  'Conditional statements',
  'Loops',
  'Functions and methods',
  'Arrays and lists',
  'Strings',
  'Code tracing',
  'Debugging and common errors',
  'Foundation problem practice',
]

const suggestedQuestions = [
  'What is binary search?',
  'What is the difference between a stack and a queue?',
  'Explain object-oriented programming.',
]

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Hi! I’m your PlacementPrepLM assistant. Ask a placement-preparation question, and I’ll look for a reliable match in the reviewed question dataset.',
      meta: 'Connected to the reviewed Q&A feature when the backend is running.',
    },
  ])
  const [selectedLesson, setSelectedLesson] = useState(1)

  const currentLesson =
    pilotLessons.find((lesson) => lesson.id === selectedLesson) || pilotLessons[0]

  async function sendQuestion(textToSend = question) {
    const cleanQuestion = textToSend.trim()
    if (!cleanQuestion || loading) return

    setActivePage('AI Assistant')
    setMessages((previous) => [
      ...previous,
      { role: 'user', text: cleanQuestion },
    ])
    setQuestion('')
    setLoading(true)

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: cleanQuestion }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'The request could not be completed.')
      }

      const answerText = data.found
        ? data.answer
        : data.message || 'No reliable match was found in the reviewed content.'

      const answerMeta = data.found
        ? `${data.source || 'Reviewed content'} · Similarity: ${Math.round((data.similarity || 0) * 100)}% · Matched: ${data.matched_question}`
        : 'No sufficiently reliable match in the reviewed dataset.'

      setMessages((previous) => [
        ...previous,
        { role: 'assistant', text: answerText, meta: answerMeta },
      ])
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          text: 'I could not reach the backend. Check that Flask is running at http://127.0.0.1:5000 and that the Vite API proxy is configured.',
          meta: error.message || 'Connection issue',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleQuestionSubmit(event) {
    event.preventDefault()
    sendQuestion()
  }

  function renderDashboard() {
    return (
      <>
        <section className="hero-card">
          <div className="hero-copy">
            <span className="eyebrow light">YOUR PLACEMENT JOURNEY</span>
            <h2>Small steps.<br />Stronger skills.</h2>
            <p>Build your placement preparation one focused study session at a time. Learn the basics, practise what you learn, and keep moving forward.</p>
            <div className="hero-actions">
              <button className="button button-light" onClick={() => setActivePage('Learn & Practise')}>Start learning <span>→</span></button>
              <button className="button button-ghost" onClick={() => setActivePage('AI Assistant')}>Ask a question</button>
            </div>
          </div>
          <div className="hero-visual" aria-hidden="true">
            <div className="visual-circle circle-one" />
            <div className="visual-circle circle-two" />
            <div className="visual-note">
              <span className="visual-check">✓</span>
              <div><strong>One task at a time</strong><small>Learn · Practise · Reflect</small></div>
            </div>
            <div className="visual-number">60<span> min</span></div>
          </div>
        </section>

        <div className="section-heading">
          <div><h2>Your study framework</h2><p>A suggested daily plan you can adjust later.</p></div>
          <span className="soft-badge">60 minutes</span>
        </div>

        <section className="plan-grid">
          {dailyPlan.map((item) => (
            <article className="plan-card" key={item.number}>
              <div className="plan-card-top"><span className="plan-number">{item.number}</span><span className="plan-time">{item.time}</span></div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </section>

        <div className="dashboard-columns">
          <section className="content-card">
            <div className="card-heading"><div><span className="eyebrow">YOUR NEXT STEP</span><h2>Start with the foundations</h2></div><span className="card-icon">✳</span></div>
            <p className="muted-copy">Learn how to break problems into steps before moving into more complex programming topics.</p>
            {pilotLessons.slice(0, 3).map((lesson, index) => (
              <button className="next-lesson-row" key={lesson.id} onClick={() => { setSelectedLesson(lesson.id); setActivePage('Learn & Practise') }}>
                <span className="lesson-index">{String(index + 1).padStart(2, '0')}</span>
                <span className="lesson-row-copy"><strong>{lesson.title}</strong><small>{lesson.time} · Beginner</small></span>
                <span className="row-arrow">→</span>
              </button>
            ))}
            <button className="text-button" onClick={() => setActivePage('Roadmap')}>Explore the full roadmap <span>→</span></button>
          </section>

          <section className="content-card assistant-promo">
            <span className="promo-symbol">✳</span>
            <span className="eyebrow">STUCK ON A CONCEPT?</span>
            <h2>Ask. Understand. Practise.</h2>
            <p className="muted-copy">Ask a placement question. The assistant searches the reviewed Q&A dataset and tells you when it cannot find a reliable match.</p>
            <div className="suggestion-list">
              {suggestedQuestions.slice(0, 2).map((item) => (
                <button className="suggestion-chip" key={item} onClick={() => { setQuestion(item); setActivePage('AI Assistant') }}>{item}<span>↗</span></button>
              ))}
            </div>
            <button className="button button-primary full-button" onClick={() => setActivePage('AI Assistant')}>Open AI Assistant <span>→</span></button>
          </section>
        </div>
        <p className="prototype-note">Preview version · Student accounts and saved learning progress are not connected yet.</p>
      </>
    )
  }

  function renderRoadmap() {
    return (
      <section className="content-card roadmap-card">
        <div className="section-heading"><div><h2>Your learning path</h2><p>Follow the foundations, then focus on the topics that match your goals.</p></div><span className="soft-badge">8 stages</span></div>
        <div className="roadmap-list">
          {phases.map((phase, index) => (
            <div className="roadmap-row" key={phase.title}>
              <div className={`roadmap-step ${index === 0 ? 'step-current' : ''}`}>{String(index + 1).padStart(2, '0')}</div>
              <div className="roadmap-copy"><h3>{phase.title}</h3><p>{phase.detail}</p></div>
              <span className={`roadmap-tag ${index === 0 ? 'tag-current' : ''}`}>{phase.tag}</span>
            </div>
          ))}
        </div>
        <p className="prototype-note">Roadmap statuses are a preview. Prerequisites and saved mastery decisions will be added in the next development steps.</p>
      </section>
    )
  }

  function renderLessons() {
    return (
      <>
        <section className="learning-intro">
          <span className="eyebrow">PHASE 1 · PROGRAMMING FOUNDATIONS</span>
          <h2>Build understanding before speed.</h2>
          <p>Start with these three pilot lessons. Each lesson includes a simple explanation, a worked example and a self-check question.</p>
        </section>
        <div className="learning-layout">
          <section className="content-card lesson-list-card">
            <h2 className="small-card-title">Pilot lessons</h2>
            {pilotLessons.map((lesson) => (
              <button key={lesson.id} className={`lesson-select ${selectedLesson === lesson.id ? 'lesson-selected' : ''}`} onClick={() => setSelectedLesson(lesson.id)}>
                <span className="lesson-index">{String(lesson.id).padStart(2, '0')}</span>
                <span className="lesson-row-copy"><strong>{lesson.title}</strong><small>{lesson.time} · {lesson.level}</small></span>
                <span className="row-arrow">→</span>
              </button>
            ))}
            <h3 className="upcoming-heading">Coming next</h3>
            {upcomingLessons.slice(0, 5).map((title) => <div className="upcoming-row" key={title}><span>○</span>{title}</div>)}
          </section>
          <article className="content-card lesson-detail">
            <div className="lesson-detail-top"><span className="soft-badge">LESSON {String(currentLesson.id).padStart(2, '0')}</span><span className="muted-small">{currentLesson.time} · {currentLesson.level}</span></div>
            <h2>{currentLesson.title}</h2>
            <p className="lesson-objective"><strong>Learning objective:</strong> {currentLesson.objective}</p>
            <h3>Understand the idea</h3>
            <p>{currentLesson.explanation}</p>
            <h3>Worked example</h3>
            <pre className="example-block">{currentLesson.example}</pre>
            <div className="self-check"><span className="self-check-icon">?</span><div><strong>Check your understanding</strong><p>{currentLesson.checkpoint}</p></div></div>
            <button className="button button-primary" onClick={() => setActivePage('AI Assistant')}>Ask the assistant for help <span>→</span></button>
            <p className="prototype-note">Self-check answers, coding exercises and mastery assessment will be added next.</p>
          </article>
        </div>
      </>
    )
  }

  function renderAssistant() {
    return (
      <div className="assistant-layout">
        <section className="content-card chat-card">
          <div className="chat-header">
            <div className="assistant-avatar">✳</div>
            <div className="chat-heading-copy"><h2>PlacementPrepLM assistant</h2><p>Placement Q&A · Reviewed content</p></div>
            <span className="status-pill"><span /> Retrieval mode</span>
          </div>
          <div className="message-list" role="log" aria-live="polite">
            {messages.map((message, index) => (
              <div className={`message-row ${message.role === 'user' ? 'user-row' : ''}`} key={`${index}-${message.role}`}>
                {message.role === 'assistant' && <span className="message-avatar">✳</span>}
                <div className={`message-bubble ${message.role === 'user' ? 'user-bubble' : 'assistant-bubble'}`}>
                  <p>{message.text}</p>
                  {message.meta && <small>{message.meta}</small>}
                </div>
              </div>
            ))}
            {loading && <div className="message-row"><span className="message-avatar">✳</span><div className="message-bubble assistant-bubble"><p className="loading-text">Searching reviewed content…</p></div></div>}
          </div>
          <div className="chat-suggestions">
            <span>Try asking</span>
            {suggestedQuestions.map((item) => <button key={item} onClick={() => setQuestion(item)}>{item}</button>)}
          </div>
          <form className="chat-form" onSubmit={handleQuestionSubmit}>
            <input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a placement preparation question…" aria-label="Your question" maxLength={500} disabled={loading} />
            <button className="button button-primary" type="submit" disabled={loading || !question.trim()}>{loading ? 'Searching…' : 'Send'} <span>↑</span></button>
          </form>
          <p className="chat-disclaimer">Answers come from the reviewed Q&A dataset when a sufficiently similar question is found. The from-scratch Transformer is not connected to this chat yet.</p>
        </section>
        <aside className="assistant-side">
          <section className="content-card info-card">
            <span className="info-icon">◎</span><h3>How answers work</h3>
            <p>PlacementPrepLM compares your question with reviewed questions and returns a matching answer when the similarity is high enough.</p>
            <div className="info-divider" />
            <div className="info-step"><span>1</span><div><strong>Ask</strong><small>Enter your question in your own words.</small></div></div>
            <div className="info-step"><span>2</span><div><strong>Match</strong><small>The backend searches the stored Q&A.</small></div></div>
            <div className="info-step"><span>3</span><div><strong>Learn</strong><small>Review the answer or try a related question.</small></div></div>
          </section>
          <section className="content-card tip-card"><span className="eyebrow">STUDY TIP</span><h3>Try explaining it yourself.</h3><p>After reading an answer, explain the concept in your own words and solve a small example. That helps you check what you actually understand.</p></section>
        </aside>
      </div>
    )
  }

  function renderProgress() {
    return (
      <section className="content-card progress-empty">
        <div className="empty-progress-icon">↗</div>
        <span className="eyebrow">YOUR LEARNING RECORD</span>
        <h2>Your progress starts here.</h2>
        <p>This preview does not save progress yet. In the next steps, we will add assessments, topic mastery, student accounts and a database so your learning record can persist between sessions.</p>
        <button className="button button-primary" onClick={() => setActivePage('Learn & Practise')}>Continue learning <span>→</span></button>
      </section>
    )
  }

  const pageDescriptions = {
    Dashboard: 'A clear next step for your placement preparation.',
    Roadmap: 'See how the topics fit together and what to learn next.',
    'Learn & Practise': 'Understand concepts, study examples and check your knowledge.',
    'AI Assistant': 'Ask placement questions and learn from reviewed answers.',
    'My Progress': 'Your learning record will appear here as progress tracking is added.',
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">P<span>.</span></div>
          <div className="brand-name">Placement<span>PrepLM</span><small>YOUR LEARNING COMPANION</small></div>
        </div>
        <div className="sidebar-label">WORKSPACE</div>
        <nav className="side-nav" aria-label="Main navigation">
          {navItems.map((item) => (
            <button key={item.label} className={`nav-item ${activePage === item.label ? 'nav-active' : ''}`} onClick={() => setActivePage(item.label)}>
              <span className="nav-icon">{item.icon}</span><span>{item.label}</span>{item.label === 'AI Assistant' && <span className="nav-new">Q&A</span>}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-mini-icon">✦</div>
          <strong>Progress, not perfection.</strong>
          <p>One focused hour can move you forward.</p>
          <div className="sidebar-progress"><span /></div>
          <small>Daily study framework · 60 min</small>
        </div>
        <div className="sidebar-footer"><div className="profile-avatar">S</div><div><strong>Student workspace</strong><small>Local preview</small></div><span className="footer-dots">···</span></div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div><div className="breadcrumb">PLACEMENT PREPARATION <span>/</span> {activePage.toUpperCase()}</div><h1>{activePage}</h1><p>{pageDescriptions[activePage]}</p></div>
          <div className="topbar-right"><span className="preview-pill"><span /> LOCAL PREVIEW</span><div className="topbar-avatar">S</div></div>
        </header>
        <div className="page-content">
          {activePage === 'Dashboard' && renderDashboard()}
          {activePage === 'Roadmap' && renderRoadmap()}
          {activePage === 'Learn & Practise' && renderLessons()}
          {activePage === 'AI Assistant' && renderAssistant()}
          {activePage === 'My Progress' && renderProgress()}
        </div>
        <footer className="main-footer"><span>PlacementPrepLM</span><span>Learn with purpose · Practise with confidence</span></footer>
      </main>
    </div>
  )
}

export default App
