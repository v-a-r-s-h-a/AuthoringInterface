import React, { useEffect, useState } from "react";
import axios from "axios";
const Sentences = () => {
  const [value_in_array, setValueInArray] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      // client\public\updatedSentence.txt
      const response = await axios.get(
        "http://localhost:3000/updatedSentence.txt"
      );
      let value = await response.data;
      let value_in_array = value.split("\n");
      setValueInArray(value_in_array);
    };
    fetchData();
  }, []);

  // const text = value;
  // const obj = JSON.parse(text);
  // console.log(obj.sentences)

  const handleClick = (index) => {
    setTimeout(() => {
      window.parent.postMessage(index, "*");
    }, 500);
    console.log(index);
  };
  // const getData=() =>{

  // }
  return (
    <div>
      {value_in_array.map((item, index) => (
        <p key={index} onClick={(event) => handleClick(index)}>
          {item}
        </p>
      ))}
    </div>
  );
};
export default Sentences;
