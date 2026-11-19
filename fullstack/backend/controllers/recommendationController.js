const { analyzeHarvestOptions } = require('../services/recommendationService');

// @desc    Analyze market prices & buyer offers for a harvest, calculating Estimated Net Revenue
// @route   POST /api/recommendations/analyze
// @access  Private (Farmer or Admin)
const analyzeRecommendation = async (req, res) => {
  try {
    const { harvestId, quantity, maxRadius } = req.body;

    if (!harvestId) {
      return res.status(400).json({ message: 'harvestId is required' });
    }

    const result = await analyzeHarvestOptions(harvestId, quantity, maxRadius);
    res.json(result);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  analyzeRecommendation,
};
