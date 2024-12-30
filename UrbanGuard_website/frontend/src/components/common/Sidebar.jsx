import { AlertCircle, BarChart2, Cctv, Settings, Menu, Users, Bell } from "lucide-react";
import { useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Link } from "react-router-dom";

const Logo = () => {
  return (
    <motion.div
      className="text-white text-xl font-bold"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <span className="text-gradient">URBAN</span> <span>GUARD</span>
    </motion.div>
  );
};

const SIDEBAR_ITEMS = [
  {
    name: "Dashboard",
    icon: BarChart2,
    color: "#6366f1",
    href: "/",
  },
  { name: "Alerts", icon: AlertCircle, color: "#FF0000", href: "/alerts", count: 0 },
  { name: "Notify", icon: Bell, color: "#8B5CF6", href: "/notify" },
  { name: "Nearest CCTV", icon: Cctv, color: "#3B82F6", href: "/nearest-cctvs" },
  { name: "Case Statistics", icon: Users, color: "#EC4899", href: "/case-statistics" },
  { name: "Settings", icon: Settings, color: "#6EE7B7", href: "/settings" },
];

const Sidebar = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [alertCount, setAlertCount] = useState(0); // Alert count

  // Fetch alert count from the backend
  useEffect(() => {
    const fetchAlertCount = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/alerts/fetch-alert-count')
        const data = await response.json();
        setAlertCount(data.count); // Update alert count from the API
      } catch (error) {
        console.error('Error fetching alert count:', error);
      }
    };

    fetchAlertCount();
  }, []);

  // Audio for alert message
  const audio = new Audio("/path-to-your-audio-file/alert-sound.mp3");

  // Play audio and display message when alertCount > 0
  useEffect(() => {
    if (alertCount > 0) {
      audio.play();
    }
  }, [alertCount, audio]);

  return (
    <motion.div
      className={`relative z-10 transition-all duration-300 ease-in-out flex-shrink-0 ${isSidebarOpen ? "w-64" : "w-20"}`}
      animate={{ width: isSidebarOpen ? 256 : 80 }}
    >
      <div className="h-full bg-gray-800 bg-opacity-50 backdrop-blur-md p-4 flex flex-col border-r border-gray-700">
        {/* Sidebar Toggle Button */}
        <div className="flex items-center justify-start mb-1 mt-3 space-x-4">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 rounded-full hover:bg-gray-700 transition-colors"
          >
            <Menu size={24} />
          </motion.button>

          {/* Logo (conditionally render based on sidebar state) */}
          {isSidebarOpen && <Logo />}
        </div>

        {/* Navigation Items */}
        <nav className="mt-4 flex-grow">
          {SIDEBAR_ITEMS.map((item) => (
            <Link key={item.href} to={item.href}>
              <motion.div className="flex items-center p-4 text-sm font-medium rounded-lg hover:bg-gray-700 transition-colors mb-2">
                {/* Alert Counter for Alerts Item */}
                {item.name === "Alerts" && (
                  <div className="relative flex items-center">
                    {isSidebarOpen ? (
                      <>
                        {/* Icon and Label */}
                        <item.icon size={20} style={{ color: item.color, minWidth: "20px" }} />
                        <AnimatePresence>
                          <motion.span
                            className={`ml-4 whitespace-nowrap ${alertCount > 0 ? "text-red-500 animate-blink" : ""}`}
                            initial={{ opacity: 0, width: 0 }}
                            animate={{ opacity: 1, width: "auto" }}
                            exit={{ opacity: 0, width: 0 }}
                            transition={{ duration: 0.2, delay: 0.3 }}
                          >
                            {item.name}
                          </motion.span>
                        </AnimatePresence>
                        {/* Alert Counter */}
                        <div className="ml-2 w-5 h-5 flex items-center justify-center rounded-full bg-red-500 text-white text-xs">
                          {alertCount}
                        </div>
                      </>
                    ) : (
                      /* Counter Only When Sidebar is Collapsed */
                      <div className="ml-0 w-5 h-5 flex items-center justify-center rounded-full bg-red-500 text-white text-xs">
                        {alertCount}
                      </div>
                    )}
                  </div>
                )}

                {/* Normal Items */}
                {item.name !== "Alerts" && (
                  <>
                    <item.icon size={20} style={{ color: item.color, minWidth: "20px" }} />
                    <AnimatePresence>
                      {isSidebarOpen && (
                        <motion.span
                          className="ml-4 whitespace-nowrap"
                          initial={{ opacity: 0, width: 0 }}
                          animate={{ opacity: 1, width: "auto" }}
                          exit={{ opacity: 0, width: 0 }}
                          transition={{ duration: 0.2, delay: 0.3 }}
                        >
                          {item.name}
                        </motion.span>
                      )}
                    </AnimatePresence>
                  </>
                )}
              </motion.div>
            </Link>
          ))}
        </nav>
      </div>
    </motion.div>
  );
};

export default Sidebar;
