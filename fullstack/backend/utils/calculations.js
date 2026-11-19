/**
 * AgriLink Financial & Logistics Calculation Utilities
 * Enhanced with Dynamic GPS Geolocation & Comprehensive Andhra Pradesh Spatial Engine
 */

const DEFAULT_ROAD_FACTOR = 1.22; // Realistic Indian highway road tortuosity multiplier (1.22x straight-line GPS)

// Comprehensive spatial coordinate registry for all 26 Andhra Pradesh districts, major mandals, and agricultural trade hubs
const COORDINATE_REGISTRY = {
  // --- North Coastal Andhra ---
  VISAKHAPATNAM: { lat: 17.6868, lng: 83.2185 },
  VIZAG: { lat: 17.6868, lng: 83.2185 },
  ANAKAPALLI: { lat: 17.6896, lng: 83.0033 },
  NARSIPATNAM: { lat: 17.6694, lng: 82.6105 },
  BHEEMUNIPATNAM: { lat: 17.8920, lng: 83.4530 },
  CHODAVARAM: { lat: 17.8285, lng: 82.9377 },
  YELLAMANCHILI: { lat: 17.5517, lng: 82.8596 },
  PADERU: { lat: 18.0833, lng: 82.6667 },
  ALLURI_SITHARAMA_RAJU: { lat: 18.0833, lng: 82.6667 },
  ARAKU: { lat: 18.3273, lng: 82.8775 },
  SRIKAKULAM: { lat: 18.2970, lng: 83.8967 },
  AMADALAVALASA: { lat: 18.4167, lng: 83.9000 },
  PALAKONDA: { lat: 18.6015, lng: 83.7562 },
  TEKKALI: { lat: 18.6144, lng: 84.2346 },
  SOMPETA: { lat: 18.9317, lng: 84.5878 },
  RAJAM: { lat: 18.4552, lng: 83.6601 },
  ICHCHAPURAM: { lat: 19.1158, lng: 84.6931 },
  VIZIANAGARAM: { lat: 18.1067, lng: 83.3956 },
  BOBBILI: { lat: 18.5723, lng: 83.3644 },
  PARVATHIPURAM: { lat: 18.7797, lng: 83.4287 },
  PARVATHIPURAM_MANYAM: { lat: 18.7797, lng: 83.4287 },
  SALUR: { lat: 18.5284, lng: 83.2131 },
  CHEEPURUPALLI: { lat: 18.3072, lng: 83.5658 },

  // --- Coastal Andhra (Godavari, Krishna, Guntur) ---
  KAKINADA: { lat: 16.9891, lng: 82.2475 },
  RAJAHMUNDRY: { lat: 17.0005, lng: 81.8040 },
  EAST_GODAVARI: { lat: 17.0005, lng: 81.8040 },
  TUNI: { lat: 17.3571, lng: 82.5489 },
  SAMALKOTA: { lat: 17.0519, lng: 82.1762 },
  PEDDAPURAM: { lat: 17.0782, lng: 82.1384 },
  PITHAPURAM: { lat: 17.1147, lng: 82.2573 },
  RAMACHANDRAPURAM: { lat: 16.8524, lng: 82.0227 },
  AMALAPURAM: { lat: 16.5787, lng: 82.0061 },
  KONASEEMA: { lat: 16.5787, lng: 82.0061 },
  RAVULAPALEM: { lat: 16.7505, lng: 81.8444 },
  MANDAPETA: { lat: 16.8667, lng: 81.9333 },
  RAZOLE: { lat: 16.4800, lng: 81.8333 },
  ELURU: { lat: 16.7107, lng: 81.0952 },
  WEST_GODAVARI: { lat: 16.5449, lng: 81.5212 },
  BHIMAVARAM: { lat: 16.5449, lng: 81.5212 },
  TADEPALLIGUDEM: { lat: 16.8143, lng: 81.5267 },
  TANUKU: { lat: 16.7570, lng: 81.6817 },
  PALAKOLLU: { lat: 16.5255, lng: 81.7336 },
  NARSAPUR: { lat: 16.4385, lng: 81.7011 },
  JANGAREDDYGUDEM: { lat: 17.1264, lng: 81.2954 },
  KOVVUR: { lat: 17.0139, lng: 81.7289 },
  VIJAYAWADA: { lat: 16.5062, lng: 80.6480 },
  NTR: { lat: 16.5062, lng: 80.6480 },
  KRISHNA: { lat: 16.1875, lng: 81.1389 },
  MACHILIPATNAM: { lat: 16.1875, lng: 81.1389 },
  GUDIVADA: { lat: 16.4316, lng: 80.9984 },
  NUZVID: { lat: 16.7904, lng: 80.8496 },
  TIRUVURU: { lat: 17.1147, lng: 80.6128 },
  MYLAVARAM: { lat: 16.7607, lng: 80.6386 },
  JAGGAYYAPETA: { lat: 16.8967, lng: 80.0984 },
  NANDIGAMA: { lat: 16.7692, lng: 80.2941 },
  VUYYURU: { lat: 16.3683, lng: 80.8464 },
  AVANIGADDA: { lat: 16.0207, lng: 80.9167 },
  GUNTUR: { lat: 16.3067, lng: 80.4365 },
  TENALI: { lat: 16.2437, lng: 80.6400 },
  MANGALAGIRI: { lat: 16.4326, lng: 80.5540 },
  PONNUR: { lat: 16.0658, lng: 80.5594 },
  BAPATLA: { lat: 15.9042, lng: 80.4674 },
  CHIRALA: { lat: 15.8246, lng: 80.3522 },
  REPALLE: { lat: 16.0200, lng: 80.8300 },
  PALNADU: { lat: 16.2354, lng: 80.0493 },
  NARASARAOPET: { lat: 16.2354, lng: 80.0493 },
  SATTENAPALLE: { lat: 16.3986, lng: 80.1475 },
  VINUKONDA: { lat: 16.0537, lng: 79.7428 },
  PIDUGURALLA: { lat: 16.4789, lng: 79.8897 },
  MACHERLA: { lat: 16.4800, lng: 79.3000 },
  CHILAKALURIPET: { lat: 16.0892, lng: 80.1672 },

  // --- South Coastal Andhra (Prakasam & Nellore) ---
  ONGOLE: { lat: 15.5057, lng: 80.0499 },
  PRAKASAM: { lat: 15.5057, lng: 80.0499 },
  MARKAPUR: { lat: 15.7356, lng: 79.2731 },
  GIDDALUR: { lat: 15.3789, lng: 78.9248 },
  KANIGIRI: { lat: 15.4057, lng: 79.5106 },
  KANDUKUR: { lat: 15.2152, lng: 79.9042 },
  PODILI: { lat: 15.6052, lng: 79.6083 },
  ADDANKI: { lat: 15.8117, lng: 79.9744 },
  DARSI: { lat: 15.7667, lng: 79.6833 },
  NELLORE: { lat: 14.4426, lng: 79.9865 },
  SPSR_NELLORE: { lat: 14.4426, lng: 79.9865 },
  KAVALI: { lat: 14.9132, lng: 79.9928 },
  GUDUR: { lat: 14.1463, lng: 79.8504 },
  VENKATAGIRI: { lat: 13.9634, lng: 79.5824 },
  SULLURPETA: { lat: 13.7008, lng: 80.0211 },
  ATMAKUR: { lat: 14.6167, lng: 79.6167 },
  NAIDUPETA: { lat: 13.9000, lng: 79.9000 },
  RAPUR: { lat: 14.2000, lng: 79.5333 },

  // --- Rayalaseema Region ---
  KURNOOL: { lat: 15.8281, lng: 78.0373 },
  NANDYAL: { lat: 15.4786, lng: 78.4836 },
  ADONI: { lat: 15.6322, lng: 77.2728 },
  YEMMIGANUR: { lat: 15.7667, lng: 77.4833 },
  DHONE: { lat: 15.4167, lng: 77.8667 },
  NANDIKOTKUR: { lat: 15.8667, lng: 78.2667 },
  ALLAGADDA: { lat: 15.1333, lng: 78.5167 },
  BANAGANAPALLE: { lat: 15.3167, lng: 78.2333 },
  PATTIKONDA: { lat: 15.4000, lng: 77.5000 },
  ANANTAPUR: { lat: 14.6819, lng: 77.6007 },
  ANANTAPURAMU: { lat: 14.6819, lng: 77.6007 },
  HINDUPUR: { lat: 13.8283, lng: 77.4919 },
  DHARMAVARAM: { lat: 14.4142, lng: 77.7126 },
  GUNTAKAL: { lat: 15.1700, lng: 77.3700 },
  TADIPATRI: { lat: 14.9100, lng: 78.0100 },
  SRI_SATHYA_SAI: { lat: 14.1652, lng: 77.8105 },
  PUTTAPARTHI: { lat: 14.1652, lng: 77.8105 },
  KADIRI: { lat: 14.1114, lng: 78.1611 },
  MADAKASIRA: { lat: 13.9333, lng: 77.2667 },
  KALYANDURG: { lat: 14.5500, lng: 77.1000 },
  RAYADURG: { lat: 14.7000, lng: 76.8667 },
  URAVAKONDA: { lat: 14.9500, lng: 77.2667 },
  KADAPA: { lat: 14.4673, lng: 78.8242 },
  CUDDAPAH: { lat: 14.4673, lng: 78.8242 },
  YSR: { lat: 14.4673, lng: 78.8242 },
  PRODDATUR: { lat: 14.7500, lng: 78.5500 },
  PULIVENDULA: { lat: 14.4167, lng: 78.2333 },
  JAMMALAMADUGU: { lat: 14.8500, lng: 78.3833 },
  ANNAMAYYA: { lat: 14.0560, lng: 78.7520 },
  RAYACHOTY: { lat: 14.0560, lng: 78.7520 },
  RAJAMPET: { lat: 14.1833, lng: 79.1667 },
  BADVEL: { lat: 14.7333, lng: 79.0500 },
  MYDUKUR: { lat: 14.7000, lng: 78.6833 },
  LAKKIREDDIPALLY: { lat: 14.1667, lng: 78.7000 },
  TENAKALLU: { lat: 13.8833, lng: 78.4167 },
  TIRUPATI: { lat: 13.6288, lng: 79.4192 },
  CHITTOOR: { lat: 13.2172, lng: 79.1003 },
  MADANAPALLE: { lat: 13.5560, lng: 78.5010 },
  PALAMANER: { lat: 13.2000, lng: 78.7500 },
  PUNGANUR: { lat: 13.3667, lng: 78.5833 },
  PUTTUR: { lat: 13.4428, lng: 79.5539 },
  SRIKALAHASTI: { lat: 13.7500, lng: 79.7000 },
  NAGARI: { lat: 13.3283, lng: 79.5878 },
  KUPPAM: { lat: 12.7500, lng: 78.3667 },
  BANGARUPALEM: { lat: 13.2000, lng: 78.9667 },

  // --- Major Border Trade Terminals ---
  HYDERABAD: { lat: 17.3850, lng: 78.4867 },
  BENGALURU: { lat: 12.9716, lng: 77.5946 },
  BANGALORE: { lat: 12.9716, lng: 77.5946 },
  CHENNAI: { lat: 13.0827, lng: 80.2707 },
};

// Common spelling variations, colloquial names, and historical aliases
const LOCATION_ALIASES = {
  VISHAKAPTNAM: 'VISAKHAPATNAM',
  VISHAKAPATNAM: 'VISAKHAPATNAM',
  VISHAKHAPATNAM: 'VISAKHAPATNAM',
  VISAKAPATNAM: 'VISAKHAPATNAM',
  VIZAG: 'VISAKHAPATNAM',
  WALTAIR: 'VISAKHAPATNAM',
  BEZAWADA: 'VIJAYAWADA',
  VIJAYWADA: 'VIJAYAWADA',
  VIJAYAWADA_CITY: 'VIJAYAWADA',
  KURNOL: 'KURNOOL',
  KURNOOLU: 'KURNOOL',
  ANANTPUR: 'ANANTAPUR',
  ANANTHAPUR: 'ANANTAPUR',
  ANANTHAPURAMU: 'ANANTAPUR',
  CUDDAPAH: 'KADAPA',
  YSR_KADAPA: 'KADAPA',
  KADAPA_CITY: 'KADAPA',
  RAJAHMUNDRI: 'RAJAHMUNDRY',
  RAJMUNDRY: 'RAJAHMUNDRY',
  RAJAHMAHENDRAVARAM: 'RAJAHMUNDRY',
  CHERALA: 'CHIRALA',
  MADANAPALLI: 'MADANAPALLE',
  BHEEMAVARAM: 'BHIMAVARAM',
  HINDUPURAM: 'HINDUPUR',
  NARASARAOPETA: 'NARASARAOPET',
  PRODDUTUR: 'PRODDATUR',
  TADEPALLIGUDAM: 'TADEPALLIGUDEM',
  MACHLIPATNAM: 'MACHILIPATNAM',
  BANDAR: 'MACHILIPATNAM',
  CHITTOORU: 'CHITTOOR',
  NELLORU: 'NELLORE',
  TIRUPATHI: 'TIRUPATI',
  SRIKAKULAMU: 'SRIKAKULAM',
};

// Multilingual dictionary for Telugu location names
const TELUGU_TO_CANONICAL = {
  'గుంటూరు': 'GUNTUR',
  'విజయవాడ': 'VIJAYAWADA',
  'కర్నూలు': 'KURNOOL',
  'తెనాలి': 'TENALI',
  'అనంతపురం': 'ANANTAPUR',
  'అనంతపురము': 'ANANTAPUR',
  'విశాఖపట్నం': 'VISAKHAPATNAM',
  'విశాఖ': 'VISAKHAPATNAM',
  'వైజాగ్': 'VISAKHAPATNAM',
  'తిరుపతి': 'TIRUPATI',
  'నెల్లూరు': 'NELLORE',
  'కడప': 'KADAPA',
  'ఒంగోలు': 'ONGOLE',
  'రాజమండ్రి': 'RAJAHMUNDRY',
  'రాజమహేంద్రవరం': 'RAJAHMUNDRY',
  'కాకినాడ': 'KAKINADA',
  'ఏలూరు': 'ELURU',
  'మచిలీపట్నం': 'MACHILIPATNAM',
  'చిత్తూరు': 'CHITTOOR',
  'నంద్యాల': 'NANDYAL',
  'బాపట్ల': 'BAPATLA',
  'చీరాల': 'CHIRALA',
  'పల్నాడు': 'PALNADU',
  'నరసరావుపేట': 'NARASARAOPET',
  'అనకాపల్లి': 'ANAKAPALLI',
  'కోనసీమ': 'KONASEEMA',
  'అమలాపురం': 'AMALAPURAM',
  'పుట్టపర్తి': 'PUTTAPARTHI',
  'శ్రీ సత్యసాయి': 'SRI_SATHYA_SAI',
  'కదిరి': 'KADIRI',
  'అన్నమయ్య': 'ANNAMAYYA',
  'రాయచోటి': 'RAYACHOTY',
  'ఆదోని': 'ADONI',
  'భీమవరం': 'BHIMAVARAM',
  'తాడేపల్లిగూడెం': 'TADEPALLIGUDEM',
  'మదనపల్లె': 'MADANAPALLE',
  'హిందూపురం': 'HINDUPUR',
  'ప్రొద్దుటూరు': 'PRODDATUR',
  'శ్రీకాకుళం': 'SRIKAKULAM',
  'విజయనగరం': 'VIZIANAGARAM',
  'హైదరాబాద్': 'HYDERABAD',
  'బెంగళూరు': 'BENGALURU',
  'చెన్నై': 'CHENNAI',
};

/**
 * Calculates Great-Circle (as-the-crow-flies) distance between two GPS coordinates using Haversine formula.
 */
const calculateHaversineKm = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

/**
 * Levenshtein distance string similarity helper for tolerant typo handling
 */
const levenshteinDistance = (a, b) => {
  const an = a ? a.length : 0;
  const bn = b ? b.length : 0;
  if (an === 0) return bn;
  if (bn === 0) return an;
  const matrix = Array(bn + 1).fill(0).map(() => Array(an + 1).fill(0));
  for (let i = 0; i <= an; i++) matrix[0][i] = i;
  for (let j = 0; j <= bn; j++) matrix[j][0] = j;
  for (let j = 1; j <= bn; j++) {
    for (let i = 1; i <= an; i++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1,
        matrix[j - 1][i] + 1,
        matrix[j - 1][i - 1] + cost
      );
    }
  }
  return matrix[bn][an];
};

/**
 * Normalizes location names (Telugu, English, market titles, buyer company names)
 * into a canonical AP district/market hub identifier using exact, alias, and fuzzy matching.
 */
const canonicalizeLocation = (name) => {
  if (!name || typeof name !== 'string') return '';
  const trimmed = name.trim();

  // 1. Check Telugu location dictionary
  for (const [teluguName, canonical] of Object.entries(TELUGU_TO_CANONICAL)) {
    if (trimmed.includes(teluguName)) {
      return canonical;
    }
  }

  // 2. Clean English words
  const clean = trimmed.toUpperCase().replace(/[^A-Z0-9]/g, ' ');
  const words = clean.split(/\s+/).filter(Boolean);
  const joined = words.join('_');

  // Direct alias dictionary check
  if (LOCATION_ALIASES[joined]) return LOCATION_ALIASES[joined];
  for (const w of words) {
    if (LOCATION_ALIASES[w]) return LOCATION_ALIASES[w];
  }

  // Direct word match against registry
  for (const w of words) {
    if (COORDINATE_REGISTRY[w]) return w;
  }

  // Substring search against registry keys
  for (const key of Object.keys(COORDINATE_REGISTRY)) {
    if (joined.includes(key) || words.includes(key)) {
      return key;
    }
  }

  // Fuzzy match against registry and aliases for typos (e.g., vishakaptnam -> VISAKHAPATNAM)
  for (const word of words) {
    if (word.length >= 4) {
      // Check aliases first
      for (const [aliasKey, canonical] of Object.entries(LOCATION_ALIASES)) {
        const d = levenshteinDistance(word, aliasKey);
        if (d <= 2 || (word.length >= 7 && d <= 3)) {
          return canonical;
        }
      }

      // Check registry keys
      for (const regKey of Object.keys(COORDINATE_REGISTRY)) {
        const d = levenshteinDistance(word, regKey);
        if (d <= 2 || (word.length >= 7 && d <= 3)) {
          return regKey;
        }
      }
    }
  }

  return joined;
};

/**
 * Helper to resolve coordinates from string name using canonical registry
 */
const resolveCoordinates = (name) => {
  if (!name) return null;
  const canonical = canonicalizeLocation(name);
  if (canonical && COORDINATE_REGISTRY[canonical]) {
    return COORDINATE_REGISTRY[canonical];
  }
  return null;
};

// Realistic verified road travel distance matrix between major Andhra Pradesh trade hubs (in km)
const DISTANCE_MATRIX = {
  // Visakhapatnam Corridors (NH16)
  'VISAKHAPATNAM-VIJAYAWADA': 350,
  'VISAKHAPATNAM-GUNTUR': 380,
  'VISAKHAPATNAM-TENALI': 375,
  'VISAKHAPATNAM-KURNOOL': 640,
  'VISAKHAPATNAM-RAJAHMUNDRY': 190,
  'VISAKHAPATNAM-KAKINADA': 150,
  'VISAKHAPATNAM-TIRUPATI': 740,
  'VISAKHAPATNAM-ANANTAPUR': 790,
  'VISAKHAPATNAM-HYDERABAD': 620,

  // Guntur Hub (Centrally located in Coastal Andhra)
  'GUNTUR-VIJAYAWADA': 35,
  'GUNTUR-TENALI': 28,
  'GUNTUR-GUNTUR': 12,
  'GUNTUR-KURNOOL': 260,
  'GUNTUR-HYDERABAD': 270,
  'GUNTUR-ANANTAPUR': 380,
  'GUNTUR-TIRUPATI': 370,
  'GUNTUR-ONGOLE': 110,
  'GUNTUR-NELLORE': 240,
  'GUNTUR-RAJAHMUNDRY': 195,
  'GUNTUR-KAKINADA': 240,
  'GUNTUR-NANDYAL': 225,

  // Vijayawada Hub
  'VIJAYAWADA-TENALI': 35,
  'VIJAYAWADA-VIJAYAWADA': 15,
  'VIJAYAWADA-KURNOOL': 290,
  'VIJAYAWADA-HYDERABAD': 275,
  'VIJAYAWADA-ANANTAPUR': 415,
  'VIJAYAWADA-TIRUPATI': 390,
  'VIJAYAWADA-ELURU': 60,
  'VIJAYAWADA-RAJAHMUNDRY': 160,

  // Kurnool Hub (Rayalaseema Gate)
  'KURNOOL-KURNOOL': 15,
  'KURNOOL-ANANTAPUR': 150,
  'KURNOOL-NANDYAL': 75,
  'KURNOOL-ADONI': 100,
  'KURNOOL-HYDERABAD': 220,
  'KURNOOL-TIRUPATI': 360,
  'KURNOOL-KADAPA': 200,

  // Tenali Hub
  'TENALI-TENALI': 10,
  'TENALI-KURNOOL': 285,
};

/**
 * Calculates estimated road distance in kilometers between two locations.
 * Supports direct GPS coordinates (lat/lng) or name-based resolution.
 * Prioritizes realistic Andhra Pradesh highway trade route matrices, then dynamic GPS routing.
 */
const calculateDistanceKm = (origin, destination, originCoords = null, destCoords = null) => {
  if (!origin && !originCoords) return 25;
  if (!destination && !destCoords) return 25;

  const oCanon = canonicalizeLocation(origin);
  const dCanon = canonicalizeLocation(destination);

  // 1. Same district / local intra-city transport
  if (oCanon && dCanon && oCanon === dCanon && !originCoords && !destCoords) {
    return 12;
  }

  // 2. Check verified highway distance matrix (bidirectional)
  if (oCanon && dCanon) {
    const key1 = `${oCanon}-${dCanon}`;
    const key2 = `${dCanon}-${oCanon}`;
    if (DISTANCE_MATRIX[key1]) return DISTANCE_MATRIX[key1];
    if (DISTANCE_MATRIX[key2]) return DISTANCE_MATRIX[key2];
  }

  // 3. Coordinate-based road distance calculation (Haversine * road winding factor)
  let coord1 = originCoords?.lat && originCoords?.lng ? originCoords : resolveCoordinates(origin);
  let coord2 = destCoords?.lat && destCoords?.lng ? destCoords : resolveCoordinates(destination);

  if (coord1 && coord2) {
    const straightLine = calculateHaversineKm(coord1.lat, coord1.lng, coord2.lat, coord2.lng);
    if (straightLine < 5) return 12; // Within same town / market yard
    // Apply road factor (1.22x)
    return Math.round(straightLine * DEFAULT_ROAD_FACTOR);
  }

  // 4. Fallback: if one location is known and the other is unknown, calculate distance from AP state geographic center
  const apCenter = { lat: 16.3067, lng: 80.4365 }; // Centered at Guntur / Amaravati Capital Region
  const knownCoord = coord1 || coord2 || apCenter;
  const targetCoord = coord2 || apCenter;
  const estDist = Math.round(calculateHaversineKm(knownCoord.lat, knownCoord.lng, targetCoord.lat, targetCoord.lng) * DEFAULT_ROAD_FACTOR);
  return estDist > 20 ? estDist : 120;
};

/**
 * Calculates estimated logistics transportation cost.
 * Base fare + (Weight in Tons * Distance in Km * Rate per Km per Ton)
 */
const calculateLogisticsCost = (quantityKg, distanceKm) => {
  const weightTons = Math.max(0.5, quantityKg / 1000);
  const baseCost = 2000; // Flat loading/unloading & base haulage fee
  const ratePerKmPerTon = 12; // INR 12 per km per ton

  const transportCost = baseCost + distanceKm * weightTons * ratePerKmPerTon;
  return Math.round(transportCost);
};

/**
 * Calculates Gross Revenue, Logistics Cost, and Estimated Net Revenue.
 */
const calculateNetRevenue = (pricePerKg, quantityKg, distanceKm) => {
  const grossRevenue = Math.round(pricePerKg * quantityKg);
  const estimatedLogisticsCost = calculateLogisticsCost(quantityKg, distanceKm);
  const estimatedNetRevenue = Math.max(0, grossRevenue - estimatedLogisticsCost);

  return {
    sellingPrice: pricePerKg,
    grossRevenue,
    estimatedLogisticsCost,
    estimatedNetRevenue,
    distanceKm,
  };
};

module.exports = {
  COORDINATE_REGISTRY,
  LOCATION_ALIASES,
  TELUGU_TO_CANONICAL,
  canonicalizeLocation,
  resolveCoordinates,
  calculateHaversineKm,
  calculateDistanceKm,
  calculateLogisticsCost,
  calculateNetRevenue,
};
