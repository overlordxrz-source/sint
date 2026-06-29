import React from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { time: "22:00", stage: 1, label: "Awake" },
    { time: "23:00", stage: 2, label: "Light" },
    { time: "00:00", stage: 3, label: "Deep" },
    { time: "01:00", stage: 2, label: "Light" },
    { time: "02:00", stage: 4, label: "REM" },
    { time: "03:00", stage: 3, label: "Deep" },
    { time: "04:00", stage: 2, label: "Light" },
    { time: "05:00", stage: 4, label: "REM" },
    { time: "06:00", stage: 1, label: "Awake" },
];

export default function SleepReport() {
    return (
        <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6 mt-8">
            <h2 className="text-xl font-bold text-white mb-6">Overnight Sleep Stages (Mock History)</h2>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorStage" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="time" stroke="#6b7280" />
                        <YAxis stroke="#6b7280" domain={[0, 4]} ticks={[1,2,3,4]} tickFormatter={(val) => {
                            if(val===1) return "Awake";
                            if(val===2) return "Light";
                            if(val===3) return "Deep";
                            if(val===4) return "REM";
                            return "";
                        }} />
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                        <Tooltip contentStyle={{ backgroundColor: "#1f2937", borderColor: "#374151", color: "#fff" }} />
                        <Area type="stepAfter" dataKey="stage" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorStage)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
