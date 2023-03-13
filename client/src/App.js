import React from "react";
import Home from "./Navigation/Home";
import About from "./Navigation/About";
import Dashboard from "./Navigation/Dashboard";
import ContactUs from "./Navigation/ContactUs";
import Login from "./Navigation/Login";
import USRgenerate from "./USRgenerationFolder/USRgenerate";
import SignUp from "./Navigation/Signup";
import Sentences from "./USRgenerationFolder/Sentences";
import USR from "./USRgenerationFolder/USR";
import { Routes, Route } from "react-router-dom";
import Logout from "./Navigation/Logout";
import componentB from "./Navigation/componentB";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<ContactUs />} />
      <Route path="/login" element={<Login />} />
      <Route path="/logout" element={<Logout />} />
      <Route path="/usrgenerate" element={<USRgenerate />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/componentB" element={<componentB />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/sentences/" element={<Sentences />} />
      <Route path="/usr/" element={<USR />} />
    </Routes>

  );
}

export default App;
