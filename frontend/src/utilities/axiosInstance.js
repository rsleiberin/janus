import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // Replace with your Flask API's URL
    // You can add more default settings here, like headers
});

export default axiosInstance;
