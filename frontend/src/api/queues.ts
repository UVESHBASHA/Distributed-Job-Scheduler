import api from './axios';

export const getQueues = async () => {
  return api.get('/queues');
};
