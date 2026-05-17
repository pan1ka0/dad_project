import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate("/dashboard");
      } else {
        alert(data.detail || "Login failed");
      }
    } catch (error) {
      console.log(error);
      alert("Server error");
    }
  };

  return (
    <div className="auth-page">
      <div className="glass-card">
        <h1>Welcome Back 👋</h1>
        <p className="subtitle">Login to continue learning</p>

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Login</button>
        </form>

        <p className="switch-text">
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: name,
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate("/");
      } else {
        alert(data.detail || "Registration failed");
      }
    } catch (error) {
      console.log(error);
      alert("Server error");
    }
  };

  return (
    <div className="auth-page">
      <div className="glass-card">
        <h1>Create Account ✨</h1>
        <p className="subtitle">Start your LMS journey</p>

        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Full Name"
            onChange={(e) => setName(e.target.value)}
          />

          <input
            type="email"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Create Account</button>
        </form>

        <p className="switch-text">
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}
function Dashboard() {
  const schedule = {
  Monday: [
    "Web Development",
    "Python Basics",
  ],

  Tuesday: [
    "Networking",
    "Database Systems",
  ],

  Wednesday: [
    "Cyber Security",
    "UI/UX Design",
  ],

  Thursday: [
    "Java Programming",
    "Cloud Computing",
  ],

  Friday: [
    "Mobile Development",
    "AI Fundamentals",
  ],
};

  const assignments = [
  {
    title: "HTML Assignment",
    due: "May 25",
  },
  {
    title: "CSS Project",
    due: "May 28",
  },
  {
    title: "JavaScript Quiz",
    due: "June 1",
  },
  {
    title: "Python Functions Lab",
    due: "June 3",
  },
  {
    title: "Networking Report",
    due: "June 5",
  },
  {
    title: "Database ER Diagram",
    due: "June 7",
  },
];

  const grades = [
  {
    subject: "Web Development",
    grade: "95%",
  },
  {
    subject: "Networking",
    grade: "88%",
  },
  {
    subject: "Python Basics",
    grade: "91%",
  },
  {
    subject: "Cyber Security",
    grade: "86%",
  },
  {
    subject: "Database Systems",
    grade: "93%",
  },
  {
    subject: "UI/UX Design",
    grade: "97%",
  },
];

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2>LMS</h2>

        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </nav>
      </aside>

      <main className="main-content">
        <h1>Dashboard</h1>

        <div className="stats-grid">
          <div className="stat-card">
            <span>📚</span>
<h2>{Object.values(schedule).flat().length}</h2>
            <p>Courses</p>
          </div>

          <div className="stat-card">
            <span>📝</span>
<h2>{grades.length}</h2>
            <p>Assignments</p>
          </div>

          <div className="stat-card">
            <span>🏆</span>
            <h2>{grades.length}</h2>
            <p>Grades</p>
          </div>
        </div>

        <div className="dashboard-sections">
          <div className="dashboard-card">
  <h2>Weekly Schedule</h2>

  {Object.entries(schedule).map(([day, courses]) => (
    <div className="schedule-day" key={day}>
      <h3>{day}</h3>

      {courses.map((course, index) => (
        <div
          className="dashboard-item"
          key={index}
        >
          📘 {course}
        </div>
      ))}
    </div>
  ))}
</div>

          <div className="dashboard-card">
            <h2>Upcoming Assignments</h2>

            {assignments.map((assignment, index) => (
              <div className="dashboard-item" key={index}>
                <strong>{assignment.title}</strong>

                <p>Due: {assignment.due}</p>
              </div>
            ))}
          </div>

          <div className="dashboard-card">
            <h2>Grades</h2>

            {grades.map((grade, index) => (
              <div className="dashboard-item" key={index}>
                <strong>{grade.subject}</strong>

                <p>{grade.grade}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

function Courses() {
  const fakeCourses = [
    {
      id: 1,
      title: "Web Development",
      description: "Learn HTML CSS JS",
    },
    {
      id: 2,
      title: "Python Basics",
      description: "Introduction to Python",
    },
    {
      id: 3,
      title: "Networking",
      description: "TCP/IP and Routing",
    },
  ];

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2>LMS</h2>

        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </nav>
      </aside>

      <main className="main-content">
        <h1>Courses</h1>

        <div className="courses-grid">
          {fakeCourses.map((course) => (
            <div className="course-card" key={course.id}>
              <div>
                <div className="course-badge">Popular</div>
                <h2>{course.title}</h2>
                <p>{course.description}</p>
              </div>

              <Link to={`/courses/${course.id}`}>
                <button>Open Course</button>
              </Link>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

function CourseDetails() {
  const assignments = [
    {
      id: 1,
      title: "HTML Assignment",
      due: "May 25",
    },
    {
      id: 2,
      title: "CSS Project",
      due: "May 28",
    },
    {
      id: 3,
      title: "JavaScript Quiz",
      due: "June 1",
    },
  ];

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2>LMS</h2>

        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </nav>
      </aside>

      <main className="main-content">
        <div className="details-card">
          <div className="course-header">
            <div>
              <div className="course-badge">
                Active Course
              </div>

              <h1>Web Development</h1>

              <p>
                Learn frontend and backend development
                with real projects and assignments.
              </p>
            </div>

<Link to="/chat">
  <button>Join Chat</button>
</Link>
          </div>
        </div>

        <h2 className="section-title">
          Assignments
        </h2>

        <div className="assignment-grid">
          {assignments.map((assignment) => (
            <div
              className="assignment-card"
              key={assignment.id}
            >
              <h3>{assignment.title}</h3>

              <p>Due: {assignment.due}</p>

              <div className="assignment-buttons">
<Link to={`/assignment/${assignment.id}`}>
  <button>Open</button>
</Link>
<button
  onClick={() => alert("Assignment submitted successfully!")}
>
  Submit
</button>
              </div>
            </div>
          ))}
        </div>

        <h2 className="section-title">
          Course Progress
        </h2>

        <div className="progress-card">
          <div className="progress-bar">
            <div className="progress-fill"></div>
          </div>

          <p>75% completed</p>
        </div>
      </main>
    </div>
  );
}
function ChatPage() {
  const [messages, setMessages] = useState([
    {
      text: "Teacher: Welcome everyone 👋",
      user: false,
    },
    {
      text: "You: Hello!",
      user: true,
    },
  ]);

  const [newMessage, setNewMessage] = useState("");

  const sendMessage = () => {
    if (newMessage.trim() === "") return;

    setMessages([
      ...messages,
      {
        text: `You: ${newMessage}`,
        user: true,
      },
    ]);

    setNewMessage("");
  };

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2>LMS</h2>

        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </nav>
      </aside>

      <main className="main-content">
        <div className="details-card">
          <h1>Course Chat 💬</h1>

          <div className="chat-box">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.user ? "user" : ""}`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              placeholder="Write a message..."
              value={newMessage}
              onChange={(e) =>
                setNewMessage(e.target.value)
              }
            />

            <button onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
function AssignmentPage() {
  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2>LMS</h2>

        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </nav>
      </aside>

      <main className="main-content">
        <div className="details-card">
          <h1>Assignment 📄</h1>

          <p>
            Complete the assignment and submit your work.
          </p>

          <textarea
            className="assignment-textarea"
            placeholder="Write your answer..."
          ></textarea>

          <button style={{ marginTop: "20px" }}>
            Submit Assignment
          </button>
        </div>
      </main>
    </div>
  );
}


function App() {
  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
          font-family: Inter, sans-serif;
        }

        body {
          background: #020617;
          color: white;
        }

        a {
          text-decoration: none;
        }

        .auth-page {
          min-height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
          background:
            radial-gradient(circle at top left, #2563eb, transparent 30%),
            radial-gradient(circle at bottom right, #7c3aed, transparent 30%),
            #020617;
        }

        .glass-card {
          width: 420px;
          padding: 40px;
          border-radius: 28px;
          background: rgba(255,255,255,0.08);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255,255,255,0.1);
        }

        .glass-card h1 {
          font-size: 38px;
          margin-bottom: 10px;
        }

        .subtitle {
          color: #cbd5e1;
          margin-bottom: 30px;
        }

        form {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        input {
          padding: 16px;
          border-radius: 14px;
          border: none;
          background: rgba(255,255,255,0.1);
          color: white;
        }

        button {
          padding: 16px;
          border-radius: 14px;
          border: none;
          background: linear-gradient(135deg,#2563eb,#7c3aed);
          color: white;
          cursor: pointer;
          font-weight: bold;
        }

        .switch-text {
          margin-top: 20px;
          text-align: center;
          color: #cbd5e1;
        }

        .switch-text a {
          color: #60a5fa;
        }

        .dashboard-layout {
          display: flex;
          min-height: 100vh;
        }

        .sidebar {
          width: 240px;
          background: #0f172a;
          padding: 30px;
        }

        .sidebar h2 {
          font-size: 32px;
          margin-bottom: 40px;
        }

        .sidebar nav {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .sidebar a {
          color: #cbd5e1;
        }

        .main-content {
          flex: 1;
          padding: 50px;
        }

        .stats-grid,
        .courses-grid {
          display: grid;
          grid-template-columns: repeat(3,1fr);
          gap: 25px;
        }

        .stat-card,
        .course-card,
        .details-card {
          background: rgba(255,255,255,0.06);
          padding: 30px;
          border-radius: 24px;
        }

        .course-card {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }

        .course-badge {
          width: fit-content;
          padding: 8px 14px;
          border-radius: 999px;
          background: rgba(37,99,235,0.2);
          color: #60a5fa;
          margin-bottom: 20px;
        }

        .details-buttons {
          display: flex;
          gap: 20px;
          margin-top: 20px;
        }
          .course-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.section-title {
  margin: 40px 0 20px;
  font-size: 30px;
}

.assignment-grid {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 20px;
}

.assignment-card {
  background: rgba(255,255,255,0.06);
  padding: 25px;
  border-radius: 20px;
}

.assignment-card h3 {
  margin-bottom: 10px;
}

.assignment-card p {
  color: #cbd5e1;
  margin-bottom: 20px;
}

.assignment-buttons {
  display: flex;
  gap: 10px;
}

.progress-card {
  background: rgba(255,255,255,0.06);
  padding: 30px;
  border-radius: 20px;
}

.progress-bar {
  width: 100%;
  height: 18px;
  background: rgba(255,255,255,0.08);
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  width: 75%;
  height: 100%;
  background: linear-gradient(135deg,#2563eb,#7c3aed);
}
.chat-box {
  height: 300px;
  overflow-y: auto;
  margin: 30px 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  background: rgba(255,255,255,0.08);
  padding: 15px;
  border-radius: 14px;
  width: fit-content;
  max-width: 70%;
}

.user {
  align-self: flex-end;
  background: linear-gradient(135deg,#2563eb,#7c3aed);
}

.chat-input {
  display: flex;
  gap: 15px;
}

.chat-input input {
  flex: 1;
}

.assignment-textarea {
  width: 100%;
  height: 220px;
  margin-top: 30px;
  border-radius: 18px;
  padding: 20px;
  background: rgba(255,255,255,0.08);
  border: none;
  color: white;
  resize: none;
}
  .dashboard-sections {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 25px;
  margin-top: 40px;
}

.dashboard-card {
  background: rgba(255,255,255,0.06);
  padding: 30px;
  border-radius: 24px;
}

.dashboard-card h2 {
  margin-bottom: 25px;
}

.dashboard-item {
  background: rgba(255,255,255,0.05);
  padding: 18px;
  border-radius: 16px;
  margin-bottom: 15px;
}

.dashboard-item p {
  margin-top: 8px;
  color: #cbd5e1;
}
  .schedule-day {
  margin-bottom: 25px;
}

.schedule-day h3 {
  margin-bottom: 12px;
  color: #60a5fa;
}
      `}</style>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:id" element={<CourseDetails />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/assignment/:id" element={<AssignmentPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;