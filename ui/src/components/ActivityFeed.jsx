import React from "react";
import { Bell } from "lucide-react";

export default function ActivityFeed({ alerts }) {
    return (
        <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6 h-96 overflow-y-auto">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                <Bell className="mr-2 text-indigo-400" /> Live Alerts & Events
            </h2>
            
            {alerts.length === 0 ? (
                <div className="text-gray-500 text-center mt-10">No recent alerts.</div>
            ) : (
                <div className="space-y-3">
                    {alerts.map((alert, i) => (
                        <div key={i} className={`p-4 rounded-lg border ${
                            alert.severity === "CRITICAL" ? "bg-red-900/30 border-red-500 text-red-200" :
                            alert.severity === "HIGH" ? "bg-orange-900/30 border-orange-500 text-orange-200" :
                            "bg-gray-700 border-gray-600 text-gray-200"
                        }`}>
                            <div className="flex justify-between items-start">
                                <div>
                                    <span className="font-bold block text-sm">{alert.type}</span>
                                    <span className="text-sm opacity-90">{alert.msg}</span>
                                </div>
                                <span className="text-xs opacity-50">
                                    {new Date(alert.ts * 1000).toLocaleTimeString()}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
