import api from './axios';

export const getJobs = async () => {
  return api.get('/jobs');
};
