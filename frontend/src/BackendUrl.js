const host = process.env.NODE_ENV === 'production' && process.env.REACT_APP_BACKEND_URL ? process.env.REACT_APP_BACKEND_URL : 'http://localhost';
const port = process.env.NODE_ENV === 'production' ? 8000 : 3000;

let url = `${host}:${port}`
console.log("Using backend URL", url)

export default url
