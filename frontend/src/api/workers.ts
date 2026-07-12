import api from './axios';

export const getWorkers = async () => {
  return api.get('/workers');
};
