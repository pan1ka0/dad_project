import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function Login() {
  return (
    <div className="page">
      <div className="card">
        <h1>Login</h1>

        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />

        <button>Login</button>

        <p>
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}

function Register() {
  return (
    <div className="page">
      <div className="card">
        <h1>Register</h1>

        <input type="text" placeholder="Name" />
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />

        <button>Create Account</button>

        <p>
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="dashboard">
      <nav className="navbar">
        <h2>LMS System</h2>

        <div>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </div>
      </nav>

      <div className="content">
        <h1>Dashboard</h1>

        <div className="cards">
          <div className="info-card">
            <h3>Courses</h3>
            <p>12</p>
          </div>

          <div className="info-card">
            <h3>Assignments</h3>
            <p>8</p>
          </div>

          <div className="info-card">
            <h3>Grades</h3>
            <p>5</p>
          </div>
        </div>
      </div>
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
    <div className="dashboard">
      <nav className="navbar">
        <h2>LMS System</h2>

        <div>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/courses">Courses</Link>
        </div>
      </nav>

      <div className="content">
        <h1>Courses</h1>

        <div className="course-grid">
          {fakeCourses.map((course) => (
            <div className="course-card" key={course.id}>
              <h2>{course.title}</h2>

              <p>{course.description}</p>

              <button>Open Course</button>
            </div>
          ))}
        </div>
      </div>
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
          font-family: Arial;
        }

        body {
          background: #f3f4f6;
        }

        a {
          text-decoration: none;
          color: white;
          margin-left: 20px;
        }

        .page {
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .card {
          width: 400px;
          background: white;
          padding: 40px;
          border-radius: 20px;
          box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .card h1 {
          margin-bottom: 30px;
          text-align: center;
        }

        .card input {
          width: 100%;
          padding: 15px;
          margin-bottom: 15px;
          border: 1px solid #ccc;
          border-radius: 10px;
        }

        .card button {
          width: 100%;
          padding: 15px;
          border: none;
          background: #2563eb;
          color: white;
          border-radius: 10px;
          cursor: pointer;
          font-size: 16px;
        }

        .card p {
          margin-top: 20px;
          text-align: center;
        }

        .card p a {
          color: #2563eb;
          margin-left: 5px;
        }

        .navbar {
          background: #111827;
          color: white;
          padding: 20px 40px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .content {
          padding: 40px;
        }

        .content h1 {
          margin-bottom: 30px;
        }

        .cards {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 20px;
        }

        .info-card {
          background: white;
          padding: 30px;
          border-radius: 20px;
          box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        .info-card h3 {
          margin-bottom: 15px;
        }

        .info-card p {
          font-size: 35px;
          font-weight: bold;
        }

        .course-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 20px;
        }

        .course-card {
          background: white;
          padding: 25px;
          border-radius: 20px;
          box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        .course-card h2 {
          margin-bottom: 10px;
        }

        .course-card p {
          color: gray;
          margin-bottom: 20px;
        }

        .course-card button {
          padding: 12px 20px;
          background: #2563eb;
          color: white;
          border: none;
          border-radius: 10px;
          cursor: pointer;
        }
      `}</style>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/courses" element={<Courses />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;