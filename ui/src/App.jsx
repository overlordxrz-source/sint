import React, { useState, useEffect } from "react";
import VitalSigns from "./components/VitalSigns";
import ActivityFeed from "./components/ActivityFeed";
import SleepReport from "./components/SleepReport";

function App() {
    const [vitals, setVitals] = useState(null);
    const [alerts, setAlerts] = useState([]);
    const [wsConnected, setWsConnected] = useState(false);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream");
        
        ws.onopen = () => setWsConnected(true);
        ws.onclose = () => setWsConnected(false);
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.vitals) setVitals(data.vitals);
                if (data.alerts && data.alerts.length > 0) {
                    setAlerts(prev => [...data.alerts, ...prev].slice(0, 50));
                }
            } catch (err) {
                console.error("WS Parse error", err);
            }
        };

        return () => ws.close();
    }, []);

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100 font-sans p-8">
            <div className="max-w-6xl mx-auto">
                <header className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
                            WiFi CSI Sensing
                        </h1>
                        <p className="text-gray-400 text-sm mt-1">Real-time room occupancy and vitals tracking</p>
                    </div>
                    <div className="flex items-center">
                        <span className="text-sm mr-2 text-gray-400">Status:</span>
                        {wsConnected ? (
                            <span className="px-3 py-1 bg-green-900 text-green-300 rounded-full text-xs font-bold uppercase tracking-wider">Live</span>
                        ) : (
                            <span className="px-3 py-1 bg-red-900 text-red-300 rounded-full text-xs font-bold uppercase tracking-wider">Offline</span>
                        )}
                    </div>
                </header>

                <VitalSigns vitals={vitals} />

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2">
                        {/* Heatmap / Spectrogram would go here. For now we just show the SleepReport. */}
                        <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6 h-96 flex items-center justify-center text-gray-500">
                            <p>Raw CSI / Spectrogram View (Coming Soon)</p>
                        </div>
                    </div>
                    <div className="lg:col-span-1">
                        <ActivityFeed alerts={alerts} />
                    </div>
                </div>

                <SleepReport />
            </div>
        </div>
    );
}

export default App;
