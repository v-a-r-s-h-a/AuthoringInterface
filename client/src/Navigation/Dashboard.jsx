import { NavLink } from "react-router-dom";
import { FaEdit, FaEye, FaPlusCircle, FaTrash, FaUser } from "react-icons/fa";
import "./dashboard_css.css";
import Button from "@material-ui/core/Button";
import { useState, useEffect } from 'react';


const Dashboard = () => {

  const [users, setUsers] = useState([])



  // const allMessages = ["{'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}", "{'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}", "{'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}", "{'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}"]
  // function showHint(index) {
  //   const messageBox = document.getElementById('messageBox')
  //   messageBox.textContent = allMessages[index]
  // }

  const fetchData = () => {
    fetch("http://localhost:9999/dash_data")
      .then(response => {
        return response.json()
      })
      .then(data => {
        setUsers(data)
      })
  }

  useEffect(() => {
    fetchData()
  }, [])

  function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
  }

  return (
    <>
      <nav>
        <NavLink to="/">
          <p>Authoring Interface</p>
        </NavLink>
        <div>
          <ul id="navbar">
            <li>
              <NavLink to="/dashboard">
                <FaUser></FaUser> Username :
                {/* {users.map(user => ({ user.author_id }))} */}
                {/* {session.get(author_id)} */}
              </NavLink>
            </li>
            <li>
              <Button variant="contained" href="http://localhost:9999/logout">
                Logout
              </Button>
            </li>
          </ul>
        </div>
      </nav>
      <div class="components">
        <div class="cards">
          <div id="card">5 Discourses created</div>
          <div id="card">25 USRs Generated</div>
          <div id="card">2 Discourses Approved</div>
          <div id="card">
            <a href="http://localhost:3000/usrgenerate">
              <FaPlusCircle size="50px" color="black"></FaPlusCircle>
            </a>
          </div>
        </div>

        <div class="discourse_but">
          <Button variant="contained" href="http://localhost:9999/dash_out">
            See Discourses
          </Button>
        </div>



        <div class="dis_table">
          <table>
            <tr>
              <th>S.No</th>
              <th>Discourse</th>
              <th>USRs</th>
              <th>Actions</th>
              <th>Status</th>
            </tr>

            {users.length > 0 && (
              <ol>
                {users.map(user => (
                  <tr>
                    <td>1</td>
                    <td>{user.sentences}</td>
                    <td>
                      <div class="popup" onclick="{myFunction()}">Click me!
                        <span class="popuptext" id="myPopup">{user.sentences}</span>
                      </div>
                    </td>
                    <td>{user.orignal_USR_json}</td>
                    <td>
                      <button class="but">
                        <a href="http://localhost:3000/usrgenerate">
                          <FaEye id="action_button" size="30px" color="black"></FaEye>
                        </a>
                      </button>
                      <button class="but">
                        <a href="http://localhost:3000/usrgenerate">
                          <FaEdit id="action_button" size="30px" color="black"></FaEdit>
                        </a>
                      </button>
                      <button>
                        <a href="http://localhost:3000/usrgenerate">
                          <FaTrash id="action_button" size="30px" color="black"></FaTrash>
                        </a>
                      </button>
                    </td>
                    <td>Approved</td>
                  </tr>
                ))}
              </ol>
            )}
          </table>
        </div>
      </div>
    </>

  );
};
export default Dashboard;
