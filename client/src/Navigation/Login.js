import React from "react";
import "./style.css";
import { NavLink } from "react-router-dom";
import Navbar from "./Navbar";
import { useNavigate } from "react-router-dom";
import "./login_css.css"

const Login = () => {
  const navigate = useNavigate();
  return (
    <>
      <Navbar />

      <div class="adcontent">
        <form action="http://localhost:9999/login" method="post">
          <div class="headname">
            <h1>LOGIN</h1>
          </div>
          <div class="field">
            <label for="email">Email</label>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="text" name="email" id="email" required />
          </div>

          <div class="field">
            <label for="password">Password</label>
            <input type="password" name="password" id="password" />
          </div>

          <div class="radio">
            <input type="radio" id="author" name="r1" />
            <label for="author">Author</label>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="radio" id="reviewer" name="r1" />
            <label for="reviewer">Reviewer</label>
          </div>

          <div class="adbutton">
            <input type="submit" value="LOG IN" />
          </div>
        </form>

        <p>
          Don't have any account?<NavLink to="/signup">SIGN UP</NavLink>
        </p>
        <br />
        <br />
      </div>
    </>
  );
};

export default Login;
