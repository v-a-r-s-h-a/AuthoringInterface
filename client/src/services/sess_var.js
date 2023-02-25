import axios from "axios";
async function getdata() {
    const response = await axios.get("http://localhost:9999/about")
    console.log(response)
    return response
}
export default getdata;