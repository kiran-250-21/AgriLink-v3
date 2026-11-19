import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createHarvest } from '../../services/harvestApi';
import { useAuth } from '../../context/AuthContext';
import { ArrowLeft, CheckCircle2, MapPin, Navigation, Loader2 } from 'lucide-react';
import { AP_CROPS } from '../../data/crops';

export default function CreateHarvest() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [cropName, setCropName] = useState(AP_CROPS[0].name);
  const [category, setCategory] = useState(AP_CROPS[0].category);
  const [expectedQuantity, setExpectedQuantity] = useState(5000);
  const [quality, setQuality] = useState('GRADE_A');
  const [farmLocation, setFarmLocation] = useState(user?.farmerProfile?.farmLocation || 'Guntur');
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [locating, setLocating] = useState(false);
  const [gpsStatus, setGpsStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // 1-Click Browser GPS Geolocation with Reverse Geocoding
  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      return;
    }

    setLocating(true);
    setGpsStatus('Requesting GPS coordinates...');
    setError('');

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        const accuracy = Math.round(position.coords.accuracy);

        setLatitude(lat);
        setLongitude(lng);
        setGpsStatus(`GPS Active: ${lat.toFixed(4)}° N, ${lng.toFixed(4)}° E (±${accuracy}m)`);

        // Reverse-geocode coordinates into district/city name via OpenStreetMap Nominatim
        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10&accept-language=en`
          );
          if (res.ok) {
            const data = await res.json();
            const addr = data.address || {};
            const resolvedCity =
              addr.state_district ||
              addr.county ||
              addr.city ||
              addr.town ||
              addr.village ||
              farmLocation;

            // Strip "District" word if present for cleaner matching
            const cleanedCity = resolvedCity.replace(/\s*district\s*/i, '').trim();
            if (cleanedCity) {
              setFarmLocation(cleanedCity);
            }
          }
        } catch {
          // If network reverse geocoding is blocked/offline, GPS coordinates are still active!
        } finally {
          setLocating(false);
        }
      },
      (err) => {
        setLocating(false);
        setGpsStatus('');
        setError(
          err.code === 1
            ? 'Location permission denied. You can manually enter your district/city.'
            : 'Could not acquire GPS position. Please enter your farm location manually.'
        );
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const newHarvest = await createHarvest({
        cropName,
        category,
        expectedQuantity: Number(expectedQuantity),
        availableQuantity: Number(expectedQuantity),
        quality,
        farmLocation,
        latitude: latitude != null ? Number(latitude) : undefined,
        longitude: longitude != null ? Number(longitude) : undefined,
      });

      // Navigate immediately to Market Intelligence tool for this newly created harvest!
      navigate('/farmer/intelligence', { state: { harvestId: newHarvest._id } });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create harvest');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate(-1)}
          className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold font-heading text-white">Plan & Declare Harvest</h1>
          <p className="text-xs text-slate-400">Declare your harvest details to analyze estimated net returns across markets</p>
        </div>
      </div>

      <div className="glass-panel p-8 rounded-3xl border border-slate-800 shadow-2xl">
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
                Crop Name
              </label>
              <select
                value={cropName}
                onChange={(e) => {
                  const selected = e.target.value;
                  setCropName(selected);
                  const found = AP_CROPS.find((c) => c.name === selected);
                  if (found) setCategory(found.category);
                }}
                className="w-full px-3 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm focus:ring-2 focus:ring-emerald-500 font-medium"
              >
                {AP_CROPS.map((c) => (
                  <option key={c.name} value={c.name}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
                Crop Category
              </label>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
                Quantity (Kg)
              </label>
              <input
                type="number"
                required
                min="100"
                value={expectedQuantity}
                onChange={(e) => setExpectedQuantity(e.target.value)}
                className="w-full px-3 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm focus:ring-2 focus:ring-emerald-500"
                placeholder="5000"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">
                Quality Grade
              </label>
              <select
                value={quality}
                onChange={(e) => setQuality(e.target.value)}
                className="w-full px-3 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm"
              >
                <option value="GRADE_A">Grade A (Premium)</option>
                <option value="GRADE_B">Grade B (Standard)</option>
                <option value="GRADE_C">Grade C (Fair)</option>
              </select>
            </div>
          </div>

          {/* Location field with 1-click GPS detection */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
                Farm Location / Origin District
              </label>
              <button
                type="button"
                onClick={handleDetectLocation}
                disabled={locating}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 rounded-lg transition cursor-pointer"
                title="Detect live GPS coordinates from your device"
              >
                {locating ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" /> Detecting...
                  </>
                ) : (
                  <>
                    <Navigation className="w-3.5 h-3.5" /> 📍 Use Current Location
                  </>
                )}
              </button>
            </div>

            <div className="relative">
              <input
                type="text"
                required
                list="ap-locations"
                value={farmLocation}
                onChange={(e) => setFarmLocation(e.target.value)}
                className="w-full pl-9 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g. Visakhapatnam, Guntur, Kurnool, Chirala"
              />
              <MapPin className="w-4 h-4 text-slate-500 absolute left-3 top-3 pointer-events-none" />
              <datalist id="ap-locations">
                <option value="Visakhapatnam" />
                <option value="Vijayawada" />
                <option value="Guntur" />
                <option value="Kurnool" />
                <option value="Tirupati" />
                <option value="Anantapur" />
                <option value="Rajahmundry" />
                <option value="Kakinada" />
                <option value="Nellore" />
                <option value="Kadapa" />
                <option value="Ongole" />
                <option value="Eluru" />
                <option value="Tenali" />
                <option value="Chirala" />
                <option value="Bhimavaram" />
                <option value="Madanapalle" />
                <option value="Hindupur" />
                <option value="Proddatur" />
                <option value="Narasaraopet" />
                <option value="Tadepalligudem" />
                <option value="Srikakulam" />
                <option value="Vizianagaram" />
                <option value="Machilipatnam" />
                <option value="Nandyal" />
                <option value="Adoni" />
                <option value="Bapatla" />
                <option value="Palnadu" />
                <option value="Anakapalli" />
                <option value="Amalapuram" />
                <option value="Kadiri" />
                <option value="Puttaparthi" />
                <option value="Rayachoty" />
                <option value="Gudur" />
                <option value="Kavali" />
                <option value="Dharmavaram" />
                <option value="Guntakal" />
              </datalist>
            </div>

            {gpsStatus && (
              <p className="mt-1.5 text-xs text-emerald-400 flex items-center gap-1.5 font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                {gpsStatus}
              </p>
            )}
            <p className="text-[11px] text-slate-500 mt-1">
              Accurate GPS coordinates calculate precision haulage distances and true net returns to regional APMC mandis.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 rounded-xl font-bold font-heading text-sm bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 text-white shadow-lg shadow-emerald-600/25 flex items-center justify-center gap-2 cursor-pointer"
          >
            {loading ? 'Declaring Harvest...' : 'Save & Calculate Best Market Net Return'} <CheckCircle2 className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
