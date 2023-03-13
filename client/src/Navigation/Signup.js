import React from "react";
import Navbar from "./Navbar";
import { useNavigate } from "react-router-dom";
import "./login_css.css"

// import FlashMessage from 'react-flash-message'

// fetch('http://localhost:9999/signup', {
//     method: 'POST',
//       headers: {
//           'Accept': 'application/json',
//           'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ "author_name" : author_name, "email" : email, 'password':password, 'reviewer_role' : reviewer_role })
//   })

const Signup = () => {
  const navigate = useNavigate();

  // function handleClick() {
  //   navigate("/login");
  // }

  // const[author_name,setAuthorname] = useState('');
  // const[email,setemail] = useState('');
  // const[password,setpassword] = useState('');
  // const[reviewer_role,setreviewer_role] = useState('');

  // const handleauthor_nameChange = event => {
  //   setAuthorname(event.target.value);
  // };
  // const handleemailChange = event => {
  //   setemail(event.target.value);
  // };
  // const handlepasswordChange = event => {
  //   setpassword(event.target.value);
  // };
  // const handlereviewer_roleChange = event => {
  //   setreviewer_role(event.target.value);
  // };

  // const getData = () => {
  //   fetch('http://localhost:9999/signup', {
  //   method: 'POST',
  //     headers: {
  //         'Accept': 'application/json',
  //         // 'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({ "author_name" : author_name, "email" : email, 'password':password, 'reviewer_role' : reviewer_role })
  // })
  // .then(response => response.json())
  // .then(response => console.log(JSON.stringify(response)))
  // }

  return (
    <>
      <Navbar />

      <div class="adcontent">
        <form action="http://localhost:9999/signup" method="post">
          <div class="headname">
            <h1>SIGN UP</h1>
          </div>

          <div class="field">
            <label for="author_name">Username</label>
            <input id="author_name" type="text" name="author_name" required />
          </div>
          <div class="field">
            <label for="email">Email</label>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input id="email" type="text" name="email" required />
          </div>
          <div class="field">
            <label for="password">Password</label>&nbsp;&nbsp;
            <input id="password" type="password" name="password" />
          </div>

          <div class="radio2">
            <p>
              Reviewer role:&nbsp;&nbsp;
              <input
                type="radio"
                id="reviewer_role"
                name="reviewer_role"
                value="Yes"
              />
              <label for="reviewer_role">Yes</label>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <input
                type="radio"
                id="reviewer_role"
                name="reviewer_role"
                value="No"
              />
              <label for="reviewer_role">No</label>
            </p>
          </div>

          <div class="adbutton">
            <button type="submit" value="SIGN UP" >SIGN UP</button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Signup;
