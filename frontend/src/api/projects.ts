import api from './axios';

export const getProjects = async () => {
  return api.get('/projects');
};
