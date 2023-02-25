import axios from "axios";
async function getdata() {
    const response = await axios.get("http://localhost:9999/discourse")
    // console.log(response)
    return response
}
export default getdata;