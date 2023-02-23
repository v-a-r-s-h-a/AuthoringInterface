import React, { useEffect, useState } from "react";
import "./usr.css";
//import cjson from 'cjson';

const USR = () => {
  const [index, setIndex] = useState(0);
  const [selectedData, setSelectedData] = useState({});
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(false);

  let finalJson;

  const handleChange = (event, key, index) => {
    const newSelectedData = { ...selectedData };
    newSelectedData[key][index] = event.target.value;
    setSelectedData(newSelectedData);
    console.log(newSelectedData);
  };

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const receivedIndex = searchParams.get("receivedindex") || 0;
    setIndex(receivedIndex ? receivedIndex : 0);
    const result = require("http://localhost:9999/USR");
    setSelectedData(result[index]);
    setLoading(false);
    finalJson = result;
  }, [index, selectedData]);

  const viewTable = () => {
    setShowTable(true);
  };
  const saveChanges = () => {
    console.log(finalJson);
    /*cjson.write('../data/data.json', finalJson, { spaces: 2 }, function(error) {
      if (error) {
        console.error(error);
      } else {
        console.log('Data written to file.json');
      }
    });*/
  };

  return loading ? (
    <div>Loading...</div>
  ) : (
    <>
      <input
        type="submit"
        className="usrEditButton"
        onClick={viewTable}
        value="Edit"
      />
      <input
        type="submit"
        className="usrEditButton"
        onClick={saveChanges}
        value="Save"
      />
      {showTable && selectedData ? (
        <form>
          <table>
            <tr>
              <div className="headerdiv">
                <th>Concept</th>
              </div>
              {selectedData.Concept.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) => handleChange(event, "Concept", i)}
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Index</th>
              </div>
              {selectedData.Index.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) => handleChange(event, "Index", i)}
                        disabled="True"
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Sem. Cat</th>
              </div>
              {selectedData.SemCateOfNouns.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) =>
                          handleChange(event, "SemCateOfNouns", i)
                        }
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>G-N-P</th>
              </div>
              {selectedData.GNP.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) => handleChange(event, "GNP", i)}
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Dep-Rel</th>
              </div>
              {selectedData.DepRel.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) => handleChange(event, "DepRel", i)}
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Discourse</th>
              </div>
              {selectedData.Discourse.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) =>
                          handleChange(event, "Discourse", i)
                        }
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Speaker's View</th>
              </div>
              {selectedData.SpeakersView.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) =>
                          handleChange(event, "SpeakersView", i)
                        }
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Scope</th>
              </div>
              {selectedData.Scope.map((item, i) => {
                return (
                  <td>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) => handleChange(event, "Scope", i)}
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
            <tr>
              <div className="headerdiv">
                <th>Sentence Type</th>
              </div>
              {selectedData.SentenceType.map((item, i) => {
                return (
                  <td colSpan={selectedData.Concept.length}>
                    <div className="headerdiv2">
                      <input
                        type="text"
                        value={item}
                        onChange={(event) =>
                          handleChange(event, "SentenceType", i)
                        }
                      />
                    </div>
                  </td>
                );
              })}
            </tr>
          </table>
        </form>
      ) : (
        <table>
          <tr>
            <div className="headerdiv">
              <th>Concept</th>
            </div>
            {selectedData.Concept.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Index</th>
            </div>
            {selectedData.Index.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Sem. Cat</th>
            </div>
            {selectedData.SemCateOfNouns.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>G-N-P</th>
            </div>
            {selectedData.GNP.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Dep-Rel</th>
            </div>
            {selectedData.DepRel.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Discourse</th>
            </div>
            {selectedData.Discourse.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Speaker's View</th>
            </div>
            {selectedData.SpeakersView.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Scope</th>
            </div>
            {selectedData.Scope.map((item, i) => {
              return (
                <td>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
          <tr>
            <div className="headerdiv">
              <th>Sentence Type</th>
            </div>
            {selectedData.SentenceType.map((item, i) => {
              return (
                <td colSpan={selectedData.Concept.length}>
                  <div className="headerdiv2">{item}</div>
                </td>
              );
            })}
          </tr>
        </table>
      )}
    </>
  );
};

export default USR;
