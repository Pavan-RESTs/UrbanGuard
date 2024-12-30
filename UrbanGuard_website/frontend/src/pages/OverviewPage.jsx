import { useEffect, useState } from "react";
import { AlertCircle, AlertOctagon, AlertTriangle, Camera, CameraOff, Cctv, CheckCircle, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { FiRefreshCcw } from "react-icons/fi"; // Importing refresh icon
import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import AlertOverviewChart from "../components/overview/AlertOverviewChart";
import CategoryDistributionChart from "../components/overview/CategoryDistributionChart";
import SalesChannelChart from "../components/overview/AlertSourcesChart";
import dashboardStats from "../../../backend/data/dashboardStats.json";

const OverviewPage = () => {
  const [stats, setStats] = useState(dashboardStats);

  // Function to handle refreshing stats and reloading the page
  const handleRefresh = async () => {
    try {
      // Call the GET request without expecting a response
      await fetch("http://localhost:5000/api/dashboard/fetch-stats", {
        method: "GET",
      });
      console.log("Stats refreshed");

      // Reload the page after refreshing the stats
      window.location.reload();
    } catch (error) {
      console.error("Error refreshing stats:", error);
    }
  };

  return (
    <div className="flex-1 overflow-auto relative z-10">
      <Header title="Urban Guard - Police Surveillance Department [ Team-OPS3D | 848961 ]" />

      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        {/* STATS */}
        <motion.div
          className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          {/* Dynamically Render StatCards */}
          {stats.map((stat, index) => {
            const icons = {
              "Total Alerts Today": Zap,
              "Resolved Alerts": CheckCircle,
              "Pending Alerts": AlertTriangle,
              "Critical Alerts": AlertOctagon,
              "Total Cameras": Cctv,
              "Active Cameras": Camera,
              "Offline Cameras": CameraOff,
              "Cameras with Active Alerts": AlertCircle,
            };

            const staticColors = {
              "Total Alerts Today": "#6366F1",
              "Resolved Alerts": "#90EE90",
              "Pending Alerts": "#FF0000",
              "Critical Alerts": "#FF6961",
              "Total Cameras": "#6366F1",
              "Active Cameras": "#90EE90",
              "Offline Cameras": "#FF0000",
              "Cameras with Active Alerts": "#FF6961",
            };

            const Icon = icons[stat.name] || Zap;
            const color = staticColors[stat.name] || "#6366F1";

            return (
              <StatCard
                key={index}
                name={stat.name}
                icon={Icon}
                value={stat.value}
                color={color}
              />
            );
          })}
        </motion.div>

        {/* CHARTS */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <AlertOverviewChart />
          <CategoryDistributionChart />
          <SalesChannelChart />
        </div>
      </main>

      {/* REFRESH BUTTON */}
      <button
        onClick={handleRefresh}
        className="fixed bottom-8 right-8 bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-full shadow-lg flex items-center justify-center transition duration-300"
      >
        <FiRefreshCcw size={24} />
      </button>
    </div>
  );
};

export default OverviewPage;
