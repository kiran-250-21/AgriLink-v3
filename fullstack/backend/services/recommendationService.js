const Harvest = require('../models/Harvest');
const Market = require('../models/Market');
const MarketPrice = require('../models/MarketPrice');
const BuyerRequirement = require('../models/BuyerRequirement');
const Recommendation = require('../models/Recommendation');
const { calculateNetRevenue, calculateDistanceKm, resolveCoordinates } = require('../utils/calculations');

/**
 * AgriLink Core Recommendation Engine
 * Analyzes market prices and buyer offers for a specific harvest,
 * subtracts estimated logistics costs, and ranks options by Estimated Net Revenue.
 */
const analyzeHarvestOptions = async (harvestId, requestedQuantity, maxRadius = null) => {
  const harvest = await Harvest.findById(harvestId);
  if (!harvest) throw new Error('Harvest not found');

  const parsedMaxRadius = (maxRadius && !isNaN(Number(maxRadius))) ? Number(maxRadius) : null;
  const qty = Number(requestedQuantity) || harvest.availableQuantity;
  const farmLoc = harvest.farmLocation || 'Guntur';
  let farmCoords = (harvest.latitude != null && harvest.longitude != null)
    ? { lat: harvest.latitude, lng: harvest.longitude }
    : resolveCoordinates(farmLoc);

  // Automatically cache resolved coordinates to harvest document
  if ((harvest.latitude == null || harvest.longitude == null) && farmCoords) {
    Harvest.updateOne({ _id: harvest._id }, { latitude: farmCoords.lat, longitude: farmCoords.lng }).catch(() => { });
  }

  const crop = harvest.cropName;

  const options = [];

  // Extract base English name (before any parentheses) for flexible matching
  const baseCrop = crop.split('(')[0].trim();
  const escapedFull = crop.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapedBase = baseCrop.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Flexible matching for both full Telugu-bracketed string and base English crop name
  const cropFilter = {
    $or: [
      { crop: new RegExp(`^${escapedFull}$`, 'i') },
      { crop: new RegExp(`^${escapedBase}$`, 'i') },
      { crop: new RegExp(escapedBase, 'i') },
    ],
  };

  // 1. Fetch official Market Prices for this crop
  const marketPrices = await MarketPrice.find(cropFilter).populate('marketId');

  for (const mp of marketPrices) {
    if (mp.marketId && mp.marketId.active) {
      const destCoords = (mp.marketId.latitude != null && mp.marketId.longitude != null)
        ? { lat: mp.marketId.latitude, lng: mp.marketId.longitude }
        : null;
      const distance = calculateDistanceKm(farmLoc, mp.marketId.location, farmCoords, destCoords);
      if (parsedMaxRadius && distance > parsedMaxRadius) {
        continue; // Prune mandis beyond requested operational radius
      }
      const metrics = calculateNetRevenue(mp.pricePerUnit, qty, distance);

      options.push({
        destinationName: mp.marketId.name,
        destinationType: 'MARKET',
        marketId: mp.marketId._id,
        location: mp.marketId.location,
        sellingPrice: mp.pricePerUnit,
        grossRevenue: metrics.grossRevenue,
        estimatedLogisticsCost: metrics.estimatedLogisticsCost,
        estimatedNetRevenue: metrics.estimatedNetRevenue,
        distanceKm: distance,
      });
    }
  }

  // Also include all active markets with regional pricing if not already included
  const existingMarketIds = options.map(o => o.marketId ? o.marketId.toString() : '');
  const allMarkets = await Market.find({ active: true });

  for (const m of allMarkets) {
    if (!existingMarketIds.includes(m._id.toString())) {
      const destCoords = (m.latitude != null && m.longitude != null)
        ? { lat: m.latitude, lng: m.longitude }
        : null;
      const distance = calculateDistanceKm(farmLoc, m.location, farmCoords, destCoords);
      if (parsedMaxRadius && distance > parsedMaxRadius) {
        continue; // Prune regional mandis beyond requested operational radius
      }
      // Dynamic fallback base price based on Andhra Pradesh market benchmarks
      let fallbackPrice = 50;
      if (/dry chilli|dry chili|endu mirchi/i.test(crop)) fallbackPrice = 210;
      else if (/chilli|chili|mirchi/i.test(crop)) fallbackPrice = 180;
      else if (/turmeric|pasupu/i.test(crop)) fallbackPrice = 120;
      else if (/cotton|patti/i.test(crop)) fallbackPrice = 75;
      else if (/paddy|rice|vari/i.test(crop)) fallbackPrice = 32;
      else if (/maize|corn|mokka jonna/i.test(crop)) fallbackPrice = 24;
      else if (/groundnut|peanut|verusenaga/i.test(crop)) fallbackPrice = 65;
      else if (/bengal gram|chickpea|senagalu/i.test(crop)) fallbackPrice = 58;
      else if (/red gram|arhar|toor|kandulu/i.test(crop)) fallbackPrice = 85;
      else if (/black gram|urad|minumulu/i.test(crop)) fallbackPrice = 78;
      else if (/green gram|moong|pesalu/i.test(crop)) fallbackPrice = 80;
      else if (/mango|mamidi/i.test(crop)) fallbackPrice = 45;
      else if (/banana|arati/i.test(crop)) fallbackPrice = 22;
      else if (/sweet orange|mosambi|batthayi/i.test(crop)) fallbackPrice = 40;
      else if (/tomato/i.test(crop)) fallbackPrice = 28;
      else if (/onion|ullipaya/i.test(crop)) fallbackPrice = 35;
      else if (/tobacco|pogaku/i.test(crop)) fallbackPrice = 160;
      else if (/sugarcane|cheraku/i.test(crop)) fallbackPrice = 4;
      else if (/jowar|sorghum|jonnalu/i.test(crop)) fallbackPrice = 30;
      else if (/bajra|pearl millet|sajjalu/i.test(crop)) fallbackPrice = 26;
      else if (/sunflower|podduthirugudu/i.test(crop)) fallbackPrice = 52;
      else if (/castor|aamudamu/i.test(crop)) fallbackPrice = 56;
      else if (/oil palm/i.test(crop)) fallbackPrice = 15;

      const metrics = calculateNetRevenue(fallbackPrice, qty, distance);

      options.push({
        destinationName: m.name,
        destinationType: 'MARKET',
        marketId: m._id,
        location: m.location,
        sellingPrice: fallbackPrice,
        grossRevenue: metrics.grossRevenue,
        estimatedLogisticsCost: metrics.estimatedLogisticsCost,
        estimatedNetRevenue: metrics.estimatedNetRevenue,
        distanceKm: distance,
      });
    }
  }

  // 2. Fetch active Buyer Requirements for this crop (flexible matching)
  const buyerReqs = await BuyerRequirement.find({
    ...cropFilter,
    status: 'ACTIVE',
    validUntil: { $gte: new Date() },
  }).populate('buyerId', 'name buyerProfile status');

  for (const br of buyerReqs) {
    if (br.buyerId && br.buyerId.status === 'ACTIVE') {
      const buyerLoc = br.location || br.buyerId.buyerProfile?.businessLocation || 'Vijayawada';
      const buyerCoords = resolveCoordinates(buyerLoc);
      const distance = calculateDistanceKm(farmLoc, buyerLoc, farmCoords, buyerCoords);
      if (parsedMaxRadius && distance > parsedMaxRadius) {
        continue; // Prune buyer requirements beyond requested operational radius
      }
      const metrics = calculateNetRevenue(br.offeredPrice, qty, distance);
      const buyerName = br.buyerId.buyerProfile?.businessName || br.buyerId.name || 'Verified Buyer';

      options.push({
        destinationName: `Buyer: ${buyerName}`,
        destinationType: 'BUYER',
        buyerId: br.buyerId._id,
        requirementId: br._id,
        location: buyerLoc,
        sellingPrice: br.offeredPrice,
        grossRevenue: metrics.grossRevenue,
        estimatedLogisticsCost: metrics.estimatedLogisticsCost,
        estimatedNetRevenue: metrics.estimatedNetRevenue,
        distanceKm: distance,
      });
    }
  }

  // 3. Sort options DESCENDING by Estimated Net Revenue
  options.sort((a, b) => b.estimatedNetRevenue - a.estimatedNetRevenue);

  // Assign ranks and recommendation flags
  const rankedOptions = options.map((opt, index) => ({
    ...opt,
    rank: index + 1,
    isRecommended: index === 0,
  }));

  const bestOption = rankedOptions.length > 0 ? rankedOptions[0] : null;

  // Persist Recommendation in database
  const recommendationDoc = await Recommendation.create({
    harvestId: harvest._id,
    farmerId: harvest.farmerId,
    quantityAnalyzed: qty,
    recommendedOption: bestOption,
    allOptions: rankedOptions,
  });

  return {
    harvest: {
      id: harvest._id,
      cropName: harvest.cropName,
      availableQuantity: harvest.availableQuantity,
      farmLocation: harvest.farmLocation,
      quality: harvest.quality,
    },
    quantityAnalyzed: qty,
    recommendedOption: bestOption,
    allOptions: rankedOptions,
    recommendationId: recommendationDoc._id,
  };
};

module.exports = { analyzeHarvestOptions };
