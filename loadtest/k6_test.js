import http from 'k6/http';
export const options = { vus: 200, duration: '2m' };
export default function () {
  const res = http.get('http://app:8000/api/books', { headers: { 'X-User': 'loadtest' }});
}
