import { NavLink } from "react-router-dom";
import { FaEdit, FaEye, FaPlusCircle, FaTrash, FaUser } from "react-icons/fa";
import "./dashboard_css.css";
import Button from "@material-ui/core/Button";
import { useState, useEffect } from 'react';
import getdata from "../services/test";
// import TextField from '@material-ui/core/TextField';
import React from 'react';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';


const Dashboard = () => {

  const [users, setUsers] = useState([])
  const [discourse, setdis] = useState([])
  const [autnam, setautnam] = useState([])
  const [counts, setcounts] = useState([])
  let counter = 0;

  let counter2 = 0;


  useEffect(() => {
    Promise.all([
      fetch('http://localhost:9999/dash_data'),
      fetch('http://localhost:9999/authName'),
      fetch('http://localhost:9999/about'),
    ])
      .then(([resUsers, resAut, resabout]) =>
        Promise.all([resUsers.json(), resAut.json(), resabout.json()])
      )
      .then(([dataUsers, dataAuth, dataCount]) => {
        setUsers(dataUsers);
        setautnam(dataAuth);
        setcounts(dataCount);
      });
  }, []);

  async function getdatavalues() {
    const response = await getdata()
    if (response.status === 200) {
      setdis(response.data)
    }
  }
  function refreshPage() {
    window.location.reload(false);
  }
  // console.log(users.discourse_count)

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
                <FaUser></FaUser> Username : {autnam.author_name}
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
          <div id="card">{counts.discourse_count} Discourses created</div>
          <div id="card">{counts.usr_count} USRs Generated</div>
          <div id="card">4 Discourses Approved</div>
          <div id="card">
            <a href="http://localhost:3000/usrgenerate">
              <FaPlusCircle size="50px" color="black"></FaPlusCircle>
            </a>
          </div>
        </div>
        {/* <div>
          <button onClick={refreshPage}>Click to reload!</button>
        </div> */}

        {/* <div class="discourse_but">
          <Button variant="contained" href="http://localhost:9999/dash_out">
            See Discourses
          </Button>
        </div> */}
        <div class="dis_table">
          <div class="dis_table_row1">
            <div class="dis_table_col">
              S.No
            </div>
            <div class="dis_table_col">
              Discourse
            </div>
            <div class="dis_table_col">
              USRs
            </div>
            <div class="dis_table_col">
              Actions
            </div>
            <div class="dis_table_col">
              Status
            </div>
          </div>

          {users.length > 0 && (
            <ol>
              {users.map(user => (
                <div class="dis_table_row">
                  <div class="dis_table_col">{counter += 1}</div>
                  {/* <div class="dis_table_col">{this.setState(({ length }) => ({ length: length + 1 }));}</div> */}
                  <div class="dis_table_col">{user.sentences}</div>
                  <div class="dis_table_col">
                    <Popup trigger=
                      {<a className="usr_a"> USR {counter2 += 1} </a>}
                      modal nested>
                      {
                        close => (
                          <div className='modal'>
                            <div className='content'>
                              {user.orignal_USR_json}
                            </div>
                            <div>
                              <button onClick=
                                {() => close()}>
                                Close
                              </button>
                            </div>
                          </div>
                        )
                      }
                    </Popup>
                  </div>
                  <div class="dis_table_col">
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
                    <button class="but">
                      <a href="http://localhost:3000/usrgenerate">
                        <FaTrash id="action_button" size="30px" color="black"></FaTrash>
                      </a>
                    </button>
                  </div>
                  <div class="dis_table_col">Approved</div>

                </div>
              ))}
            </ol>
          )}
        </div>
      </div>
    </>

  );
};
export default Dashboard;
