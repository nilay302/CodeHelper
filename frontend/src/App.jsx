import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
import './App.css';
import Login from "./Pages/Login"
function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route exact path = "/" element={<Login/>} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
