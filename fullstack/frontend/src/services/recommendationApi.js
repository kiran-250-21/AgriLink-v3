import API from './api';

export const analyzeRecommendation = async (harvestId, quantity, maxRadius = null) => {
  const payload = { harvestId, quantity };
  if (maxRadius && maxRadius !== 'ALL') {
    payload.maxRadius = Number(maxRadius);
  }
  const response = await API.post('/recommendations/analyze', payload);
  return response.data;
};
