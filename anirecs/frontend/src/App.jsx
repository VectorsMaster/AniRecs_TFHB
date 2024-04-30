import "./App.css";
import SignIn from "./SignIn";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SingUp from "./SingUp";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import PrivateRoute from "./PrivateRoute";
import Home from "./Home";
import Recommendations from "./Recommendations";
import History from "./History";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<SignIn />}/>
          <Route path="/signup" element={<SingUp />}/>
          <Route element={<PrivateRoute />}>
            <Route path="/" element={<Home />}></Route>
            <Route path="/history" element={<History />}></Route>
            <Route path="/recommend" element={<Recommendations />}></Route>
          </Route>
        </Routes>
      </BrowserRouter>
      <ToastContainer position="bottom-right"/>
    </div>
  );
}

export default App;
