import React from 'react';
import { Award, ArrowRight, Truck, Store, UserCheck, ShieldCheck } from 'lucide-react';

export default function RecommendationCard({ option, onSelectOption, isSelecting }) {
  const isBest = option.isRecommended || option.rank === 1;

  return (
    <div
      className={`rounded-2xl p-4 sm:p-6 transition-all duration-300 relative overflow-hidden ${
        isBest
          ? 'glass-card-gold ring-2 ring-amber-500/50 shadow-2xl shadow-amber-500/10'
          : 'glass-card hover:border-slate-600'
      }`}
    >
      {/* Top Banner / Badge */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3 sm:mb-4">
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
          {isBest ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-1 rounded-full text-[11px] sm:text-xs font-extrabold bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 uppercase tracking-wider shadow-md">
              <Award className="w-3.5 h-3.5 sm:w-4 sm:h-4" /> 🏆 Best Net Return
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] sm:text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
              Rank #{option.rank}
            </span>
          )}

          <span
            className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] sm:text-xs font-medium border ${
              option.destinationType === 'MARKET'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
            }`}
          >
            {option.destinationType === 'MARKET' ? (
              <>
                <Store className="w-3 h-3" /> Direct APMC Market
              </>
            ) : (
              <>
                <UserCheck className="w-3 h-3" /> Verified Buyer Offer
              </>
            )}
          </span>
        </div>

        <div className="text-right">
          <span className="text-[10px] sm:text-xs text-slate-400 block">Transport Dist.</span>
          <span className="text-xs sm:text-sm font-semibold text-slate-200 flex items-center justify-end gap-1">
            <Truck className="w-3.5 h-3.5 text-slate-400" /> {option.distanceKm} Km
          </span>
        </div>
      </div>

      {/* Destination Title & Offered Price */}
      <div className="flex flex-col sm:flex-row justify-between items-start gap-2 mb-4 sm:mb-6">
        <div>
          <h3 className="text-lg sm:text-xl font-bold font-heading text-white">{option.destinationName}</h3>
          <p className="text-xs text-slate-400 flex items-center gap-1 mt-0.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span className="truncate">Location: {option.location || 'Regional Hub'}</span>
          </p>
        </div>
        <div className="text-left sm:text-right mt-1 sm:mt-0">
          <div className="text-[10px] sm:text-xs text-slate-400">Crop Unit Price</div>
          <div className="text-lg sm:text-xl font-extrabold font-heading text-emerald-400">
            ₹{option.sellingPrice} <span className="text-xs font-normal text-slate-400">/ Kg</span>
          </div>
        </div>
      </div>

      {/* Financial Net Breakdown Matrix */}
      <div className="grid grid-cols-3 gap-2 sm:gap-3 p-3 sm:p-4 rounded-xl bg-slate-900/70 border border-slate-800/80 mb-4 sm:mb-6">
        <div>
          <p className="text-[9px] sm:text-[10px] uppercase tracking-wider font-semibold text-slate-400 truncate">Gross Revenue</p>
          <p className="text-xs sm:text-base font-bold text-slate-200 mt-0.5 truncate">
            ₹{option.grossRevenue ? option.grossRevenue.toLocaleString('en-IN') : '0'}
          </p>
        </div>
        <div>
          <p className="text-[9px] sm:text-[10px] uppercase tracking-wider font-semibold text-slate-400 truncate">Est. Freight</p>
          <p className="text-xs sm:text-base font-bold text-rose-400 mt-0.5 truncate">
            -₹{option.estimatedLogisticsCost ? option.estimatedLogisticsCost.toLocaleString('en-IN') : '0'}
          </p>
        </div>
        <div className="border-l border-slate-800 pl-2 sm:pl-3">
          <p className="text-[9px] sm:text-[10px] uppercase tracking-wider font-bold text-amber-400 truncate">Estimated Net</p>
          <p className="text-xs sm:text-base font-extrabold text-amber-400 mt-0.5 truncate">
            ₹{option.estimatedNetRevenue ? option.estimatedNetRevenue.toLocaleString('en-IN') : '0'}
          </p>
        </div>
      </div>

      {/* Action Button */}
      <button
        type="button"
        onClick={() => onSelectOption(option)}
        disabled={isSelecting}
        className={`w-full py-2.5 sm:py-3 px-4 rounded-xl font-bold font-heading text-xs sm:text-sm flex items-center justify-center gap-2 transition-all cursor-pointer shadow-lg ${
          isBest
            ? 'bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-amber-500/20'
            : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-600/20'
        }`}
      >
        <span>{isBest ? 'Select Best Recommendation' : 'Choose This Destination'}</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
}
