import { NavLink } from "react-router-dom";
import { FaEdit, FaEye, FaPlusCircle, FaTrash, FaUser } from "react-icons/fa";
import "./dashboard_css.css";
import Button from "@material-ui/core/Button";
// import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import { useState, useEffect } from 'react';
// import getdata from "../services/test";
// import TextField from '@material-ui/core/TextField';
import React from 'react';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { Link, useNavigate } from 'react-router-dom';
import ComponentB from "./componentB";
// import { Pages } from "@material-ui/icons";



const Dashboard = () => {

  const [users, setUsers] = useState([])
  const [discourse, setdis] = useState([])
  const [usr, setusr] = useState([])
  const [autnam, setautnam] = useState([])
  const [counts, setcounts] = useState([])

  let counter = 0;

  var counter2 = 0;

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:9999/dash_data'),
      fetch('http://localhost:9999/uni_discourse'),
      fetch('http://localhost:9999/USR'),
      fetch('http://localhost:9999/authName'),
      fetch('http://localhost:9999/about'),
    ])
      .then(([resUsers, resdis, resusr, resAut, resabout]) =>
        Promise.all([resUsers.json(), resdis.json(), resusr.json(), resAut.json(), resabout.json()])
      )
      .then(([dataUsers, datadis, datausr, dataAuth, dataCount]) => {
        setUsers(dataUsers);
        setdis(datadis);
        setusr(datausr);
        setautnam(dataAuth);
        setcounts(dataCount);
      });
  }, []);


  // async function getdatavalues() {
  //   const response = await getdata()
  //   if (response.status === 200) {
  //     setdis(response.data)
  //   }
  // }
  // function refreshPage() {
  //   window.location.reload(false);
  // }
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
                <FaUser></FaUser> {autnam.author_name}
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

      {/* <div class="truncated"><a href="#">kaj  askdfj ;askdf;askdfj ksadf ;asjdf ;ksad fsadjf ;kasd fa;sfjd ;ksadf;sad;fkl jsa;kfd;askdjf aksjd f;sajdf ;as aksjd;f as;dfkj as;kfdj a;sfaksaj d;fkasdf;asjfd ;sad  asdk</a></div> */}

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

          {discourse.length > 0 && (
            <ol>
              {discourse.map(dis => (
                <div class="dis_table_row">
                  <div class="dis_table_col">{counter += 1}</div>
                  <div class="dis_table_col">
                    <div class="expanded-text">
                      {dis.sentences.length > 50
                        ? <div class="short-name">{dis.sentences.substring(0, 50)}...</div>
                        : <div class="short-name">{dis.sentences}</div>
                      }
                      <div class="longer-name">{dis.sentences}</div>
                    </div>
                  </div>

                  <div class="dis_table_col">
                    {users.length > 0 && (
                      <ul>
                        {counter2 = 0}
                        {users.map(user => {
                          return user.discourse_id === dis.discourse_id ? (
                            <div class="usr_buttons">
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
                          ) : (
                            <h2></h2>
                          );
                        })}
                      </ul>
                    )}
                  </div>
                  <div class="dis_table_col">
                    <button class="but">
                      <a href="http://localhost:3000/componentB">
                        <div>
                          <componentB data={dis.sentences} />
                        </div>
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
                  <div class="dis_table_col">{dis.USR_status}</div>
                </div>
              ))}
            </ol>
          )}
        </div>
      </div >
      {/* <Stack spacing={2}>
        <Pagination count={10} showFirstButton showLastButton />
      </Stack> */}
    </>

  );
};
export default Dashboard;
