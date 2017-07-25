import axios from 'axios';
import cookies from 'cookiesjs';

export const http = axios.create({
  headers: { 'X-CSRFToken': cookies('csrftoken') },
});

export const getAccountInfo = () => http.get('/api/account');
