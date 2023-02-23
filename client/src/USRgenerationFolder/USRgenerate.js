import React, { useState } from "react";
import Navbar from "../Navigation/Navbar";
const USRgenerate = () => {
  const [sentences, setMessage] = useState("");
  const [showIframe, setShowIframe] = useState(false);
  const [receivedIndex, setReceivedIndex] = useState("");
  window.addEventListener("message", receiveMessage, false);

  function receiveMessage(event) {
    if (typeof event.data === "object") {
      setReceivedIndex(event.data.data);
    } else {
      setReceivedIndex(event.data);
    }
    console.log(event.data);
  }

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const getData = () => {
    setShowIframe(true);
  };

  return (
    <>
      <Navbar />
      <form action="http://localhost:9999/usrgenerate" method="post">
        <p className="lab_discourse">Discourse</p>
        <div className="tta">
          <textarea
            id="sentences"
            name="sentences"
            type="text"
            onChange={handleMessageChange}
          ></textarea>
        </div>
        <div className="ttab">
          <div classname="label_discourse">
            <p>Enter discourse name:</p>
          </div>
          <input
            id="discourse_name"
            name="discourse_name"
            type="text"
            onChange={handleMessageChange}
          />
        </div>
        <div className="ttab2">
          <input
            type="submit"
            name="Save Sentences"
            value="Save discourse"
            disabled={!sentences}
            onClick={getData}
          />
        </div>
        <div className="ttab1">
          <input
            type="submit"
            name="Generate USR"
            value="USR Generate"
            disabled={!sentences}
            onClick={getData}
          />
        </div>
        <div style={{ display: showIframe ? "block" : "none" }}>
          <iframe
            className="outl"
            width="500"
            height="540"
            title="sentence"
            src="/sentences/"
          />
          <div className="usrtop">
            <iframe
              className="usr"
              width="994px"
              id="usr"
              height="540"
              title="usr"
              src={`/usr/?receivedindex=${receivedIndex}`}
            />{" "}
          </div>
        </div>
      </form>
    </>
  );
};

export default USRgenerate;
