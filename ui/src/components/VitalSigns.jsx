import React from "react";
import { Activity, Heart, Wind, AlertCircle } from "lucide-react";

export default function VitalSigns({ vitals }) {
    if (!vitals) return <div className="p-4 bg-gray-900 rounded-lg">Waiting for data...</div>;

    const { breathing_bpm, heart_bpm, motion_energy, anomaly_score, state } = vitals;

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="p-6 bg-gray-800 rounded-xl shadow-lg border border-gray-700 flex flex-col items-center">
                <Wind className="text-blue-400 mb-2" size={32} />
                <span className="text-gray-400 text-sm">Breathing</span>
                <span className="text-3xl font-bold text-white">{breathing_bpm?.toFixed(1) || "--"} <span className="text-sm font-normal text-gray-500">BPM</span></span>
            </div>
            
            <div className="p-6 bg-gray-800 rounded-xl shadow-lg border border-gray-700 flex flex-col items-center">
                <Heart className="text-red-400 mb-2" size={32} />
                <span className="text-gray-400 text-sm">Heart Rate</span>
                <span className="text-3xl font-bold text-white">{heart_bpm?.toFixed(1) || "--"} <span className="text-sm font-normal text-gray-500">BPM</span></span>
            </div>

            <div className="p-6 bg-gray-800 rounded-xl shadow-lg border border-gray-700 flex flex-col items-center">
                <Activity className="text-green-400 mb-2" size={32} />
                <span className="text-gray-400 text-sm">Motion Energy</span>
                <span className="text-3xl font-bold text-white">{motion_energy?.toFixed(3) || "0.0"}</span>
            </div>

            <div className={`p-6 rounded-xl shadow-lg border flex flex-col items-center ${state === "FALLING" ? "bg-red-900 border-red-500 animate-pulse" : "bg-gray-800 border-gray-700"}`}>
                <AlertCircle className={state === "FALLING" ? "text-red-200 mb-2" : "text-yellow-400 mb-2"} size={32} />
                <span className={state === "FALLING" ? "text-red-200 text-sm" : "text-gray-400 text-sm"}>Room State</span>
                <span className="text-2xl font-bold text-white mt-1">{state || "UNKNOWN"}</span>
            </div>
        </div>
    );
}
